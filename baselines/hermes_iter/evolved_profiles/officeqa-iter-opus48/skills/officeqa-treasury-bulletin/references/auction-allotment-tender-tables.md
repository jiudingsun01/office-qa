# Treasury Auction / Allotment / Tender Tables

Q-TYPE: "total dollar value of bids submitted by investors for the <N>-year
Treasury notes/bills maturing <date>" and "what percent of these were <subset>
tenders accepted submitted on behalf of <investor class>". Two-part: a TOTAL and
a PERCENT-of-total.

## Where the data lives
- Section: "Public Debt Operations" / "Treasury Financing Operations" /
  "Disposition of ... Tenders" / auction allotment tables (sometimes a chart +
  backing table). Search the bulletin index for the security ("2-year notes"),
  the maturity/issue month, and words like "Tenders", "Accepted", "Allotted".
- Each auction has its OWN sub-table keyed by ISSUE/MATURITY date. Pin the row
  to the EXACT maturity phrasing ("maturing at the end of July 1984" => the note
  whose maturity is 7/31/1984). Do NOT grab a neighboring auction's block.

## Column / row anatomy (recurring)
- A "Tenders received" / "Bids submitted" total (this is sub-question 1's value —
  the GROSS amount investors bid, NOT the amount accepted/allotted).
- Breakdown columns: "Cash" vs "Noncash (rollover/exchange)" tenders, and/or
  "Accepted" vs "Total". Rollover/exchange tenders = holders of maturing issue
  rolling into the new one.
- Investor-class rows or columns: domestic vs "foreign"/"global non-domestic"
  (often "foreign and international" or "F.R. Banks for foreign account").
  "global non-domestic investors" = the FOREIGN line, not domestic, not the
  grand total.

## Computation
- Sub-Q1 (total bids/tenders submitted): read the GROSS total tenders-received
  figure for that auction. Round to nearest nominal dollar. Values are usually
  already in actual dollars (e.g. 10,102,000,000) — confirm the table's unit
  header (often "in thousands" or "in millions"); scale up to whole dollars
  before reporting.
- Sub-Q2 (percent): numerator = the SPECIFIC subset cell asked
  (noncash/rollover tenders ACCEPTED for the foreign/global class); denominator
  = the sub-Q1 total bids. percent = num/den, then express as 0.1234 -> 12.34,
  ROUND_HALF_UP to hundredths.
- Read the qualifier chain literally: "noncash rollover tenders ACCEPTED
  submitted on behalf of global non-domestic investors" = intersection of
  (noncash/rollover) AND (accepted) AND (foreign). Use the single cell at that
  intersection, not a row/column subtotal.

## Verified example (CORRECT)
2-year notes maturing end of July 1984: total bids submitted = 10,102,000,000;
noncash rollover accepted for foreign/global = 4.73% of total. Answer
[10102000000, 4.73]. Confirms: sub-Q1 = gross tenders received (whole dollars,
no scaling needed here); sub-Q2 = subset-cell / gross-total as percent.

## Pitfalls
- Don't confuse "bids submitted/tenders received" (gross) with "accepted/
  allotted" (the auction took less than was bid). Sub-Q1 wants the GROSS unless
  it says "accepted".
- Percent denominator is the TOTAL BIDS (sub-Q1), not the accepted total.
- Verify unit header before reporting a nominal-dollar answer.
