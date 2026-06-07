---
name: officeqa-treasury-yield-ols-forecast-maturity-bucket
description: OfficeQA Treasury Bulletin — fit an OLS linear regression to a MONTHLY series of "nominal average yields of taxable Treasury bonds due or callable in N years or after" (a maturity/callable bucket column) over a multi-year window, then FORECAST the next month's yield. This is the 1950s-era "Average Yields of Taxable Bonds by maturity" table, NOT the 1990s MY-2 market-yields table. PURE forecast (output the prediction itself), NO actual-value subtraction. PASSED Jul1953 through Jun1956 forecast Jul1956 equals 2.916.
category: research
---

# OfficeQA: Treasury yield OLS forecast on a maturity/callable bucket

## Trigger phrasing (this EXACT family)
"Using the nominal average yields from the **taxable treasury bonds that are
due or callable in N years or after**, construct an **OLS linear regression**
for the period <Month YYYY> through <Month YYYY> (**calendar months, not
federal fiscal year**) and **forecast** the equation to predict the yield for
<next Month YYYY>, rounded to N decimal places."

Bucket variants: "due or callable in 20 years or after", "...12 years or
after", "...5 to 10 years", etc. — pick the column whose maturity/callable
wording matches the question EXACTLY.

PASSED: Jul 1953 through Jun 1956, "due or callable in 20 years or after",
forecast Jul 1956 = **2.916** (3 dp). GOLD.

## CRITICAL: this is PURE forecast — output the prediction, do NOT subtract
Unlike the MY-2 corporate-bond regression (my2-corporate-bond-yield-regression),
which is |predicted − actual|, THIS question asks only for the **predicted
yield**. The answer IS the regression's forecast value. There is no "actual"
to look up and no subtraction. Do NOT import the MY-2 two-step here.

## Which table / where the data lives (1950s bulletins)
The series is the monthly "Average Yields of **Taxable** Treasury Bonds" table,
broken into MATURITY/CALLABLE buckets as columns:
  - "Due or callable within 5 years" (short)
  - "5 to 10 years"
  - "10 to 20 years" (or "12 years and over" in some years)
  - "Due or callable in 20 years or after" / "in N years or after" (long)
Rows are calendar months. The table sits in the interest-rate / "Yields of
Treasury Securities" / "Treasury Market Yields by Maturity" section.
A mid-1950s bulletin carries a multi-year monthly history, so ONE bulletin
(published shortly after the window's end) usually contains the entire
Jul1953-Jun1956 span. Read with `pdftotext -layout`; if columns collapse,
`pdftoppm -r 300` + vision the grid.

## Month-index / forecast-step convention (the off-by-one to watch)
- Window Jul 1953 through Jun 1956 INCLUSIVE = 36 calendar months.
- x = 1,2,...,36 in chronological order (Jul1953=1 ... Jun1956=36).
- Forecast Jul 1956 = the NEXT month = x = 37.
- General: months in window = (end_year-start_year)*12 + (end_month-start_month)
  + 1; the forecast month is x = that count + 1.
- "calendar months, not fiscal year" just means index by Jan-Dec calendar
  ordering; do NOT reindex to a Jul-start fiscal year. The window itself can
  start mid-year — that's fine, x just starts at 1 at the window's first month.

## Computation (verified recipe)
```python
import numpy as np
y = [...]                      # 36 monthly yields, chronological
x = np.arange(1, len(y)+1)     # 1..36
m, b = np.polyfit(x, y, 1)     # OLS slope, intercept
pred = m*(len(y)+1) + b        # x=37 -> Jul 1956
print(round(pred, 3))          # 2.916
```
numpy not importable in execute_code sandbox -> run via
`cd /home/azureuser/office-qa && python3 script.py`.

## Pitfalls
- Wrong column: "due or callable in 20 years or after" is not "within 5 years"
  nor "10 to 20 years". Adjacent buckets differ by 0.1-0.5 pp and fail to-the-dp.
- "TAXABLE" matters — older tables may also list "partially tax-exempt" /
  "tax-exempt" Treasury issues. Use the TAXABLE block.
- Do NOT subtract an actual value (that's the MY-2 question, a different table
  and decade). Output the bare prediction.
- Rounding: round ONLY the final prediction to the stated dp; keep full
  precision through polyfit.
- Don't reindex to fiscal-year months; index 1..N over the literal calendar
  window given.

## Distinct from neighbours
- vs my2-corporate-bond-yield-regression: that = 1990s/2000s MY-2 "New Aa
  corporate" market-yield table, two-step |pred-actual|, pinned actual 6.17.
  THIS = 1950s taxable-Treasury-by-maturity table, pure forecast.
- vs officeqa-bond-yield-spread-monthly: that = spread-then-mean, no regression.
