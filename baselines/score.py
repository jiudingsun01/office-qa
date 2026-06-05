#!/usr/bin/env python3
"""Score predictions produced by run_oracle.py against the OfficeQA ground truth.

Uses the official databricks/officeqa scorer (reward.score_answer + extract_final_answer).
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
RUNS = ROOT / "baselines" / "runs"

sys.path.insert(0, str(Path(__file__).resolve().parent))
from reward import extract_final_answer, score_answer  # noqa: E402


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--run-name", required=True)
    p.add_argument("--csv", default=str(DATA / "officeqa_pro.csv"))
    p.add_argument("--out", default="", help="optional path to write per-question results JSONL")
    args = p.parse_args()

    run_dir = RUNS / args.run_name
    preds_dir = run_dir / "preds"
    if not preds_dir.exists():
        print(f"no preds dir: {preds_dir}", file=sys.stderr)
        return 2

    with open(args.csv) as f:
        gold = {r["uid"]: r for r in csv.DictReader(f)}

    n_total = len(gold)
    n_pred = 0
    n_correct = 0
    n_extract_fail = 0
    n_score_fail = 0
    total_cost = 0.0
    results = []

    for uid, row in gold.items():
        pred_path = preds_dir / f"{uid}.json"
        if not pred_path.exists():
            results.append({"uid": uid, "status": "missing"})
            continue
        n_pred += 1
        rec = json.loads(pred_path.read_text())
        if isinstance(rec.get("cost_usd"), (int, float)):
            total_cost += rec["cost_usd"]

        raw = rec.get("raw_response") or ""
        try:
            extracted = extract_final_answer(raw)
        except ValueError:
            extracted = ""
        if not extracted:
            n_extract_fail += 1

        try:
            score = score_answer(row["answer"], extracted) if extracted else 0.0
        except Exception as e:
            score = 0.0
            n_score_fail += 1
            err = f"{type(e).__name__}:{e}"
        else:
            err = None

        if score >= 1.0:
            n_correct += 1
        results.append({
            "uid": uid,
            "difficulty": row.get("difficulty"),
            "gold": row["answer"],
            "predicted": extracted,
            "score": score,
            "err": err,
        })

    acc = n_correct / n_total if n_total else 0.0
    acc_predicted = n_correct / n_pred if n_pred else 0.0
    print(f"run: {args.run_name}")
    print(f"questions in CSV:    {n_total}")
    print(f"predictions present: {n_pred}")
    print(f"correct:             {n_correct}")
    print(f"accuracy (all):      {acc:.3f}")
    print(f"accuracy (predicted only): {acc_predicted:.3f}")
    print(f"extract failures:    {n_extract_fail}")
    print(f"score exceptions:    {n_score_fail}")
    print(f"total cost (USD):    ${total_cost:.2f}")

    if args.out:
        Path(args.out).write_text("\n".join(json.dumps(r, ensure_ascii=False) for r in results))
        print(f"per-question results -> {args.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
