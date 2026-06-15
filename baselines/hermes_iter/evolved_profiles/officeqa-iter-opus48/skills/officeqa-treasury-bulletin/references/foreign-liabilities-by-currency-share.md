# Liabilities to Foreign Countries BY CURRENCY of denomination — SHARE across year-ends, pick MAX/MIN

## When this applies
Q asks for the "share of <CURRENCY> dollar/denominated liabilities out of TOTAL
liabilities to foreign countries by the U.S." over a span of CALENDAR-YEAR-END
reported values (e.g. 2009-2011 inclusive), then asks for the MAX (or min) of
those per-year shares, as a DECIMAL (0.1234 form, not percent). Worked: max CAD
share of total foreign liabilities, CY-ends 2009/2010/2011 -> [redacted] (gold [redacted]).

This is the CURRENCY-DENOMINATION breakdown — NOT the by-COUNTRY breakdown
(see capital-movements-liabilities-by-country-fx-convert.md for that, which is a
different table). Here the rows are CURRENCIES (U.S. dollar, Canadian dollar,
euro, yen, pound, Swiss franc, "other") and the denominator is the grand TOTAL.

## Where the data lives
- International Financial Statistics / "Liabilities to Foreign Countries"
  section of the modern Treasury Bulletin. The relevant table breaks the U.S.
  Treasury's foreign liabilities down BY CURRENCY of denomination, with a row
  for "Total" and a row per foreign currency.
- Each column is a CALENDAR-YEAR-END snapshot (Dec 31). Pull the SAME year-end
  column. A single bulletin often shows several recent year-ends side by side,
  so 2009, 2010, 2011 may all be in ONE later-issue table — but verify each, and
  if not present, pull each year-end from its own bulletin issue.
- Amounts are in MILLIONS USD. The share is unitless, so scaling cancels — just
  use raw millions for both numerator and denominator.

## The arithmetic
For each year-end Y in the inclusive span:
  share_Y = (Canadian-dollar liabilities cell) / (Total liabilities cell)
Then answer = MAX(share_2009, share_2010, share_2011), as a DECIMAL.
Round to the requested places (here nearest thousandths -> [redacted]).

The non-USD currency shares are TINY (CAD ~0.5% = [redacted]). At thousandths
rounding the answer can be a very small decimal; do NOT report as a percent
(0.5 would be wrong — the Q's own example maps 12.34% -> 0.1234, so a 0.5% share
is [redacted]). Keep numerator/denominator both in the SAME currency-of-report (USD
millions) — these tables report all currency-denominated liabilities CONVERTED
to USD already, so no FX conversion is needed.

## Pitfalls
- DECIMAL vs percent: the share is a ratio in [0,1]. [redacted] NOT 0.5. The Q always
  restates "if 12.34 is percent, 0.1234 is decimal" — obey it.
- Denominator = the GRAND "Total" liabilities row, not a regional/country
  subtotal and not the USD-denominated subtotal.
- "calendar year end" = Dec 31 column, not a quarter or monthly figure.
- MAX across the years means compute all per-year shares first, then take the
  largest — do not assume the latest or earliest year is the max.
- Scaling cancels in a ratio, so ignore millions-vs-billions here.
