# Skills authored by Claude Fable 5 (curtailed curation run)

The **28 skills below were written by `claude-fable-5`** during iteration 1 of the
Claude Code skill-curation loop (`iterate_claude.py`), starting from an **empty
scaffold**, on the OfficeQA Treasury-Bulletin **train split** (parsed-md, no-oracle).

They are a one-of-a-kind artifact: **Anthropic pulled Fable 5 mid-run** (the API now
returns *"Claude Fable 5 is not available. Please use Opus 4.8"*), so this run can't be
reproduced with the same model.

## Provenance / trajectory (`../loop.log`)
```
iter-0 baseline eval : 17/25 = 0.680   (empty scaffold)
iter-1 train         : 48/80 = 0.600
iter-1 reflect       : skills 0 -> 28   ← these files (Fable, serial reflection)
iter-1 curate        : rc=1             ← curate pass ERRORED as Fable was being pulled
iter-1 eval onward   : 0/25, 0/80       ← invalid (model gone), discarded
```

**Caveat:** these are the **raw per-question reflection writes**. The consolidation
(curate) pass failed (`rc=1`) right as Fable dropped, so they are **un-curated** — expect
some overlap/redundancy and possible answer-value examples that a curate pass would have
merged/scrubbed. Per-question reflection rationales are in `../iter-1/reflections/`.

## Contents (28 skills)
Each `<name>/SKILL.md` is a standard Claude Code skill (frontmatter `name` + `description`,
then procedural steps). Topics span the benchmark's table families — e.g.
`tb-statutory-debt-limit`, `tb-esf-balance-sheet`, `tb-capital-movements-weekly`,
`tb-bill-auction-rates`, `tb-securities-ownership`, `tb-bond-yields`, plus cross-cutting
ones like `answer-format-exact-match` and `tb-math-transform-wrappers`.

The follow-on run (`runs/opus48_claude_loop_fableseed/`) continues curation from these 28
with `claude-opus-4-8` as the backbone (Fable's replacement).
