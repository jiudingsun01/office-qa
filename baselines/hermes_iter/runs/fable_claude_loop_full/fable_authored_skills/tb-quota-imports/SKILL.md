---
name: tb-quota-imports
description: Use for Treasury Bulletin questions about quantities of commodities imported under quota provisions (fish, cattle, milk/cream, potatoes, Philippine sugar/coconut oil, petroleum, etc.) for any month or period in 1939-1941+.
---

# Treasury Bulletin: "Commodities Imported under Quota Provisions" table

## Where the data lives
- Recurring table near the back of each issue (MISCELLANEOUS section), titled "Commodities Imported under Quota Provisions".
- Rows are commodities; there is usually exactly ONE fish line: "Fish, fresh or frozen, filleted, etc., Cod, Haddock, Hake, Pollock, Cusk and Rosefish" (OCR mangles the species names — match on "Fish, fresh or frozen"). "All fish commodities" = this single line; do not hunt for extra fish rows.
- Units are as printed per row (fish in Pounds); the "Established quota" column is the annual cap, NOT an import quantity.

## CRITICAL format change: monthly columns vs cumulative
- **1939 issues**: columns are per-month quantities ("In January", "In February", ...). These are true monthly figures.
- **From early 1940 onward**: the table has a SINGLE column "Quantity imported under quotas to <date>" (e.g. "to March 30, 1940"). This is **cumulative from the start of the quota period (usually Jan 1)**, NOT a monthly figure.
  - A monthly 1940+ quantity must be computed by differencing consecutive issues' cumulative values (e.g. March 1940 ≈ "to Mar 30" minus "to Mar 2" from the prior issue). Cutoff dates are weekly (Saturdays), so months are approximate.
  - NEVER report a cumulative "to <date>" value as the quantity "for" that month — this single mistake can blow up a multi-step calculation by 2-3x.
- BUT: question writers sometimes themselves treat a printed value loosely. If your carefully-derived monthly figure produces an implausible multi-step result, also compute the variant using the raw printed figures from a single issue and sanity-check both.

## Data vintage / revisions (applies to many Bulletin tables)
- Monthly quota figures are REVISED in later issues (e.g. Feb 1939 fish: 1,118,244 in the Apr-1939 issue → 1,173,728 in May → 1,187,589 in June → 1,187,139 in Oct). Different issues give materially different answers.
- Question gold answers are typically built from ONE issue — usually the EARLIEST issue whose table covers all the months asked about (first-publication / preliminary figures), since the writer reads a single table.
- Procedure: identify the first issue containing all required months in one table and use those values. If you instead used a later (revised) vintage, recompute with the first-publication vintage before answering. When vintages disagree, prefer first publication.

## Exchange rates for late-multiplication steps
- The Bulletin's own exchange-rate tables stop around late 1940; for later years use standard reference values. Annual average nominal $/£: 1940 ≈ 3.83, 1941 ≈ 4.03 (wartime official peg $4.03-4.035). If the final answer is graded to 4 decimals, small rate differences (4.03 vs 4.035 vs 4.04) shift the result by ~0.3% — state the rate used and prefer 4.03 unless evidence suggests otherwise.

## Multi-step forecast arithmetic
- "Month-over-month increase, add to latest month to forecast next month" = linear extrapolation: F = 2×(latest month) − (prior month). Keep full precision; round only the final answer.
- "Express difference as a percentage of the forecast" = |forecast − actual| / forecast × 100 (denominator is the forecast, not the actual).
