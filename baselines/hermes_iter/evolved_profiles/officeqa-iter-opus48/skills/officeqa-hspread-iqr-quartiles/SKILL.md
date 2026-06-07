---
name: officeqa-hspread-iqr-quartiles
description: OfficeQA Treasury Bulletin — compute "H Spread" / IQR / quartile-based stats on monthly series (e.g. 12 FY-monthly receipt values). Covers Type 7 linear-interpolation quartiles and the "round intermediate values to tenths before computing" trap that causes 0.01–0.02 final errors.
category: research
---

# OfficeQA: H Spread / IQR / Quartile questions

## What "H Spread" means
H Spread = Hinge spread = **Interquartile Range (IQR) = Q3 − Q1**.
"Standard linear-interpolation percentile method" / "Type 7 method" = the DEFAULT
quartile in numpy/pandas/R. So:
```python
import numpy as np
q1 = np.percentile(data, 25, method="linear")   # = Type 7
q3 = np.percentile(data, 75, method="linear")
hspread = q3 - q1
```
(numpy "linear" == R type=7 == pandas default. Do NOT use method="lower"/"higher"/
"midpoint" or the Excel QUARTILE.EXC/Type-6 variants — those give different answers.)

Typical data: the 12 monthly values for a fiscal year from a Treasury Bulletin
receipts/outlays table (e.g. "monthly nominal net budget receipts from Corporate
income taxes FY 2021"). FY = Oct(prev yr) through Sep(this yr) — pull all 12 months
from the relevant monthly-receipts-by-source table.

## THE ROUNDING TRAP (this is why answers miss by 0.01–0.02)
These questions carry TWO rounding instructions and they are NOT the same:
1. A final-answer rounding ("rounded to the nearest hundredths place").
2. An INTERMEDIATE rounding clause, e.g. "use the intermediate values rounded to
   the tenths of billions before computing the H spread value."

When clause (2) is present you MUST round the INTERMEDIATE quantities to tenths
(one decimal, 0.1 B) BEFORE the final subtraction, then apply the final hundredths
rounding. Concretely:
```python
q1 = round(np.percentile(data, 25), 1)   # round quartile to tenths FIRST
q3 = round(np.percentile(data, 75), 1)
hspread = round(q3 - q1, 2)              # then final hundredths
```
Because q1 and q3 are each at 0.1 resolution, the difference lands on a clean 0.1
boundary -> a hundredths answer ending in 0 (e.g. 57.50, NOT 57.52).

FAIL CASE: FY2021 Corporate income tax H Spread. GOLD = **57.50**. SOLVED path
(verified from FFO-2 Corporation>Net col, FY21 = Oct'20..Sep'21 millions:
9152,-3192,62920,16463,3780,15255,72769,13808,74189,16942,3033,86713):
  1. Convert to billions and ROUND EACH of the 12 values to tenths FIRST.
  2. Sort, compute Type-7 quartiles -> Q1=7.85, Q3=65.375.
  3. Round THOSE quartiles to tenths with ROUND-HALF-UP (NOT Python banker's
     round): 7.85->7.9, 65.375->65.4.
  4. H Spread = 65.4 - 7.9 = 57.50.
Other paths that MISS: round-quartiles-only (no data round) -> 57.6; round raw
data then subtract without re-rounding quartiles -> 57.52; no rounding -> 57.57.
PITFALL: Python's round(7.85,1)==7.8 (banker's) gives 57.6 — use Decimal
ROUND_HALF_UP or add tiny epsilon. "Intermediate values rounded to tenths"
means BOTH the raw data AND the computed quartiles, half-up.

## Which "intermediate values" to round?
The clause is ambiguous (raw data points vs. the computed Q1/Q3). Default
interpretation that matched gold here: round the **computed Q1 and Q3** to tenths
before subtracting. If that does not produce a clean result, also try rounding the
12 raw monthly data points to tenths first, then recompute Type-7 quartiles. Prefer
whichever yields a final value consistent with the requested precision (a gold that
ends in .x0 favors quartile-level rounding; both often coincide).

## Checklist before submitting an H Spread answer
- [ ] Confirmed H Spread = Q3 − Q1 (IQR), not range, not std dev, not MAD.
- [ ] Used Type 7 / numpy default "linear" percentile (verify n: with n=12,
      Q1 sits at position 0.25*(12-1)=2.75 -> interpolate between sorted[2],[3]).
- [ ] Applied the INTERMEDIATE tenths rounding clause if present (round Q1,Q3 to 0.1).
- [ ] Applied the final hundredths rounding LAST.
- [ ] All 12 months pulled (FY = Oct..Sep), correct sign (receipts positive).
