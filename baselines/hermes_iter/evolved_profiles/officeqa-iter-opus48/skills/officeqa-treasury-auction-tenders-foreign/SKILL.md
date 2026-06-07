---
name: officeqa-treasury-auction-tenders-foreign
description: OfficeQA Treasury Bulletin — auction/financing-results tables for a specific note/bond offering (e.g. "2-year notes maturing end of July 1984"). Covers total bids/tenders submitted, noncash rollover tenders, and the foreign/non-domestic ("on behalf of foreign investors") investor breakdown. Distinct from yield/maturity-schedule tables.
category: research
---

# OfficeQA: Treasury Auction Tenders & Foreign-Investor Breakdown

Some questions ask about a SPECIFIC Treasury security offering identified by
tenor + maturity date (e.g. "the 2-year U.S. Treasury notes maturing at the end
of July 1984"). They want auction-results figures: total dollar value of bids
(tenders) submitted, and a sub-share such as "noncash rollover tenders accepted
submitted on behalf of foreign investors."

## Where the data lives
- Section: **Treasury Financing Operations** (the auction/offering results tables),
  NOT the "Average Yields" or "Maturity Schedule" tables.
- Each offering has its own results block keyed by the AUCTION/ISSUE, but the
  question identifies it by **maturity date + tenor** ("2-year ... maturing end
  of July 1984"). Match the row whose stated maturity is that date. A 2-year note
  maturing Jul 1984 was issued ~Jul/Aug 1982 — but you index by the maturity the
  question gives, not the issue date.
- The bulletin reporting it is typically the one covering the auction month
  (issue month), so search bulletins around the issue period, not the maturity.

## Terminology decode (the non-obvious part)
- "total dollar value of bids submitted" = **total tenders received/submitted**
  for that offering (the gross "Tenders" or "Total subscriptions/bids" figure),
  in whole dollars. Example value seen: 10,102,000,000.
- "noncash rollover tenders" = rollover/exchange tenders that are NOT new cash —
  reinvestment of maturing holdings. The table separates **cash** vs **noncash
  (rollover/exchange)** tenders.
- "on behalf of foreign investors" / "global non-domestic investors" = the
  **foreign and international / official foreign** sub-line (often a "Foreign and
  international" or "On behalf of foreign and international monetary authorities"
  row, or a federal-reserve-as-agent-for-foreign-accounts line).
- The 2nd answer = (foreign noncash rollover tenders ACCEPTED) / (total bids
  submitted) × 100, to hundredths. "Accepted" matters — use the accepted column,
  not the submitted column, for the numerator if both exist. Denominator is the
  total SUBMITTED bids from sub-question 1.

## Output
- Bracketed CSV in sub-question order: `[<total_bids_whole_dollars>, <pct>]`.
- Round sub-Q1 to nearest nominal dollar; sub-Q2 percent to hundredths
  (0.0473 -> 4.73).
- PASSED: 2-yr notes maturing end of Jul 1984 = [10102000000, 4.73].

## Pitfalls
- Don't confuse with the maturity-schedule or yield tables — this is the
  auction RESULTS table.
- Whole dollars, not millions/billions, for the bids figure — these tables list
  full dollar amounts (e.g. 10,102,000,000 not 10,102).
- Read submitted vs accepted carefully: denominator usually "submitted",
  numerator for the share usually the "accepted" foreign noncash line.
