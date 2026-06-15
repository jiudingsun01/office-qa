---
name: maturity-schedule-fixed-vs-callable-marketable
description: OfficeQA Treasury Bulletin — the "Maturity Schedule of Interest-Bearing Public Marketable Securities" table. Distinguish FIXED-MATURITY-TYPE issues from CALLABLE issues; do NOT use the grand total. Amounts in $ millions -> scale to billions. Used for OLS projection across yearly bulletins.
category: research
---

# Maturity Schedule: "fixed maturity type" vs "callable" marketable securities

## Trigger
Q mentions "interest-bearing public marketable securities ... of **fixed maturity
type**" (or "callable type") "as of the maturity schedule published on the last
day of <Month> of each year YYYY-YYYY", often asking to fit OLS and project the
next year. 1940s-1950s bulletins.

## THE TABLE (don't confuse with neighbors)
Treasury Bulletin table titled **"Maturity Schedule of Interest-Bearing Public
Marketable Securities Issued by the United States Government"**. It lists, by
maturity-date bucket, the amounts outstanding. Crucially the securities are
SPLIT INTO TWO TYPE CLASSES, each with its own subtotal:
- **Fixed maturity** issues (a single fixed redemption date), and
- **Callable** issues (redeemable on/after a first call date, before final
  maturity — printed as a date RANGE, e.g. "1967-72").

The table also shows a **GRAND TOTAL** of all marketable issues. THAT GRAND
TOTAL (~$150-160B in 1948-1951) IS NOT THE ANSWER when the Q says "fixed
maturity type." You want only the FIXED-MATURITY subtotal.

## THE FAILURE (this is why this ref exists)
Q: fixed-maturity marketable amount (billions) on last day of Jan 1948,1949,
1950,1951; OLS-project end-Jan-1952. Gold = **[redacted]**. I answered **57.0** —
a strongly RISING projection. Root cause: wrong rows. The fixed-maturity
subtotal in this era is FLAT-TO-DECLINING (~$40-45B falling to ~$39B), because
the postwar debt was concentrated in long callable issues + bills/notes, and
fixed-maturity bonds were being refunded/retired. A rising 57.0 means I either
(a) summed fixed+callable, (b) grabbed the grand total slope, or (c) picked a
different growing aggregate (total marketable, or "issued during period").

## CONFIRMED READING THAT REPRODUCES GOLD [redacted] (1948-1951 Jan, fixed, OLS->1952)
The "fixed-maturity value" per schedule = the **Total of the "Fixed maturity
issues" column for that schedule's OWN calendar-year group** (the first/nearest
year-group at top-left, which lumps that year's bills+certs+fixed bonds). Do NOT
sum the Fixed column across ALL maturity-year groups (that gives ~48-57B RISING
-> wrong 54.7 projection, the classic trap).
Confirmed reads ($ millions, Jan 31 schedule, current-year group Total):
- 1948: 46,615   1949: 36,068   1950: 44,467   1951: 40,537
-> /1000 = 46.615, 36.068, 44.467, 40.537
np.polyfit([1948..1951], values, 1) -> proj 1952 = 39.46 -> **[redacted]** (matches gold).
Pages: 1948 p19, 1949 p19, 1950 p21, 1951 p22 (cover-month bulletin, March issue).
Render at -r 250 and read with vision; pdftotext scrambles these grids.

## SANITY CHECKS BEFORE SUBMITTING
1. The fixed-maturity subtotal for late-1940s/early-1950s should be roughly
   **$38-46 billion** per year and TRENDING DOWN slightly. If your four values
   are all >$50B or RISING, you almost certainly used callable+fixed or the
   grand total. Re-pull only the FIXED-maturity-type subtotal.
2. A linear projection of a flat/declining series must land NEAR the last
   observed value, not far above it. [redacted] ≈ continuation of a gentle decline.
   If your projection is well above every input year, the slope sign is wrong
   for the series the Q named — recheck the rows.
3. Callable issues are identifiable by a DATE RANGE in the maturity column
   ("1967-72", "1956-58"). Fixed issues show a SINGLE date. Subtotal only the
   single-date (fixed) group, OR read the explicitly labeled
   "Total — fixed maturity" line if present.

## Units
Amounts print in **millions of dollars**; the Q wants **billions** -> divide by
1000 before regression (e.g. 39,500 -> [redacted]). Round per the Q (here tenths).

## Reading method
1940s-50s maturity-schedule pages are dense multi-column grids; pdftotext often
scrambles them. Render and read with vision:
`pdftoppm -r 300 -png -f P -l P <pdf> /tmp/mat` then vision_analyze, and read
the line labeled as the fixed-maturity subtotal for each year's bulletin.
The "published on the last day of January" wording means use the maturity
schedule dated Jan 31 of that year — typically appears in the FEBRUARY or
month-after bulletin, or in a Jan-dated schedule. Match the schedule DATE, not
the bulletin's cover month.

## Variant: "amount scheduled to mature IN calendar year Y" (NOT fixed/callable)
Some Qs don't ask for the fixed/callable type split at all. Instead: "the total
amount of interest-bearing marketable public debt scheduled to mature in that
calendar year, as reported in the maturity schedule outstanding at the end of
<Month> for each year YYYY-YYYY." Here you read ONE NUMBER per bulletin: the
GRAND-TOTAL row of the maturity bucket corresponding to that calendar year, from
the schedule dated end-of-<Month> of that same year.
- "end of February for each year" -> use the Feb-dated schedule (appears in the
  Feb or Mar bulletin). Match schedule DATE to cover month per the Q.
- The bucket is the calendar-year maturity row (e.g. for year 1972, the row of
  securities maturing during 1972). Take the TOTAL across both fixed+callable
  for that year's maturities — this variant wants the all-securities total
  maturing in the year, NOT a type subtotal. (Confirmed CORRECT on the
  1972-1976 z-score question.)
- Amounts in $ millions; this variant often keeps them in millions (no billions
  scaling) — follow the Q's stated unit.

## Z-score / "how many sample standard deviations off the average" mechanic
When the Q asks "how many sample standard deviations off the N-year sample
average was year T's value":
- z = (value_T - mean) / sample_stddev, where sample_stddev uses ddof=1
  (n-1 denominator), NOT population stddev (ddof=0). "SAMPLE standard deviation"
  is explicit — numpy default ddof=0 is WRONG; use `np.std(arr, ddof=1)` or
  statistics.stdev().
- The result is SIGNED. If year T is below the mean, answer is NEGATIVE. Don't
  drop the sign. (1972 total below the 5-yr mean -> [redacted], CORRECT.)
- Round to the requested decimals at the very end only.

## Regression mechanics
Same as other OLS refs: x = year (or 1..4, projection is index-base invariant),
y = the four fixed-maturity billions values, `numpy.polyfit(x,y,1)`, predict the
next year. numpy not importable in execute_code sandbox -> run via
`cd /home/azureuser/office-qa && python3 script.py`.
