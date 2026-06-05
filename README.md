# office-qa

Harness and experiments for evaluating and **self-evolving** the Hermes Agent on
**OfficeQA** — a grounded document-reasoning benchmark over U.S. Treasury Bulletins
(1939–2025).

## Layout

```
baselines/
  reward.py                 # official-style fuzzy answer scorer
  run_oracle*.py, score.py  # non-agent oracle baselines
  viewer/                   # run inspection UI
  hermes_iter/              # Hermes self-evolution harness
    build_splits.py         # render per-question prompts for a corpus mode (seed 42)
    run_hermes_split.py     # run + score a profile over a split
    score_split.py          # (re)score a run dir
    iterate.py              # meta-optimization controller (train+reflect / eval / plateau)
    EXPERIMENTS.md          # >>> full experiment log & results <<<
    runs/                   # aggregate result summaries (heavy artifacts gitignored)
data/                       # gated OfficeQA corpus — NOT committed (see data/README.md)
```

## Start here

**[`baselines/hermes_iter/EXPERIMENTS.md`](baselines/hermes_iter/EXPERIMENTS.md)** —
methods, every run, the three corpus modes (PDF / parsed-MD / parsed-MD+PDF), the
Claude Opus 4.8 meta-optimization, cost analysis, and error analysis.

Headline: best held-out test result is **gpt-5.5 + raw-PDF + evolved scaffold,
24/28 = 0.857**. An Opus 4.8 fresh-profile meta-optimization did not beat its own
untrained baseline (0.643 vs 0.679) — see the report for why.

## Data & secrets

The OfficeQA corpus (PDFs, parsed text/JSON, augmented Markdown) and answer CSVs
are **gated** (CC-BY-SA + answer-key clause) and are **not** in this repo — download
them per [`data/README.md`](data/README.md). API keys go in `.env`
(see `.env.example`); never commit it.
