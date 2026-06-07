---
name: treasury-bulletin-marketable-debt-maturity-schedules
description: Use for OfficeQA/Treasury Bulletin questions asking about Treasury/public debt maturity schedules outstanding at a month-end, especially total interest-bearing marketable public debt securities scheduled to mature in specific calendar years.
---

# Treasury Bulletin marketable debt maturity schedules

Use this skill when the prompt mentions `maturity schedules`, securities `scheduled to mature`, or public debt securities outstanding at a specific month-end (e.g. `at the end of February`) and asks for totals by calendar year.

## Locate the source table

1. Use the Treasury Bulletin issue for the same year/month as the stated reporting date. For `outstanding at the end of February 1974`, use the maturity schedule printed for February 1974, not a later annual summary unless the prompt explicitly says so.
2. Search within the Public Debt section for table titles/phrases such as:
   - `Maturity distribution and average length of marketable interest-bearing public debt securities`
   - `Maturity schedule of interest-bearing marketable public debt securities`
   - `Securities outstanding at end of month`
   - `maturing in calendar year`
3. Prefer the table whose header states the required outstanding date (`end of February`, `February 28`, etc.). These schedules are date snapshots; do not substitute schedules from January/March or fiscal-year-end tables.

## Reading the maturity-year totals

1. Use the row/line for the total amount of `interest-bearing marketable public debt securities` or `Total marketable public debt securities` scheduled to mature in the calendar year requested.
2. If the prompt says the securities are `of fixed maturity type` (common in 1940s/early-1950s schedules), do NOT use the grand total for all marketable securities. Use the `fixed maturity` / `Total fixed maturity issues` amount from the maturity schedule snapshot. Older tables separate fixed-maturity securities from callable/other maturity categories; the fixed-maturity line is the requested stock.
3. Do not use offering/auction tables, bids, tenders, or issue amounts; this is an outstanding-stock maturity schedule.
4. The table unit is typically `millions of dollars`. Convert to `billions` only if the prompt asks for billions or the regression target is reported in billions; otherwise keep values in millions when the statistic only compares values (mean, SD, z-score), since scaling cancels.
5. Match the column/calendar-year label literally. For a question about `calendar years 1972 through 1976 inclusive`, collect the five maturity-year totals from the end-of-February schedule(s) as printed for those years.
   - If the wording is `for calendar years 1972 through 1976 ... as reported in the maturity schedules outstanding at the end of February for each year`, this means a rolling same-year snapshot series: take the amount maturing in 1972 from the end-February 1972 schedule, the amount maturing in 1973 from the end-February 1973 schedule, and so on. Do not take the 1972-1976 maturity-year columns from a single February schedule.
6. Watch for continuation pages: row labels may be on the left page and the year columns on a right/continued page. `pdftotext -layout` usually preserves the grid; if columns wrap, inspect/crop the pages around the Public Debt maturity schedule.

## Snapshot time-series / projection questions

1. If the prompt asks for values `as of` the maturity schedule published on a date in several calendar years (for example, `last day of January of each calendar year from 1948-1951`), build a time series from the same schedule snapshot date in each issue (Jan. 31, 1948; Jan. 31, 1949; etc.). Do not instead read maturity-year columns inside a single schedule, and do not use the issue date as an issue/offering amount.
2. For older 1940s/early-1950s prompts asking for `interest-bearing public marketable securities issued by the United States Government ... of fixed maturity type`, take the total stock line/subtotal for `Fixed maturity` (or `Total fixed maturity issues`) within the `issued by the United States Government` section of the maturity schedule. Do not use the overall/grand total of all interest-bearing marketable public securities, and do not include guaranteed securities, callable/perpetual categories, or nonmarketable debt unless the prompt explicitly asks for them. This grand-total-vs-fixed-maturity confusion can materially overstate projections (e.g. a 1948-1951 January fixed-maturity OLS projection should be around 39.5 billion, while using the broader total can produce about 57.0).
3. For OLS projection to the next year, regress the requested stock amount against the calendar year (or equivalently against 0,1,2,...; predictions are identical if used consistently), then evaluate at the next calendar year. Round only the final projection to the requested precision.

## Statistics and rounding

1. For `sample standard deviations off the sample average`, compute
   - `mean = sum(x) / n`
   - `s = sqrt(sum((x_i - mean)^2) / (n - 1))`
   - requested standardized value = `(target_value - mean) / s`
2. Use sample standard deviation (`n-1`), not population SD (`n`).
3. Preserve signs: if the target year is below the average, the standardized value is negative.
4. Round only the final standardized value to the requested decimals (commonly three decimals). Do not round intermediate mean or SD unless the prompt explicitly requires it.

## Verification checklist

Before answering, verify:

1. the schedule date matches the prompt's `outstanding at end of ...` date;
2. the entries are maturity-year totals for marketable interest-bearing public debt, not auction proceeds;
3. values are all in the same printed unit;
4. the target value (e.g. the 1972 maturity total) is included in the same 5-year sample used for the mean/SD;
5. sample SD uses denominator `n-1` and the final sign is correct.
