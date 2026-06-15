# U.S. Reserve Assets table + Geometric mean aggregation

## When this applies
Q phrasing: "geometric mean across each of the 4 U.S. reserve asset values
in end of calendar month <Mon> across <Y1>-<Y2> inclusive" — or any Q that
references "U.S. reserve assets" and its components.

## Where the numbers live: "U.S. Reserve Assets" table
- Section: International Financial Statistics (IFS) part of the Treasury
  Bulletin (same neighborhood as the "Liabilities to Foreign Countries" /
  exchange-stabilization tables). Table title is literally
  "U.S. Reserve Assets" (sometimes "International Reserves and Foreign
  Currency Liquidity" in newer layouts).
- It has exactly 4 component columns (this is the "4 reserve asset values"):
    1. Total reserve assets   <- do NOT use Total; the 4 are the COMPONENTS,
       OR the Q means the 4 line items. READ CAREFULLY which 4 are wanted.
    Components are:
    1. Gold stock (or "Gold")
    2. Special Drawing Rights (SDRs)
    3. Reserve position in the IMF
    4. Foreign currencies (holdings of convertible foreign currencies)
  These four sum to total reserve assets. The Q "4 U.S. reserve asset values"
  = these 4 components (gold, SDRs, IMF reserve position, foreign currencies).
- Values are reported in MILLIONS of dollars, end-of-period. The Q asks for
  "end of calendar month July" -> read the July (or the period-end) column /
  row for each year.
- DO NOT scale to billions unless the Q explicitly says billions. The
  example Q wanted raw millions; gold answer [redacted] is a millions-scale
  geometric mean.

## The computation: geometric mean
For N values v_1..v_N (here N = 4 components x 4 years = 16 values):
    geomean = (v_1 * v_2 * ... * v_N) ** (1/N)
Equivalently exp(mean(ln(v_i))) — use this log form to avoid overflow when
multiplying 16 millions-scale numbers (product ~ 1e70+).

    import numpy as np
    geomean = np.exp(np.mean(np.log(vals)))   # vals = list of all 16

Round HALF_UP to the requested places (here hundredths). 2010-2013 July
end-of-month, 4 components each -> 16 values -> 29347.01.

## Pitfalls
- "across 16 total values" confirms it is ONE geometric mean over the full
  flattened pool (4 comp x 4 yr), NOT a mean-of-yearly-means or per-component
  geomean. Flatten all 16, take one geomean.
- All reserve-asset values are positive, so geomean is well-defined; never a
  negative/zero entry to worry about.
- "end of calendar month July" = the July column for each year (month-end
  reporting). If the table is monthly, pick the July row; if quarterly, July
  falls in the same period as the Q2/Q3 boundary — prefer the explicit July
  monthly figure if present.
- Decimal-output convention: answer has a decimal point ([redacted]) -> MODE A
  delimiter rules (bare comma, no space) if ever bracketed with siblings.
- Do NOT confuse this in-bulletin reserve-assets table with external IMF/IFS
  web data; the bulletin prints its own monthly figures.
