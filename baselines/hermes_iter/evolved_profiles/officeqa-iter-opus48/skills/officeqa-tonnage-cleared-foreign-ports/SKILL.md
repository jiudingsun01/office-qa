---
name: officeqa-tonnage-cleared-foreign-ports
description: OfficeQA Treasury Bulletin — the "Tonnage of Vessels Cleared from the United States for Foreign Ports" (American vessels vs Foreign vessels vs Grand Total) shipping table found in early-1940s bulletins. Covers locating it, the "single percentage point difference" phrasing, and Pearson correlation on the short monthly series.
category: research
---

# OfficeQA: Tonnage Cleared from the U.S. for Foreign Ports

A distinct table family in early-1940s (WWII-era) Treasury Bulletins, unrelated
to the budget/balance-sheet tables. It reports **net registered tonnage (in
thousands of tons)** of vessels ENTERED and CLEARED in U.S. foreign trade, split
by flag:

- **American vessels**
- **Foreign vessels**
- **Grand total** (= American + Foreign)

Rows are by **calendar month** (Jan, Feb, Mar, ...). Watch the ENTERED vs
CLEARED distinction — there are usually two parallel sub-tables; pick the one the
question names ("cleared from the United States for foreign ports" = CLEARED).

PASSED first try: Jan/Feb/Mar 1941, "% of total cleared tonnage attributed to
American vessels" + Pearson r(American, Grand Total) → gold [34.4, 0.391].

## Locating the table
- It lives in the **commerce / merchant-marine statistics** part of the bulletin
  (not the budget section). Index by the phrase "tonnage of vessels" or
  "cleared from the United States."
- The text layer for these dense grids can garble columns. If `pdftotext -layout`
  produces misaligned numbers, `pdftoppm -r 300` the page and VISION-read the
  Jan/Feb/Mar rows for the American + Grand Total columns.
- Values are already "in thousands of tons" — do NOT rescale; the question
  asks for a percentage and a correlation, both unit-free.

## "Single percentage point difference" phrasing
The question wanted "what percentage of the total ... was attributed to American
vessels ... as the single percentage point difference rounded to one decimal."
This is a slightly clumsy way to ask for ONE percentage figure:

    pct = American_total(Jan+Feb+Mar) / GrandTotal(Jan+Feb+Mar) * 100

i.e. SUM the three months for American, SUM the three months for Grand Total,
divide, ×100, round to 1 decimal → 34.4. ("percentage point difference" here is
just the share itself; it is NOT (American − Foreign). Confirm by sanity check:
American share of a 3-flag mix in 1941 plausibly ~30-35%.)

## Pearson correlation on the 3-month series
Second value = Pearson r between the American-vessels monthly series and the
Grand-Total monthly series across the SAME three months (n=3):

    series_A = [Amer_Jan, Amer_Feb, Amer_Mar]
    series_G = [Grand_Jan, Grand_Feb, Grand_Mar]
    r = pearson(series_A, series_G)   # numpy.corrcoef / scipy.stats.pearsonr

Round to nearest thousandth → 0.391. With n=3 the correlation is volatile; it is
NOT forced to be near 1 even though Grand Total includes American (Foreign
vessels co-vary and can dominate month-to-month swings). Compute it literally
from the three pairs — do not assume ~1.0.

## Output format
Two values, comma-separated, in square brackets, first = percentage (1 dp),
second = correlation (3 dp): `[redacted]`.

## Pitfalls
- ENTERED vs CLEARED: wrong sub-table = wrong numbers entirely.
- Use the GRAND TOTAL row, not "Foreign vessels", as the denominator/second series.
- Sum the months BEFORE dividing for the percentage (don't average monthly
  percentages).
- n=3 Pearson: keep full-precision tonnage values through corrcoef, round only
  the final r.
