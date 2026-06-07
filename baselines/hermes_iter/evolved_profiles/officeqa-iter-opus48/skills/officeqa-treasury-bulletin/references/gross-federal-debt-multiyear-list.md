# "Gross federal debt incl. agency securities" — WHICH ROW to read

## Trigger
Q: "total gross U.S. federal debt at end of fiscal month <M> from Y1 to Y2 ...
include any securities issued by federal agencies like the FHA ... comma
separated list ... figures exclusively from <M> treasury bulletins."
(Delimiter/Mode-B formatting for this is already in SKILL.md lines 72-92; this
ref is ONLY about row identification + the per-year extraction loop.)

## The row-selection lesson (net-new)
The Bulletin's federal-debt table has nested subtotals:
    Public debt securities (Treasury-issued) .......... subtotal
  + Agency securities (guaranteed + non-guaranteed:
    FHA, etc.) ........................................ subtotal
  = TOTAL GROSS FEDERAL DEBT ......................... <-- READ THIS
- "include securities issued by federal agencies like the FHA" is the tell that
  you want the GRAND TOTAL gross line, NOT the "Total public debt outstanding"
  subtotal. The grand total > public-debt-only by the agency amount.
- Contrast: a question that says "total public debt outstanding" (no agency
  clause) wants the public-debt subtotal instead. The FHA/agency clause is the
  switch between the two rows.
- Values are integer MILLIONS of dollars in the 1969-1980 era.

## Per-year extraction loop
1. The question pins the SOURCE month: each year's value must come from THAT
   month's own issue (e.g. every January bulletin), not a later annual recap.
2. Read the SAME total-gross-federal-debt row in each year's issue; the
   end-of-fiscal-month-<M> figure is the one carried in that month's bulletin.
3. Emit strictly chronological Y1..Y2. Pure extraction, NO arithmetic.

## Worked CORRECT (Jan 1969-1980, $millions)
374,443 / 381,327 / 401,845 / 433,432 / 461,855 / 478,957 / 505,483 /
595,307 / 664,852 / 731,821 / 798,733 / 854,741

## Takeaway
Agency/FHA clause -> TOTAL GROSS FEDERAL DEBT line (public debt + agency
securities), one read per year's own target-month issue, chronological, no math.
