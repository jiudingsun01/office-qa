# Definitional framing & "extremum by absolute value" questions

## Legal/definitional citations are CONFIRMATORY, not computational
When a question says "according to the definition of X within <statute>" (e.g.
"the definition of OCS within 43 U.S. Code § 1331"), the citation is a red
herring for the math. You do NOT need to read the statute. It only tells you
WHICH line item / category / row in the Bulletin table to read.
- OCS = Outer Continental Shelf -> read the "Outer Continental Shelf rents and
  royalties" line (appears in receipts/deposits tables).
- Treat the statute reference as a label disambiguator, then do a normal cell
  lookup. Don't burn time fetching legal text.

## "Lowest / highest amount" with an ABSOLUTE-VALUE twist
Read the qualifier carefully. Three distinct extremum modes appear:
1. "lowest amount ... lowest ABSOLUTE value" + "report as absolute value":
   - Collect all candidate cells for the period (e.g. each month / each
     category in calendar-year 2016).
   - Compute |x| for each, pick the MINIMUM |x| (closest to zero).
   - Strip the sign in the final answer.
   - Worked: OCS rents/royalties CY2016, lowest |value| -> 56.
2. "lowest amount" (no abs mention): take the most-negative signed value if
   negatives exist; otherwise the numeric minimum.
3. "highest absolute value": take MAX |x| (largest magnitude either sign),
   then apply whatever sign rule the question states.

PITFALL: "lowest absolute value" is NOT "most negative." A -3 has smaller
|x| than +56 only if -3 is a candidate; conversely +56 can be the lowest-|x|
answer even when larger negatives exist. Always rank by |x|, not signed value.

## Calendar-year scope
"in the calendar year of 2016" = Jan–Dec 2016 monthly cells (12 candidates),
NOT fiscal year (Oct 2015–Sep 2016). Pick the right 12 months before ranking.
