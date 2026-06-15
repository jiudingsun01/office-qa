#!/usr/bin/env python3
"""Failure-driven pipeline optimization (ADAS-style code evolution).

Loop: run the current pipeline on a dev set -> digest its failures (with per-question
traces) -> a meta-agent (Opus) rewrites the WHOLE pipeline file to fix the dominant
failure cause -> validate (compile + 2-q smoke) -> dev-eval -> keep only if dev score
improves. The optimizable artifact is a self-contained pipeline file that exposes the
same CLI (--split/--run-dir/--limit/--concurrency, writes summary.json + preds/).
Finally evaluates the best pipeline on held-out test-28.
"""
from __future__ import annotations
import argparse, json, os, re, shutil, subprocess, sys, time, urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
PY = sys.executable
API = "https://api.anthropic.com/v1/messages"
KEY = os.environ["ANTHROPIC_API_KEY"]
MODEL = "claude-opus-4-8"

META_SYS = """You are improving a Python agentic pipeline for OfficeQA (U.S. Treasury Bulletin QA, no-oracle: the agent must find the right monthly-issue Markdown file in a corpus and compute the answer). You receive the FULL current pipeline source and a digest of its failures on a dev set (per-question traces: located files, keywords, computed result, predicted vs gold, whether retrieval was empty / it abstained).

Diagnose the DOMINANT, recurring failure cause and rewrite the pipeline to fix it. You may change anything: the retrieval mechanism (e.g., read fuller/whole files instead of small grep windows, multi-round grep, better keyword or window logic, follow table continuations), the stage prompts, the control/verify/retry flow, value extraction, formatting. Make a focused, substantive change — not cosmetic.

HARD CONSTRAINTS (must hold or your version is discarded):
- Keep the command-line interface: argparse with --split, --run-dir, --limit, --concurrency.
- Write run_dir/summary.json as {"n_total":int,"n_correct":int,"accuracy":float} and run_dir/preds/<uid>.json per question.
- Score with reward.py: `from reward import extract_final_answer, score_answer` (importable; PYTHONPATH is set). A prediction is correct iff score_answer(gold, pred) >= 1.0. Each split row has keys: uid, question, gold_answer.
- Read the corpus directory from `os.environ.get("OFFICEQA_CORPUS")` (fall back to "data/final_parsed_db_augmented"); it holds <stem>.sonnet46.md files, stem = treasury_bulletin_{YEAR}_{MM}. Make Anthropic API calls (model claude-opus-4-8) using ANTHROPIC_API_KEY; do NOT use any other network. If you exec model-written python, keep it sandboxed (subprocess, timeout, no network/fs-write).
- Self-contained single file; runs with the same venv.

Output ONLY the complete revised python file (no prose, no code fences)."""


def anthropic(system: str, user: str, max_tokens: int) -> str:
    body = json.dumps({"model": MODEL, "max_tokens": max_tokens, "system": system,
                       "messages": [{"role": "user", "content": user}]}).encode()
    req = urllib.request.Request(API, data=body, headers={
        "x-api-key": KEY, "anthropic-version": "2023-06-01", "content-type": "application/json"})
    for attempt in range(4):
        try:
            with urllib.request.urlopen(req, timeout=300) as r:
                d = json.loads(r.read())
            return "".join(b.get("text", "") for b in d.get("content", []) if b.get("type") == "text")
        except Exception:
            if attempt == 3:
                return ""
            time.sleep(20 * (attempt + 1))
    return ""


def run_candidate(cand: Path, split: str, run_dir: Path, limit: int, conc: int, timeout: int):
    root = HERE.parent.parent
    split = split if Path(split).is_absolute() else str(root / split)
    run_dir = run_dir if run_dir.is_absolute() else (root / run_dir)
    env = {**os.environ, "OFFICEQA_ROOT": str(root),
           "OFFICEQA_CORPUS": str(root / "data" / "final_parsed_db_augmented"),
           "PYTHONPATH": f"{root}/baselines:{root}/baselines/hermes_iter"
                         + (":" + os.environ["PYTHONPATH"] if os.environ.get("PYTHONPATH") else "")}
    if run_dir.exists():
        shutil.rmtree(run_dir)
    cmd = [PY, str(cand), "--split", split, "--run-dir", str(run_dir),
           "--limit", str(limit), "--concurrency", str(conc)]
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout, cwd=str(root), env=env)
    except subprocess.TimeoutExpired:
        r = None
    summ = run_dir / "summary.json"
    if not summ.exists():
        if r is not None:
            (run_dir.parent / (run_dir.name + "_stderr.txt")).write_text((r.stderr or "")[-3000:])
        return None
    s = json.loads(summ.read_text())
    preds = [json.loads(p.read_text()) for p in (run_dir / "preds").glob("*.json")]
    return s["n_correct"], s["n_total"], preds


def digest(preds: list[dict]) -> str:
    fails = [d for d in preds if d.get("score", 0) < 1]
    abst = sum(1 for d in fails if "cannot" in (d.get("predicted") or "").lower()
               or "insufficient" in (d.get("predicted") or "").lower() or not d.get("result"))
    lines = [f"{len(fails)}/{len(preds)} failed (abstentions: {abst})."]
    for d in fails[:12]:
        att = d.get("attempts") or []
        last = att[-1] if att else {}
        lines.append(f"- {d['uid']}: pred {str(d.get('predicted'))[:45]!r} vs gold {str(d.get('gold'))[:28]!r}; "
                     f"files={d.get('files')} kw={ (d.get('keywords') or [])[:3]} n_attempts={d.get('n_attempts',1)} "
                     f"last={ {k: str(v)[:60] for k,v in last.items()} }")
    return "\n".join(lines)


def validate(cand: Path, split: str, tmp: Path, timeout: int) -> bool:
    r = subprocess.run([PY, "-m", "py_compile", str(cand)], capture_output=True, text=True)
    if r.returncode != 0:
        return False
    out = run_candidate(cand, split, tmp, 2, 2, timeout)
    return out is not None


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--seed", default=str(HERE / "pipeline_eval.py"))
    p.add_argument("--dev-split", default="baselines/hermes_iter/splits_parsed_md_nooracle/train.jsonl")
    p.add_argument("--test-split", default="baselines/hermes_iter/splits_parsed_md_nooracle/test.jsonl")
    p.add_argument("--dev-limit", type=int, default=12)
    p.add_argument("--max-iters", type=int, default=4)
    p.add_argument("--concurrency", type=int, default=4)
    p.add_argument("--state-dir", default="baselines/hermes_iter/runs/pipeline_optloop")
    args = p.parse_args()

    state = Path(args.state_dir); state.mkdir(parents=True, exist_ok=True)
    log = lambda m: (print(m, flush=True), open(state / "loop.log", "a").write(m + "\n"))

    best = state / "best_pipeline.py"
    shutil.copy(args.seed, best)
    out = run_candidate(best, args.dev_split, state / "iter-0_dev", args.dev_limit, args.concurrency, 2400)
    if out is None:
        log("seed failed to run"); return 1
    best_c, n, best_preds = out
    log(f"iter-0 (seed) dev: {best_c}/{n} = {best_c/n:.3f}")
    hist = [{"iter": 0, "dev": best_c / n}]

    for it in range(1, args.max_iters + 1):
        src = best.read_text()
        dig = digest(best_preds)
        (state / f"iter-{it}_failures.txt").write_text(dig)
        log(f"=== iter-{it}: meta-agent proposing a fix ===")
        raw = anthropic(META_SYS, f"CURRENT PIPELINE SOURCE:\n```python\n{src}\n```\n\nDEV FAILURE DIGEST:\n{dig}", 20000)
        (state / f"iter-{it}_raw.txt").write_text(raw)
        # robustly extract the code: take everything after the first ```python fence, drop a trailing fence
        mt = re.search(r"```(?:python)?[ \t]*\n", raw)
        new = raw[mt.end():] if mt else raw.strip()
        new = re.sub(r"\n```[ \t]*\n?\s*$", "\n", new)
        cand = state / f"iter-{it}_candidate.py"
        cand.write_text(new)
        if not validate(cand, args.dev_split, state / f"iter-{it}_smoke", 600):
            log(f"  iter-{it}: candidate invalid (compile/smoke failed) — revert"); hist.append({"iter": it, "dev": "invalid"}); continue
        out = run_candidate(cand, args.dev_split, state / f"iter-{it}_dev", args.dev_limit, args.concurrency, 2400)
        if out is None:
            log(f"  iter-{it}: candidate dev-eval failed — revert"); hist.append({"iter": it, "dev": "failed"}); continue
        c, n, preds = out
        log(f"  iter-{it} dev: {c}/{n} = {c/n:.3f}  (best {best_c}/{n})")
        hist.append({"iter": it, "dev": c / n})
        if c > best_c:
            best_c, best_preds = c, preds; shutil.copy(cand, best)
            log(f"  iter-{it}: NEW BEST dev {c/n:.3f} — adopted")
        else:
            log(f"  iter-{it}: no dev improvement — kept previous best")
        (state / "history.json").write_text(json.dumps(hist, indent=2))

    log("=== final: best pipeline on held-out TEST-28 ===")
    out = run_candidate(best, args.test_split, state / "final_test", 0, args.concurrency, 3000)
    if out:
        c, n, _ = out
        log(f"  best pipeline test-28: {c}/{n} = {c/n:.3f}  (basic pipeline was 1/28=0.036; free agent ~0.64)")
        (state / "summary.json").write_text(json.dumps({"dev_best": best_c / args.dev_limit, "test_correct": c, "test_n": n, "test_acc": c / n, "history": hist}, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
