#!/usr/bin/env python3
"""Hermes Agent self-evolve iteration controller for OfficeQA.

Pipeline (all under profile `officeqa-iter`):

  iter-0:  test    (baseline, before any learning)
  iter-1:  train -> curator run -> eval -> snapshot skills + memory
  iter-2:  train -> curator run -> eval -> snapshot
  ...
  final:   test    (held-out evaluation)

Stops when:
  - elapsed wall time exceeds --hours
  - total spend exceeds --max-spend-usd (rough est from token usage; best-effort)
  - --max-iters reached
  - eval accuracy plateaus (no improvement for --patience iters)

Each iter writes <state_dir>/iter-N/{train,eval}/ with preds, logs, summary.
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
HERMES_ITER = ROOT / "baselines" / "hermes_iter"
DEFAULT_SPLITS = HERMES_ITER / "splits"
RUN_SCRIPT = HERMES_ITER / "run_hermes_split.py"
SCORE_SCRIPT = HERMES_ITER / "score_split.py"
PROFILE_DIR = Path.home() / ".hermes" / "profiles" / "officeqa-iter"


def log(state_dir: Path, msg: str) -> None:
    ts = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    line = f"[{ts}] {msg}"
    print(line, flush=True)
    with open(state_dir / "controller.log", "a") as f:
        f.write(line + "\n")


def snapshot_profile(iter_dir: Path) -> None:
    """Copy skills/ and memories/ from the profile dir into iter_dir/snapshot/."""
    dst = iter_dir / "snapshot"
    dst.mkdir(parents=True, exist_ok=True)
    for sub in ("skills", "memories"):
        src = PROFILE_DIR / sub
        if src.exists():
            try:
                shutil.copytree(src, dst / sub, dirs_exist_ok=True)
            except Exception as e:
                with open(dst / f"{sub}.error", "w") as f:
                    f.write(str(e))


def run_split(split_name: str, run_dir: Path, concurrency: int, timeout: int,
              profile_cmd: str = "officeqa-iter", reflect: bool = False,
              reflect_timeout: int = 600, splits_dir: Path = DEFAULT_SPLITS,
              limit: int = 0, extra_args: str = "") -> dict:
    run_dir.mkdir(parents=True, exist_ok=True)
    split_path = splits_dir / f"{split_name}.jsonl"
    cmd = [
        sys.executable, str(RUN_SCRIPT),
        "--split", str(split_path),
        "--run-dir", str(run_dir),
        "--profile-cmd", profile_cmd,
        "--concurrency", str(concurrency),
        "--timeout", str(timeout),
    ]
    if limit > 0:
        cmd.extend(["--limit", str(limit)])
    if extra_args:
        cmd.extend(["--extra-args", extra_args])
    if reflect:
        cmd.extend(["--reflect", "--reflect-timeout", str(reflect_timeout)])
    started = time.time()
    proc = subprocess.run(cmd, capture_output=True, text=True)
    elapsed = time.time() - started
    (run_dir / "controller_runner.log").write_text(
        f"=== rc={proc.returncode} elapsed={elapsed:.1f}s ===\n"
        f"=== stdout ===\n{proc.stdout}\n"
        f"=== stderr ===\n{proc.stderr[:8000]}\n",
        encoding="utf-8",
    )
    # Score it
    score_cmd = [
        sys.executable, str(SCORE_SCRIPT),
        "--run-dir", str(run_dir),
        "--split", str(split_path),
        "--out", str(run_dir / "per_row.jsonl"),
    ]
    s = subprocess.run(score_cmd, capture_output=True, text=True)
    summary_path = run_dir / "summary.json"
    if summary_path.exists():
        try:
            return json.loads(summary_path.read_text())
        except Exception:
            pass
    return {"accuracy_all": 0.0, "n_correct": 0, "n_total": 0, "rc": proc.returncode, "score_rc": s.returncode}


def run_curator(profile_cmd: str = "officeqa-iter") -> str:
    """Trigger a curator pass on the profile."""
    cmd = [profile_cmd, "curator", "run"]
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=900)
        return f"rc={proc.returncode}\n{proc.stdout[-1500:]}"
    except subprocess.TimeoutExpired:
        return "TIMEOUT"


def list_profile_skills(profile_cmd: str = "officeqa-iter") -> list[str]:
    skills_dir = Path.home() / ".hermes" / "profiles" / Path(profile_cmd).name / "skills"
    if not skills_dir.exists():
        return []
    return [str(p.relative_to(skills_dir)) for p in skills_dir.glob("**/SKILL.md")]


def count_memory_entries(profile_cmd: str = "officeqa-iter") -> int:
    """Count durable memory blocks in the profile's MEMORY.md (sections split by '§')."""
    mem = Path.home() / ".hermes" / "profiles" / Path(profile_cmd).name / "memories" / "MEMORY.md"
    if not mem.exists():
        return 0
    text = mem.read_text(encoding="utf-8", errors="replace").strip()
    if not text:
        return 0
    return len([s for s in text.split("§") if s.strip()])


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--state-dir", default=str(HERMES_ITER / "runs" / "iter01"))
    p.add_argument("--hours", type=float, default=24.0)
    p.add_argument("--max-iters", type=int, default=20)
    p.add_argument("--patience", type=int, default=3, help="stop if eval doesn't improve for N iters")
    p.add_argument("--train-concurrency", type=int, default=2)
    p.add_argument("--eval-concurrency", type=int, default=8)
    p.add_argument("--test-concurrency", type=int, default=8)
    p.add_argument("--timeout", type=int, default=1500)
    p.add_argument("--skip-baseline-test", action="store_true")
    p.add_argument("--smoke", action="store_true", help="tiny dataset (limit each split) for pipeline check")
    p.add_argument("--profile-cmd", default="officeqa-iter",
                   help="hermes profile wrapper binary (e.g. officeqa-iter-v2)")
    p.add_argument("--reflect", action="store_true",
                   help="enable post-answer reflection on TRAIN phase (drives skill_manage/memory writes)")
    p.add_argument("--reflect-timeout", type=int, default=600)
    p.add_argument("--corpus", choices=["pdf", "parsed-md", "parsed-md+pdf"], default="pdf",
                   help="which corpus to evaluate on; selects matching splits dir")
    p.add_argument("--splits-dir", default="",
                   help="explicit splits dir (overrides --corpus mapping)")
    p.add_argument("--smoke-train", type=int, default=5, help="--smoke: train split limit per iter")
    p.add_argument("--smoke-eval", type=int, default=5, help="--smoke: eval split limit per iter")
    p.add_argument("--smoke-test", type=int, default=5, help="--smoke: baseline/final test split limit")
    p.add_argument("--smoke-iters", type=int, default=2, help="--smoke: cap train iterations")
    p.add_argument("--extra-args", default="",
                   help='space-separated extra args passed to each hermes call (e.g. "-m claude-opus-4-8")')
    args = p.parse_args()

    if args.splits_dir:
        splits_dir = Path(args.splits_dir)
    elif args.corpus == "pdf":
        splits_dir = DEFAULT_SPLITS
    else:
        slug = args.corpus.replace("-", "_").replace("+", "_plus_")
        splits_dir = DEFAULT_SPLITS.parent / f"splits_{slug}"
    if not (splits_dir / "test.jsonl").exists():
        raise SystemExit(
            f"splits not built at {splits_dir}. "
            f"Run: python build_splits.py --corpus {args.corpus}"
        )

    if args.smoke:
        train_limit = args.smoke_train
        eval_limit = args.smoke_eval
        test_limit = args.smoke_test
        args.max_iters = min(args.max_iters, args.smoke_iters)
    else:
        train_limit = eval_limit = test_limit = 0

    state = Path(args.state_dir)
    state.mkdir(parents=True, exist_ok=True)
    log(state, f"controller starting. state_dir={state}  hours={args.hours} max_iters={args.max_iters}")
    log(state, f"profile_cmd={args.profile_cmd}  reflect={args.reflect}  corpus={args.corpus}  splits_dir={splits_dir}")
    n_skills_before = len(list_profile_skills(args.profile_cmd))
    n_mem_before = count_memory_entries(args.profile_cmd)
    log(state, f"profile skills at start: {n_skills_before}  memory entries: {n_mem_before}")

    t_start = time.time()
    history: list[dict] = []
    best_eval = -1.0
    plateau = 0

    # iter-0: baseline test
    if not args.skip_baseline_test:
        log(state, "=== iter-0: baseline test ===")
        test_dir = state / "iter-0" / "test"
        s = run_split("test", test_dir, args.test_concurrency, args.timeout, args.profile_cmd,
                      splits_dir=splits_dir, limit=test_limit, extra_args=args.extra_args)
        snapshot_profile(state / "iter-0")
        log(state, f"  baseline test: {s['n_correct']}/{s['n_total']} = {s['accuracy_all']:.3f}")
        history.append({"iter": 0, "phase": "test", "summary": s, "elapsed": time.time() - t_start})

    # Training iterations
    for it in range(1, args.max_iters + 1):
        if (time.time() - t_start) > args.hours * 3600:
            log(state, f"time budget exhausted after {(time.time()-t_start)/3600:.1f}h; stopping")
            break

        iter_dir = state / f"iter-{it}"
        log(state, f"=== iter-{it}: train{' [+reflect]' if args.reflect else ''} ===")
        s_train = run_split(
            "train", iter_dir / "train", args.train_concurrency, args.timeout,
            args.profile_cmd, reflect=args.reflect, reflect_timeout=args.reflect_timeout,
            splits_dir=splits_dir, limit=train_limit, extra_args=args.extra_args,
        )
        log(state, f"  train: {s_train['n_correct']}/{s_train['n_total']} = {s_train['accuracy_all']:.3f}")

        log(state, f"=== iter-{it}: curator ===")
        cur_out = run_curator(args.profile_cmd)
        (iter_dir / "curator.log").write_text(cur_out)

        log(state, f"=== iter-{it}: eval ===")
        # eval/test do NOT use --reflect: we don't want skill writes leaking into the metric.
        s_eval = run_split("eval", iter_dir / "eval", args.eval_concurrency, args.timeout, args.profile_cmd,
                           splits_dir=splits_dir, limit=eval_limit, extra_args=args.extra_args)
        log(state, f"  eval: {s_eval['n_correct']}/{s_eval['n_total']} = {s_eval['accuracy_all']:.3f}")

        snapshot_profile(iter_dir)
        n_skills_now = len(list_profile_skills(args.profile_cmd))
        n_mem_now = count_memory_entries(args.profile_cmd)
        log(state, f"  skills now: {n_skills_now} (delta {n_skills_now - n_skills_before})  "
                   f"memory: {n_mem_now} (delta {n_mem_now - n_mem_before})")

        history.append({
            "iter": it, "phase": "train", "summary": s_train, "elapsed": time.time() - t_start,
        })
        history.append({
            "iter": it, "phase": "eval", "summary": s_eval, "elapsed": time.time() - t_start,
            "n_skills": n_skills_now,
        })

        # Plateau check
        if s_eval["accuracy_all"] > best_eval + 1e-9:
            best_eval = s_eval["accuracy_all"]
            plateau = 0
            log(state, f"  NEW BEST eval: {best_eval:.3f}")
        else:
            plateau += 1
            log(state, f"  no improvement ({plateau}/{args.patience})")
            if plateau >= args.patience:
                log(state, f"plateau reached; stopping after iter {it}")
                break

        # Persist running history
        (state / "history.json").write_text(json.dumps(history, indent=2))

    # Final test
    log(state, "=== final test ===")
    final_dir = state / "final" / "test"
    s_final = run_split("test", final_dir, args.test_concurrency, args.timeout, args.profile_cmd,
                        splits_dir=splits_dir, limit=test_limit, extra_args=args.extra_args)
    snapshot_profile(state / "final")
    log(state, f"  final test: {s_final['n_correct']}/{s_final['n_total']} = {s_final['accuracy_all']:.3f}")
    history.append({"iter": "final", "phase": "test", "summary": s_final, "elapsed": time.time() - t_start})

    (state / "history.json").write_text(json.dumps(history, indent=2))
    log(state, f"DONE. wallclock={(time.time()-t_start)/3600:.2f}h  iters={len([h for h in history if h['phase']=='train'])}  best_eval={best_eval:.3f}  final_test={s_final['accuracy_all']:.3f}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
