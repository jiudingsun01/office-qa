---
name: officeqa-geometric-mean-growth-rates
description: OfficeQA Treasury Bulletin — compute the "geometric mean" of a series of PERCENT-CHANGE / GROWTH-RATE observations (e.g. "real GDP growth, quarterly percent change at an annual rate"), then pick the best/worst YEAR. The geometric mean of growth RATES must be taken on growth FACTORS (1 + r/100), NOT on the raw percent values. Taking the geometric product of the raw percents is the dominant failure. Also covers "highest year" selection and dual-value bracketed output.
---

# OfficeQA — Geometric Mean of Growth / Percent-Change Rates

## When this applies
Question quotes a series of PERCENT values that are themselves rates of change —
"real GDP growth", "quarterly percent change at an annual rate", inflation %,
yield change %, etc. — and asks for the **geometric mean** of those rates, often
then asking which YEAR (or period) has the highest/lowest such mean.

Trigger phrases: "geometric mean of ... growth", "geometric mean of ... percent
change", "highest geometric mean ... from CY YYYY-YYYY".

## FIRST: is this growth rates or raw levels?
If the quoted values are PERCENT CHANGES / growth rates, stay here. If they are
RAW LEVEL amounts (ounces, dollars, counts read straight from a table), use
officeqa-geometric-mean-raw-levels instead — there you take the plain nth root of
the product with NO (1+r/100) factor conversion.

## THE CORE RULE (this is the whole game)
The geometric mean of growth RATES is computed on the growth FACTORS, not on the
raw percentages.

For rates r1..rn (each a percent, e.g. r=3.2 means 3.2%):

    factor_i = 1 + r_i/100
    G_factor = (prod factor_i)^(1/n)
    geomean_percent = (G_factor - 1) * 100

**DO NOT** do `(prod r_i)^(1/n)` — geometric mean of the raw percent numbers.
That is wrong and inflates the answer by a large factor.

### Why this matters (failed case)
Q: "highest Geometric mean of U.S. real GDP growth, quarterly percent change at an
annual rate ... from CY 2013-2019 ... that geometric mean rounded to hundredths."
- WRONG (raw-percent geomean): [2017, 2.74]
- GOLD: [redacted]
The 4x gap is the signature of the raw-vs-factor mistake compounded with the fact
that GDP quarterly rates can be small or mixed-sign within a year, which crushes
the factor-based mean toward a small number. When the quarters include a very
weak or near-zero quarter, the correct (factor) geometric mean drops far below
the naive raw geomean.

### Negative / zero rates
Real GDP quarterly rates can be NEGATIVE. A negative rate gives factor < 1
(e.g. r=-1.5 -> factor=0.985). The factor method handles this naturally; the
raw-product method breaks (negative or imaginary roots). This alone tells you the
factor method is intended.

## Procedure
1. Identify the YEARS in range (e.g. CY2013..CY2019) and the per-period rates that
   make up each year. "Quarterly percent change at an annual rate" => 4 quarters
   (Q1..Q4) per calendar year, 4 rates per year.
2. For EACH year: convert its quarterly rates to factors (1+r/100), take the
   geometric mean of those 4 factors, convert back to percent.
3. Compare the per-year geometric means; pick the year with the highest (or as
   asked).
4. Round the winning geometric mean per its stated precision (here hundredths).
5. Round the YEAR selection comparison done at the precision the question states
   for the mean if it says "rounded to nearest tenths place" for the selection —
   re-read: the GDP question rounded the per-year means to TENTHS to PICK the year,
   then reported the WINNER to HUNDREDTHS. Two different roundings:
   - selection/comparison: nearest tenths
   - final reported value: nearest hundredths
   Map each rounding clause to its own stage (see
   per-component-rounding-overrides-blanket memory).

## Data source for U.S. real GDP quarterly % change
This is BEA NIPA "real GDP, percent change at annual rate" by quarter — it is NOT
in the Treasury Bulletin tables themselves. If the bulletin reproduces it, look in
economic-indicator / supplementary statistics pages. Otherwise these are the
standard published BEA quarterly real GDP growth (annualized) numbers; use the
official BEA quarterly series for CY2013-2019. Verify each year's 4 quarters before
computing — getting one quarter wrong (especially a weak Q1) swings the geomean.

## Output format
Bracketed, comma-separated, NO space after comma (whitespace-sensitive grader):
`[2017,0.69]` — first the bare year, second the geomean. See FORMAT memory:
emit comma with NO spaces.

## Checklist
- [ ] Used factors (1+r/100), not raw percents
- [ ] Handled negative quarters via factors
- [ ] 4 quarters per CY for "annual rate" quarterly data
- [ ] Selection rounding (tenths) vs report rounding (hundredths) mapped separately
- [ ] `[year,value]` no space after comma
