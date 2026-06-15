# Meta-optimization on OfficeQA: skill curation vs GEPA (reflective prompt evolution)

All numbers below are on the **held-out test split (28 Q)**, **no-oracle** retrieval over
the **parsed-md** corpus, **Claude Opus 4.8** as the agent (`claude -p`). Same setting,
so they're directly comparable.

## Headline

| approach | what is optimized | data (train/val) | test-28 | clean? |
|---|---|---|---|---|
| hand-written seed prompt | — | — | **0.607–0.643** (same prompt, two runs) | ✅ |
| **Skill curation** (Claude Code loop, memorized 26 skills) | a skill library | 80 / 25 | 0.607 | ❌ answer-key memorized |
| Skill curation, **scrubbed** 26 skills | skill library (answers removed) | 80 / 25 | 0.607 | ✅ |
| GEPA, small run | the answering **instructions** | 15 / 10 | seed 0.607 → best **0.643** | ✅ |
| **GEPA, data-matched** | the answering **instructions** | 80 / 25 | seed 0.643 → best **0.607** | ✅ |

**Takeaways (revised after the data-matched GEPA run)**
1. **It's within noise — no method reliably beats the seed.** The *identical seed prompt*
   scored **0.607** in one run and **0.643** in another (the agent, `claude -p`, is
   stochastic). So the small GEPA run's "win" (0.607→0.643) and the data-matched run's
   "loss" (0.643→0.607) are **both noise**. On 28 questions, ±1 question = ±3.6 pp, and the
   agent alone swings the same prompt by a question. Curation (0.607), both GEPA runs, and
   the bare seed all sit in a **~0.60–0.64 band inside the eval's noise floor**. No
   meta-optimization method here moves held-out accuracy beyond that.
2. **The qualitative difference is real, though.** Curation *memorizes* — 111 "Verified"
   answer markers and 732 specific values across the 26 skills (60% of the 180 KB library is
   embedded answers), and scrubbing them changed held-out accuracy by **zero** (0.607→0.607).
   GEPA *doesn't* — ≈0 memorized values across all candidates (8 KB of pure method). So GEPA
   is structurally cleaner and ~10–20× cheaper, even though neither lifts accuracy.
3. **What IS beyond noise:** the *model* gap (Fable-5 parsed-md no-oracle 0.821 vs Opus ~0.64,
   a 5-question gap) and the *oracle* gap (gpt-5.5 + raw-PDF + oracle 0.857). Method/scaffold
   changes within Opus are noise; model and retrieval-setting changes are not.

> Methodological note: a 28-question held-out set is too small to resolve the ±1–2-question
> deltas these meta-opt methods produce. A real signal would need a much larger held-out set
> (or repeated runs with variance estimation). The 0.607↔0.643 seed swing above is the
> direct evidence of that noise floor.

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
