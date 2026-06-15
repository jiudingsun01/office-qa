---
name: officeqa-monthly-outlays-by-function-pstdev
description: OfficeQA Treasury Bulletin — compute the POPULATION standard deviation (or mean/dispersion) of a 12-month series of MONTHLY nominal federal net OUTLAYS (or receipts) "by function" in $ millions for a fiscal year. Covers building the monthly series from the by-function outlay table (sum the function rows within each month to get that month's total net outlays), the population (÷N) std convention, and where the monthly outlays-by-function table lives. PASSED FY1981 monthly net outlays pstdev = 2760.44.
---

# Monthly net outlays "by function" — population std dev over a fiscal year

## When this applies
Question asks for the population standard deviation (or mean, variance, range) of
"monthly nominal federal U.S. Government net outlays by function" (or receipts by
function/source) over a stated FISCAL YEAR **or CALENDAR YEAR (CYxxxx)**, returning
$ millions. READ THE YEAR FRAMING CAREFULLY — "CY1981" means the 12 months
Jan–Dec 1981; "FY1981" means Oct 1980 – Sep 1981. Same table, DIFFERENT 12 months,
substantially different answers (CY1981 pstdev = [redacted] vs FY1981 = 2760.44).
Often phrased
"include all of these monthly values in one place" — a hint to use the single
bulletin table that lists all 12 months in columns.

## Data source
- The table is the federal **budget receipts and outlays BY FUNCTION** broken out
  by month (12 monthly columns + often a fiscal-year-total column). In modern
  bulletins this is the "Budget Results" / Monthly Treasury Statement-derived
  "Summary of Receipts and Outlays" area; the by-function/by-major-function outlay
  schedule shows National defense, International affairs, Health, Income security,
  Net interest, etc., as rows and the 12 months as columns.
- "Use the LATEST treasury bulletin table" = pick the bulletin that reports the
  FULL fiscal year (typically the Oct/Nov bulletin after FY-end, or a later-year
  bulletin that still prints that FY's complete 12-month row). Prefer the most
  recent bulletin containing the complete 12-month series for that FY.

## Build the series (the key step)
You need ONE total-net-outlays number per month (12 values), then take the stat.
- If the table gives a **"Total outlays" (or "Total net outlays") ROW** per month,
  read those 12 monthly totals directly. Use that row — do NOT re-derive.
- If the table only gives by-function detail with NO monthly total row, SUM all the
  function rows within EACH month to get that month's total net outlays (12 sums).
- **CALENDAR year (CYxxxx)** = the 12 months Jan–Dec of that year. You will likely
  need TWO bulletins: the monthly outlays tables print a fiscal-year window, so
  Jan–Sep of CY1981 come from the FY1981 table and Oct–Dec 1981 come from the
  FY1982 table. Assemble all 12 calendar months before computing.
- **FISCAL year (FYxxxx)** = Oct (prior calendar year) … Sep. Grab the 12 months
  Oct–Sep, not Jan–Dec, and do NOT include the FY-total column as a 13th value.

## Compute
- "population standard deviation" => divide by N (=12), NOT N-1 (sample).
  `statistics.pstdev(values)`. Sample stdev is the dominant failure mode here.
- Round to the requested places (usually hundredths).

## Pitfalls
- CONFUSING CY vs FY. "CY1981" = Jan–Dec 1981; "FY1981" = Oct 1980–Sep 1981.
  The two share only Jan–Sep 1981. Different answers. Re-read the year prefix.
- Accidentally including the FY-total column -> 13 values.
- Using sample std (÷N-1) when "population" is requested.
- Double counting if both a "Total outlays" row AND function rows are summed.

## Verified
- FY1981 monthly nominal federal net outlays, population std dev = 2760.44 (PASSED).
- CY1981 (Jan–Dec 1981) monthly nominal federal net outlays, population std dev
  = [redacted] (PASSED).
