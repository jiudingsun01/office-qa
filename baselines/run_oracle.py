#!/usr/bin/env python3
"""Run the Claude Code oracle baseline on OfficeQA.

Reads questions from a CSV (default: officeqa_pro.csv), inlines the gold
source-file text as context, calls `claude -p` per question, and writes one
JSON file per uid to runs/<run_name>/preds/<uid>.json. Resumes by skipping
uids that already have a prediction file. Use score.py to evaluate.
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
CORPUS = DATA / "treasury_bulletins_parsed" / "transformed"
RUNS = ROOT / "baselines" / "runs"

SYSTEM_PROMPT = """You are an expert analyst answering questions about U.S. Treasury Bulletins.

You will be given a question and the full text of the relevant source documents. The documents are parsed from PDFs; tables appear in Markdown. Read carefully, locate the relevant figures or passages, and perform any arithmetic needed.

OUTPUT FORMAT (mandatory):
- End your response with the final answer wrapped in <FINAL_ANSWER>...</FINAL_ANSWER> tags.
- Inside the tags, output only the value: a number, a date, a short phrase. No commentary, no units unless the question asks for them, no surrounding text.
- For numeric answers, match the scale implied by the question (e.g. "in millions of dollars" -> just the number in millions; do not add a "$" or "million").
- If the question asks for a list of numbers, output them comma-separated inside the tags."""

USER_TEMPLATE = """Question: {question}

Source documents:
{docs}

Think carefully, then provide your final answer wrapped in <FINAL_ANSWER>...</FINAL_ANSWER>."""


def build_docs(source_files_cell: str) -> tuple[str, list[str]]:
    files = [s.strip() for s in source_files_cell.splitlines() if s.strip()]
    parts = []
    for fn in files:
        text = (CORPUS / fn).read_text(encoding="utf-8", errors="replace")
        parts.append(f"### {fn}\n\n{text}")
    return "\n\n---\n\n".join(parts), files


def _parse_stream(stdout: str) -> tuple[list[dict], str, dict]:
    """Parse stream-json output: returns (events, final_text, summary).

    `events` is every JSON line. `final_text` is the assistant's final result.
    `summary` is the trailing "result" event (cost, usage, num_turns, etc.).
    """
    events: list[dict] = []
    final_text = ""
    summary: dict = {}
    for line in stdout.splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            evt = json.loads(line)
        except json.JSONDecodeError:
            continue
        events.append(evt)
        t = evt.get("type")
        if t == "result":
            summary = evt
            final_text = evt.get("result") or final_text
        elif t == "assistant" and not final_text:
            msg = evt.get("message") or {}
            for blk in msg.get("content") or []:
                if blk.get("type") == "text":
                    final_text = (final_text + blk.get("text", "")).strip()
    return events, final_text, summary


def run_one(row: dict, model: str, max_budget: float, run_dir: Path, timeout: int, env: dict) -> dict:
    uid = row["uid"]
    pred_path = run_dir / "preds" / f"{uid}.json"
    trace_path = run_dir / "traces" / f"{uid}.jsonl"
    log_path = run_dir / "logs" / f"{uid}.log"
    if pred_path.exists():
        return {"uid": uid, "status": "cached"}

    docs, files = build_docs(row["source_files"])
    prompt = USER_TEMPLATE.format(question=row["question"], docs=docs)

    cmd = [
        "claude",
        "--print",
        "--model", model,
        "--max-budget-usd", str(max_budget),
        "--output-format", "stream-json",
        "--include-partial-messages",
        "--verbose",
        "--append-system-prompt", SYSTEM_PROMPT,
        "--disallowedTools",
        "Bash,Edit,Write,Read,Glob,Grep,WebFetch,WebSearch,TodoWrite,NotebookEdit,Task",
        "--permission-mode", "default",
        "--no-session-persistence",
    ]
    if env.get("ANTHROPIC_API_KEY"):
        cmd.append("--bare")

    start = time.time()
    try:
        result = subprocess.run(
            cmd,
            input=prompt,
            capture_output=True,
            text=True,
            timeout=timeout,
            env=env,
        )
        elapsed = time.time() - start
        stdout, stderr, rc = result.stdout, result.stderr, result.returncode
    except subprocess.TimeoutExpired as e:
        elapsed = time.time() - start
        stdout = (e.stdout or b"").decode("utf-8", "replace") if isinstance(e.stdout, bytes) else (e.stdout or "")
        stderr, rc = "TIMEOUT", -1

    events, text_response, summary = _parse_stream(stdout)
    cost_usd = summary.get("total_cost_usd") if isinstance(summary, dict) else None
    usage = summary.get("usage") if isinstance(summary, dict) else None
    num_turns = summary.get("num_turns") if isinstance(summary, dict) else None

    trace_path.parent.mkdir(parents=True, exist_ok=True)
    with open(trace_path, "w", encoding="utf-8") as fh:
        for evt in events:
            fh.write(json.dumps(evt, ensure_ascii=False) + "\n")

    log_path.write_text(
        f"=== rc={rc} elapsed={elapsed:.1f}s cost_usd={cost_usd} turns={num_turns} ===\n"
        f"=== events: {len(events)} ===\n"
        f"=== stderr ({len(stderr)} chars) ===\n{stderr[:4000]}\n",
        encoding="utf-8",
    )

    rec = {
        "uid": uid,
        "question": row["question"],
        "gold_answer": row["answer"],
        "source_files": files,
        "model": model,
        "rc": rc,
        "elapsed_sec": round(elapsed, 2),
        "cost_usd": cost_usd,
        "num_turns": num_turns,
        "usage": usage,
        "n_events": len(events),
        "raw_response": text_response,
    }
    pred_path.write_text(json.dumps(rec, ensure_ascii=False))
    return {"uid": uid, "status": "ok" if rc == 0 else f"rc={rc}", "cost_usd": cost_usd, "elapsed": elapsed}


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--csv", default=str(DATA / "officeqa_pro.csv"))
    p.add_argument("--run-name", default="claude_sonnet_4_6_oracle")
    p.add_argument("--model", default="claude-sonnet-4-6")
    p.add_argument("--max-budget-usd", type=float, default=2.0)
    p.add_argument("--concurrency", type=int, default=16)
    p.add_argument("--timeout", type=int, default=900, help="per-question subprocess timeout in seconds")
    p.add_argument("--limit", type=int, default=0, help="if >0, run only the first N questions (smoke test)")
    p.add_argument("--uids", default="", help="comma-separated uids to run (overrides --limit)")
    p.add_argument(
        "--env-file",
        default=str(ROOT / ".env"),
        help="dotenv file to source; ANTHROPIC_API_KEY here switches to --bare mode (API-key auth, no OAuth).",
    )
    args = p.parse_args()

    env = dict(os.environ)
    env_file = Path(args.env_file)
    if env_file.is_file():
        for line in env_file.read_text().splitlines():
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, v = line.split("=", 1)
            env[k.strip()] = v.strip().strip('"').strip("'")
    auth_mode = "api-key (--bare)" if env.get("ANTHROPIC_API_KEY") else "OAuth (default)"

    run_dir = RUNS / args.run_name
    (run_dir / "preds").mkdir(parents=True, exist_ok=True)
    (run_dir / "logs").mkdir(parents=True, exist_ok=True)
    (run_dir / "traces").mkdir(parents=True, exist_ok=True)

    with open(args.csv) as f:
        rows = list(csv.DictReader(f))

    if args.uids:
        keep = {u.strip() for u in args.uids.split(",") if u.strip()}
        rows = [r for r in rows if r["uid"] in keep]
    elif args.limit > 0:
        rows = rows[: args.limit]

    print(f"run_dir: {run_dir}", flush=True)
    print(f"model: {args.model}  budget: ${args.max_budget_usd}/q  concurrency: {args.concurrency}  auth: {auth_mode}", flush=True)
    print(f"questions: {len(rows)}", flush=True)

    t0 = time.time()
    done = 0
    total_cost = 0.0
    with ThreadPoolExecutor(max_workers=args.concurrency) as ex:
        futs = {ex.submit(run_one, r, args.model, args.max_budget_usd, run_dir, args.timeout, env): r["uid"] for r in rows}
        for fut in as_completed(futs):
            uid = futs[fut]
            try:
                info = fut.result()
            except Exception as e:
                info = {"uid": uid, "status": f"exception:{type(e).__name__}:{e}"}
            done += 1
            c = info.get("cost_usd")
            if isinstance(c, (int, float)):
                total_cost += c
            print(
                f"[{done}/{len(rows)}] {uid}  {info.get('status')}  "
                f"cost=${c if c is not None else '?':}  elapsed={info.get('elapsed', 0):.1f}s  "
                f"total_cost=${total_cost:.2f}  wallclock={time.time()-t0:.0f}s",
                flush=True,
            )

    print(f"\nDONE. {done} questions in {time.time()-t0:.0f}s.  total_cost=${total_cost:.2f}", flush=True)
    print(f"Score with:  python {ROOT}/baselines/score.py --run-name {args.run_name}", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
