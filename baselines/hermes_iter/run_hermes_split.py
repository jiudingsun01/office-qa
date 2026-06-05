#!/usr/bin/env python3
"""Run Hermes Agent (profile officeqa-iter) on a split JSONL.

For each row, invoke `officeqa-iter -z <prompt>` as a subprocess. Save:
- per-uid prediction record in <run_dir>/preds/<uid>.json
- per-uid raw stdout/stderr log in <run_dir>/logs/<uid>.log
- per-uid trajectory dump if `hermes sessions export` is available (best-effort)

Resumes by skipping uids that already have a prediction file.
Concurrency via ThreadPoolExecutor. Per-question wallclock timeout.
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT / "baselines"))
from reward import extract_final_answer, score_answer  # noqa: E402

def _profile_skills_dir(profile_cmd: str) -> Path:
    """Map a profile-cmd name (e.g. 'officeqa-iter') to its skills dir under ~/.hermes/profiles/."""
    return Path.home() / ".hermes" / "profiles" / Path(profile_cmd).name / "skills"


REFLECTION_PROMPT = """You just attempted an OfficeQA benchmark question about a U.S. Treasury Bulletin. This is part of an iterative loop where future runs benefit from skills and memory you write right now.

The question (as you saw it):
---
{question}
---

Your final answer:    {predicted}
Correct gold answer:  {gold}
Verdict:              {verdict}

Reflect briefly: did this question expose anything generalizable that will help future Treasury Bulletin questions? Concrete examples of what is worth saving:

- Recurring table layouts ("monthly expenditure tables in 1939-1949 bulletins span 2 pages, use millions of dollars")
- FRASER-to-PDF page offsets ("FRASER page=15 maps to PDF page 11 for 1940s bulletins")
- Unit / scaling conventions ("(r) suffix = revised, use revised value; columns labeled 'millions' sometimes need further scaling")
- Parsing gotchas ("pdftotext -layout works for pages 1-50, raw mode for >50; tesseract OCR fails on cols < 8pt")
- Source-document patterns ("Treasury Bulletin contents page is usually p.3-5; index by 'Table' rather than 'Chart'")
- Arithmetic pitfalls you tripped on (sign errors, geometric mean conventions, rounding direction)

IF anything generalizable was learned, USE THE TOOLS NOW (this is required for self-evolution to happen):
- `skill_manage` with action=create (or action=patch on an existing skill) to write a procedural skill. The SKILL.md body must be concrete and actionable; a future agent should be able to apply it without re-deriving it.
- `memory` to record durable cross-session facts about the dataset or environment.

If nothing genuinely new and generalizable came up (most questions will be like this), respond "no skill needed" and exit. Do NOT save per-question trivia ("UID0044 answer is 1461") or generic platitudes ("read carefully").

Begin reflection now."""


def count_skills(profile_cmd: str = "officeqa-iter") -> int:
    d = _profile_skills_dir(profile_cmd)
    if not d.exists():
        return 0
    return sum(1 for _ in d.glob("**/SKILL.md"))


def run_one(rec: dict, run_dir: Path, timeout: int, profile_cmd: str, extra_args: list[str],
            reflect: bool = False, reflect_timeout: int = 600) -> dict:
    uid = rec["uid"]
    pred_path = run_dir / "preds" / f"{uid}.json"
    log_path = run_dir / "logs" / f"{uid}.log"
    if pred_path.exists():
        return {"uid": uid, "status": "cached"}

    cmd = [profile_cmd, "--yolo", *extra_args, "-z", rec["prompt"]]

    start = time.time()
    try:
        proc = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout,
            env=os.environ.copy(),
        )
        elapsed = time.time() - start
        stdout, stderr, rc = proc.stdout, proc.stderr, proc.returncode
    except subprocess.TimeoutExpired as e:
        elapsed = time.time() - start
        stdout = (e.stdout or b"").decode("utf-8", "replace") if isinstance(e.stdout, bytes) else (e.stdout or "")
        stderr, rc = "TIMEOUT", -1

    log_path.write_text(
        f"=== rc={rc} elapsed={elapsed:.1f}s ===\n"
        f"=== stdout ({len(stdout)} chars) ===\n{stdout}\n"
        f"=== stderr ({len(stderr)} chars) ===\n{stderr[:4000]}\n",
        encoding="utf-8",
    )

    # score for the reflection prompt
    try:
        predicted = extract_final_answer(stdout) if stdout else ""
    except Exception:
        predicted = ""
    try:
        score = score_answer(rec["gold_answer"], predicted) if predicted else 0.0
    except Exception:
        score = 0.0

    pred_record = {
        "uid": uid,
        "question": rec.get("question", ""),
        "gold_answer": rec["gold_answer"],
        "source_files": rec.get("source_files", []),
        "rc": rc,
        "elapsed_sec": round(elapsed, 2),
        "raw_response": stdout,
        "stderr_tail": stderr[-2000:] if stderr else "",
        "predicted": predicted,
        "score": score,
    }

    reflect_info = None
    if reflect:
        skills_before = count_skills(profile_cmd)
        verdict = "CORRECT" if score >= 1.0 else "WRONG"
        rprompt = REFLECTION_PROMPT.format(
            question=rec.get("question", "(unknown)"),
            predicted=predicted or "(no answer extracted)",
            gold=rec["gold_answer"],
            verdict=verdict,
        )
        rcmd = [profile_cmd, "--yolo", *extra_args, "-z", rprompt]
        rstart = time.time()
        try:
            rproc = subprocess.run(
                rcmd,
                capture_output=True,
                text=True,
                timeout=reflect_timeout,
                env=os.environ.copy(),
            )
            r_elapsed = time.time() - rstart
            r_stdout, r_stderr, r_rc = rproc.stdout, rproc.stderr, rproc.returncode
        except subprocess.TimeoutExpired as e:
            r_elapsed = time.time() - rstart
            r_stdout = (e.stdout or b"").decode("utf-8", "replace") if isinstance(e.stdout, bytes) else (e.stdout or "")
            r_stderr, r_rc = "TIMEOUT", -1

        skills_after = count_skills(profile_cmd)
        reflect_info = {
            "rc": r_rc,
            "elapsed_sec": round(r_elapsed, 2),
            "skills_before": skills_before,
            "skills_after": skills_after,
            "skills_delta": skills_after - skills_before,
            "verdict": verdict,
            "raw_response": r_stdout,
            "stderr_tail": (r_stderr or "")[-2000:],
        }
        refl_dir = run_dir / "reflections"
        refl_dir.mkdir(parents=True, exist_ok=True)
        (refl_dir / f"{uid}.json").write_text(json.dumps(reflect_info, ensure_ascii=False))

    pred_record["reflect"] = (
        {"skills_delta": reflect_info["skills_delta"], "rc": reflect_info["rc"], "verdict": reflect_info["verdict"]}
        if reflect_info else None
    )
    pred_path.write_text(json.dumps(pred_record, ensure_ascii=False))

    status_str = "ok" if rc == 0 else f"rc={rc}"
    if reflect_info:
        status_str += f"  reflect(+{reflect_info['skills_delta']} skills)"
    return {"uid": uid, "status": status_str, "elapsed": elapsed, "score": score,
            "reflect_skills_delta": reflect_info["skills_delta"] if reflect_info else 0}


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--split", required=True, help="path to split jsonl (train/eval/test)")
    p.add_argument("--run-dir", required=True, help="output dir for preds/ and logs/")
    p.add_argument("--profile-cmd", default="officeqa-iter", help="hermes profile wrapper binary")
    p.add_argument("--concurrency", type=int, default=4)
    p.add_argument("--timeout", type=int, default=1200)
    p.add_argument("--limit", type=int, default=0)
    p.add_argument("--uids", default="", help="comma-separated uids to run only")
    p.add_argument("--extra-args", default="", help="space-separated extra args passed to hermes")
    p.add_argument("--reflect", action="store_true",
                   help="after answering, make a 2nd Hermes call directing skill_manage/memory writes (train phase only)")
    p.add_argument("--reflect-timeout", type=int, default=600,
                   help="timeout for the reflection call")
    args = p.parse_args()

    run_dir = Path(args.run_dir)
    (run_dir / "preds").mkdir(parents=True, exist_ok=True)
    (run_dir / "logs").mkdir(parents=True, exist_ok=True)

    rows = [json.loads(l) for l in open(args.split) if l.strip()]
    if args.uids:
        keep = {u.strip() for u in args.uids.split(",") if u.strip()}
        rows = [r for r in rows if r["uid"] in keep]
    elif args.limit > 0:
        rows = rows[: args.limit]

    extra = args.extra_args.split() if args.extra_args else []

    print(f"run_dir: {run_dir}", flush=True)
    print(f"split: {args.split}  rows: {len(rows)}  concurrency: {args.concurrency}", flush=True)
    print(f"profile_cmd: {args.profile_cmd}  extra_args: {extra}", flush=True)

    print(f"reflect: {args.reflect}  reflect_timeout: {args.reflect_timeout}", flush=True)
    skills_start = count_skills(args.profile_cmd) if args.reflect else None

    t0 = time.time()
    done = 0
    total_reflect_delta = 0
    with ThreadPoolExecutor(max_workers=args.concurrency) as ex:
        futs = {
            ex.submit(run_one, r, run_dir, args.timeout, args.profile_cmd, extra,
                      args.reflect, args.reflect_timeout): r["uid"]
            for r in rows
        }
        for fut in as_completed(futs):
            uid = futs[fut]
            try:
                info = fut.result()
            except Exception as e:
                info = {"uid": uid, "status": f"exception:{type(e).__name__}:{e}"}
            done += 1
            total_reflect_delta += info.get("reflect_skills_delta", 0)
            print(
                f"[{done}/{len(rows)}] {uid}  {info.get('status')}  "
                f"elapsed={info.get('elapsed', 0):.1f}s  wallclock={time.time()-t0:.0f}s",
                flush=True,
            )

    print(f"\nDONE. {done} rows in {time.time()-t0:.0f}s", flush=True)
    if args.reflect:
        skills_end = count_skills(args.profile_cmd)
        print(f"reflection: skills {skills_start} -> {skills_end} (delta {skills_end - skills_start})",
              flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
