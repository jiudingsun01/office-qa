# Percentile via a PLOTTING POSITION (Hazen / Weibull / etc.) over N annual values

Question shape: "What is the 85th HAZEN Percentile value (using the Hazen
Plotting Position) of <metric> from FY YYYY to FY YYYY, rounded to nearest
hundredths, in millions of dollars?"

This is a "read ONE value per year, then compute a percentile" question. The
data extraction is easy (one cell per fiscal year from a by-agency / by-function
table). The ONLY thing that decides correctness is using the SPECIFIC plotting-
position percentile convention named in the question — NOT numpy's default
`np.percentile`, NOT Excel's PERCENTILE.INC, NOT R type-7. Those give different
answers because they use different plotting positions.

## What a "plotting position" is
Sort the N values ASCENDING: x_(1) <= x_(2) <= ... <= x_(N). Assign each ordered
value a cumulative probability ("plotting position") p_i. The general family is:
    p_i = (i - a) / (N + 1 - 2a)        for i = 1..N
Different conventions pick different `a`:
- HAZEN:    a = 0.5  =>  p_i = (i - 0.5) / N
- WEIBULL:  a = 0    =>  p_i = i / (N + 1)
- (Cunnane a=0.4, Gringorten a=0.44, Blom a=0.375 — read whichever is named.)

To get the value at percentile P (e.g. P = 85 => target probability q = 0.85):
1. Sort ascending, compute p_i for each rank i.
2. If q exactly equals some p_i  -> answer = x_(i) (no interpolation).
3. If q < p_1 (below smallest plotting position) -> answer = x_(1).
   If q > p_N (above largest) -> answer = x_(N).
4. Otherwise find the bracket p_k <= q <= p_{k+1} and LINEARLY interpolate:
       x = x_(k) + (q - p_k)/(p_{k+1} - p_k) * (x_(k+1) - x_(k))

## HAZEN with N=10 (FY2011..FY2020 = 10 fiscal years) — the common case
Hazen p_i = (i - 0.5)/10 = {0.05, 0.15, 0.25, 0.35, 0.45, 0.55, 0.65, 0.75,
0.85, 0.95} for i = 1..10. So q = 0.85 lands EXACTLY on i = 9 => the answer is
the 9th-smallest value, no interpolation. (q = 0.95 -> 10th = max; q = 0.05 ->
min.) This clean alignment is why a 10-year Hazen percentile at a multiple of 10
+ 5 (15th, 25th, ..., 85th, 95th) is just the k-th order statistic.

## Recipe (copy/paste)
    import numpy as np
    x = np.sort([... N annual values ...])          # ascending
    N = len(x)
    a = 0.5                                          # HAZEN; 0 for Weibull, etc.
    p = (np.arange(1, N+1) - a) / (N + 1 - 2*a)      # plotting positions
    q = 85/100                                       # the requested percentile
    ans = round(float(np.interp(q, p, x)), 2)        # np.interp does steps 2-4
    # np.interp clamps to endpoints for q outside [p_1, p_N] — matches rule 3.

`np.interp(q, p, x)` reproduces the whole procedure (exact hit, endpoint clamp,
linear interpolation) in one call. Just build `p` with the right `a`.

## Where the data lives (Defense / agency / function outlays)
"total nominal on-budget and off-budget outlays for the Department of Defense"
= the by-agency table (FFO "On-Budget and Off-Budget Outlays by Agency",
see references/outlays-by-agency.md). For each fiscal year read the Defense row's
FY total = on-budget + off-budget combined (the agency's total outlay line).
Collect one value per FY in the window. Values already in millions — no scaling.
Across a 10-year window you'll need SEVERAL bulletins (each issue prints a few
fiscal years); prefer the latest/revised figure for any given FY.

## Pitfalls
- DEFAULT percentile != plotting-position percentile. `np.percentile(x, 85)`
  uses linear interp on positions i-1 over N-1 (R type-7), giving a DIFFERENT
  number than Hazen. If the question NAMES a plotting position, you MUST build
  p_i with that convention. Ignoring the name is the #1 failure mode.
- a-value: Hazen a=0.5 (=> (i-0.5)/N). Do not confuse with Weibull i/(N+1).
  Re-read which plotting position is named.
- Sort ASCENDING before assigning ranks. A descending sort flips the answer to
  the (N+1-i) order statistic.
- Count the years: "FY2011 to FY2020" inclusive = 10 values. An off-by-one in
  the window changes N, hence every p_i, hence the interpolation.
- Rounding: keep trailing zeros to the requested place (678077.00 not 678077.0).
  The answer here is a single value equal to one data point (no interp), so it's
  a whole number with .00 appended. Decimal point present but it's a plain count-
  of-dollars value -> emit as Mode A bare number (no thousands separators).

## Worked success
Q: 85th Hazen Percentile of total on+off-budget DoD outlays, FY2011-FY2020,
nearest hundredths, millions. N=10, Hazen p_9 = 0.85 exactly => answer = 9th-
smallest annual DoD outlay = 678077.00 ✓ (gold 678077.00). No interpolation
needed because 0.85 hit a plotting position exactly.
