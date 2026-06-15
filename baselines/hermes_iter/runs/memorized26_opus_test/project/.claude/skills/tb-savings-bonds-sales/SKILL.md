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
- Questions may say **"interest-bearing debt for Series I savings bonds"** at
  a given month. The exact source is **Table SBN-3** ("Sales and Redemptions
  by Period, Series E, EE, H, HH and I"), the **Series I panel**, column
  **"Interest-bearing debt"** (the column ~8th across). That column is a
  running month-END OUTSTANDING LEVEL, not a flow. One issue per distant month
  (a month-end value appears in an issue ~3-6 months later).
- **ROW-SELECTION PITFALL (this cost a wrong answer).** Each per-series panel
  in SBN-3 interleaves three kinds of rows in one column: **fiscal-year** rows
  (labeled e.g. "1999-00", "2003"), **calendar-year** rows (labeled "2000",
  "2005"), and **monthly** rows (labeled "2001 - Jan", "Feb", "Mar", ...).
  For "calendar March 2001" you MUST use the monthly row **"2001 - Mar"**, NOT
  a fiscal-year or annual row. Because the column is a running level, the wrong
  row holds a plausible-looking number that silently corrupts the result.
  Concretely: Series I interest-bearing debt = **3554** at Mar 2001 (monthly
  row) — but the fiscal-year "1999-00" row reads **2152** (= the Sept-2000
  level). Using 2152 by mistake gave 560682.94 instead of the correct
  [redacted] when projected to Mar 2011.
- **Cross-check via monotonicity:** since this column is a running outstanding
  level for a series still being sold, consecutive monthly values should rise
  smoothly. Confirm your March cell sits between the Feb and Apr cells of the
  same panel before using it (e.g. Mar 2001 = 3554 lies between Feb 3244 and
  Apr's value; Mar 2006 = 34736 lies between Feb 33997 and Apr 35291).
- If the question then projects forward at a constant compound rate, see
  tb-math-transform-wrappers ("Constant compound-rate projection"). Note the
  algebra: projecting an N-year window forward by exactly N more years gives
  end²/start regardless of how you annualize (geometric or continuous), so the
  ONLY thing that can be wrong is the two retrieved values. Verified: Mar [redacted]
  (3554) & Mar 2006 (34736) projected to Mar 2011 = 34736²/3554 = 339501.88.

## Share-of-total in percentage points (absolute)
- "Change in the share of total redemptions accounted for by series X" =
  100 × X_redemptions/total_redemptions computed for EACH year from the same
  table (series panel and all-series panel of the same issue), then a plain
  subtraction of the two shares. This is the ABSOLUTE pp change — unlike the
  "relative difference in percentage points" wording below, which divides by
  the base rate. Keep full precision until the final rounding.
- **Sanity-check the two retrieved cells before dividing.** Small OCR misreads
  in the monthly SBN redemption cells propagate into BOTH outputs (the pp share
  AND the absolute change), so one wrong digit fails the whole answer.
  Cross-check by confirming the all-series-combined "Redemptions" total for the
  month roughly equals the sum of the per-series redemption columns (E/EE, H/HH,
  Series I, savings notes). If they disagree, you misread a cell or grabbed a
  fiscal-year-to-date row instead of the single-month row — re-read before
  computing. For Series I specifically (introduced late 1998), its share of
  monthly redemptions in the early 2000s is still modest; an implausibly large
  share (well above ~10% by 2005) signals a misread of either the Series I cell
  or the all-series total.
- **VALUATION-BASIS CONSISTENCY (this cost a wrong answer; both outputs came out
  slightly HIGH — 7.7/90 instead of 7.1/82 for Mar 2000→Mar 2005 Series I).**
  Redemptions in these tables exist on two bases: **"Redemptions at issue
  price"** and **current "Redemptions" (current redemption value = issue price +
  accrued discount)**. The numerator (Series I) and the denominator (all-series
  total) MUST be read on the SAME basis, AND the all-series total you divide by
  must be the genuine grand total for that basis — not a subtotal that omits one
  series. A mismatch (e.g. Series I at current redemption value over an
  all-series total at issue price, or over a total missing a column) biases the
  share UP by a fraction of a point and the absolute change by several million,
  which reads as a "plausible but slightly off" wrong answer. When the question
  just says "total redemptions (all series)", use the plain **Redemptions**
  (current redemption value) column for BOTH numerator and denominator, and
  verify the denominator equals the sum of all per-series Redemptions cells on
  that same basis before computing.

## Decoding obfuscated column names (accrued discount)
- Questions often paraphrase a column instead of naming it. **"Redemptions that
  elapsed value buildup from the original price markdown"** (or similar wording
  about value accrued/built up from the discount/markdown) = the **accrued
  discount** portion of redemptions. Savings bonds are sold at a discount
  ("markdown" from maturity value); the interest that accrues over time is the
  "value buildup".
- For "what percent of total redemptions came from [accrued discount]" in a
  month: in the **All series combined** monthly panel, redemptions are reported
  as **Redemptions at issue price** plus **Accrued discount**, and their sum is
  total **Redemptions (current redemption value)**. Answer =
  Accrued discount / (Redemptions at issue price + Accrued discount) × 100.
  Verified: October [redacted] all series combined → [redacted].
- Same decode applies to sales: "Sales plus accrued discount" already bundles
  the buildup; the plain "Accrued discount" column is the buildup alone.

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
  Verified: [redacted] vs [redacted] rates differing [redacted] pp absolute → accepted answer
  [redacted] (relative).

## Arithmetic recipe (multi-year mean)
1. Read the Sales value for each requested calendar year from the All series
   combined panel of a single issue.
2. Mean = sum of the annual values / number of years; round only the final
   result to the requested precision (do not round intermediate values).
