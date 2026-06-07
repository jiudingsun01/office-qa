---
name: officeqa-arc-elasticity-collections
description: OfficeQA Treasury Bulletin — compute the "arc elasticity" of one series with respect to another between two dated periods (e.g. total IRS collections w.r.t. unemployment-insurance contributions, Jan 1960 vs Mar 1960). Covers the midpoint arc-elasticity formula, the dependent/independent ordering trap, sign handling, and where the "Internal Revenue Collections" table lives.
category: research
---

# OfficeQA: Arc Elasticity of Internal Revenue Collections

## When this applies
Question says "compute the arc elasticity of Y with respect to X for
<period A> and <period B>". Typically Y = "total collections reported by the
Internal Revenue Service" and X = a single line item like "unemployment
insurance contributions", "income tax", "employment taxes", etc. Two dated
columns (e.g. January 1960 and March 1960). Report to N decimals.

## Where the data lives
- Table: "Internal Revenue Collections" (Treasury Bulletin, in thousands of
  dollars). In 1960-era bulletins this is in the Internal Revenue section.
  Find it: pdftotext -layout, search for "Internal Revenue Collections" or
  "Unemployment insurance".
- Rows are collection categories; columns are months (and sometimes
  fiscal-year-to-date totals). Pick the two MONTH columns named in the question,
  not the YTD/cumulative column.
- "Total" / "Total Internal Revenue collections" is the Y series. The named
  sub-item (e.g. "Unemployment insurance") is the X series.

## The formula (midpoint / arc elasticity)
Let X = independent variable (the "with respect to" series),
    Y = dependent variable (the lead series, e.g. total collections).
Period 1 = first date named, Period 2 = second date named.

    %ΔY (arc) = (Y2 - Y1) / ((Y2 + Y1)/2)
    %ΔX (arc) = (X2 - X1) / ((X2 + X1)/2)
    elasticity = %ΔY / %ΔX

Equivalently:
    E = [(Y2 - Y1)/(Y2 + Y1)] / [(X2 - X1)/(X2 + X1)]
(the /2 in each midpoint cancels). Units cancel — no need to scale thousands.

## Traps
1. ORDER / which-is-which: "elasticity of Y with respect to X" => Y is the
   NUMERATOR (dependent, lead series after "elasticity of"), X is the
   DENOMINATOR (the "with respect to" series). Getting these swapped inverts
   the magnitude. Total collections is almost always Y.
2. SIGN: this is genuinely signed. If one series rises while the other falls
   between the two periods, the elasticity is NEGATIVE — keep the minus sign.
   (PASSED: total IRS collections w.r.t. unemployment-insurance contributions,
   Jan 1960 vs Mar 1960 = -3.524. Collections rose, UI contributions fell ->
   negative.)
3. USE ARC (midpoint) denominators, not a single base period. Arc elasticity
   averages the two endpoints; do NOT use %change-from-period-1 (that's point
   elasticity and gives a different number).
4. Keep full precision in intermediates; round only the final elasticity to the
   requested decimals.

## Worked check
Y1, Y2 = total collections at period 1, 2. X1, X2 = sub-item at period 1, 2.
  E = ((Y2-Y1)/(Y2+Y1)) / ((X2-X1)/(X2+X1))
Compute in Python with exact cell values read from the -layout dump; verify the
sign matches the directions of the two series before reporting.
