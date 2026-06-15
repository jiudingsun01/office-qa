# MSR projected-vs-actual federal budget deficit (abs diff, trillions)

## Trigger
Question asks for the absolute difference between a PROJECTED federal budget /
deficit (based on MSR = Mid-Session Review estimates) for a given fiscal year and
the ACTUAL value, "in trillions of dollars," rounded to the nearest hundredths.
Often phrases it as "trillion dollar deficit projections ... reported in the
September YYYY and YYYY US Treasury Bulletin publications."

## KEY INSIGHT: both numbers live in bulletins (NOT external)
Unlike the regression abs-diff questions (where the "actual" is an external
constant not in any document), this MSR pattern gives you BOTH values inside
Treasury Bulletins, and the question usually names the two issues explicitly:
- The PROJECTION for FY N is in the **September YEAR N** bulletin (the MSR for
  that fiscal year, published mid-year before the year closes).
- The ACTUAL for FY N is in the **September YEAR N+1** bulletin (the next year's
  issue, which reports the realized/actual deficit for FY N).

So: "September 2010 and 2011 bulletins" for FY 2010 →
  projection = Sept 2010 issue, actual = Sept 2011 issue.

## Where in the bulletin
The deficit/budget figures appear in the federal-finance / budget-results
narrative or summary tables (Treasury financial-operations summary), already
expressed in dollars; convert to trillions and round each to hundredths BEFORE
subtracting if the question says the projections are "rounded to the nearest
hundredths." Both operands are already given to ~hundredth-of-a-trillion
precision in the text, so you usually just read two numbers like 1.47 and 1.30.

## Compute
answer = | projection_T(rounded 2dp) − actual_T(rounded 2dp) |
Worked example (FY2010): |1.47 − 1.30| = 0.17. Gold = 0.17.

## Delimiter / format
Single scalar with a decimal point → MODE A bare number (e.g. [redacted]). No sign
needed (absolute difference). No thousands separators at this magnitude.

## Pitfalls
- Don't confuse with the regression abs-diff family (actual NOT external here).
- Round EACH operand to hundredths first, then subtract — matches "projections
  rounded to the nearest hundredths."
- Pull projection from year-N issue and actual from year-(N+1) issue; do not read
  both from the same bulletin.
