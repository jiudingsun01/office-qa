---
name: tb-chained-arithmetic-and-fx
description: Use when a Treasury Bulletin question (a) chains several arithmetic operations in one sentence (forecast → difference → percent → divide by exchange rate → round) or involves exchange rates or "imports under quota" tables, or (b) asks for a statistic computed from table values — CAGR/geometric rate, geometric mean, arc elasticity, standard deviation/volatility, Box-Cox or log transform, or TIPS adjusted prices/index ratios.
---

# Chained multi-step arithmetic + exchange rates + quota tables

A question chaining 6+ operations (MoM increase → naive forecast → YoY
difference → percent of forecast → divide by FX rate → round) was answered
~4.1× too high — exactly the size of the skipped/misapplied final division
by the $/£ rate. Apply the following every time.

## 1. Turn the sentence into an explicit operation checklist FIRST
Before touching any table, rewrite the question as a numbered list of
operations with named intermediates, e.g.:
1. `inc = Feb1939 - Jan1939` (absolute, in pounds)
2. `forecast_Mar1939 = Feb1939 + inc`
3. `actual_Mar1940` (from a later bulletin)
4. `diff = |actual_Mar1940 - forecast_Mar1939|`
5. `pct = 100 * diff / forecast_Mar1939`  ← note the DENOMINATOR the question names
6. `result = pct / fx_rate_1941`
7. round to the requested decimals, format per answer-format skill.

Then execute in order and print every intermediate. After computing, re-read
the question once more and tick off each clause against your list — the most
common failure is silently dropping or reordering one late-stage operation
(especially the final "divide by ..." clause).

### 1b. MANDATORY back-substitution check (this failure happened TWICE)
The checklist above was already in place and a run STILL reported the
percentage instead of percentage/fx_rate. So after writing your candidate
final answer, verify it mechanically, right-to-left:
- `final × fx_rate` must reproduce your `pct` intermediate. If instead
  `final ≈ pct` (within a few %), the FX division was skipped — divide now.
- Run this as actual arithmetic (python/bc), not by eyeballing: print
  `pct`, `fx_rate`, `pct / fx_rate` on one line and confirm the last value
  is the one you are reporting.
- Magnitude anchor for $/£ in 1940–41: the rate is ≈ 4.03 (official
  $4.035 per £ throughout 1941), so the final answer must be ≈ pct/4.
  A final answer in the same ballpark as the percentage itself is wrong.

## 2. Exchange-rate conventions (Treasury Bulletin "Exchange Rates" table)
- The Bulletin's exchange-rate table reports **averages of noon buying rates
  for cable transfers in New York, in U.S. dollars per unit of foreign
  currency**. "U.S. dollar to British pound rate" = dollars per 1 pound —
  a number around **4.0 in 1940–41** (old par was 4.8665), NOT the
  reciprocal (~0.25).
- "Annual average for calendar year YYYY" = the average-of-monthly (or the
  printed annual-average row) for that year; do not use a single month or a
  fiscal year.
- Sanity check after dividing a percentage by the $/£ rate: the result must
  be roughly a quarter of the percentage. If your final answer ≈ your
  percentage (rate ≈ 1) or ≈ 4× smaller/larger than expected, you skipped
  or inverted the division.
- **Converting USD → foreign currency** ("convert from USD to <currency>",
  "USD/XXX exchange rate"): MULTIPLY the dollar amount by the
  foreign-units-per-dollar rate. Since the Bulletin table prints dollars
  per foreign unit, take the reciprocal of the printed rate. Direction
  check: a USD amount converted into a weaker currency must get BIGGER.
  Useful 1950s pegs: Indian rupee = 4.7619 rupees/USD (printed ≈ $0.21 per
  rupee); pound = $2.80 post-1949.
- **If the question says the rate itself is "rounded to the nearest
  hundredths place", round the RATE FIRST, then apply it** — e.g. 4.7619
  rupees/USD → use exactly [redacted]. Verified correct: (Jan+Feb [redacted] total
  receipts from the public, 12,104 $M) × 4.76 = [redacted] INR-millions.

## 3. "Imports under quota" tables (fish, cattle, lumber, etc.)
- Quota-import tables in 1939–41 bulletins frequently report quantities
  **cumulative from the start of the quota period to date**, not per-month.
  Check the column heading. A month-over-month change then requires
  differencing cumulative columns; using cumulative values as monthly ones
  silently inflates levels and changes.
- "All <commodity> commodities" = **sum every row of that commodity class**
  (e.g. multiple fish line items under separate quota provisions), not the
  single largest row.
- Quantities are usually in **pounds** (check header); keep raw pounds
  through the whole chain and rescale only if the question asks.
- The percent intermediate is sensitive to small errors in the monthly
  quota quantities: cross-validate each Jan/Feb/Mar figure against the
  next issue's table (see tb-cross-issue-ocr-check) — a single misread row
  shifts the final percent by 1–2%, enough to fail exact-match grading.

## 4. Cross-year retrieval
- An "actual" value for month M of year Y is published in a bulletin a month
  or two AFTER M/Y. Pull each year's figure from its own later bulletin;
  do not reuse the earlier year's table layout assuming identical rows.

## 5. Geometric (compound) annual rate of change — verified pattern
"Geometric annual rate of change in X between periods ending <month Y1> and
<month Y2>" means CAGR on the two endpoint values:

  `rate = (X_end / X_start)^(1/n) - 1`,  with `n = Y2 - Y1`

- **n = the number of year-gaps between the endpoints**, not the count of
  periods: Dec 1938 → Dec 1940 is n = 2 (not 3).
- If X is itself a ratio (e.g. working balance / total balance of the
  Treasury's **General Fund** — found in the "General Fund" / status-of-the-
  Treasury table near the front of each bulletin), compute the ratio at each
  endpoint from raw table values first, then apply the CAGR formula. Do not
  round the intermediate ratios.
- A declining series gives `X_end/X_start < 1` and a **negative** rate —
  keep the minus sign.
- "Outputted as a decimal value (e.g. 0.1234, not 12.34%)" means do NOT
  multiply by 100; round the decimal itself to the asked precision
  (e.g. [redacted] for 3 decimals). Verified correct: this exact pattern
  produced [redacted] for the Dec 1938 → Dec 1940 working/total balance ratio.

## 6. Geometric mean of a SET of values (distinct from CAGR)
"Geometric mean of all the <rates/values> ..." over a list of N datapoints
is `(x1 * x2 * ... * xN)^(1/N)` — no `- 1`, no year-gap exponent. Do not
confuse it with the CAGR pattern in §5; CAGR uses only two endpoints.
- Collect EVERY qualifying datapoint first and count N explicitly — N varies
  (a calendar month has 4 or 5 of a given weekday depending on the year).
- Rates stay in percent throughout (geometric mean of percents is a
  percent); don't convert to decimals unless asked.
- Use full printed precision for each value; round only the final result.
- Verified correct: geometric mean of the 13 weekly 91-day bill rates for
  September 1953–1955 → 1.558.

## 7. Weekly Treasury bill rates — where to find them
- Each monthly Treasury Bulletin has an "Offerings of Treasury Bills" table
  (market-financing / public-debt section) with ONE ROW PER WEEKLY AUCTION:
  issue date, maturity date, amounts tendered/accepted, and the **average
  rate on a bank discount basis (percent)**.
- Regular 91-day (13-week) bills in the 1950s are **dated/issued on
  Thursdays**; "the Thursday of each week in month M" = every issue date
  falling within calendar month M (4 or 5 rows per month).
- A given bulletin issue covers only recent weeks — pull each year's
  September rows from a bulletin published 1–2 months later (e.g. the
  Oct/Nov issue of that same year), one bulletin per year.

## 8. Box-Cox (and other nonlinear) transforms — verified pattern
"Difference between Box-Cox transformed values of X in FY1 and FY2, expressed
in billions, lambda = λ":

  `BC(x) = (x^λ - 1) / λ`  for λ ≠ 0   (λ = 0 → `ln(x)`)

- **Rescale units FIRST, transform SECOND.** The transform is nonlinear, so
  BC(millions) ≠ 1000·BC(thousands-of-millions). The phrase "expressed in
  billions of dollars" describes the INPUT to the transform: convert each
  table value (usually printed in millions) to billions, then apply BC.
- **Transform each value separately, then difference**: answer =
  `BC(x_FY1) - BC(x_FY2)`, NOT `BC(x_FY1 - x_FY2)`.
- Keep full precision through both transforms; round only the final
  difference to the asked decimals.
- "The comparable <prior year> fiscal period" = the prior-fiscal-year column
  of the SAME table in the SAME bulletin issue (budget-results tables print
  current FY and prior FY side by side).
- Budget outlay categories like **net interest** are in the federal budget
  results / Federal Fiscal Operations summary table near the front of the
  bulletin, values in millions of dollars.
- Verified correct: net interest FY[redacted] vs FY[redacted] (Nov [redacted] bulletin),
  λ = 0.75, values in billions → 6.1596.

## 9. Volatility / standard deviation over a date range — verified pattern
"Price volatility (measured in terms of population standard deviation) ...
between <date1> and <date2>":
- **Population std dev divides by N**, not N-1: `σ = sqrt(Σ(x-μ)²/N)`. Only
  use the sample (N-1) formula if the question explicitly says "sample".
- **Both endpoint dates are inclusive.** "Between January 1st and August
  1st" with monthly (end/start-of-month) observations = the Jan, Feb, ...,
  Aug observations → N = 8 datapoints. Count N explicitly before computing.
- One observation per bulletin issue/month: pull the same security's row
  from each consecutive monthly table over the range. Match the security by
  its FULL description (coupon, e.g. "2-3/8%" = 2⅜ percent, AND type, e.g.
  "Inflation-Protected") — multiple securities can share a coupon rate.
- Keep full precision on every observation and on the mean; round only the
  final σ to the requested decimals.
- Verified correct: 2⅜% TIPS adjusted prices, Jan–Aug [redacted] population σ
  rounded to 6 decimals → 0.900544.

## 10. TIPS (inflation-protected) securities — adjusted price
- Treasury market-quotation tables list TIPS with a quoted price and an
  **index ratio** (the cumulative CPI inflation adjustment factor).
- "Adjusted price accounting for inflation / index ratios" =
  `quoted price × index ratio`. If the table already prints an
  "adjusted price" column, use it directly; otherwise multiply.
- Do the multiplication per observation BEFORE any statistics — never
  compute stats on raw prices and adjust afterward (the index ratio changes
  every month, so the operations don't commute).

## 11. Arc elasticity — verified pattern
"Arc elasticity of Q with respect to P between t1 and t2" = midpoint
formula:

  `E = [(Q2-Q1)/((Q1+Q2)/2)] / [(P2-P1)/((P1+P2)/2)]`

- Keep the sign; round only the final result. Cross-validate every input
  per tb-cross-issue-ocr-check — one corrupted digit in a denominator
  changes the answer.
- IRS data lives in "Internal Revenue Collections — Table 1. Summary by
  Principal Sources", **thousands of dollars**, near the back of each
  issue (columns: total collections | corporation income | individual
  withheld/not withheld | OASI | railroad retirement | unemployment
  insurance; monthly rows follow the fiscal-year rows).
- Verified correct: total IRS collections (Jan [redacted]: [redacted] → Mar [redacted]:
  11,893,553) vs unemployment insurance contributions (26,461 → 20,774)
  gives 0.848521 / (−0.240796) = −3.524.

## 12. Final magnitude audit
Before reporting, do one order-of-magnitude pass over the whole chain
(pounds in the millions? percentage plausible? division applied?). If the
wrong/right ratio of a dry run equals one of your divisors, that divisor
was the dropped step.
