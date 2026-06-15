# Geometric mean of quarterly GDP growth (annualized rates)

## Trigger
Q asks for the "Geometric mean of U.S. real GDP growth, quarterly percent change
at an annual rate" over a span of years, and which year is highest. Source values
are the 4 quarterly real GDP growth rates per year, each expressed as an
ANNUALIZED percent change (the standard BEA presentation, e.g. +2.3, +2.0, +3.4, +2.9).

## THE TRAP (what failed)
Naive answer = geometric mean of the 4 annualized VALUES directly:
  GM_values = (prod(R_i))^(1/4)   -> for 2017 gave 2.74. WRONG.

## Correct convention (gold)
"Geometric mean of quarterly growth" means a PER-QUARTER growth rate. Each
annualized rate must first be de-annualized to a quarterly growth FACTOR, then
geometric-mean those factors, then convert back to percent:

  q_factor_i = (1 + R_i/100) ** (1/4)        # annualized -> quarterly factor
  GM_q       = (prod_i q_factor_i) ** (1/n)   # n = number of quarters (4)
  answer_%   = (GM_q - 1) * 100

A flat 2.74% annualized -> 0.68% quarterly. Real 2017 quarters -> 0.69 (gold).

```python
import math
def quarterly_gm_pct(annualized_vals):
    prod = 1.0
    for R in annualized_vals:
        prod *= (1 + R/100) ** (1/4)
    return ((prod ** (1/len(annualized_vals))) - 1) * 100
```

## Year ranking is UNAFFECTED
The de-annualization is monotonic, so the year with the highest GM is the same
under either convention. 2017 ranks highest either way. ONLY the reported value
changes (2.74 vs 0.69). So: pick the year by the simple geomean if you must, but
ALWAYS report the per-quarter value via the formula above.

## Rounding
"Year to nearest tenth" applies to the SELECTION criterion only; report the year
as an integer. Report the geometric mean rounded to the requested place
(hundredths here -> 0.69). Delimiter: both have/are numbers; the value has a
decimal -> MODE A bare comma, BUT the year is a bare integer, so format is
[redacted] — note the gold uses ", " here (year is integer, not decimal).

## FAIL LOG
- 2013-2019 highest-GM Q: returned [2017, 2.74] (geomean of raw annualized values),
  gold [redacted] (per-quarter de-annualized geomean). Year correct, value wrong.
- SAME Q FAILED AGAIN [2017,2.74] vs [2017,0.69]. This reference was already
  complete & correct at the time — the run did NOT load it and fell into the
  documented trap. ROOT CAUSE = routing, not knowledge. Mitigation: the trap is
  now mirrored in top-level MEMORY so it surfaces without loading this file.
  Any Q containing "geometric mean" + "GDP growth" + "annual rate" -> de-annualize
  FIRST (1+R/100)**0.25 per quarter before geomean. NEVER geomean raw % values.
