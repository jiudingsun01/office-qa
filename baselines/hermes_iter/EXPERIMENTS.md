# Hermes Agent self-evolution on OfficeQA — experiment log

This document records the full set of experiments run with the **Hermes Agent**
self-evolution harness against the **OfficeQA** benchmark (U.S. Treasury Bulletin
document-reasoning QA), including the corpus ablations and the
**Claude Opus 4.8** meta-optimization.

- Benchmark: OfficeQA Pro, N=133 (Treasury Bulletins, 1939–2025).
- Split (seed 42): **train 80 / eval 25 / test 28**. `test` is held out from all training.
- Scoring: `baselines/reward.py` — fuzzy numeric match, unit-aware, tolerance 0.
- Answer protocol: agent must emit `<FINAL_ANSWER>…</FINAL_ANSWER>`.

> **TL;DR.** The best configuration on the held-out test split remains the
> original **gpt-5.5 + raw-PDF + gpt-5.5-evolved scaffold = 24/28 (0.857)**.
> Switching the backend to Opus 4.8 did **not** beat it: a fresh-profile Opus 4.8
> meta-optimization (10.8 h, ~$1,230) ended at **18/28 (0.643)** on test — *below*
> its own untrained baseline of 19/28 (0.679). Evidence points to (a) the
> gpt-5.5-evolved scaffold being actively harmful to Opus, and (b) the Opus
> meta-opt over-fitting the train split (0.762) while the eval ceiling stayed flat
> at 0.720.

---

## 1. Harness

All code lives in `baselines/hermes_iter/`.

| file | role |
|---|---|
| `build_splits.py` | Deterministically split `officeqa_pro.csv` (seed 42) and render per-question prompts for a chosen **corpus** mode. Writes `<split>.jsonl` + `manifest.json`. |
| `run_hermes_split.py` | Run a Hermes profile over a split (one subprocess per question), extract `<FINAL_ANSWER>`, score with `reward.py`. Optional `--reflect` second pass that drives `skill_manage`/`memory` writes. Resumable; `--limit`, `--uids`, `--extra-args`. |
| `score_split.py` | Re-score a run dir against a split → `summary.json` + `per_row.jsonl`. |
| `iterate.py` | Meta-optimization controller (see §3). |

### Corpus modes (`build_splits.py --corpus`)

| mode | what the prompt points at | tools suggested |
|---|---|---|
| `pdf` | original Treasury Bulletin PDF(s) | `pdftotext -layout`, `pdftoppm` |
| `parsed-md` | Sonnet-4.6-parsed Markdown (`data/final_parsed_db_augmented/*.sonnet46.md`): extracted text + Markdown tables + appended chart/figure descriptions | `read_file`, `grep -n`, `sed` |
| `parsed-md+pdf` | **both** paths per bulletin; Markdown is primary, PDF is the authoritative fallback for ambiguous parses / charts | markdown-first, PDF fallback |

The parsed-MD corpus was delivered as `final_parsed_db_augmented.tar.gz` (697
`*.sonnet46.md` files, ~372 MB) and extracted to `data/final_parsed_db_augmented/`.
Format details and an integration walkthrough are in §6.

---

## 2. The parsed-MD format

Each `treasury_bulletin_<YEAR>_<MM>.sonnet46.md` (~2k–10k lines) is, top to bottom:

1. **Front matter / TOC** — cover prose + the table of contents as a 2-col Markdown table.
2. **Body** — text and tables in document order. Tables are Markdown pipe tables;
   multi-level headers are flattened with `>` separators in a single header row;
   empty cells are `nan`; footnote markers (`(r)`, `*`, `1/`) are preserved inline.
   Original PDF pages are marked by standalone lines like `-15-` (best-effort).
3. **`# Chart Descriptions`** (trailing) — natural-language descriptions of charts/
   figures that were rasterized in the source PDF (axes, series, legend, source
   cross-ref, and `See chart at: <pdf> page N`). Pages without a chart say
   `[No chart detected on this page]`.

---

## 3. Meta-optimization controller (`iterate.py`)

```
iter-0:  test                                  (baseline, before any learning)
iter-N:  train [+reflect] → curator run → eval → snapshot skills+memory
final:   test                                  (held-out)
```

- `--reflect` makes a second Hermes call after each *train* question, instructing it
  to write a procedural **skill** (`skill_manage`) or a durable **memory** entry when
  something generalizable was learned. Reflection runs on **train only** — never on
  eval/test, so skill writes don't leak into the reported metric.
- Stops on any of: `--hours` budget, `--max-iters`, or **eval plateau** (`--patience`
  iters with no new best eval).
- `--corpus` selects the matching splits dir; `--extra-args` is forwarded to every
  Hermes call (used to pass `-m claude-opus-4-8 --provider anthropic`); `--smoke`
  shrinks every split for a cheap pipeline check.

---

## 4. Runs

Profiles:
- **`officeqa-iter-v2`** — gpt-5.5 (Stanford Azure Foundry gateway). The original
  meta-opt evolved this to 123 skills / 22 memory entries.
- **`officeqa-iter-opus48`** — **claude-opus-4-8** (Anthropic). Cloned from v2's
  *config only*, then reset to the 87 base skills / 0 memory before training, so it
  starts where v2 started.

| # | run dir | corpus | backend | scaffold at eval | phase reported |
|---|---|---|---|---|---|
| 1 | `runs/iter02` | pdf | gpt-5.5 | gpt-5.5-evolved (8 iters) | final test |
| 2 | `runs/parsed_md_test` | parsed-md | gpt-5.5 | gpt-5.5-evolved (v2) | test |
| 3 | `runs/opus48_parsed_md_test` | parsed-md | **opus-4.8** | gpt-5.5-evolved (v2) | test |
| 4 | `runs/opus48_smoke_metaopt` | parsed-md+pdf | **opus-4.8** | fresh, smoke (2 iters, 5-Q) | — |
| 5 | `runs/opus48_full_metaopt` | parsed-md+pdf | **opus-4.8** | fresh, full meta-opt (5 iters) | baseline + final test |

---

## 5. Results

### 5.1 Held-out test (28 Q)

| config | corpus | backend | scaffold | **test acc** |
|---|---|---|---|---|
| iter02 baseline | pdf | gpt-5.5 | none | 21/28 = 0.750 |
| **iter02 final** | pdf | gpt-5.5 | gpt-5.5-evolved | **24/28 = 0.857** |
| parsed_md_test | parsed-md | gpt-5.5 | gpt-5.5-evolved | 21/28 = 0.750 |
| opus48_parsed_md | parsed-md | opus-4.8 | gpt-5.5-evolved | 18/28 = 0.643 |
| opus48 baseline | parsed-md+pdf | opus-4.8 | none | 19/28 = 0.679 |
| **opus48 evolved** | parsed-md+pdf | opus-4.8 | opus-evolved | **18/28 = 0.643** |

### 5.2 Opus 4.8 full meta-opt trajectory (`opus48_full_metaopt`)

| phase | train | eval | note |
|---|---|---|---|
| iter-0 baseline test | — | — | test 19/28 = 0.679 |
| iter-1 | 53/80 = .662 | 17/25 = .680 | new best |
| iter-2 | 57/80 = .713 | 18/25 = **.720** | **best eval** |
| iter-3 | 58/80 = .725 | 15/25 = .600 | plateau 1/3 |
| iter-4 | 59/80 = .738 | 18/25 = .720 | plateau 2/3 |
| iter-5 | 61/80 = .762 | 17/25 = .680 | plateau 3/3 → stop |
| final test | — | — | **18/28 = 0.643** |

Train accuracy climbed monotonically (.662 → .762) while eval never beat 0.720 →
classic over-fitting. Skill growth was lopsided: +1 skill across iters 1–3, then
**+47 in iters 4–5** (87 → 135 total), with no eval payoff.

For reference, the gpt-5.5 meta-opt (`iter02`) evolved 87 → 123 skills / 0 → 22
memory over 8 iters, eval best 0.800, final test 0.857.

### 5.3 Cost & wall-clock

Hermes did not populate `actual_cost_usd`, so dollars are estimated from token
counts in each profile's `state.db` at published list prices. gpt-5.5 ran on the
Stanford Azure gateway (estimated at gpt-5 list); Opus on the Anthropic API
(Opus 4.x list: $15/M in · $1.50/M cache-read · $18.75/M cache-write · $75/M out).

| run | wall-clock | est. cost | cost / correct (test) |
|---|---|---|---|
| parsed_md_test (gpt-5.5) | 9.5 min | ~$3.93 | $0.19 |
| opus48_parsed_md (opus) | 14 min | $39.27 | $2.18 |
| opus48_smoke_metaopt | 18.6 min | $37.65 | — |
| **opus48_full_metaopt** | **10.82 h** | **$1,230.53** | — |

The full Opus meta-opt: 1,010 sessions, 9,284 API calls, 292M cache-read +
28.7M cache-write + 3.4M output tokens.

---

## 6. Error analysis — is parsed-MD lossy vs PDF?

We audited the questions where parsed-MD/gpt-5.5 (run 2) regressed vs PDF/gpt-5.5
(run 1). **None were parsing losses** — every needed value was present in the
parsed Markdown:

| UID | category | detail |
|---|---|---|
| UID0111 | scoring artifact | `[-1832816,-2049753,216937]` correct, but missing spaces after commas → `reward.py` fuses `,-` and miscounts list arity. |
| UID0148 | scoring artifact | same whitespace artifact on `[28,2444.28]`. |
| UID0135 | table selection | agent read table CM-I-1 instead of CM-I-2; **both tables are in the parsed MD** with correct values. |
| UID0177 | column selection | agent computed the gold 236.7 as one of three candidates, then reported the "subject to statutory limit" column (236.4) instead of "total outstanding" (236.7). All columns present in the parse. |

Two of the four "regressions" are a `reward.py` whitespace edge case, not a model
or corpus error. Effective parsed-MD/gpt-5.5 ≈ 23/28 once those are normalized.

### Persistent hard questions
UID0018, UID0062, UID0150 are wrong in **all six** configurations. Opus
additionally never solves UID0005, UID0180, UID0237.

---

## 7. Findings

1. **Best setup unchanged:** gpt-5.5 + raw PDF + gpt-5.5-evolved scaffold = **0.857**.
2. **parsed-MD is cheap and fast** (~3× faster, ~⅕ the cost of PDF on gpt-5.5) and
   loses ~1 genuinely-hard question; most of the apparent gap is a scorer artifact.
3. **Scaffold is backend-specific.** Dropping Opus 4.8 onto the gpt-5.5-evolved
   profile *lowered* accuracy (0.750 → 0.643 on the same parsed-MD corpus). A fresh
   Opus baseline (0.679) beats Opus-on-gpt5-scaffold (0.643): the inherited skills
   are noise (or worse) for a different model.
4. **Opus meta-opt did not generalize.** 10.8 h / ~$1,230 of self-evolution over-fit
   train (→0.762) while eval plateaued at 0.720 and final test *fell* to 0.643. The
   late skill-creation burst (iters 4–5) coincided with zero eval gain — likely
   scaffold bloat / mutually-contradictory skills.
5. **Two reward.py bugs surfaced:** comma-separated list answers without spaces are
   mis-parsed (UID0111, UID0148). Worth a `re-normalize commas` fix before drawing
   fine-grained conclusions.

---

## 8. Reproducing

```bash
# 0. data: download the OfficeQA corpus (gated) into data/ per data/README.md,
#    and extract final_parsed_db_augmented.tar.gz into data/.

# 1. build splits for a corpus mode (deterministic, seed 42)
python baselines/hermes_iter/build_splits.py --corpus parsed-md+pdf

# 2a. one-off eval of a profile on the test split
python baselines/hermes_iter/run_hermes_split.py \
  --split baselines/hermes_iter/splits_parsed_md_plus_pdf/test.jsonl \
  --run-dir baselines/hermes_iter/runs/my_eval \
  --profile-cmd officeqa-iter-opus48 \
  --extra-args "-m claude-opus-4-8 --provider anthropic" \
  --concurrency 4

# 2b. full meta-optimization (fresh profile recommended)
python baselines/hermes_iter/iterate.py \
  --state-dir baselines/hermes_iter/runs/my_metaopt \
  --profile-cmd officeqa-iter-opus48 \
  --corpus parsed-md+pdf --reflect \
  --extra-args "-m claude-opus-4-8 --provider anthropic" \
  --max-iters 8 --patience 3 --hours 23
```

## 9. What's committed, and the answer-key caveat

Committed:
- **Code** + this report.
- **Aggregate results:** `summary.json`, `history.json`, `*.log`, `manifest.json`.
- **Per-question trajectories + results:** `runs/**/preds/<uid>.json` (final answer +
  rationale + score), `runs/**/logs/<uid>.log`, `runs/**/reflections/<uid>.json`
  (train-phase reflections), and `runs/**/per_row.jsonl` (uid, gold, predicted, score).
- **Evolved scaffold** (the meta-opt output): `evolved_profiles/<profile>/`
  (`MEMORY.md` + the authored Treasury skills).

Not committed (gitignored):
- The gated OfficeQA corpus under `data/` and `final_parsed_db_augmented.tar.gz`.
- Generated split prompts (`splits*/<split>.jsonl`) — they embed gold answers + local
  absolute paths; regenerate with `build_splits.py` (the `question`/`source_files`
  needed to interpret a trajectory are already inside each `preds/<uid>.json`).
- The redundant ~19 MB-per-iter `snapshot/` skill-library copies; result plots (`*.png`).
- Secrets (`.env`).

> ⚠️ **Answer-key caveat.** The committed trajectories (`preds`, `reflections`,
> `per_row.jsonl`) and some evolved SKILL.md worked-examples contain OfficeQA **gold
> answers / values**, which the dataset's gating explicitly asks not to be
> redistributed in a way that could inflate benchmark scores. This is acceptable for
> a **private** repo, but **review before making the repository public.** A scrub
> option: drop `gold`/`gold_answer` fields from `per_row.jsonl`/`preds/*.json` and the
> `reflections/` dir, which removes the answer key while keeping the model outputs.
