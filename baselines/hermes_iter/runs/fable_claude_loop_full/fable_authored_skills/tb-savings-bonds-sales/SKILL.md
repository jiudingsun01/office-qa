---
name: tb-savings-bonds-sales
description: Use for Treasury Bulletin questions about U.S. savings bonds OR savings notes sales, redemptions, redemption rates, or amounts outstanding — by series (E, F, G, etc.) or "all series combined" — for calendar years, fiscal years, or months.
---

# U.S. Savings Bonds — Sales and Redemptions tables

## Where the data lives
- Treasury Bulletin section **"United States Savings Bonds"**. The lead table is
  **"Sales and redemptions by series"**, split into panels: **"All series combined"**
  first, then per-series panels (Series E, Series F and G, etc.).
- When the question says "all series combined (U.S. Treasury)", use the
  **All series combined** panel — do NOT sum the per-series panels yourself.

## Choosing the right issue
- The table's annual rows only extend through completed years, so to cover
  calendar year Y you need a Bulletin issue from **year Y+1 or later** (e.g. a
  1954 or 1955 issue covers calendar 1949–1953 in one table).
- Prefer one issue whose annual rows span all requested years; this avoids
  cross-issue revisions.

## Row and column pitfalls
- Rows mix **calendar years, fiscal years, and months**. Match the question's
  period type exactly — "calendar years" means the calendar-year rows, not
  fiscal-year rows (which differ substantially).
- Columns include **Sales**, **Accrued discount**, **Sales plus accrued
  discount**, **Redemptions**, and **Amount outstanding**. "Total sales" means
  the plain **Sales** column, NOT "Sales plus accrued discount".
- Units are **millions of dollars** at issue price (nominal). No rescaling
  needed when the question asks for millions.

## Modern issues (1990s–2000s): SBN tables and Series I
- Later bulletins label the savings-bond tables with an **SBN- prefix**
  (e.g. SBN-1/SBN-2/SBN-3) in the "U.S. Savings Bonds and Notes" section;
  layout is the same idea — an all-series panel plus per-series panels/columns
  (Series E/EE, H/HH, and **Series I** from late 1998 onward).
- **Monthly values for two distant years need two different issues**: each
  issue's monthly rows cover only roughly the preceding year. For "March 2000
  vs March 2005", pull March 2000 from a mid/late-2000 issue and March 2005
  from a mid/late-2005 issue. Pick the same month-row label in both.
- Questions may say **"interest-bearing debt for Series I savings bonds"** —
  this is still a per-series month-end amount-outstanding lookup (savings
  bonds are nonmarketable interest-bearing public debt), resolved the same
  way: one issue per distant month. If the question then projects forward at
  a constant compound rate, see tb-math-transform-wrappers ("Constant
  compound-rate projection"). Verified: Mar 2001 & Mar 2006 Series I values
  projected to Mar 2011 = 339501.88 (millions).

## Share-of-total in percentage points (absolute)
- "Change in the share of total redemptions accounted for by series X" =
  100 × X_redemptions/total_redemptions computed for EACH year from the same
  table (series panel and all-series panel of the same issue), then a plain
  subtraction of the two shares. This is the ABSOLUTE pp change — unlike the
  "relative difference in percentage points" wording below, which divides by
  the base rate. Keep full precision until the final rounding.

## Savings NOTES (not bonds)
- U.S. **savings notes** have their own panel/table ("Sales and redemptions of
  United States savings notes", adjacent to the savings-bonds tables, same
  column layout). Do not pull savings-bond rows for a savings-note question.
- "Redemption rate out of the average amount outstanding" for a year =
  Redemptions(year) / average Amount outstanding × 100. Compute the rate per
  year, keep full precision.
- If the question then asks for the **"relative difference in percentage
  points"** between two years' rates, that is the RELATIVE change
  (Δrate / base rate × 100), not the absolute pp subtraction — see
  tb-math-transform-wrappers ("Relative difference in percentage points").
  Verified: 1980 vs 1981 rates differing 3.85 pp absolute → accepted answer
  17.69 (relative).

## Arithmetic recipe (multi-year mean)
1. Read the Sales value for each requested calendar year from the All series
   combined panel of a single issue.
2. Mean = sum of the annual values / number of years; round only the final
   result to the requested precision (do not round intermediate values).
