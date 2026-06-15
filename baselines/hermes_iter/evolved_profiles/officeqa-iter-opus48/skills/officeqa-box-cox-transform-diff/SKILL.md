---
name: officeqa-box-cox-transform-diff
description: OfficeQA Treasury Bulletin — questions that apply a Box-Cox (or other power/log) transform to two fiscal-year dollar values and take their difference. Covers the exact Box-Cox formula for a stated lambda, the lambda=0 special case, the unit convention (transform values that are already in BILLIONS), and where federal "net interest outlays" / receipt-outlay summary figures live. PASSED net interest outlays FY1981 vs FY1980 (Nov 1981 bulletin), lambda=0.75 = 6.1596.
---

# OfficeQA — Box-Cox transformed difference of two fiscal-year values

## When this applies
The question says something like: "difference between Box-Cox transformed values of
[category] in fiscal year A ... and the same category value for the comparable B
fiscal period reported by the US Treasury in [month year] ... Assume Box-Cox lambda
value of L." Sometimes phrased as "power transform", "Yeo-Johnson", or plain "log
transform". The structure is always: pull two raw dollar values, transform each,
subtract.

## The Box-Cox formula (memorize)
For a value x and lambda L:
  - if L != 0:   T(x) = (x^L - 1) / L
  - if L == 0:   T(x) = ln(x)
Answer = T(x_A) - T(x_B), rounded to the stated decimals.

Worked example that PASSED:
  net interest outlays FY1981 = 68.734 (billion), FY1980 = 52.512 (billion), L=0.75
  T(68.734) = (68.734^0.75 - 1)/0.75 = (23.852... - 1)/0.75 = 30.4699...
  T(52.512) = (52.512^0.75 - 1)/0.75 = (19.480... - 1)/0.75 = 24.3105...
  diff = [redacted]  (GOLD = [redacted])
(Exact raw figures may differ slightly by bulletin edition; the method is the point.)

## CRITICAL unit convention
The question states the values are "expressed in billions of nominal dollars" and asks
for the answer "in billions". So TRANSFORM THE BILLIONS-SCALED NUMBERS, not the raw
millions cell. Treasury Bulletin "Federal Fiscal Operations" / receipt-outlay summary
tables report outlays in MILLIONS — convert millions -> billions (divide by 1000)
BEFORE applying the transform. Box-Cox is nonlinear, so feeding millions vs billions
gives wildly different answers. Get the scale right first.

## Where the data lives
"Net interest" is a function/superfunction line in the federal OUTLAYS-by-function
summary (the "Summary of Federal Fiscal Operations" / "Budget Results" style table in
the Federal Fiscal Operations section, early pages of the bulletin). A bulletin dated
"November 1981" reports the just-closed fiscal year (FY1981, ended Sep 30 1981) and
shows the prior year (FY1980) as the comparison column — "comparable 1980 fiscal
period" = that side-by-side prior-FY column in the SAME table. You do NOT need a
separate 1980 bulletin; both values sit in one table.

## Pitfalls
- lambda=0 is log, NOT (x^0-1)/0 (undefined). Branch on it.
- Use the value as reported for the FY column, not a monthly/quarterly figure.
- Round only the FINAL difference to the stated decimals; keep full precision in T(x).
- If a "revised" (r) figure is shown for the prior FY, use the revised value.
- Don't subtract raw then transform — transform EACH value, THEN subtract.
