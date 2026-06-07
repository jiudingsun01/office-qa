---
name: officeqa-msr-projection-vs-actual-deficit
description: OfficeQA Treasury Bulletin — read PRE-PRINTED trillion-dollar deficit figures (no math/regression) — a Mid-Session Review (MSR) PROJECTION for FY YYYY and the later-reported ACTUAL for FY YYYY — from two consecutive September bulletins, then take the absolute difference in trillions rounded to hundredths. PASSED FY2010 MSR-vs-actual = 0.17.
category: research
---

# OfficeQA: MSR projection vs actual deficit (absolute difference, $ trillions)

## Trigger
"absolute difference between the projected federal budget for FY YYYY based on
**MSR estimates** and the **actual** value ... in **trillions** of dollars ...
reference the trillion dollar deficit projections ... reported in the
**September YYYY and YYYY+1** US Treasury Bulletin publications."

Key tells: "MSR estimates", "projected ... and the actual", "in trillions",
"September YYYY and (YYYY+1)". This is NOT a regression question — both numbers
are PRE-PRINTED in the bulletins. Just read two figures and subtract.

## The sourcing convention (the whole trick)
- **September YYYY bulletin** carries the FY YYYY **projection / MSR estimate**
  (forward-looking, the deficit Treasury/OMB expected for the fiscal year that
  is just closing or about to close).
- **September YYYY+1 bulletin** carries the FY YYYY **actual** (now that the
  fiscal year is done and final figures are in).
So for FY2010: projection from **Sept 2010** bulletin, actual from **Sept 2011**
bulletin. The two-bulletin spread (consecutive Septembers) is the standard way
OfficeQA sources a projection-vs-actual pair. Map:
  - "September YYYY"   -> projection (MSR estimate) for FY YYYY
  - "September YYYY+1" -> actual for FY YYYY

## Where in the bulletin
The FY deficit headline appears in the narrative / highlights front matter of
these modern (2010-era) bulletins, quoted in **trillions** (e.g. "$1.3 trillion"
/ "$1.29 trillion"). Also recoverable from the FFO-1 "Summary of Fiscal
Operations" surplus/deficit (-) column (in $ millions -> /1e6 for trillions).
Grep `deficit` and `trillion` in the front pages; cross-check against FFO-1.

## Recipe
1. Open Sept YYYY bulletin -> read the FY YYYY **projected** deficit, round to
   nearest 0.01 trillion.
2. Open Sept YYYY+1 bulletin -> read the FY YYYY **actual** deficit, round to
   nearest 0.01 trillion.
3. Answer = |projection - actual| (absolute value), already in trillions,
   rounded to hundredths.

## Verified instance
FY2010: projection (Sept 2010) and actual (Sept 2011) differ by **0.17**
trillion. PASSED.

## Pitfalls
- Don't fit a regression — the numbers are reported directly. (Distinct from
  `officeqa-surplus-deficit-cubic-forecast`, which DOES fit a polynomial.)
- Honor the per-clause rounding: "rounded to the nearest hundredths place"
  applies to EACH trillion figure before subtracting, and the question may
  repeat it for the final answer. Rounding each to 0.01 first is correct here.
- Units: answer stays in TRILLIONS. Do not convert to millions/billions.
- Sign: it's an ABSOLUTE difference -> always non-negative.
