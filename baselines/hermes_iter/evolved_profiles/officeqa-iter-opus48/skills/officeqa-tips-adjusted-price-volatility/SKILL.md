---
name: officeqa-tips-adjusted-price-volatility
description: OfficeQA Treasury Bulletin — "price volatility" (population standard deviation) of a TIPS (Treasury Inflation-Protected Security) of a given coupon (e.g. 2-3/8% / 2⅜%) over a date window, using "adjusted price accounting for inflation / index ratios". The data is NOT a daily/monthly index-ratio price series — it is the AUCTION-results table PDO-2 ("Public Debt Operations"), where column 6 ("Accepted yield and equivalent price") already holds the inflation-ADJUSTED equivalent price for TIPS rows. Select the TIPS rows matching the coupon whose auction/issue date falls in the window, then pstdev. PASSED 2-3/8% TIPS Jan1-Aug1 2007 = 0.900544.
---

# OfficeQA — TIPS adjusted-price volatility (Table PDO-2)

## When this fires
Question phrasing like: "price volatility (measured in terms of population standard
deviation) for securities classified <coupon>% U.S. Treasury Inflation-Protected
Security with a coupon rate of <coupon> between <date1> and <date2>. Use adjusted
price accounting for inflation / index ratios."

Key signals: "Inflation-Protected Security" / "TIPS", explicit coupon (e.g. 2⅜% =
2-3/8% = 2.375%), a date window, "adjusted price" / "index ratios", "population
standard deviation". Hint page is usually the PDO-2 page (e.g. ~p.53 in the Dec 2007
bulletin, which is printed page 45).

## The trap (do NOT chase the wrong table)
There is NO separate daily/monthly "Index Ratios for Inflation-Protected Securities"
table in the Bulletin to build a price time-series from. Searching for "Index Ratio",
"Reference CPI", "Adjusted principal" finds nothing useful. Both prior solves wasted
~8-10 calls hunting for it. STOP looking — the answer lives in the auction table.

## The right source: Table PDO-2 (Public Debt Operations)
PDO-2 is a cumulative fiscal-year auction-results table. Each auctioned issue is a row.
Column 6 header is roughly "Accepted yield and equivalent price for notes and bonds".
For TIPS rows, the "equivalent price" printed there is the INFLATION-ADJUSTED equivalent
price (= unadjusted price × index ratio). Confirm via the auction narrative when present,
e.g. Jul 24 2007: unadjusted 96.580051 × index ratio 1.03096 = 99.570169 = the PDO-2
column-6 value. So PDO-2 column 6 IS the "adjusted price accounting for index ratios"
the question wants. No further multiplication needed.

## Procedure
1. `grep -n` the markdown for the coupon and "Inflation"/"Protected"/"TIPS". The
   search_files tool sometimes returns 0 hits on these pages due to encoding of the
   ⅜ glyph / mangled parse — fall back to terminal `grep -n` on the .md, and if still
   thin, go straight to the PDF.
2. Open the PDO-2 page(s) in the PDF:
   `pdftotext -layout -f <p> -l <p> <pdf> -`  (sweep a few pages around the hint).
   Identify rows whose security description is "<coupon>% TIPS—<maturity>" (multiple
   maturities/reopenings can share the coupon).
3. Filter to rows whose auction date OR issue date falls inside [date1, date2]. In
   practice all matching rows fall in the window under either convention — if auction
   and issue dates land on the same side of both bounds, you don't need to disambiguate.
4. Collect the column-6 equivalent (adjusted) prices for those rows. Example
   (2-3/8% TIPS, Jan 1 – Aug 1 2007):
     - 2-3/8% TIPS—01/15/17-A, 01/16/07 → 99.342280
     - 2-3/8% TIPS—01/15/27,   01/31/07 → 99.213485
     - 2-3/8% TIPS—01/15/17-A, 04/16/07 → 101.434007
     - 2-3/8% TIPS—01/15/27,   07/31/07 → 99.570169
5. Population standard deviation (statistics.pstdev, divide by N not N-1):
     pstdev([99.342280, 99.213485, 101.434007, 99.570169]) = 0.900544
   Round to the requested decimals (here 6).

## Pitfalls
- "population standard deviation" = pstdev (÷N). Do NOT use sample stdev (÷N-1).
- Select by COUPON, not by maturity — both 01/15/17-A and 01/15/27 issues are 2-3/8%
  and both count. Different coupons in the window are excluded.
- Reopenings ("-A") are separate auction rows and count as separate price observations.
- Column 6 is already adjusted for TIPS; do NOT multiply by an index ratio again.
- The auction narratives for issues earlier in the year live in EARLIER-quarter
  bulletins, but the cumulative PDO-2 table in the year-end (Dec) bulletin already
  lists all of them — you only need that one table.
