# ESF asset-share with CPI-U real-dollar adjustment

## Question shape
"Using the US Treasury **Exchange Stabilization Fund (ESF)** balances reported
as of the last day of <month> for calendar years YYYY-YYYY ..., what is the
[absolute difference in the] **average share of the Fund's total assets** that
came from its <foreign-exchange / securities / SDR / etc> holdings between
these period sets, when considering each nominal value in thousands of dollars
**adjusted to <Month Year> dollars using the BLS CPI-U, not seasonally
adjusted**? Report in percentage points rounded to nearest thousandth."

## Where the numbers live
- The ESF balance sheet is in the Treasury Bulletin section titled
  **"Exchange Stabilization Fund"** (a 2-3 column statement: Assets,
  Liabilities, Capital). Look in the "International Statistics" /
  "Capital Movements" / "Exchange Stabilization Fund" area of the bulletin.
- Balances are reported as of a **period-end date** (e.g. "June 30, 2000",
  "September 30, 2000"). Q asks for last-day-of-June AND last-day-of-Sep for
  several years -> you need MULTIPLE bulletin issues (the quarterly issues that
  report those quarter-ends). One bulletin issue typically shows two columns:
  current quarter-end and prior period-end.
- Asset line items typically include: **U.S. dollar assets** (cash/securities),
  **Special Drawing Rights (SDRs)**, **Foreign exchange and securities**
  (sometimes split), and **Total assets**. Values are in **thousands of
  dollars** unless the column header says otherwise.

## KEY INSIGHT: CPI adjustment is IRRELEVANT to a SHARE — but DO it anyway if asked
A share = (FX holdings) / (Total assets). If EVERY line item in one period-end
column is deflated by the SAME CPI factor (same period -> same CPI), the factor
**cancels** in the ratio. So the share for a given date is identical whether or
not you CPI-adjust.

HOWEVER: the deflation factor differs ACROSS period-ends (June 2000 CPI != Sep
2000 CPI != June 2001 CPI ...). The question asks for the **AVERAGE share**
over a set of dates, then a difference of two averages. Because each date's
share is a pure ratio that is CPI-invariant, **the CPI adjustment does NOT
change the answer at all** for a simple per-date share-then-average.

  => If the metric is "average of (FX/Total) across dates", you can SKIP the CPI
     math entirely and still get the gold answer. The CPI clause is a red
     herring / distractor in that case.

  => BUT if the metric instead pools dollars first (e.g. "share of the SUMMED
     real FX across all dates over the SUMMED real total assets"), then the CPI
     factors do NOT cancel and you MUST deflate each date's dollars to the
     target month before summing. Read the clause: "average **share**" (ratio
     per date, then mean) vs "share of the **total/summed**" (sum reals first).
     This question was the per-date-average form -> CPI-invariant -> 0.953.

## Procedure (per-date-average form, the common one)
1. For each required period-end date, pull from that date's ESF balance sheet:
   - numerator line(s): "Foreign exchange and securities" (sum the relevant
     asset lines the question names),
   - denominator: "Total assets".
2. share_date = 100 * numerator / denominator  (percent; keep full float).
3. avg_set1 = mean(shares for the June dates);
   avg_set2 = mean(shares for the September dates).
4. answer = round(abs(avg_set1 - avg_set2), 3) in PERCENTAGE POINTS.
   (Use ROUND_HALF_UP.)

## If the metric is the pooled/summed-real form
1. Get BLS CPI-U (NSA) monthly index for each period-end month AND for the
   target month (e.g. March 2003). CPI-U NSA is EXTERNAL to the bulletin —
   use BLS series CUUR0000SA0 values. Deflate: real = nominal * (CPI_target /
   CPI_date).
2. Sum real numerators, sum real denominators, take ratio, *100, then average /
   difference as the wording dictates.

## Pitfalls
- Confirm the asset column you pick is "Total assets", NOT "Total assets and
  liabilities" or a capital subtotal.
- thousands-of-dollars units cancel in a share; don't rescale.
- "last day of June" = the June 30 (or fiscal quarter-end) column, not the
  June issue's prior-period column.
- Don't average the two sets together; keep June-set and Sep-set separate, then
  abs-difference.
