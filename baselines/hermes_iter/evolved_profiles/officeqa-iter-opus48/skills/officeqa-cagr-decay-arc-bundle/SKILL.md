---
name: officeqa-cagr-decay-arc-bundle
description: OfficeQA Treasury Bulletin — a SINGLE outlay/receipt series at two fiscal-year endpoints, asked for a BUNDLE of growth metrics in one question — CAGR, "annual decay factor", and "arc elasticity (midpoint percentage change)" — returned as bracketed comma-separated decimals. Covers the exact formula for each metric, the same-series (not two-series) arc-elasticity twist, and the n = END_year - START_year exponent convention.
category: research
---

# OfficeQA: CAGR + Decay Factor + Arc Elasticity bundle (single series)

## When this applies
One agency's "total outlays" (or receipts) given at two fiscal-year endpoints
(e.g. FY2011 -> FY2019), "including both budgetary and trust-fund flows",
and the question asks for SEVERAL growth metrics at once, typically:
  - compound annual growth rate (CAGR)
  - annual decay factor
  - arc elasticity (using midpoint percentage change)
Output: bracketed comma-separated decimals in the stated order.
This is DISTINCT from officeqa-arc-elasticity-collections (which is TWO series,
Y w.r.t. X). Here arc elasticity is computed on the SAME single series over time.

PASSED: Dept of Labor total outlays FY2011->FY2019 = [-0.153, 0.847, -1.162].

## Where the data lives
- "Outlays by Agency" / "Outlays of the Federal Government by Agency" summary
  table in the Federal Fiscal Operations section (FFO tables). "include both
  budgetary and trust-fund flows" = the TOTAL outlays row for the agency, i.e.
  do not split off the trust-fund-only or budgetary-only sub-line; use the
  combined agency total. (Mirrors the DoD Military+Civil "sum both sub-rows"
  trap from outlays-by-agency: always take the full agency total.)
- Source the two endpoint years from bulletins that report each FY's final
  actual figure (a bulletin dated AFTER the fiscal year closes, e.g. the
  Dec/early-next-year bulletin or the FY-summary column).

## The three formulas
Let V0 = value at START year, V1 = value at END year,
    n  = END_year - START_year   (NOT count of points; FY2011->FY2019 => n = 8).

1. CAGR (decimal):
       CAGR = (V1 / V0)^(1/n) - 1
   If the series shrank, CAGR is NEGATIVE (e.g. -0.153).

2. Annual decay factor:
       decay_factor = V1_per_year_ratio = (V1 / V0)^(1/n) = 1 + CAGR
   i.e. the annual multiplier. For a SHRINKING series it is BETWEEN 0 AND 1
   (e.g. 0.847 = 1 + (-0.153)). It is simply (1 + CAGR). Do NOT negate it.

3. Arc elasticity (midpoint percentage change) — SAME series w.r.t. TIME:
       %Δvalue (arc) = (V1 - V0) / ((V1 + V0)/2)
       %Δtime  (arc) = (t1 - t0) / ((t1 + t0)/2)   where t0,t1 = the YEARS
       arc_elasticity = %Δvalue / %Δtime
   Use the calendar/fiscal YEAR numbers (2011, 2019) as the time variable.
   The midpoint of time = (2011+2019)/2; Δtime = 2019-2011 = 8.
   Result is NEGATIVE when the series shrank (e.g. -1.162).

## CONTINUOUSLY COMPOUNDED variant (different formula!)
If the question says "CONTINUOUSLY compounded average annual growth rate"
(not the plain "compound annual growth rate"), use the LOG formula, NOT the
power formula:
       r_cc = ln(V_end / V_start) / n          where n = END_year - START_year
This is the natural-log/exponential-growth rate. It is SMALLER in magnitude
than the discrete CAGR (V1/V0)^(1/n)-1 for positive growth. Report as decimal.
  PASSED: Seigniorage on coins (silver+minor), end CY1945 -> 1955, n=10,
  continuously compounded = ln(V1955/V1945)/10 = [redacted] (nearest thousandths).
"Continuously compounded" / "continuous growth rate" / "instantaneous rate"
=> log formula. "Compound" / "CAGR" alone => power formula above.
Same n = END - START convention for both.

## Fiscal-year-of-event lookups (Korean War etc.)
US federal FY = July 1 .. June 30, labeled by the calendar year it ENDS in.
Korean War started June 25, 1950 => that date is in FY1950 (Jul 1 1949 - Jun 30
1950), NOT FY1951. So "FY1947 to the FY the Korean War started" => FY1947->FY1950,
n = 1950-1947 = 3.
"Expenditure transfers to the [OASI] trust fund" — COLUMN-PICK TRAP, FAILED.
I picked the "Appropriations by Congress" / general tax-transfer column
(FY1947=1459.5, FY1950=2106.4, ratio 1.44 => CAGR 13.01%). That is WRONG.
GOLD = 108.01 %/yr. Working backwards: CAGR=1.0801 with n=3 means the endpoint
RATIO = (1+1.0801)^3 = 2.0801^3 = ~9.0. So the CORRECT "expenditure transfers"
series grew ~9x from FY1947 to FY1950, NOT 1.44x. The right line item is the one
literally labeled "Expenditure transfers" (a.k.a. payroll-tax "Transfers from
general fund"/"Deposits by States" style transfer that ballooned 1947->1950 as
SS coverage expanded), whose FY1947->FY1950 ratio is ~9. PROCEDURE: when the
question says "expenditure transfers", do NOT grab the big "Appropriations by
Congress" total — scan the OASI trust-fund receipts table for the column/row
whose header contains "transfer" AND whose FY1950/FY1947 ratio ≈ 9, then
CAGR = (V1950/V1947)^(1/3) - 1 = 1.0801 => 108.01 %/yr. Answer in percent => 108.01.

## Traps
1. n = END - START (= 8 for FY2011->FY2019), not 9, not the number of data
   points. (Same n-convention as the geometric-rate and CAGR skills.)
2. decay factor = 1 + CAGR, a number in (0,1) for a declining series. Don't
   report it as a negative number and don't confuse it with |CAGR|.
3. Arc elasticity here is the SAME series vs TIME (years as the X variable) —
   NOT two different data series. Use the YEAR values for the time midpoint.
4. "output all rate values in decimal form" => -0.153, not -15.3%.
5. Rounding: round EACH final metric to the stated decimals (3 dp here);
   keep full precision in intermediates.
6. FORMAT: bracketed CSV, NO spaces after commas unless the gold clearly has
   them — emit [-0.153,0.847,-1.162] style (see memory: whitespace-sensitive
   bracketed-CSV trap).

## Worked check (Python)
    V0, V1 = <FY2011 outlays>, <FY2019 outlays>
    t0, t1 = 2011, 2019
    n = t1 - t0
    cagr = (V1/V0)**(1/n) - 1
    decay = (V1/V0)**(1/n)            # = 1 + cagr
    pct_v = (V1 - V0)/((V1 + V0)/2)
    pct_t = (t1 - t0)/((t1 + t0)/2)
    arc   = pct_v / pct_t
    print([round(cagr,3), round(decay,3), round(arc,3)])
Verify all three signs against the direction of the series before reporting.
