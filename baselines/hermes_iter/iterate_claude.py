#!/usr/bin/env python3
"""Claude Code + Fable 5 skill-curation loop (self-contained).

A meta-optimization loop where headless **Claude Code** (model `claude-fable-5`
by default) iteratively improves on the OfficeQA training set by **curating
skills** — the Claude-harness analogue of the Hermes `iterate.py` loop.

Per iteration:
  train+reflect : answer each train question (`claude -p`), then a reflection
                  call that may Write/patch `SKILL.md` files into the project's
                  `.claude/skills/` (the persistent, evolving scaffold).
  curate        : one `claude -p` pass that reviews / merges / prunes the skills.
  eval          : answer-only pass on the eval split, scored.
Stops on plateau (`--patience`) or `--max-iters`.

The ONLY persistent scaffold is `<state>/project/.claude/skills/`. Auto-memory
and CLAUDE.md are disabled on every call so nothing else leaks across questions;
the reflection/curate calls may still WRITE skill files there.
"""
from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import time
import uuid
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT / "baselines"))
from reward import extract_final_answer, score_answer  # noqa: E402

# auto-memory + CLAUDE.md off → the staged skills are the only cross-question scaffold
HERMETIC_ENV = {"CLAUDE_CODE_DISABLE_AUTO_MEMORY": "1", "CLAUDE_CODE_DISABLE_CLAUDE_MDS": "1"}

REFLECT_PROMPT = """You just attempted an OfficeQA Treasury-Bulletin question. This is an iterative loop in which FUTURE runs read the skills you write right now.

Question:
{question}

Your answer:    {predicted}
Correct answer: {gold}
Verdict:        {verdict}

If — and ONLY if — something GENERALIZABLE was learned that will help future Treasury-Bulletin questions (a recurring table location, a unit/scaling convention, a retrieval/parsing tactic, an arithmetic pitfall), record it as a procedural skill:
- Use the Write tool to create or update `.claude/skills/<short-kebab-name>/SKILL.md` (relative to the current directory).
- SKILL.md must begin with frontmatter (`---` then `name:` and a one-line `description:` that says WHEN to use it, then `---`), followed by concrete, actionable steps a future agent can apply without re-deriving them.
- First read the existing `.claude/skills/` dir; PREFER patching a relevant existing skill over creating a near-duplicate.
Do NOT save per-question trivia (e.g. "UID0044 = 1461") or platitudes ("read carefully"). If nothing generalizable came up — which is common — reply "no skill needed" and write nothing.
"""

CURATE_PROMPT = """You are curating the skills library at `.claude/skills/` for an OfficeQA Treasury-Bulletin agent. Review every `.claude/skills/*/SKILL.md`, then improve the library IN PLACE using Read / Write / Bash:
- Merge near-duplicate skills into one stronger skill (and `rm -rf` the redundant dirs).
- Delete skills that are per-question trivia, wrong, or not generalizable.
- Tighten each `description:` so it clearly states when the skill applies.
Keep the library small and high-signal. End with a one-line summary of what you changed.
"""


def log(state: Path, msg: str) -> None:
    line = f"[{datetime.now().strftime('%H:%M:%S')}] {msg}"
    print(line, flush=True)
    with open(state / "loop.log", "a") as f:
        f.write(line + "\n")


def claude_call(prompt: str, project: Path, extra_args: list[str], timeout: int,
                allow_write: bool) -> tuple[str, int]:
    env = os.environ.copy()
    env.update(HERMETIC_ENV)  # skills are still read/writable; this only blocks CLAUDE.md/auto-memory
    cmd = ["claude", "-p", "--dangerously-skip-permissions", "--session-id", str(uuid.uuid4()),
           *extra_args, prompt]
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout,
                           cwd=str(project), env=env)
        return p.stdout, p.returncode
    except subprocess.TimeoutExpired as e:
        out = (e.stdout or b"").decode("utf-8", "replace") if isinstance(e.stdout, bytes) else (e.stdout or "")
        return out, -1


def skills_dir(project: Path) -> Path:
    return project / ".claude" / "skills"


def count_skills(project: Path) -> int:
    return sum(1 for _ in skills_dir(project).glob("*/SKILL.md"))


def _ok(out: str, rc: int) -> bool:
    """A genuine completion (not a crash / rate-limit / SIGINT)."""
    s = (out or "").strip()
    return rc == 0 and bool(s) and s != "Execution error"


def call_retry(prompt: str, project: Path, extra_args: list[str], timeout: int,
               allow_write: bool, tries: int = 3) -> tuple[str, int]:
    """claude_call with backoff — so a transient rate-limit doesn't get scored as wrong."""
    out, rc = "", -1
    for attempt in range(tries):
        out, rc = claude_call(prompt, project, extra_args, timeout, allow_write)
        if _ok(out, rc):
            return out, rc
        time.sleep(30 * (attempt + 1))
    return out, rc


def answer_one(rec: dict, project: Path, extra_args: list[str], timeout: int,
               out_dir: Path) -> dict:
    # resume: reuse a cached genuine completion (a real wrong answer counts; a
    # crash/rate-limit does not, so it re-runs)
    cache = out_dir / f"{rec['uid']}.json"
    if cache.exists():
        try:
            d = json.loads(cache.read_text())
            if d.get("rc") == 0 and d.get("raw"):
                return d
        except Exception:
            pass
    out, rc = call_retry(rec["prompt"], project, extra_args, timeout, allow_write=False)
    try:
        pred = extract_final_answer(out) if out else ""
    except Exception:
        pred = ""
    try:
        sc = score_answer(rec["gold_answer"], pred) if pred else 0.0
    except Exception:
        sc = 0.0
    d = {"uid": rec["uid"], "predicted": pred, "score": sc, "rc": rc, "raw": out,
         "question": rec.get("question", ""), "gold": rec["gold_answer"]}
    if _ok(out, rc):
        cache.write_text(json.dumps(d, ensure_ascii=False))
    return d


def run_answers(rows: list[dict], project: Path, extra_args: list[str], timeout: int,
                concurrency: int, out_dir: Path) -> dict:
    out_dir.mkdir(parents=True, exist_ok=True)
    res = {}
    with ThreadPoolExecutor(max_workers=concurrency) as ex:
        futs = {ex.submit(answer_one, r, project, extra_args, timeout, out_dir): r["uid"] for r in rows}
        for fut in as_completed(futs):
            d = fut.result()
            res[d["uid"]] = d
    return res


def acc(res: dict) -> tuple[int, int]:
    n_corr = sum(1 for d in res.values() if d["score"] >= 1.0)
    return n_corr, len(res)


def load_rows(split: Path, limit: int) -> list[dict]:
    rows = [json.loads(l) for l in open(split) if l.strip()]
    return rows[:limit] if limit > 0 else rows


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--state-dir", required=True)
    p.add_argument("--train-split", required=True)
    p.add_argument("--eval-split", required=True)
    p.add_argument("--train-limit", type=int, default=0)
    p.add_argument("--eval-limit", type=int, default=0)
    p.add_argument("--max-iters", type=int, default=3)
    p.add_argument("--patience", type=int, default=2)
    p.add_argument("--model-args", default="--model claude-fable-5")
    p.add_argument("--answer-timeout", type=int, default=900)
    p.add_argument("--reflect-timeout", type=int, default=600)
    p.add_argument("--curate-timeout", type=int, default=1200)
    p.add_argument("--answer-concurrency", type=int, default=4)
    p.add_argument("--seed-skills", default="", help="dir of <name>/SKILL.md to copy in as the starting scaffold (default: empty)")
    p.add_argument("--no-curate", action="store_true", help="skip the curate pass")
    args = p.parse_args()

    extra = args.model_args.split()
    state = Path(args.state_dir)
    project = state / "project"
    (skills_dir(project)).mkdir(parents=True, exist_ok=True)
    state.mkdir(parents=True, exist_ok=True)

    # seed scaffold ONCE (default: empty). A marker guards against a resume/relaunch
    # re-copying seed skills over ones the loop has since curated.
    seeded = state / ".seeded"
    if args.seed_skills and not seeded.exists():
        seed = Path(args.seed_skills)
        for sk in seed.glob("*/SKILL.md"):
            shutil.copytree(sk.parent, skills_dir(project) / sk.parent.name, dirs_exist_ok=True)
        seeded.write_text(args.seed_skills)

    train = load_rows(Path(args.train_split), args.train_limit)
    ev = load_rows(Path(args.eval_split), args.eval_limit)
    log(state, f"start. model={args.model_args}  train={len(train)} eval={len(ev)}  "
               f"seed_skills={count_skills(project)}  max_iters={args.max_iters} patience={args.patience}")

    history = []
    best, plateau = -1.0, 0

    # iter-0 baseline eval (before any curation)
    r0 = run_answers(ev, project, extra, args.answer_timeout, args.answer_concurrency, state / "iter-0" / "eval")
    c, n = acc(r0)
    log(state, f"iter-0 baseline eval: {c}/{n} = {c/n:.3f}   skills={count_skills(project)}")
    history.append({"iter": 0, "phase": "eval", "correct": c, "n": n, "skills": count_skills(project)})

    for it in range(1, args.max_iters + 1):
        idir = state / f"iter-{it}"
        # 1. TRAIN (answers, concurrent)
        tr = run_answers(train, project, extra, args.answer_timeout, args.answer_concurrency, idir / "train")
        tc, tn = acc(tr)
        log(state, f"iter-{it} train: {tc}/{tn} = {tc/tn:.3f}")

        # 2. REFLECT (serial — concurrent skill writes would race on .claude/skills/)
        sb = count_skills(project)
        refl_dir = idir / "reflections"; refl_dir.mkdir(parents=True, exist_ok=True)
        for r in train:
            d = tr[r["uid"]]
            rfile = refl_dir / f"{d['uid']}.txt"
            if rfile.exists():      # resume: this question's reflection already applied
                continue
            verdict = "CORRECT" if d["score"] >= 1.0 else "WRONG"
            rp = REFLECT_PROMPT.format(question=d["question"], predicted=d["predicted"] or "(none)",
                                       gold=d["gold"], verdict=verdict)
            out, rc = call_retry(rp, project, extra, args.reflect_timeout, allow_write=True)
            if _ok(out, rc):        # only mark done on success, so failures re-run on resume
                rfile.write_text(out, encoding="utf-8")
        sa = count_skills(project)
        log(state, f"iter-{it} reflect: skills {sb} -> {sa} (+{sa - sb})")

        # 3. CURATE (one pass merges/prunes the concurrently-written skills)
        cfile = idir / "curate.txt"
        if not args.no_curate and sa > 0 and not cfile.exists():  # skip if already curated (resume)
            out, rc = call_retry(CURATE_PROMPT, project, extra, args.curate_timeout, allow_write=True)
            if _ok(out, rc):
                cfile.write_text(out, encoding="utf-8")
            log(state, f"iter-{it} curate: skills now {count_skills(project)} (rc={rc})")

        # 4. EVAL (answer-only, scored)
        er = run_answers(ev, project, extra, args.answer_timeout, args.answer_concurrency, idir / "eval")
        ec, en = acc(er)
        log(state, f"iter-{it} eval: {ec}/{en} = {ec/en:.3f}   skills={count_skills(project)}")

        # snapshot skills
        snap = idir / "skills_snapshot"
        if skills_dir(project).exists():
            shutil.copytree(skills_dir(project), snap, dirs_exist_ok=True)
        history.append({"iter": it, "phase": "eval", "correct": ec, "n": en,
                        "skills": count_skills(project), "train_acc": tc / tn})
        (state / "history.json").write_text(json.dumps(history, indent=2))

        if ec / en > best + 1e-9:
            best, plateau = ec / en, 0
            log(state, f"  NEW BEST eval {best:.3f}")
        else:
            plateau += 1
            log(state, f"  no improvement ({plateau}/{args.patience})")
            if plateau >= args.patience:
                log(state, "plateau; stopping")
                break

    log(state, f"DONE. best_eval={best:.3f}  final_skills={count_skills(project)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
