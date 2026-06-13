---
name: tb-bill-auction-rates
description: Use for Treasury Bulletin questions about rates on NEW Treasury bill issues — weekly bills (e.g. 91-day) with average discount rates per auction/issue week, often aggregated (mean/geometric mean) over a month or years, AND cash management bills (irregular short tenors like 2-day, 19-day) reported under "Treasury Financing Operations".
---

# Treasury Bulletin: weekly Treasury bill offering (auction) rates

## Where the data lives
- Each Bulletin issue has a recurring table in the market/ownership section titled like **"Offerings of Treasury Bills"** / "Treasury bills offered and tenders accepted". One row per weekly auction, with columns for the **date of issue**, amount tendered/accepted, and the **average rate of discount** on accepted tenders (percent per annum, printed to ~3 decimals, e.g. 1.876).
- In the 1950s the regular weekly bill is the **91-day bill, issued on Thursdays** (occasionally shifted a day by a holiday). "The average rate reported on the Thursday of each week" = the average discount rate of the bill **issued (dated) that Thursday** — match rows by issue date, not by auction/announcement date.
- Coverage: each issue's table lists the most recent ~3 months of auctions. To cover one calendar month in each of several years, pull one issue per year (an issue dated 1–3 months after the target month, e.g. the Oct/Nov/Dec issue for September data).

## Procedure for "all weekly bills issued in month M across years Y1–Yn"
1. For each year, enumerate the actual **Thursdays falling in month M** (compute the calendar — some months have 4 Thursdays, some 5; do NOT assume 4). Each Thursday = one bill issue = one rate.
2. Extract the average discount rate for every such issue date. Expect n_years × (4 or 5) values; count them explicitly before aggregating.
3. Distinguish the **average rate** column from the high/low accepted-price or coupon-equivalent columns if present.

## Geometric mean of rates
- Geometric mean = (r1 × r2 × … × rk)^(1/k), or exp(mean(ln r)). Compute with a script/explicit arithmetic, not by eyeballing — with rates clustered near each other it is close to, but not equal to, the arithmetic mean.
- Use the rates as printed in percent (e.g. 1.876, not 0.01876) — the answer is expected in the same percent units.
- Round only the final result to the requested precision (thousandths → 3 decimals).

## Cash management bills (irregular short tenors: 2-day, 19-day, etc.)
- Cash management bills are NOT in the regular weekly "Offerings of Treasury Bills" table. They are described in the **"Treasury Financing Operations"** section — the narrative/summary of recent financings near the FRONT of each Bulletin issue — which states, per operation, the bill's tenor (days), the **date tenders were opened** (the auction date), the issue/maturity dates, amount raised, and the **average bank discount rate** (percent per annum).
- Match operations by the **tender-opening date** when the question gives one ("tenders opened on May 27, 1980"), not by issue or maturity date — for very short bills these differ by only days and are easy to confuse.
- The Financing Operations narrative in an issue covers roughly the 2–3 months before publication, so a 6/1980 issue covers May–early-June 1980 operations.
- Very short tenors carry unusual-looking annualized rates (a 2-day bill can print a rate far from the contemporaneous 13-week rate) — don't "sanity-correct" them; use as printed.

## Pitfalls
- Don't grab the secondary-market yield table ("Market quotations on Treasury securities") — the question is about NEW issues at auction.
- Don't include bills DATED in adjacent months even if auctioned in month M, or special/tax-anticipation bill issues mixed into the table — only the regular weekly bills whose issue date falls in month M.
- A 5-Thursday month silently breaks an assumed-4 extraction; the wrong count changes both the product and the 1/k exponent.
