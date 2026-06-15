# R-square / correlation BETWEEN TWO contemporaneous series (multi-bulletin)

## Trigger
"Calculate the R-square (or correlation/r) value of the relationship between
[series A] and [series B] for fiscal years YYYY-YYYY. ... Use bulletins from
September 1996, 2001, 2006, and 2011 in your reporting." Round to 4 decimals.

This is NOT a projection/forecast (no target year, no external comparison
constant). It is a pure statistic computed from two columns of the SAME table,
one (x,y) pair per fiscal year. Distinct from
multi-bulletin-timeseries-regression.md (which projects one series forward and
compares to an external Treasury figure).

## Where the values live
Table **FFO-1 "Summary of Fiscal Operations"** in each bulletin (same table as
the projection question). It breaks RECEIPTS into:
- "On-budget receipts" and "Off-budget receipts" (off-budget ~= Social Security
  trust funds + Postal Service; on-budget = everything else).
- Likewise on-/off-budget OUTLAYS and surplus/deficit further down.
Read the requested two rows. Values in millions of dollars. Strip "r"/"(r)"
revised markers, footnote digits glued to the year, and thousands commas.

## Bulletin -> fiscal-year chaining (September bulletins, 5-yr spacing)
Each FFO-1 lists ~5 ACTUAL annual rows = the five fiscal years ending before the
bulletin's own FY. September YYYY bulletin -> actual FY rows (YYYY-5)..(YYYY-1):
- Sep 1996 -> FY 1991,1992,1993,1994,1995
- Sep 2001 -> FY 1996,1997,1998,1999,2000
- Sep 2006 -> FY 2001,2002,2003,2004,2005
- Sep 2011 -> FY 2006,2007,2008,2009,2010
Four bulletins chain to exactly 20 consecutive fiscal years 1991-2010.
For overlap years take the ACTUAL (non "- Est.") row. Each FY has one actual row.

## The math — R-square = (Pearson r) squared
R-square here means the coefficient of determination of the simple linear
relationship A~B, which for a two-variable bivariate relationship EQUALS the
square of the Pearson correlation coefficient. Do NOT confuse with adjusted R².

```python
import numpy as np
on  = [...20 on-budget receipts in FY order...]
off = [...20 off-budget receipts, same FY order...]
r  = np.corrcoef(on, off)[0,1]   # Pearson r
r2 = r**2
print(round(r2, 4))              # e.g. [redacted]
```
Equivalent: r2 = (np.cov pearson)²; or numpy.polyfit deg=1 then 1 - SSres/SStot
gives the same r² for a single predictor. All three agree.
numpy not importable in execute_code sandbox; run via project python:
`cd /home/azureuser/office-qa && python3 script.py`.

## Answer formatting
Single scalar, decimal in [0,1], rounded to 4 places -> Mode A bare-bracket,
e.g. [[redacted]]. Keep trailing zeros to 4 dp if rounding produces them.

## Worked example (CORRECT)
On-budget vs off-budget NOMINAL RECEIPTS, FY1991-2010, bulletins Sep
[redacted]/[redacted]/[redacted]/[redacted] -> R-square = **[redacted]**. (Verified gold.)

## VARIANT — Pearson r (NOT squared) from foreign-currency positions table
Trigger: "calculate the Pearson correlation coefficient between [currency A]
positions and [currency B] positions ... for [calendar months]". Report DECIMAL
r itself (np.corrcoef(...)[0,1]), do NOT square it. Sign can be negative.

Source table: Treasury Bulletin section "Foreign Exchange / nonbanking firms'
positions in foreign currencies" — the report on NONBANKING (or banking) FIRMS'
FOREIGN-CURRENCY POSITIONS (Capital Movements / "CM" series, 1970s-80s
bulletins). Columns are individual currencies (Belgian franc, Canadian dollar,
French franc, German mark, Swiss franc, sterling, yen, etc.); rows are quarterly
month-ends (Dec, Mar, Jun, Sep). Values in MILLIONS of the foreign currency
unit, not USD. Read the requested two currency columns at the requested 4
month-end rows -> 4 (x,y) pairs.

## PRECISION near-miss pitfall (cost a WRONG: my 0.3723 vs gold [redacted])
With only ~4 data points, a Pearson r near-miss at the 4th decimal
(|delta| ~ 0.0004) means the METHOD was right and ONE extracted cell value is
slightly off (a misread digit, transposed digits, or wrong row/quarter). It is
NOT a formula error. When r matches gold to 2-3 decimals but the 4th is off:
1. Do NOT pre-round any intermediate. Feed raw integer millions straight to
   np.corrcoef; round ONLY the final r to 4 dp.
2. Re-read ALL 2*N source cells from the PDF, digit by digit, including thousands
   commas and any (r)/footnote markers glued to the number. One transposed or
   off-by-a-few-million cell in a 4-point series moves r by exactly this much.
3. Confirm you read the right quarter rows (Dec 1975 vs Dec 1976 are different
   pages/years — quarterly tables repeat the month names every year).
4. Belgian franc and Canadian dollar magnitudes differ ~100x; double-check you
   didn't swap a column or grab an adjacent currency.

## VARIANT — combined [share %, Pearson r] over shipping/vessels table (1940s)
Trigger: "what percentage of the total net registered tonnage cleared from the
US for foreign ports in [Jan,Feb,Mar] of YYYY was attributed to 'American
vessels', AND compute the Pearson correlation coefficient between the American
vessels value and the grand total series? Return both ... first value the single
percentage point difference rounded to one decimal, second the correlation
rounded to thousandths." TWO-PART ANSWER, [pct,r].

Source: 1940s Treasury Bulletin commerce/navigation table "Tonnage of vessels
ENTERED and CLEARED ... in foreign trade" (a.k.a. waterborne foreign commerce).
Columns split tonnage by FLAG: "American vessels" vs "Foreign vessels", plus a
"Total" (grand total) column. Rows are calendar months. Net registered tonnage
in THOUSANDS of tons. Read American-vessels and grand-total cells for the 3
requested months -> 3 (x,y) pairs.

The two computations use the SAME 3 months but DIFFERENT aggregation:
- Part 1 (share %): sum American over the 3 months / sum grand total over the
  3 months * 100, rounded to ONE decimal. ("single percentage point difference"
  = the one aggregate share value, NOT a month-to-month delta). e.g. 34.4.
- Part 2 (Pearson r): np.corrcoef([3 American monthly vals],[3 grand-total
  monthly vals])[0,1], rounded to 3 dp. With only 3 points r can be small/noisy
  (e.g. 0.391). Feed raw values, round only final r.

Answer formatting: both values have decimals -> MODE A. Worked-correct example
submitted [34.4,0.391] (bare comma, no space) and gold was [redacted] — grader
accepted the no-space form, so MODE A bare-comma is safe even when gold prints a
space.
