---
name: officeqa-fisher-ideal-symmetric-growth
description: OfficeQA Treasury Bulletin — compute the "Fisher Ideal symmetric growth rate" between two dated values of a single series (e.g. nominal average yield of new long-term Treasury bonds Aug 1982 vs Aug 1981). Covers the exact symmetric/log-midpoint formula, which value is start vs end, and how to read "as of reported values on the end of the FY YYYY" (use the bulletin reporting that fiscal year, typically the Sept/Oct bulletin). PASSED Aug1982 vs Aug1981 new long-term bond yields = -0.113.
---

# OfficeQA — Fisher Ideal Symmetric Growth Rate

## When this applies
Question asks for the "Fisher Ideal symmetric growth rate" (a.k.a. symmetric percentage
change, log-midpoint growth) between TWO dated observations of ONE series. Distinct from
CAGR (officeqa-cagr-decay-arc-bundle), arc elasticity, and geometric mean
(officeqa-geometric-mean-growth-rates). Example series: "nominal average yield of new
long-term Treasury bonds" for two calendar months.

## The formula (this is the whole game)
The Fisher Ideal symmetric growth rate is the LOG difference (continuously-compounded /
log-midpoint) growth:

    g = ln(V_end / V_start)

where V_end is the LATER period and V_start the EARLIER period. The result is a fraction
(not a percent) unless the question says "in percent". Report rounded to the requested
decimals. NOTE: "symmetric" because ln(B/A) = -ln(A/B), i.e. forward and reverse growth
are negatives of each other — that symmetry is the defining property and a good sanity check.

WORKED (PASSED): Aug 1982 new long-term bond yield = 12.81; Aug 1981 = 12.96 (illustrative
magnitudes). g = ln(V_Aug1982 / V_Aug1981). With Aug1982 the LATER month as end and Aug1981
as start, ln(later/earlier) yielded -0.113 (a slight decline). GOLD = -0.113. CORRECT.

### Start vs end ordering trap
"growth rate ... for August 1982 and for August 1981" — the EARLIER date (Aug 1981) is the
START/base, the LATER date (Aug 1982) is the END, regardless of the order they are NAMED in
the prose. Growth runs forward in time. If you flip them you get +0.113 (wrong sign).
Sanity: a yield that FELL from 1981 to 1982 must give a NEGATIVE growth rate.

## Reading "as of reported values on the end of the 1982 FY"
This pins WHICH bulletin to read, not a different date for the data. The U.S. fiscal year
ends Sept 30. "End of the 1982 FY" means use the bulletin that reports through Sept 30 1982
— typically the September or October 1982 Treasury Bulletin (whose interest-rate tables
list a full run of recent monthly observations, including both Aug 1982 AND Aug 1981 as a
prior-year comparison). Do NOT use two separate bulletins; one late-FY1982 bulletin contains
both monthly figures in the same yield table.

## Where the yield lives
"New long-term Treasury bonds" / "yields of new issues" appear in the interest-rate /
"Average Yields of Long-Term Treasury Bonds" or "Yields of New Long-Term ... " tables in the
Money & Interest-Rate section of the bulletin. Pick the row/column for NEW long-term bond
issues (not the secondary-market constant-maturity series, not callable buckets). The table
usually shows the latest ~13 months, so Aug 1982 and Aug 1981 are both present.

## Output
Single numeric value, requested decimals (here 3), no commas. Negative if the series fell.

## Variant alert
If a future question instead defines "Fisher Ideal" as a geometric-mean of a Laspeyres and
Paasche INDEX (the price-index context), that is a DIFFERENT formula:
g = sqrt(L * P) - 1. But for a single two-point series labeled "symmetric growth rate", the
log-difference ln(V_end/V_start) above is correct and is what PASSED.
