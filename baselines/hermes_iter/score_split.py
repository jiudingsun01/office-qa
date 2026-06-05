#!/usr/bin/env python3
"""Score a Hermes split run using officeqa reward.score_answer.

Reads <run_dir>/preds/<uid>.json files (raw_response field), extracts
FINAL_ANSWER, scores against gold. Prints summary + writes per-row JSONL.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT / "baselines"))
from reward import extract_final_answer, score_answer  # noqa: E402


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--run-dir", required=True)
    p.add_argument("--split", required=True, help="path to the split jsonl (used for total count)")
    p.add_argument("--out", default="")
    args = p.parse_args()

    run_dir = Path(args.run_dir)
    preds_dir = run_dir / "preds"
    rows = [json.loads(l) for l in open(args.split) if l.strip()]
    total = len(rows)

    n_pred = n_correct = n_extract_fail = 0
    results = []
    for r in rows:
        uid = r["uid"]
        p = preds_dir / f"{uid}.json"
        if not p.exists():
            results.append({"uid": uid, "status": "missing"})
            continue
        n_pred += 1
        rec = json.loads(p.read_text())
        raw = rec.get("raw_response") or ""
        try:
            ext = extract_final_answer(raw) if raw else ""
        except ValueError:
            ext = ""
        if not ext:
            n_extract_fail += 1
        try:
            sc = score_answer(r["gold_answer"], ext) if ext else 0.0
        except Exception:
            sc = 0.0
        if sc >= 1.0:
            n_correct += 1
        results.append({"uid": uid, "gold": r["gold_answer"], "predicted": ext, "score": sc, "rc": rec.get("rc")})

    print(f"run: {run_dir.name}")
    print(f"questions in split:  {total}")
    print(f"predictions present: {n_pred}")
    print(f"correct:             {n_correct}")
    if total:
        print(f"accuracy (all):      {n_correct/total:.3f}")
    if n_pred:
        print(f"accuracy (predicted): {n_correct/n_pred:.3f}")
    print(f"extract failures:    {n_extract_fail}")

    if args.out:
        Path(args.out).write_text("\n".join(json.dumps(r, ensure_ascii=False) for r in results))
        print(f"per-row -> {args.out}")
    # Machine-readable summary
    summary = {
        "run_dir": str(run_dir),
        "split": args.split,
        "n_total": total,
        "n_pred": n_pred,
        "n_correct": n_correct,
        "n_extract_fail": n_extract_fail,
        "accuracy_all": (n_correct / total) if total else 0.0,
        "accuracy_predicted": (n_correct / n_pred) if n_pred else 0.0,
    }
    (run_dir / "summary.json").write_text(json.dumps(summary, indent=2))
    print(f"summary -> {run_dir/'summary.json'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
