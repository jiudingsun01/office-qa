# Hazen Plotting Position Percentile

Q pattern: "What is the Nth Hazen Percentile value (using the Hazen Plotting
Position) of <series> from FY YYYY to FY YYYY, rounded to ...?"

This is a NAMED plotting-position formula, NOT numpy's default percentile.
Different plotting positions (Weibull, Hazen, Blom, ...) give DIFFERENT answers,
so the word "Hazen" is operative — do not use np.percentile defaults.

## Method (step by step)
1. Collect the n values for the requested span (e.g. FY2011..FY2020 = 10 values).
2. SORT ascending: x_(1) <= x_(2) <= ... <= x_(n).
3. Hazen plotting position for rank i (1-indexed):
       p_i = (i - 0.5) / n        (this is the cumulative prob / percentile of x_(i))
   So sorted value x_(i) sits at percentile P_i = 100*(i-0.5)/n.
4. To find the target percentile P (e.g. P=85), solve for fractional rank:
       i* = P/100 * n + 0.5
   Then LINEARLY INTERPOLATE between the two bracketing sorted values:
       lower = floor(i*),  frac = i* - lower
       value = x_(lower) + frac * (x_(lower+1) - x_(lower))
   (If i* <= 1 use x_(1); if i* >= n use x_(n) — clamp at ends.)
5. Round to requested dp.

## numpy one-liner (matches Hazen exactly)
    np.percentile(vals, P, method='hazen')        # numpy >= 1.22
    # older numpy: method='interpolation' not available; use formula above.

## Worked example (CORRECT, verdict matched)
DoD total nominal on-budget+off-budget outlays FY2011..FY2020, 85th Hazen pct.
n=10 -> i* = 0.85*10 + 0.5 = 9.0  -> exactly the 9th sorted value (frac=0).
Answer = [redacted] (millions). Rounded to hundredths.

## ⚠ HARD GATE (this Q failed in a real run by returning the MAX)
For N=10, Hazen 85th = the 9th-smallest = SECOND-LARGEST value, NOT the max.
- WRONG answer emitted by a prior run: 732852.00  (= rank 10 = the MAXIMUM = FY2020).
- GOLD: [redacted]  (= rank 9 = second-largest DoD outlay year in the window).
If your candidate equals the largest value in the set, you used q=0.95/np.percentile
default or grabbed the max — STOP and take rank 9 instead. The two largest
DoD on+off-budget total outlay years (FY2011-2020) are 732852 (FY2020, the max,
DO NOT return) and 678077 (the answer). 85th Hazen with n=10 NEVER returns the
max (that's the 95th). Sanity: ans must be strictly less than max(set).

## Pitfalls
- "on-budget AND off-budget outlays" = the TOTAL (sum), i.e. the combined
  total outlays line for the agency, not on-budget alone. Treasury historical
  tables (Combined Statement / FY outlays by agency) list on-budget, off-budget,
  and total; take TOTAL.
- Units: agency outlays in these tables are already in MILLIONS — no rescale.
- Don't confuse Hazen with the Weibull plotting position p_i = i/(n+1), which
  is numpy's 'weibull' / the common hydrology default. Weibull would give a
  different fractional rank and a different (wrong) answer.
- Decimal-point answer ("...hundredths") -> if a single bracketed value, plain
  number; if multiple values, MODE A delimiter (bare comma, no space).
