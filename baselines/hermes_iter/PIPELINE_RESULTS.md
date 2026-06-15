# Fixed agentic pipeline + failure-driven optimization (vs the free agent)

Held-out **test-28**, **no-oracle** retrieval over the **parsed-md** corpus, **Claude Opus 4.8**.
Directly comparable to the meta-optimization numbers in `METHODS_COMPARISON.md`.

## The two artifacts
- **`pipeline_eval.py`** — a *fixed*, code-orchestrated agentic pipeline (the ADAS/AFlow
  point in the design space, as opposed to the free monolithic `claude -p` agent):
  `LOCATE` (LLM→issue files+keywords) → `RETRIEVE` (deterministic grep windows) →
  `SOLVE` (LLM→python, executed sandboxed) → `FORMAT` (LLM→exact answer), with an
  optional bounded **`VERIFY`→retry** loop (re-LOCATE on retrieval failure, re-SOLVE on a
  failed verify).
- **`optimize_pipeline.py`** — a failure-driven **self-improvement loop** (ADAS-style code
  evolution): run the pipeline on a dev set → digest the failures (traces) → a meta-agent
  (Opus) rewrites the *whole pipeline file* to fix the dominant failure → validate
  (compile + smoke) → dev-eval → keep only if dev improves → repeat → report on held-out test.

## Results

| configuration | test-28 | note |
|---|---|---|
| free adaptive agent (Opus, no-oracle) | **~0.61–0.64** | the strong baseline (`METHODS_COMPARISON.md`) |
| fixed pipeline, single-pass | **1/28 = 0.036** | 6 retrieval-fail, 4 near-miss, ~17 wrong |
| fixed pipeline + verify/retry | **1/28 = 0.036** | 4× the work, abstentions 6→14, **no gain** |
| fixed pipeline, 4-iter optimization loop | **1/28 = 0.036** | no rewrite beat the seed on dev |

## What we learned (the interesting part)

1. **A fixed pipeline collapses (~18× below the free agent).** Decomposing the agent into
   single-pass stages removes its *iterate-and-verify* behavior — re-grep until the right
   table is found, re-read to confirm each value, retry the computation. The near-misses
   prove the pipeline often *locates* the data but can't *nail the precision* in one pass.

2. **Verify/retry doesn't help — it just abstains more.** Adding a VERIFY gate drove the
   pipeline to "Cannot be determined" (abstentions 6→14) instead of recovering, because the
   bottleneck is the *retrieval mechanism* (a one-shot grep window), not lack of verification.

3. **Failure-driven optimization fixes the loudest symptom and unmasks the next layer.**
   The meta-agent correctly diagnosed "7/12 abstain → retrieval starvation" every iteration
   and correctly fixed it (read full files → **abstentions 7→0**) — but **accuracy didn't
   move**: it converted "I can't find it" abstentions into "here's a wrong answer" errors.
   So retrieval was never the real bottleneck — it was the loudest one. The true gate is
   **single-pass extraction/reasoning precision**, which the loop can't reach without
   essentially rebuilding the agent's iteration. (It also can't hill-climb cleanly: a 12-Q
   dev set at 1/12 is within noise.)

**Bottom line.** The free, adaptive agent's edge is the iterative extract-and-verify loop,
not retrieval *access*. Consistent with the meta-opt findings: scaffold/structure changes
don't lift Opus on this benchmark — **model** (Fable-5 0.821) and **oracle retrieval**
(gpt-5.5+PDF 0.857) do.

## Reproduce
```bash
# fixed pipeline (basic + verify/retry are the same file; verify/retry is on by default):
python baselines/hermes_iter/pipeline_eval.py --split <test.jsonl> --run-dir runs/fixed_pipeline_test
# failure-driven optimization loop:
python baselines/hermes_iter/optimize_pipeline.py --max-iters 4 --dev-limit 12 --concurrency 4
```

> Artifacts under `runs/fixed_pipeline_test/`, `runs/fixed_pipeline_v2_test/`,
> `runs/pipeline_optloop/` are scrubbed of gated gold-answer values
> (`scrub_pipeline_artifacts.py`); the `gold` field is dropped and verbatim answers redacted.
