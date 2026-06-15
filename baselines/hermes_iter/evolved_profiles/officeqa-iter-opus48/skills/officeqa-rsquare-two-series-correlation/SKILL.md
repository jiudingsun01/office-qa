---
name: officeqa-rsquare-two-series-correlation
description: OfficeQA Treasury Bulletin — compute the "R-square value of the relationship between" two nominal series (e.g. on-budget receipts vs off-budget receipts) across a fiscal-year range. R-square of a bivariate relationship = Pearson correlation SQUARED; no regression fit / no slope/intercept needed. Covers where on-budget vs off-budget receipts/outlays live and the "use bulletins from Sept YYYY at 5-yr intervals" data-sourcing pattern. ALSO covers variants: plain Pearson r (not squared), partial correlation controlling for time, and the ABS DIFFERENCE between two per-year within-year monthly Pearson r's (e.g. Treasury vs New Aa corporate monthly yields, CY1979 vs CY1984 = [redacted]). PASSED on-budget vs off-budget receipts FY1991-2010 = 0.8298.
category: research
---

# OfficeQA: R-square of the relationship between TWO series

## Trigger phrasing (this family)
"Calculate the **R-square value of the relationship between** <series A> and
<series B> for fiscal years YYYY–ZZZZ. ... round to N nearest decimal places.
Use bulletins from September YYYY, ... in your reporting."

Key signals that select THIS recipe:
  - "R-square of the RELATIONSHIP BETWEEN two named series" (a bivariate pair),
    NOT "fit a regression and return slope/intercept", NOT a forecast.
  - Two data columns, one per fiscal year, over a year range.

PASSED: U.S. Treasury nominal **on-budget receipts** vs nominal **off-budget
receipts**, FY1991-2010 -> **[redacted]**. GOLD.

## THE RULE: R² = (Pearson r)², nothing more
For the relationship between exactly TWO variables, the coefficient of
determination R² equals the square of their Pearson correlation coefficient.
You do NOT need to run a least-squares fit, and it does not matter which series
you call x vs y — r² is symmetric.

```python
import numpy as np
a = [ ... ]   # series A, one value per fiscal year, chronological
b = [ ... ]   # series B, same fiscal years, same order
r = np.corrcoef(a, b)[0, 1]
print(round(r**2, 4))          # [redacted]
```
- Equivalent: `from scipy.stats import linregress; linregress(a,b).rvalue**2`.
- Keep FULL precision through corrcoef; round ONLY the final R² to the
  requested decimals (here 4 -> [redacted]).
- np.corrcoef is fine in execute_code; if scipy/np missing there, run via
  `cd /home/azureuser/office-qa && python3 script.py`.

## Data location: on-budget vs off-budget receipts/outlays
- "On-budget" vs "off-budget" receipts (and outlays) come from the federal
  budget-results / Monthly Treasury Statement summary in modern bulletins
  ("Summary of Receipts, Outlays, and the Deficit/Surplus"), which breaks the
  total into ON-BUDGET and OFF-BUDGET components. Off-budget is dominated by
  Social Security (OASDI) and the Postal Service.
- Use the ANNUAL fiscal-year totals, nominal $ (the question says "nominal" =
  do NOT inflation-adjust). Units (millions vs billions) cancel out in a
  correlation, so scaling does not affect R² — but keep A and B in the SAME
  units as each other within each year.

## The "use bulletins from September YYYY at 5-yr intervals" pattern
- A fiscal-year range like 1991-2010 is sourced from bulletins spaced ~5 years
  apart: Sept 1996 covers FY1991-1995, Sept 2001 covers FY1996-2000, Sept 2006
  covers FY2001-2005, Sept 2011 covers FY2006-2010. Each September bulletin's
  budget-results table carries the trailing ~5 fiscal years of annual data, so
  4 bulletins cover a 20-year window with no gaps.
- Cross-check overlap years where consecutive bulletins both report a year; use
  the later (revised) bulletin's figure if they differ.
- FY range 1991-2010 inclusive = 20 data points (2010-1991+1).

## Pitfalls
- Do NOT fit a regression to extract slope/intercept and report those — the
  question wants R², a single number. R² = r², full stop.
- Do NOT confuse "R-square of the relationship between A and B" (bivariate
  correlation²) with "R-square of a regression of Y on year" (goodness of fit
  of a trend). This family is the former: correlate the two SERIES directly.
- "nominal" = raw reported dollars; never deflate.
- Inclusive year count: 1991-2010 = 20 points, not 19.
- Round only at the very end to the requested decimals.

## Variant: correlation coef + PARTIAL correlation controlling for time
Q form: "coefficient of correlation between <A> and <B> over calendar years
Y1-Y2 inclusive AND the partial correlation controlling for time, round to
nearest thousandths. Return [corr, partial]."
- corr = Pearson r(A,B) (NOT squared here — this asks for r itself).
- partial r(A,B | time) = (r_AB - r_At*r_Bt)/sqrt((1-r_At^2)(1-r_Bt^2)),
  where t = calendar year. Keep full precision, round each to 3 dp.
- PASSED: Treasury bonds vs Moody's Aaa corporate annual yields, CY1942-1966
  inclusive (25 pts) -> [0.997, 0.977]. Data: "Average Yields of Treasury and
  Corporate Bonds by Periods" / "Annual series - calendar year averages".
  1942 row lives in the 1960-12 bulletin (PDF p.71, NOT in markdown parse —
  rasterize+vision); 1943-1966 in the 1967-12 bulletin annual table.

## Variant: abs diff of TWO per-year Pearson r's (monthly within-year)
Q form: "absolute difference between the sample Pearson correlation
coefficients of monthly yields for <series A> and <series B> during calendar
years Y1 and Y2. Treat monthly yields as percent values ... nominal ...
rounded to four decimal places."
- This is NOT one correlation. Compute r SEPARATELY for EACH calendar year on
  that year's 12 monthly observations, then take abs(r_Y1 - r_Y2).
- Within each year: r = corrcoef of the 12 monthly A-values vs the 12 monthly
  B-values for THAT year. Use all 12 months (Jan-Dec) of that calendar year.
- "sample Pearson" = ordinary Pearson r (np.corrcoef); the sample-vs-population
  distinction does not change r (it cancels in numerator/denominator).
```python
import numpy as np
A79=[...]; B79=[...]   # 12 monthly yields each, CY1979
A84=[...]; B84=[...]   # 12 monthly yields each, CY1984
r79=np.corrcoef(A79,B79)[0,1]; r84=np.corrcoef(A84,B84)[0,1]
print(round(abs(r79-r84),4))
```
- Data: "Average Yields of Long-Term Bonds" interest-rate table (same family as
  officeqa-bond-yield-spread-monthly). Columns: U.S. Treasury bonds, New Aa
  corporate bonds, etc., one row per calendar month. Read all 12 months/year.
- PASSED: Treasury bonds vs New Aa corporate, CY1979 vs CY1984 -> 0.0003.
- Pitfall: do NOT pool both years into one 24-point correlation; keep the two
  years separate and diff their r's. Round only the final abs diff to 4 dp.

## Distinct from neighbours
- vs officeqa-ols-slope-intercept-raw-year: that returns [slope, intercept] of
  Y-on-year. THIS returns a single R² of A-vs-B and needs no fit.
- vs my2-corporate-bond-yield-regression: that = |predicted - actual|. THIS = r².
- vs officeqa-surplus-deficit-cubic-forecast: that = cubic forecast. THIS = r².
