---
name: treasury-bulletin-import-quotas-exchange-rates
description: Use when OfficeQA/Treasury Bulletin questions ask about monthly import quantities under U.S. provisioned quotas (especially fish commodities) and then combine the result with historical exchange-rate series.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [officeqa, treasury-bulletin, imports, quotas, exchange-rates, fraser]
    related_skills: [ocr-and-documents]
---

# Treasury Bulletin Import Quotas + Exchange Rate Questions

## When to Use

Use this skill for OfficeQA questions that mention:

- U.S. Treasury Bulletin tables of imports under U.S. provisioned/proclaimed quotas.
- Monthly quantities of commodity imports, especially fish commodities.
- Forecasting a later month from a month-over-month absolute increase.
- Comparing a forecasted monthly import value to an actual value in another year.
- Dividing a computed percentage by an annual average nominal exchange rate, e.g. U.S. dollar to British pound for a calendar year.

## Procedure

1. Locate the import-quota table in the Treasury Bulletin source.
   - Search OCR/layout text for combinations such as `fish commodities`, `provisioned quotas`, `quota`, `imports`, `January`, `February`, and `March`.
   - Prefer `pdftotext -layout` or FRASER OCR with preserved columns for monthly tables; commodity names and month columns are easy to misalign in plain/raw extraction.

2. Identify the exact commodity aggregate and unit.
   - If the question says `all fish commodities`, use the aggregate/total line for all fish commodities, not a single species or subcategory.
   - Record the table unit exactly. For these quota tables, quantities may be reported directly in pounds; do not convert unless the table heading or footnote says thousands/millions.
   - Ignore currency columns when the requested import measure is `quantity` or `pounds`.

3. Extract all month/year values from aligned columns before doing arithmetic.
   - For a forecast from January 1939 to February 1939:
     - `increase = abs(February_1939_quantity - January_1939_quantity)`.
     - `March_1939_forecast = February_1939_quantity + increase`.
   - If the later comparison asks for actual March 1940, get that from the March 1940 column/row of the same commodity aggregate, not from March 1939 actuals.
   - Preserve integer pounds until the percentage step.

4. Compute the year-over-year absolute difference and percentage.
   - `absolute_difference = abs(actual_March_1940 - March_1939_forecast)`.
   - `percentage = (absolute_difference / March_1939_forecast) * 100`.
   - If the question requests a number like `5.25, not a decimal`, use the percentage value, not the fraction.

5. Apply annual average exchange-rate divisor only at the end.
   - Locate the requested annual average nominal exchange rate (for example, U.S. dollar to British pound for calendar year 1941) from the exchange-rate source specified or implied by the benchmark.
   - Confirm quote direction before dividing. If the question says `U.S. dollar to British pound exchange rate`, use the series exactly as labeled; do not invert it unless the source label is opposite the requested direction.
   - Final calculation pattern: `(percentage_value) / (annual_average_exchange_rate)`.

6. Round and format exactly as requested.
   - Use high precision for intermediate arithmetic.
   - Round the final quotient to the requested number of decimal places, commonly 4.
   - If the answer must be a single number with no commas, output only that number (e.g. `[redacted]`).

## Common Pitfalls

- Do not treat `absolute month-over-month increase` as signed change; use `abs(Feb - Jan)` and then add it to February when forecasting.
- Do not compare the March 1939 forecast to March 1939 actual when the prompt asks for actual March 1940.
- Do not divide the raw fraction by the exchange rate if the prompt asks for a percentage value like `5.25`; multiply by 100 first.
- Do not round the forecast, difference, or percentage early; only round the final reported value.
- Column alignment matters: quota/import tables can have dense month columns and wrapped commodity labels. Verify the aggregate row and year/month column visually or with layout-preserving text.

## Verification Checklist

- [ ] Source table is the import-quota table, not a general trade value table.
- [ ] The row is the aggregate `all fish commodities` row when requested.
- [ ] Units are pounds (or table-specific unit applied exactly once).
- [ ] January 1939, February 1939, and March 1940 values were read from correct columns.
- [ ] Forecast used `Feb 1939 + abs(Feb 1939 - Jan 1939)`.
- [ ] Percentage used `abs(actual Mar 1940 - forecast Mar 1939) / forecast * 100`.
- [ ] Annual average exchange-rate divisor is quote-direction checked and applied last.
- [ ] Final answer has the requested decimal places and no commas.
