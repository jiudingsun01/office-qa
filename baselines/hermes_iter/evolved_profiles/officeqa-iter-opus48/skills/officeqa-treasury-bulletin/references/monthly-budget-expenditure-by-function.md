# Monthly Budget Expenditures by Function/Classification (1940s–1950s bulletins)

## Trigger
Q asks for a SUM (or comparison) of a named expenditure CATEGORY across all
individual calendar months of a given year, e.g.:
- "total sum of monthly values of expenditures for U.S. national defense and
  associated activities in 1953"
- "...for major national security", "...veterans services and benefits",
  "...interest on the public debt", monthly, for a calendar/fiscal year.
Answer requested in **millions of nominal dollars** (NOT billions, NO FX).

PASSED: 1953 national defense + associated activities, sum of all 12 calendar
months = **44463** (millions). Clean pass, no rounding/scaling trap.

## Where it lives
- These come from the "Budget Receipts and Expenditures" / "Expenditures by
  Major National Security and Other Classifications" tables in 1940s–1950s
  bulletins (statistical section, not front matter).
- The table is typically a MONTHLY breakdown: rows = expenditure function
  (National defense, Veterans, Interest on public debt, International affairs,
  etc.), columns = the 12 calendar/fiscal months (sometimes with a yearly
  total column already printed — verify your hand-sum against it if present).
- "National defense and associated activities" / "major national security"
  is usually a single labeled row (or a subtotal line); take that row's 12
  monthly cells. Watch for a printed annual total — it's a free cross-check.

## Extraction
- `pdftotext -layout` on the table page keeps the 12 monthly columns aligned.
- Sum all individual MONTHLY cells (do NOT just read the year-total column if
  the question says "using specifically only the reported values for all
  individual calendar months" — but the two should match; mismatch = parse error).

## Convention / don't over-engineer
- Output is plain nominal MILLIONS — do NOT scale to billions, do NOT apply FX,
  do NOT round to thirds. The default billions/rounding conventions for other
  Treasury Bulletin questions DO NOT apply here.
- If a monthly total column exists, summing the 12 months should equal it;
  use that to catch a dropped/misread cell.
