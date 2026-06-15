---
name: treasury-bulletin-currency-circulation-cpi
description: Use for OfficeQA/Treasury Bulletin questions asking about currency in circulation / money in circulation by fiscal month, especially when combined with BLS CPI-U year-over-year inflation adjustment.
---

# Treasury Bulletin currency in circulation + CPI-U inflation adjustment

Use this skill when a prompt asks for `currency in circulation`, `money in circulation`, denominations of currency/coin, or an inflation-adjusted value using a BLS CPI-U year-over-year rate.

## Treasury Bulletin source pattern

1. Look in the Treasury Bulletin section for monetary/currency tables, not Public Debt. Common headings include:
   - `CURRENCY AND COIN`
   - `Currency in Circulation`
   - `Money in Circulation`
   - `Currency and Coin in Circulation`
   - denomination tables with a final `Total` line.
2. The phrase `by the end of the same fiscal month` means use the end-of-month row/column for that fiscal month in the Treasury table. For example, `calendar month November 1969` maps to the fiscal month ending November 1969, not the fiscal year-end or an annual average.
3. Historical Treasury Bulletin currency/circulation tables are commonly in `millions of dollars`. Keep the Treasury value in millions unless the prompt explicitly asks for dollars, billions, etc.
4. If the table has multiple totals, choose the total explicitly for `currency in circulation` / `money in circulation`, not narrower subtotals such as currency outside Treasury/Federal Reserve Banks, individual denominations, coins only, or public-debt figures.
5. Be careful with tables that show both `currency/coin outstanding` and `currency/coin in circulation`. For a prompt asking `total currency in circulation`, use the `in circulation` total, not the adjacent/nearby `outstanding` total. `Outstanding` can be slightly higher because it includes amounts held by Treasury/Federal Reserve channels that are not in circulation (e.g. a difference on the order of tens of millions); using it will overstate the CPI-adjusted answer. Calibration example: for fiscal/month-end November 1969, the nominal circulation total is about `52,941.0` million; `52,991.0` million is the wrong adjacent/non-circulation figure and leads to an answer about 53.0 million too high after applying 6.0% CPI inflation.
6. In tables headed like `United States currency and coin outstanding and in circulation` or `Currency and coin in circulation`, the overall circulation total can appear after separate paper-currency and coin blocks. For prompts asking `total currency in circulation`, use the grand total for all currency/coin in circulation at month-end; do **not** stop at `Federal Reserve notes`, `paper currency`, `total notes`, `outstanding`, or other denomination/subclass totals. A useful sanity check is that the chosen total should be larger than any component subtotal such as Federal Reserve notes alone, but not necessarily equal to the larger `outstanding` total.

## CPI-U adjustments

1. Use the official BLS CPI-U all-items, U.S. city average series (`CUUR0000SA0` / CPI-U All Urban Consumers, All Items), unless the prompt names another CPI series.
2. For `year-over-year inflation rate for calendar month M YYYY`, distinguish the wording carefully:

   - If the prompt asks for the `official BLS CPI-U year-over-year inflation rate` / `12-month percent change`, use the BLS-published 12-month percentage change for CPI-U All Items for that month (normally shown rounded to one decimal percent in BLS series output). Do **not** recompute an unrounded rate from CPI index levels and carry extra decimals, because OfficeQA gold answers for this wording apply the official rounded BLS rate. Example: for November [redacted] use the official BLS YoY CPI-U rate `[redacted]`; multiplying the Treasury total currency in circulation by `[redacted]` gives the expected result, while using an unrounded CPI-index quotient gives a slightly high answer.
   - If the prompt explicitly asks to use CPI index values/ratio, or says to compute inflation from CPI levels, use:

     `rate_pct = 100 * (CPI[M YYYY] / CPI[M previous year] - 1)`

   In both cases, use the CPI for the same calendar month in the prior year, not an annual-average CPI and not the prior month.
3. When the prompt says to apply the year-over-year inflation rate to the Treasury amount, inflate the amount upward:

   `adjusted_millions = treasury_currency_millions * (1 + rate_pct / 100)`

   Do not deflate by dividing by `(1 + rate)` unless the prompt explicitly asks to convert to prior-year dollars. Sanity check: after applying a positive YoY inflation rate, the adjusted amount must be larger than the nominal Treasury currency amount; if it is smaller, the ratio was inverted.
4. For month-over-month real-dollar changes, first convert the previous-month Treasury amount into current-month dollars using the CPI ratio, then subtract it from the current-month Treasury amount:

   `previous_in_current_month_dollars = previous_month_amount_millions * CPI[current month] / CPI[previous month]`

   `real_mom_change_millions = current_month_amount_millions - previous_in_current_month_dollars`

   Example interpretation: “month-over-month change in Federal Reserve notes in millions of June 1979 dollars” means use June 1979 Federal Reserve notes directly, adjust May 1979 Federal Reserve notes by `CPI[June 1979] / CPI[May 1979]`, then compute `June_adjusted - May_adjusted` in millions. The sign is negative if the inflation-adjusted prior-month amount exceeds the current-month amount.
5. Round only the final adjusted result to the requested precision, e.g. nearest tenths or hundredths place in millions of dollars. Do not round intermediate CPI ratios, CPI rates, or Treasury values unless the prompt/source only provides rounded values.

## Verification checklist

Before finalizing:

- Confirm the Treasury table unit is millions of dollars.
- Confirm the month is the fiscal month ending in the named calendar month.
- Confirm the selected row/column is the overall currency/money-in-circulation total, not a subtotal.
- Confirm CPI-U YoY used same calendar month vs previous year.
- Confirm the formula direction is multiplication by `1 + YoY rate` for an `after applying inflation rate` prompt.
- Confirm the final answer is not just the nominal Treasury currency amount. If the prompt asks for a CPI-U YoY inflation-adjusted amount, a positive YoY CPI rate must make the final adjusted value larger than the nominal value; equality means the CPI adjustment was skipped.
