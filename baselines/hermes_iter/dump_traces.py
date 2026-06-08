#!/usr/bin/env python3
"""Dump full agent trajectories for a run/phase by mapping Hermes session files
to UIDs.

Sessions are not named by UID, so we map each session to a UID by matching the
`Question:` block in its first user message against the run's preds/<uid>.json,
disambiguating duplicate runs (e.g. baseline vs final test, which share the same
questions) with a session-start time window and the recorded final answer.

Outputs, per matched UID:
  <out_traces>/<uid>.md   human-readable trace (reasoning + tool calls + tool
                          outputs; base64 page images stripped)
and (optionally) a tarball of the raw session JSONs (verbatim, incl. images).

Usage:
  python dump_traces.py \
    --sessions ~/.hermes/profiles/officeqa-iter-opus48/sessions \
    --run-phase baselines/hermes_iter/runs/opus48_full_metaopt/final/test \
    --since 20260603_120500 --until 20260603_122200 \
    --out-traces <run-phase>/traces --raw-tar <run-phase>/traces_raw.tar.gz
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

B64 = re.compile(r"data:image/[^;]+;base64,[A-Za-z0-9+/=\s]+")
FINAL = re.compile(r"<FINAL_ANSWER>\s*(.*?)\s*</FINAL_ANSWER>", re.DOTALL | re.IGNORECASE)
TS = re.compile(r"session_(\d{8}_\d{6})_")


def strip_images(s: str) -> str:
    return B64.sub(lambda m: f"[BASE64 IMAGE STRIPPED: {len(m.group(0))} chars]", s or "")


def extract_question(prompt: str) -> str:
    """Pull the question text out of a run prompt (after 'Question:' up to the
    'Source' block). Returns '' if not found."""
    if not prompt:
        return ""
    m = re.search(r"Question:\s*(.*?)\n\s*Source", prompt, re.DOTALL)
    return re.sub(r"\s+", " ", m.group(1)).strip() if m else ""


def norm(s: str) -> str:
    return re.sub(r"\s+", " ", (s or "")).strip()


def final_answer(text: str) -> str:
    ms = FINAL.findall(text or "")
    return ms[-1].strip() if ms else ""


def render(session: dict, uid: str, meta: dict) -> str:
    out = [f"# Trace — {uid}", ""]
    out.append(f"- model: `{session.get('model')}`")
    out.append(f"- session: `{meta['session_file']}`")
    out.append(f"- predicted: `{meta.get('predicted')}`  gold: `{meta.get('gold')}`  "
               f"score: {meta.get('score')}")
    out.append(f"- messages: {session.get('message_count')}")
    out.append("\n---\n")
    for i, m in enumerate(session.get("messages", [])):
        role = m.get("role")
        name = m.get("name", "")
        if role == "user":
            out.append(f"## [{i}] USER (prompt)\n\n```\n{strip_images(m.get('content',''))}\n```\n")
        elif role == "assistant":
            out.append(f"## [{i}] ASSISTANT")
            rc = m.get("reasoning_content") or m.get("reasoning") or ""
            if rc.strip():
                out.append(f"\n**reasoning:**\n\n{strip_images(rc)}\n")
            ct = m.get("content") or ""
            if ct.strip():
                out.append(f"\n**content:**\n\n{strip_images(ct)}\n")
            for t in m.get("tool_calls") or []:
                fn = t.get("function", {})
                out.append(f"\n**tool_call** `{fn.get('name')}`:\n\n```json\n"
                           f"{strip_images(fn.get('arguments',''))}\n```\n")
        elif role == "tool":
            c = m.get("content", "")
            if not isinstance(c, str):
                c = json.dumps(c)
            out.append(f"## [{i}] TOOL RESULT (`{name}`)\n\n```\n{strip_images(c)}\n```\n")
    return "\n".join(out)


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--sessions", required=True)
    p.add_argument("--run-phase", required=True, help="dir containing preds/<uid>.json")
    p.add_argument("--since", default="", help="filename ts lower bound YYYYMMDD_HHMMSS")
    p.add_argument("--until", default="", help="filename ts upper bound YYYYMMDD_HHMMSS")
    p.add_argument("--out-traces", default="")
    p.add_argument("--raw-tar", default="")
    args = p.parse_args()

    run_phase = Path(args.run_phase)
    preds_dir = run_phase / "preds"
    preds = {}
    for f in sorted(preds_dir.glob("*.json")):
        r = json.loads(f.read_text())
        preds[r["uid"]] = {
            "question": norm(r.get("question", "")),
            "predicted": norm(r.get("predicted", "")),
            "gold": r.get("gold_answer", ""),
            "score": r.get("score"),
        }
    q_index = {v["question"]: uid for uid, v in preds.items() if v["question"]}
    print(f"preds: {len(preds)} uids")

    sess_dir = Path(args.sessions).expanduser()
    # candidate sessions in the time window
    cands = []
    for f in sess_dir.glob("session_*.json"):
        mt = TS.search(f.name)
        if not mt:
            continue
        ts = mt.group(1)
        if args.since and ts < args.since:
            continue
        if args.until and ts > args.until:
            continue
        cands.append(f)
    print(f"sessions in window: {len(cands)}")

    # map uid -> chosen session (prefer exact final-answer match)
    chosen: dict[str, Path] = {}
    for f in sorted(cands):
        try:
            d = json.loads(f.read_text())
        except Exception:
            continue
        msgs = d.get("messages") or []
        if not msgs:
            continue
        q = extract_question(msgs[0].get("content", "") if isinstance(msgs[0].get("content"), str) else "")
        uid = q_index.get(norm(q))
        if not uid:
            continue
        fa = norm(final_answer(json.dumps(d)))
        # prefer the session whose final answer matches the recorded prediction
        if uid not in chosen:
            chosen[uid] = f
        else:
            prev = json.loads(chosen[uid].read_text())
            prev_fa = norm(final_answer(json.dumps(prev)))
            want = preds[uid]["predicted"]
            if fa == want and prev_fa != want:
                chosen[uid] = f

    matched = sorted(chosen)
    missing = [u for u in preds if u not in chosen]
    print(f"matched: {len(matched)}/{len(preds)}")
    if missing:
        print(f"UNMATCHED: {missing}")

    if args.out_traces:
        out = Path(args.out_traces)
        out.mkdir(parents=True, exist_ok=True)
        for uid in matched:
            d = json.loads(chosen[uid].read_text())
            meta = dict(preds[uid], session_file=chosen[uid].name)
            (out / f"{uid}.md").write_text(render(d, uid, meta), encoding="utf-8")
        print(f"wrote {len(matched)} readable traces -> {out}")

    if args.raw_tar:
        import tarfile
        tarp = Path(args.raw_tar)
        with tarfile.open(tarp, "w:gz") as tf:
            for uid in matched:
                tf.add(chosen[uid], arcname=f"{uid}__{chosen[uid].name}")
        print(f"wrote raw tarball ({len(matched)} sessions) -> {tarp}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
