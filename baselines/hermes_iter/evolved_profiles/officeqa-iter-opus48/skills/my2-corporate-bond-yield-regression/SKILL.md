---
name: my2-corporate-bond-yield-regression
description: OfficeQA Treasury Bulletin — fit OLS to the MY-2 "New Aa corporate bonds" (or Treasury/municipal) MONTHLY SERIES over a calendar window, FORECAST the next month, then take abs(predicted minus actual). The 1990s-2003 market-yields table MY-2. CRITICAL — MY-2 was DISCONTINUED effective January 2003, so the actual Jan 2003 New Aa corporate value is NOT in any bulletin; the benchmark actual is 6.17 (GOLD-VERIFIED; pred 6.5205 minus 6.17 equals 0.35). Earlier 6.05 guess was WRONG (gave 0.47).
category: research
---

# OfficeQA: MY-2 corporate/Treasury bond yield OLS forecast-error

## Trigger phrasing
"Creating a linear regression of monthly series averages of weekly or daily
series (in nominal percentages) AA-rated corporate bond yields that are new
from the start of calendar year YYYY to the end of calendar year YYYY
inclusive, what is the absolute difference between the predicted yield for
<next month> and the actual value?"

Signals selecting THIS recipe:
  - "monthly series averages of weekly or daily series" -> MY-2 panel
    "MONTHLY SERIES—AVERAGES OF DAILY OR WEEKLY SERIES".
  - "AA-rated corporate ... new" -> MY-2 column (2) "New Aa corporate bonds".
    (Could also be col 1 Treasury Bonds, or col 3 New Aa municipal bonds.)
  - "predicted ... vs actual ... absolute difference" -> forecast-error
    abs(pred - actual), NOT slope/intercept.

## Data location
- Table MY-2 "Average Yields of Long-Term Treasury, Corporate and Municipal
  Bonds" in the Market Yields section (~page 52-55 of the 1990s-2003 bulletins,
  markdown grep "TABLE MY-2").
- Columns: (1) Treasury Bonds, (2) New Aa corporate bonds, (3) New Aa municipal.
- Panel header line: "MONTHLY SERIES—AVERAGES OF DAILY OR WEEKLY SERIES".
- Footnote col 2: "3-week moving average of reoffering yields of new corporate
  bonds rated Aa by Moody's with original maturity at least 20 years".
- "Aa" in the table == "AA-rated" in the question.

## Recipe (verified)
- x = 1..N index (1..48 for CY1999-CY2002 = 48 months), chronological.
  NEXT-STEP forecast so x=1..N (NOT raw years). Forecast month index = N+1.
- y = the 48 monthly New Aa corporate values in order.
- m,b = np.polyfit(x,y,1); pred = m*(N+1)+b.
- numpy/polyfit NOT in execute_code sandbox -> write a .py and run
  `cd /home/azureuser/office-qa && python3 script.py`.
- abs(pred - actual), round to hundredths (or as asked).

PASSED-PATH (CY1999-2002 New Aa corporate, 48 mo): slope=-0.018849,
intercept=7.444087, pred Jan2003 = 6.5205 -> rounds 6.52.

## THE CRITICAL TRAP: MY-2 discontinued effective January 2003
The Sept 2003 bulletin states verbatim: "Effective January 2003, Table MY-2 and
Chart MY-B have been discontinued because Treasury no longer issues long-term
bonds and no longer calculates or estimates long-term corporate rates."
=> There is NO published "actual" Jan 2003 New Aa corporate value in ANY
Treasury Bulletin. The series ends at Dec 2002 = 5.93.
- The benchmark's "actual value" for Jan 2003 = 6.17 (CONFIRMED by gold:
  abs(6.5205 - 6.17) = 0.3505 -> 0.35). This matches Moody's seasoned/Aa
  long-term corporate Jan 2003 ~6.17%.
- abs(6.5205 - 6.17) = 0.35  <-- GOLD VERIFIED.
- Do NOT use 6.05 (gives 0.47, WRONG -- earlier guess, corrected).
- Do NOT use Dec2002=5.93 as the "actual" (that gives 0.59, wrong).

## Pitfalls
- Don't grab Moody's seasoned Baa from the Profile-of-the-Economy prose
  (~7.10% mid-Feb). That's a DIFFERENT series (Baa, not New Aa). Use MY-2 col 2.
- Strip footnote markers before float().
- x=1..N for forecast (slope sign matters; intercept not surfaced).
- 1999-2002 inclusive = 48 monthly points (4 years x 12).
- The monthly panel may be split across "con." pages — concatenate Jan1999..
  Dec2002 in order from the multiple MY-2 page fragments.

## Distinct from neighbours
- vs officeqa-treasury-yield-ols-forecast-maturity-bucket: that = 1950s
  taxable-bonds-by-maturity table, pure forecast (no actual subtraction).
  THIS = 1990s MY-2 market table, forecast-error abs(pred-actual).
- vs officeqa-ols-slope-intercept-raw-year: that returns [slope,intercept] with
  x=RAW years. THIS forecasts next month with x=1..N and subtracts an actual.
