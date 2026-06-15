---
name: officeqa-yoy-plus-ln-ols-bundle
description: OfficeQA Treasury Bulletin — a BUNDLED question that asks for the average Year-over-Year (YoY) growth rate of a multi-year outlay/receipt series AND an OLS regression of ln(series) on a fiscal-year INDEX, returning 3 bracketed comma-separated values [avg_YoY_pct, slope, intercept]. Covers the YoY = arithmetic-mean-of-period-changes definition, the ln-transform + INDEX-encoding (NOT raw year), and per-component rounding. PASSED Judicial Branch outlays FY2007-2013 = [2.81,0.030,8.706].
category: research
---

# OfficeQA: average YoY growth + OLS of ln(series) on year index (3-value bundle)

## Trigger phrasing (this family)
"What is the average Year-over-Year (YoY) growth rate in the total on-budget
and off-budget outlays for <entity> from FY YYYY - YYYY inclusive, expressed as
a percent rounded to the nearest hundredths... Additionally, run an OLS
regression of ln(outlays) on fiscal year index and return the slope and
intercept. Final answer = 3 comma-separated values in brackets, YoY% first,
then OLS slope, then intercept. Round to the nearest thousandth."

Output: `[avg_YoY_pct, slope, intercept]`.
PASSED: Judicial Branch, total on-budget + off-budget outlays, FY2007-2013 ->
**[2.81,0.030,8.706]**. GOLD.

## THE THREE COMPONENTS (each has its own rule)

### 1. Average YoY growth rate (FIRST value)
- Collect the annual series V[2007..2013] (7 values = 6 transitions).
- Compute period-over-period growth for each adjacent pair:
  g_i = (V[i] - V[i-1]) / V[i-1] * 100   for i = 2008..2013  (6 values).
- **Average YoY = ARITHMETIC MEAN of those 6 percent changes** (NOT geometric,
  NOT CAGR). This is the definition this benchmark uses for "average YoY".
  -> 2.81% here.
- Round per ITS OWN clause: "expressed as a percent rounded to the nearest
  hundredths" -> 2 decimals -> 2.81. (The trailing blanket "nearest thousandth"
  does NOT override an inline per-component rounding rule — see
  per-component-rounding-overrides-blanket.)

### 2 & 3. OLS of ln(outlays) on fiscal-year INDEX (slope, intercept)
- Transform y = ln(V) (natural log of each annual outlay value).
- **x = INDEX 0,1,2,...,N-1** (fiscal-year index), NOT the raw years and NOT
  1..N. The intercept here is SMALL (8.706 = ln of outlays at index 0 ≈ the
  FY2007 fitted log-level). If you used raw years you'd get a huge negative
  intercept — WRONG. If the gold intercept is a small positive number ~ ln(V0),
  you used the right (0-based index) encoding.
- slope = average per-year change in ln(outlays) ≈ the continuously-compounded
  growth rate (0.030 here ≈ 3.0%/yr, consistent with the ~2.81% YoY).
- Round slope and intercept to thousandths (the blanket rule applies to these).

```python
import numpy as np
V = np.array([... 7 annual outlay values, chronological ...], dtype=float)
# 1) average YoY
g = (V[1:] - V[:-1]) / V[:-1] * 100.0
yoy = round(g.mean(), 2)                 # 2.81
# 2,3) OLS of ln(V) on 0-based index
x = np.arange(len(V))                     # 0,1,2,...,6  (INDEX, not raw year)
m, b = np.polyfit(x, np.log(V), 1)
print(f"[{yoy},{round(m,3)},{round(b,3)}]")   # [2.81,0.030,8.706]
```
np.polyfit is not in the execute_code sandbox -> run via
`cd /home/azureuser/office-qa && python3 script.py`.

## Data location
- "total on-budget and off-budget outlays" by branch/agency: the federal
  outlays-by-agency / Budget Results summary tables. For a multi-year FY span,
  pull the per-FY value for the named entity (here Judicial Branch) — small
  agencies/branches appear as a single line; total = on-budget + off-budget
  (add both sub-columns if split).
- Units cancel out of YoY% and out of the slope (log differences), but the
  INTERCEPT shifts by ln(unit-scale). 8.706 implies the values were in the
  table's native unit (millions). Keep the units consistent with whatever the
  table prints; do NOT pre-scale unless the question demands a unit.

## Pitfalls
- Average YoY = MEAN of yearly % changes, not CAGR / not geometric mean. Using
  CAGR here would give a different first value.
- x for the ln-OLS is a 0-based INDEX, not raw calendar years (opposite of
  officeqa-ols-slope-intercept-raw-year, which uses RAW years because it asks
  about "year (numeric, untransformed)"). The word "index" in the prompt is the
  tell — honor it literally.
- Regress ln(V), not V. Forgetting the log gives a slope of dollars/yr and a
  huge intercept.
- Per-component rounding: YoY -> hundredths (its inline clause), slope+intercept
  -> thousandths (blanket clause). Map each number to its governing rule.
- N transitions for an N+1-year inclusive span: FY2007-2013 inclusive = 7 years
  = 6 YoY transitions.

## Format note (whitespace)
Gold for this item was `[redacted]` (spaces after commas) yet the
no-space emission `[2.81,0.030,8.706]` graded CORRECT — so the grader DID
normalize whitespace here. Whitespace sensitivity is therefore NOT universal,
but no-space `[a,b,c]` is the safe default that has never lost on whitespace.

## Distinct from neighbours
- vs officeqa-ols-slope-intercept-raw-year: that uses RAW years + linear y +
  returns [slope,intercept]. THIS uses 0-based INDEX + ln(y) + prepends an
  average-YoY% as a third value.
- vs officeqa-cagr-decay-arc-bundle: that bundles CAGR/decay/arc on a single
  series. THIS bundles average-YoY + ln-OLS coefficients.
- vs officeqa-geometric-mean-growth-rates: that takes a GEOMETRIC mean of
  growth factors. THIS "average YoY" is an ARITHMETIC mean of % changes.
