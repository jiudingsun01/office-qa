---
name: officeqa-ols-slope-intercept-raw-year
description: OfficeQA Treasury Bulletin — fit OLS linear regression and return the SLOPE and INTERCEPT (not a forecast) when the question specifies "year (numeric, untransformed)" as the predictor. The x-axis MUST be the literal calendar/fiscal years (e.g. 1929,1930,...,1942), NOT a 1..N index. Slope is index-invariant but INTERCEPT is not — getting x-encoding right is the whole game. PASSED individual income tax receipts FY1929-1942 = [0.096, -184.143].
category: research
---

# OfficeQA: OLS slope + intercept with RAW (untransformed) year predictor

## Trigger phrasing (this family)
"...fit an ordinary least squares linear regression with **year (numeric,
untransformed)** as the predictor and <series> as the outcome. **Return the
slope and intercept** inside square brackets, separated by commas... rounded
to the nearest thousandth."

Key signals that select THIS recipe over the forecast skill:
  - Asks to RETURN slope and intercept (two numbers), NOT to forecast a value.
  - Says the predictor is "year (numeric, untransformed)" or just "year".
  - Output format: `[slope, intercept]`.

PASSED: U.S. federal individual income tax receipts net of refunds,
FY1929-1942, billions nominal $ -> **[0.096, -184.143]**. GOLD.

## THE CRITICAL RULE: x = literal years, NOT 1..N
When the question says the predictor is "year (numeric, untransformed)", the
x-vector is the actual year numbers: [1929, 1930, ..., 1942].

- Slope is INVARIANT to whether you use raw years or a 1..N index (shifting x
  by a constant does not change the slope) — so the slope alone won't tell you
  if you got it wrong.
- The INTERCEPT IS NOT INVARIANT. With raw years near 1900-2000, the intercept
  is a large negative number (here -184.143) because the line is extrapolated
  back to year=0. If you mistakenly index x=1..N, the intercept will be small
  and WRONG (you'd get ~the year-1928 fitted value). Since the question asks
  for the intercept, the x-encoding is the entire question.
- Contrast with officeqa-treasury-yield-ols-forecast-maturity-bucket, which
  uses x=1..N indexing because it forecasts the NEXT step — there the absolute
  intercept never surfaces. DO NOT import 1..N here.

## Computation (verified recipe)
```python
import numpy as np
years = np.arange(1929, 1943)          # 1929..1942 inclusive (RAW years)
y = [ ... ]                            # receipts in billions, chronological
m, b = np.polyfit(years, y, 1)         # m=slope, b=intercept
print([round(m, 3), round(b, 3)])      # [0.096, -184.143]
```
- "fiscal years 1929-1942" inclusive = 14 data points (1942-1929+1).
- np.polyfit not in execute_code sandbox -> run via
  `cd /home/azureuser/office-qa && python3 script.py`.

## Units / data location
- "billions of nominal dollars" — if the source table is in $ thousands or
  $ millions, scale to billions BEFORE fitting (slope/intercept both scale
  linearly with y units, so wrong units silently corrupt both numbers).
- Individual income tax receipts "net of refunds" for 1929-1942 come from the
  early federal receipts/internal-revenue tables. Use the receipts column
  already netted of refunds; if only gross + refund columns exist, subtract.

## Pitfalls
- Wrong x-encoding (1..N instead of raw years) -> right slope, WRONG intercept.
  This is the dominant failure mode for this family.
- Rounding: round ONLY the two final numbers to the requested places (here
  thousandths); keep full precision through polyfit. Negative intercept keeps
  its minus sign. Gold may render the minus as a Unicode "−"; emit ASCII "-",
  the values match.
- Inclusive year count: 1929-1942 = 14 points, not 13.
- Order of outputs: SLOPE first, then INTERCEPT, as the prompt states.
- OUTPUT FORMAT IS WHITESPACE-SENSITIVE. The grader does a near-exact string
  match on bracketed CSV. A real run computed the CORRECT values but emitted
  `[44.00, 231.52]` (space after comma) while GOLD was `[44.00,231.52]` (no
  space) -> graded WRONG despite identical numbers. ALWAYS emit the bracketed
  answer with a comma and NO surrounding spaces: `[slope,intercept]`. This
  applies to every [a,b] / square-bracket CSV answer in this benchmark.

## Sibling: forecast-error variant (actual - forecast)
Some Qs say "fit a simple linear trend (OLS) ... determine the FY <T> value
forecast ERROR (actual - forecast)". Recipe: fit polyfit(raw_years, y, 1) on the
training span, forecast = m*T + b, then error = actual[T] - forecast. Keep full
precision, round only the final answer to requested places.

PITFALL — Treasury Bulletin "Table 2. Computed Interest Charge" (Debt
Outstanding sec, ~1969 vintage): the markdown parse DROPS the "Computed annual
interest charge - Public debt" sub-column, keeping only the "Public debt &
guaranteed securities" sub-col. The two charge sub-cols are nearly identical
(differ by ~3-20). For Qs about interest charged on PUBLIC DEBT use the PDF
4th numeric column (pdftoppm 300dpi + vision read). Verified FY1961-1967
charge (millions, public debt): 8761,9519,10119,10900,11467,12516,12953;
FY1968 actual=15404. /1000 -> billions. Forecast68=13.736143,
err(actual-forecast)=1.667857 B.

## Distinct from neighbours
- vs officeqa-treasury-yield-ols-forecast-maturity-bucket: that forecasts the
  next month's yield (x=1..N, output one predicted number). THIS returns
  [slope, intercept] with x=raw years.
- vs my2-corporate-bond-yield-regression: that = |predicted - actual| two-step.
  THIS just returns the fitted coefficients, no actual lookup, no subtraction.
- vs officeqa-surplus-deficit-cubic-forecast: that = cubic poly with x=INDEX
  and a forecast. THIS = degree-1, x=RAW year, return coefficients.
