#!/usr/bin/env python3
"""Wire GEPA (reflective Pareto prompt evolution) into the OfficeQA harness.

GEPA evolves the ANSWERING INSTRUCTIONS for the no-oracle parsed-md task. Because
these questions need retrieval + python + sometimes web (a single LLM call floors
at ~0), each candidate is run as a full headless Claude Code agent (`claude -p`,
Opus 4.8) — a custom GEPAAdapter runs the batch concurrently, scores with reward.py,
and feeds natural-language feedback into GEPA's reflection. Comparable to the
opus48 curation result (0.607 on test-28).

After optimization, evaluates SEED vs BEST instructions on the held-out test split.
"""
from __future__ import annotations
import argparse, json, os, re, sys, urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT / "baselines"))
sys.path.insert(0, str(ROOT / "baselines" / "hermes_iter"))
from reward import extract_final_answer, score_answer  # noqa: E402
from iterate_claude import claude_call, skills_dir  # noqa: E402  (reuses the claude -p runner)
import gepa  # noqa: E402
from gepa.core.adapter import EvaluationBatch, GEPAAdapter  # noqa: E402

CORPUS = ROOT / "data" / "final_parsed_db_augmented"
API = "https://api.anthropic.com/v1/messages"
KEY = os.environ["ANTHROPIC_API_KEY"]
MODEL_ARGS = ["--model", "claude-opus-4-8"]

# input given to the agent per question (the candidate instructions are prepended as scaffold)
def input_block(q: str) -> str:
    return (f"Question: {q}\n\n"
            f"Treasury Bulletin corpus directory: {CORPUS}\n\n"
            f"Identify the relevant issue(s) and section(s) yourself (grep the corpus), read them, "
            f"then provide your final answer wrapped in <FINAL_ANSWER>...</FINAL_ANSWER>.")


SEED = """You are an analyst answering questions about U.S. Treasury Bulletins. You are given ONLY a question and the path to a corpus of pre-parsed Bulletin Markdown files (treasury_bulletin_{YEAR}_{MM}.sonnet46.md, monthly 1939-2025). Find the relevant issue(s) yourself.

- grep -rn the corpus for likely table titles/keywords to locate the issue and lines; a statistic usually appears in the issue for (or shortly after) its period — annual/fiscal tables often appear in a later issue.
- Tables are Markdown pipe tables; strip footnote markers ((r), *, 1/) before arithmetic; mind units (thousands vs millions vs billions), calendar vs fiscal year, and which dated column.
- Use python (execute_code) for computation; web-search for external constants the Bulletin does not print (e.g. CPI-U, FX rates) when a question requires them.

OUTPUT FORMAT (mandatory): end with the final answer wrapped in <FINAL_ANSWER>...</FINAL_ANSWER>. Inside, output only the value at the scale asked; no thousands separators; no units/'$' unless required; for a list, comma-separate exactly as the question prescribes (graders do exact-string matching)."""


def feedback(pred: str, gold: str, ok: bool) -> str:
    if ok:
        return f"Correct. Final answer '{pred}' matched gold."
    return (f"Incorrect. Extracted final answer '{pred or '(none)'}' vs gold '{gold}'. Likely cause to address in "
            f"the instructions: wrong source issue/table/row/column, wrong unit or scale, rounding/decimal-place "
            f"mismatch, footnote/revised value mishandled, a missing external constant (CPI/FX) not fetched, or an "
            f"output-format mismatch (exact-string grader). Generalize the fix, do not hardcode this answer.")


def _run_one(rec, instructions, project, timeout):
    prompt = instructions + "\n\n" + input_block(rec["question"])
    out, rc = claude_call(prompt, project, MODEL_ARGS, timeout, allow_write=False)
    try:
        pred = extract_final_answer(out) if out else ""
    except Exception:
        pred = ""
    try:
        sc = score_answer(rec["gold_answer"], pred) if pred else 0.0
    except Exception:
        sc = 0.0
    return {"uid": rec["uid"], "pred": pred, "score": sc, "out": out or ""}


class OfficeQAAgentAdapter(GEPAAdapter):
    def __init__(self, project: Path, timeout: int = 1200, concurrency: int = 4):
        self.project = project
        self.timeout = timeout
        self.concurrency = concurrency

    def evaluate(self, batch, candidate, capture_traces=False):
        instr = next(iter(candidate.values()))
        with ThreadPoolExecutor(max_workers=self.concurrency) as ex:
            results = list(ex.map(lambda r: _run_one(r, instr, self.project, self.timeout), batch))
        outputs, scores, trajs = [], [], ([] if capture_traces else None)
        for rec, res in zip(batch, results):
            outputs.append({"full_assistant_response": res["out"]})
            scores.append(res["score"])
            if trajs is not None:
                trajs.append({"data": rec, "full_assistant_response": res["out"],
                              "feedback": feedback(res["pred"], rec["gold_answer"], res["score"] >= 1.0)})
        return EvaluationBatch(outputs=outputs, scores=scores, trajectories=trajs, objective_scores=None)

    def make_reflective_dataset(self, candidate, eval_batch, components_to_update):
        comp = components_to_update[0]
        items = []
        for t in eval_batch.trajectories:
            r = t["data"]
            items.append({
                "Inputs": f"Question: {r['question']}",
                "Generated Outputs": (t["full_assistant_response"] or "")[-1500:],
                "Feedback": t["feedback"],
            })
        return {comp: items}


def reflection_lm(model: str):
    def call(prompt):
        if isinstance(prompt, list):
            system = next((m["content"] for m in prompt if m.get("role") == "system"), "")
            user = "\n\n".join(m["content"] for m in prompt if m.get("role") != "system")
        else:
            system, user = "", prompt
        body = json.dumps({"model": model, "max_tokens": 8000, "system": system,
                           "messages": [{"role": "user", "content": user}]}).encode()
        req = urllib.request.Request(API, data=body, headers={
            "x-api-key": KEY, "anthropic-version": "2023-06-01", "content-type": "application/json"})
        for attempt in range(4):
            try:
                with urllib.request.urlopen(req, timeout=180) as rr:
                    d = json.loads(rr.read())
                return "".join(b.get("text", "") for b in d.get("content", []) if b.get("type") == "text")
            except Exception:
                if attempt == 3:
                    return ""
                import time; time.sleep(20 * (attempt + 1))
    return call


def eval_on(adapter, rows, instr):
    eb = adapter.evaluate(rows, {"instructions": instr}, capture_traces=False)
    return sum(1 for s in eb.scores if s >= 1.0), len(eb.scores)


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--train", default="baselines/hermes_iter/splits_parsed_md_nooracle/train.jsonl")
    p.add_argument("--val", default="baselines/hermes_iter/splits_parsed_md_nooracle/eval.jsonl")
    p.add_argument("--test", default="baselines/hermes_iter/splits_parsed_md_nooracle/test.jsonl")
    p.add_argument("--train-limit", type=int, default=15)
    p.add_argument("--val-limit", type=int, default=10)
    p.add_argument("--max-metric-calls", type=int, default=60)
    p.add_argument("--concurrency", type=int, default=4)
    p.add_argument("--run-dir", default="baselines/hermes_iter/runs/gepa_opus_nooracle")
    args = p.parse_args()

    run = Path(args.run_dir); project = run / "project"
    skills_dir(project).mkdir(parents=True, exist_ok=True)  # empty: instructions are the only scaffold

    def load(path, lim):
        rows = [json.loads(l) for l in open(path) if l.strip()]
        return rows[:lim] if lim > 0 else rows

    trainset = load(args.train, args.train_limit)
    valset = load(args.val, args.val_limit)
    testset = load(args.test, 0)
    print(f"train={len(trainset)} val={len(valset)} test={len(testset)}  budget={args.max_metric_calls}", flush=True)

    adapter = OfficeQAAgentAdapter(project, timeout=1200, concurrency=args.concurrency)
    result = gepa.optimize(
        seed_candidate={"instructions": SEED},
        trainset=trainset, valset=valset,
        adapter=adapter,
        reflection_lm=reflection_lm("claude-opus-4-8"),
        candidate_selection_strategy="pareto",
        max_metric_calls=args.max_metric_calls,
        run_dir=str(run),
    )
    best = result.best_candidate["instructions"]
    (run / "seed_instructions.txt").write_text(SEED)
    (run / "best_instructions.txt").write_text(best)
    print("\n=== BEST INSTRUCTIONS (head) ===\n" + best[:1200], flush=True)

    print("\n=== held-out TEST-28 (no-oracle agent): SEED vs BEST ===", flush=True)
    s_c, n = eval_on(adapter, testset, SEED)
    b_c, _ = eval_on(adapter, testset, best)
    print(f"SEED: {s_c}/{n} = {s_c/n:.3f}", flush=True)
    print(f"BEST: {b_c}/{n} = {b_c/n:.3f}   (curation baseline on this split: 0.607)", flush=True)
    (run / "summary.json").write_text(json.dumps({
        "test_n": n, "seed_correct": s_c, "best_correct": b_c,
        "seed_acc": s_c / n, "best_acc": b_c / n}, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
