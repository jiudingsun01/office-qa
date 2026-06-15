---
name: tb-maturity-schedule
description: Use for Treasury Bulletin questions about the "Maturity Schedule of Interest-Bearing Public Marketable Securities" — fixed-maturity vs callable amounts, amounts maturing/callable in given years, or any series built from schedules "published on the last day of <month>" (often feeding an OLS/trend projection).
---

# Maturity Schedule of Interest-Bearing Public Marketable Securities

## Locating the table
1. Title: **"Table 1.- Maturity Schedule of Interest-Bearing Public Marketable Securities Issued by the United States Government and Outstanding <Month> 31, YYYY"**, in the **Debt Operations** section. Units: **millions of dollars** (convert to billions when asked).
2. Bulletins lag ~2 months: the schedule "Outstanding January 31, YYYY" is printed in the **March YYYY** bulletin. "Published on the last day of January" = the schedule whose as-of date is Jan 31, i.e. the March issue's table — NOT the January or February bulletin.
3. Layout: rows grouped by **calendar year of maturity** (1948, 1949, …), each year ending in a `Total` row; two print columns per page, so OCR interleaves years — match each Total to its year header carefully.

## Column semantics
- Columns: **Fixed maturity issues** | **Callable issues, classified by year of: First call / Final maturity** | bank-restriction date.
- Bills, certificates, and notes appear in the fixed column; most bonds of this era are callable and appear only in the callable columns (classified under the year of first call AND final maturity — don't double count).
- Footnote rule: **callable issues for which definite notice of call has been given are reclassified as fixed maturity** (under the call year). So a year's fixed total can include called bonds.

## CRITICAL: which total is "the value of fixed maturity securities" (gold convention)
The benchmark gold for "values of … securities that are of fixed maturity type as of the <date> schedule" is the **first year-section's `Total` row, fixed-maturity column** — i.e. fixed-maturity amounts maturing **within the schedule's own calendar year** — NOT the grand total of the fixed column across all years.
- Verified series (fixed, within-year totals, $ millions): Jan 31 [redacted] = **[redacted]**; Jan 31 [redacted] = **[redacted]**; Jan 31 [redacted] ≈ **[redacted]k**; Jan 31 [redacted] = **[redacted]**. (OLS over these in billions projects Jan [redacted] ≈ [redacted].)
- Summing the fixed column across ALL years gives ~55–57 B for these dates — that reading reconciles with total marketable debt but is WRONG for the benchmark. If your extracted series trends opposite to within-year totals, recompute with the first-section totals before answering.
- This within-year reading generalizes: "total amount scheduled to mature in calendar year Y as reported in the schedule outstanding at end of <month> Y" = that schedule's **first year-section Total row** (the schedule's own calendar year). Verified on [redacted]s-era schedules (end-of-February schedules for [redacted]–[redacted] i.e. the April-issue tables, feeding a z-score that graded correct). One schedule per year suffices — don't stitch later years' rows from a single schedule.

## OLS extrapolation shortcut (4 equally spaced points → next point)
For y1..y4 at consecutive years, the OLS prediction for year 5 is exactly
  ŷ5 = −0.5·y1 + 0·y2 + 0.5·y3 + y4
(y2 has zero weight). Use it to sanity-check a hand-fit regression; for n points generally ŷ(next) = ȳ + slope·(x_next − x̄).

## Retrieval tactic when FRASER 403s
FRASER (fraser.stlouisfed.org) often returns 403 to curl/WebFetch. Mirror: archive.org items **`sim_treasury-bulletin_YYYY-MM`** with plain OCR at
  `https://archive.org/download/sim_treasury-bulletin_YYYY-MM/sim_treasury-bulletin_YYYY-MM_djvu.txt`
(curl works directly). Find issues via archive.org advancedsearch on `title:(treasury bulletin)` plus a date range. OCR of two-column 1940s-50s tables garbles digits (e.g. 44,5xx unreadable, "¥6,625" = 46,625) — cross-check any load-bearing cell against an adjacent year's bulletin, which reprints overlapping rows.
