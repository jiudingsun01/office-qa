# Meta-optimization on OfficeQA: skill curation vs GEPA (reflective prompt evolution)

All numbers below are on the **held-out test split (28 Q)**, **no-oracle** retrieval over
the **parsed-md** corpus, **Claude Opus 4.8** as the agent (`claude -p`). Same setting,
so they're directly comparable.

## Headline

| approach | what is optimized | test-28 | clean? | cost |
|---|---|---|---|---|
| no scaffold (hand-written seed prompt) | — | 17/28 = 0.607 | ✅ | — |
| **Skill curation** (Claude Code loop, memorized 26 skills) | a skill library | 17/28 = **0.607** | ❌ answer-key memorized | ~hundreds of agent rollouts (+ a $1,230 Opus meta-opt earlier) |
| Skill curation, **scrubbed** 26 skills | skill library (answers removed) | 17/28 = 0.607 | ✅ | — |
| **GEPA** (reflective Pareto prompt evolution) | the answering **instructions** | 18/28 = **0.643** | ✅ no memorization | **60 metric calls**, ~1.5 h |

**Takeaways**
1. **GEPA ≥ curation, and cleaner.** GEPA lifted its own seed 0.607 → 0.643 and beat the
   curation loop (0.607), evolving *generalizable instructions* (no embedded answers).
2. **Curation's "learning" was memorization.** Removing the memorized answers from the 26
   curated skills changed held-out accuracy by **zero** (0.607 → 0.607) — the apparent
   train gains (0.738 → 0.800) did not generalize. See `runs/{memorized26,scrubbed26}_opus_test/`.
3. **Sample efficiency.** GEPA reached a better, leak-free result with ~60 rollouts vs the
   curation loop's hundreds (and the earlier $1,230 Opus self-evolution meta-opt).

## What GEPA evolved (the generalizable method the curation loop failed to distill)
From `runs/gepa_opus_nooracle/best_instructions.txt` — all method, no memorized values:
- "annual/fiscal-year totals & full-year monthly series often appear in a **LATER** issue
  (a complete prior-year table appears in a Jan–Mar issue of the following year)."
- "Use python (`execute_code`) for **ALL** arithmetic."
- "**PREFER THE MOST FINAL/REVISED FIGURES**" (the reprinted-and-revised-values trap).
- match the thousands-separator convention; web-search **only** for external constants (CPI/FX).

## Caveats
- **Noisy:** +1 question on 28 is within noise. The direction (and the clean mechanism) is
  the signal; a larger-budget GEPA run (train 40 / val 25 / ~200 calls) would firm up the Δ.
- **Band:** Opus on this benchmark sits in a ~0.60–0.64 held-out band regardless of method;
  GEPA reaches the top of it cleanly, but doesn't break out. The strongest results overall
  remain non-evolved: gpt-5.5 + raw-PDF + oracle = 0.857, and Fable-5 + parsed-md no-oracle
  (direct, before it was pulled) = 0.821.

## How to reproduce
```bash
# curation loop:   python baselines/hermes_iter/iterate_claude.py ...
# scrub skills:     python baselines/hermes_iter/scrub_skills.py --skills-dir <mem> --out <scrub>
# eval a library:   python baselines/hermes_iter/eval_skills_claude.py --skills-dir <dir> --split <test>
# GEPA:             python baselines/hermes_iter/gepa_optimize.py --train-limit 15 --val-limit 10 --max-metric-calls 60
```
