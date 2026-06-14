#!/usr/bin/env python3
"""Evaluate a fixed skills library on a split via headless Claude Code (no curation).

Stages --skills-dir into <run-dir>/project/.claude/skills/, runs `claude -p` per
question (model via --model-args), scores with reward.py. Resumable (cached answers).
"""
from __future__ import annotations
import argparse, json, shutil, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from iterate_claude import run_answers, count_skills, skills_dir  # noqa: E402


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--skills-dir", required=True)
    p.add_argument("--split", required=True)
    p.add_argument("--run-dir", required=True)
    p.add_argument("--model-args", default="--model claude-opus-4-8")
    p.add_argument("--concurrency", type=int, default=4)
    p.add_argument("--timeout", type=int, default=1200)
    args = p.parse_args()

    run = Path(args.run_dir)
    project = run / "project"
    skills_dir(project).mkdir(parents=True, exist_ok=True)
    for sk in sorted(Path(args.skills_dir).glob("*/SKILL.md")):
        shutil.copytree(sk.parent, skills_dir(project) / sk.parent.name, dirs_exist_ok=True)
    n_sk = count_skills(project)

    rows = [json.loads(l) for l in open(args.split) if l.strip()]
    print(f"eval: {len(rows)} Q  skills={n_sk}  model={args.model_args}", flush=True)
    res = run_answers(rows, project, args.model_args.split(), args.timeout, args.concurrency, run / "preds")
    n_corr = sum(1 for d in res.values() if d["score"] >= 1.0)
    summary = {"skills": n_sk, "n_correct": n_corr, "n_total": len(res),
               "accuracy": n_corr / len(res) if res else 0.0}
    (run / "summary.json").write_text(json.dumps(summary, indent=2))
    print(f"DONE  {n_corr}/{len(res)} = {summary['accuracy']:.3f}  skills={n_sk}", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
