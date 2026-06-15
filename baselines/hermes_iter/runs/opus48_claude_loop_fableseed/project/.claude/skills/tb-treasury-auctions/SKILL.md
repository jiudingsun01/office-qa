---
name: tb-treasury-auctions
description: Use for Treasury Bulletin questions about the results of a Treasury debt AUCTION/offering — (a) average discount RATES on new bill issues (weekly 91-day bills, and irregular-tenor cash-management bills like 2-day/19-day), often aggregated over a month or years; and (b) the TENDER/ALLOTMENT detail of a specific NOTE or BOND auction (total bids submitted vs accepted, competitive vs noncompetitive, cash vs rollover/noncash, foreign/international vs domestic). For per-security secondary-market PRICES use tb-security-price-volatility; for yields-vs-corporate use tb-bond-yields.
---

# Treasury Bulletin: auction / financing-operations results

Two recurring sources cover new-issue auctions:
- **"Offerings of Treasury Bills"** (market/ownership section, toward the back): the weekly bill table.
- **"Treasury Financing Operations"** (narrative section near the FRONT): cash-management bills AND note/bond subscription-allotment writeups. Covers roughly the 2–3 months before publication.

---

## A. Weekly Treasury bill offering (auction) discount rates

- The recurring table ("Offerings of Treasury Bills" / "Treasury bills offered and tenders accepted") has one row per weekly auction: **date of issue**, amount tendered/accepted, and the **average rate of discount** on accepted tenders (percent per annum, ~3 decimals, e.g. 1.876).
- In the 1950s the regular weekly bill is the **91-day bill, issued on Thursdays** (occasionally shifted by a holiday). "The average rate reported on the Thursday of each week" = the average discount rate of the bill **issued (dated) that Thursday** — match rows by issue date, not announcement/auction date.
- Coverage: each issue's table lists the most recent ~3 months of auctions. To cover one calendar month across several years, pull one issue per year (an issue dated 1–3 months after the target month).

### "All weekly bills issued in month M across years Y1–Yn"
1. For each year, enumerate the actual **Thursdays falling in month M** (compute the calendar — some months have 4 Thursdays, some 5; do NOT assume 4). Each Thursday = one bill issue = one rate.
2. Extract the average discount rate for every such issue date. Expect n_years × (4 or 5) values; count them explicitly before aggregating.
3. Distinguish the **average rate** column from the high/low accepted-price or coupon-equivalent columns.

### Geometric mean of rates
- GM = (r1 × … × rk)^(1/k) = exp(mean(ln r)). Compute with a script — close to but not equal to the arithmetic mean.
- Use the rates in percent as printed (1.876, not 0.01876). Round only the final result.

### Cash-management bills (irregular short tenors: 2-day, 19-day, etc.)
- NOT in the regular weekly table. They are in the **"Treasury Financing Operations"** narrative, which states per operation: tenor (days), the **date tenders were opened** (auction date), issue/maturity dates, amount raised, and the **average bank discount rate** (percent per annum).
- Match operations by the **tender-opening date** when the question gives one ("tenders opened on May 27, 1980"), not by issue/maturity date — for very short bills these differ by only days.
- Very short tenors carry unusual-looking annualized rates (a 2-day bill can print far from the 13-week rate) — use as printed; don't "sanity-correct."

### Bill-rate pitfalls
- Don't grab the secondary-market yield table ("Market quotations on Treasury securities") — the question is about NEW issues at auction.
- Don't include bills DATED in adjacent months even if auctioned in month M, or special/tax-anticipation bill issues mixed into the table.
- A 5-Thursday month silently breaks an assumed-4 extraction; the wrong count changes both the product and the 1/k exponent.

---

## B. Note/bond tender & allotment detail

### Identify the right auction from the maturity
- A security described by tenor + maturity (e.g. "**2-year notes maturing at the end of July 1984**") was ISSUED one tenor-length earlier: 2-year → issued ~end of **July 1982**. Look in the Bulletin published shortly AFTER the issue date (financing-operations writeups lag publication ~1–2 months), so a July 1982 issue appears in the Aug/Sep 1982 Bulletin.
- Match by issue/maturity date, not announcement or auction date.

### Where the data lives
- The detailed allotment table is in the **"Treasury Financing Operations"** section near the FRONT (same section as cash-management bills), as a per-offering subscription/allotment breakdown — NOT in the back ownership/market tables.
- For each coupon offering it tabulates **tenders received** ("bids submitted") and **tenders accepted**, typically split into:
  - **Competitive** vs **noncompetitive** tenders;
  - **Cash** tenders vs **noncash / rollover (exchange)** tenders — rollovers are holders of a maturing issue exchanging into the new one;
  - bidder categories often including a **foreign / international** line distinct from domestic/public.

### Answering
- "**Total dollar value of bids submitted**" = the **total tenders received/submitted** figure (the larger number), NOT tenders accepted. Read the column label — "submitted/received" vs "accepted".
- A "**percent of these were [sub-category]**" question = (the specific sub-category line) ÷ (the total-bids-submitted figure) × 100. Keep numerator and denominator the same kind (e.g. a *noncash rollover, foreign, accepted* line over *total bids submitted*).
- Watch the scale label: financing-operations amounts are usually in **millions** or **thousands** of dollars. If the question wants **nominal dollars**, multiply out (e.g. $10,102 million → 10,102,000,000) and round as instructed.
- Percent formatting: if asked "decimal 0.1234 → 12.34", multiply the ratio by 100 and round to the requested places.
