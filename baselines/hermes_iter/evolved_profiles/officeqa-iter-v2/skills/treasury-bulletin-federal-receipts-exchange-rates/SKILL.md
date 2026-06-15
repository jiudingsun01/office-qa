---
name: treasury-bulletin-federal-receipts-exchange-rates
description: Use when OfficeQA/Treasury Bulletin questions ask for U.S. federal Government receipts from the public by calendar month and conversion using annual average nominal exchange rates.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [officeqa, treasury-bulletin, federal-finance, receipts, exchange-rates, fraser]
    related_skills: []
---

# Treasury Bulletin Federal Receipts + Exchange Rate Questions

## When to Use

Use this skill for OfficeQA questions that mention:

- U.S. federal Government `total receipts from the public`.
- Calendar-month values such as January 1956 and February 1956.
- Amounts requested in `millions of nominal dollars`.
- Converting a summed USD value to another currency using an annual average exchange rate such as 1956 USD/INR.

## Procedure

1. Locate the Treasury Bulletin table for federal Government receipts/payments.
   - Search the relevant bulletin/OCR text for exact phrases such as `total receipts from the public`, `receipts from the public`, `payments to the public`, and the requested year.
   - Prefer layout-preserving extraction (`pdftotext -layout` or FRASER OCR with columns) because month columns are dense and adjacent finance tables can have similar headings.

2. Confirm row, column, and unit before extracting numbers.
   - Use the row labeled `Total receipts from the public`, not budget receipts, trust-account receipts, net receipts, or total payments.
   - Use calendar-month columns exactly as asked. For `January 1956` and `February 1956`, take the two monthly cells, not fiscal-year-to-date or quarterly totals.
   - These tables commonly report dollar amounts in millions. If the prompt asks for `in millions of nominal dollars`, keep the table values in millions and do not multiply by 1,000,000 before currency conversion.

3. Sum requested monthly receipt values in USD millions.
   - `usd_sum_millions = receipt_month_1 + receipt_month_2 + ...`
   - Preserve table precision through the sum. Do not round individual months unless the table itself is already rounded.

4. Apply the annual average exchange rate as requested.
   - Locate the yearly average nominal exchange-rate series for the requested currency pair and year.
   - Confirm the quote direction. For prompts phrased `using the yearly average 1956 USD/INR exchange rate to convert from USD to INR`, use INR per USD, so multiply USD by the USD/INR rate.
   - If the prompt says the exchange rate is `rounded to the nearest hundredths place`, round the annual average exchange rate to 2 decimals first, then use that rounded rate in the conversion.
   - Calculation pattern: `inr_sum_millions = usd_sum_millions * rounded_usd_inr_rate`.

5. Round and format the answer.
   - Round the converted value to the requested decimal places, commonly nearest hundredths.
   - If the benchmark accepts comma formatting, `[redacted]` and `57615.04` are numerically equivalent, but final responses should follow the prompt's requested style if specified.

## Worked Pattern

For a prompt asking for the sum of January 1956 and February 1956 total receipts from the public, converted with the yearly average 1956 USD/INR rate:

1. Extract the two monthly `Total receipts from the public` values in millions of nominal USD.
2. Sum them in millions.
3. Round the 1956 USD/INR yearly average exchange rate to hundredths.
4. Multiply the USD-million sum by the rounded INR-per-USD rate.
5. Round final INR-million result to hundredths.

## Regression Pattern: Receipts by Source over Fiscal Years

Use this pattern for prompts asking for OLS/trend fits on receipts categories such as `individual income tax receipts, net of refunds`, by fiscal year.

1. Locate the receipts-by-source table, not the monthly `receipts from the public` cash table.
   - Search for exact source labels such as `Individual income taxes`, `income tax receipts`, and `net of refunds`.
   - Confirm the year basis is fiscal years when the prompt says `fiscal years`; Treasury fiscal years are not calendar years.

2. Confirm units and preserve precision.
   - If the prompt asks for `billions of nominal dollars`, convert table values once to billions if the table is in millions.
   - Keep the full extracted numeric precision for all regression inputs. Do not round annual receipts before fitting.

3. Fit OLS with the requested predictor exactly.
   - For `year (numeric, untransformed)`, use years like `1929, 1930, ...` directly, not an index `0..n-1` and not centered years.
   - Fit `receipts = intercept + slope * year` using ordinary least squares.
   - Return coefficients in the prompt's requested order. If it asks `slope and intercept`, output `[slope, intercept]`.

4. Round only the final coefficients.
   - Round slope and intercept after fitting, to the requested decimal places.
   - Use benchmark-style nearest-decimal rounding for final displayed coefficients; avoid Python/NumPy `round` surprises on exact half cases (banker's rounding / binary float ties). If a coefficient is near a .0005 boundary, format with `Decimal` and `ROUND_HALF_UP`/away-from-zero semantics after computing the coefficient from full-precision inputs. This matters for negative intercepts too: a value like `-184.1425...` should display as `-184.143`, not `-184.142`.
   - Tiny differences in intermediate rounding can move the intercept by 0.001 because the uncentered year predictor is around 1900; recompute from full precision if the result is on a rounding boundary.
   - Do not compute the intercept from a rounded slope. Use the fitted full-precision slope and mean values (`intercept = ybar - slope_full * xbar`) or an exact/rational least-squares calculation, then round the final intercept once.

## OCS Rents and Royalties Pattern

Use this pattern for prompts that cite 43 U.S. Code § 1331 or ask about `OCS` receipts. In these Treasury Bulletin / Monthly Treasury Statement receipt tables, `OCS` means Outer Continental Shelf, and the relevant recorded source is typically labeled `rents and royalties on the Outer Continental Shelf` or similar.

1. Search receipt-source tables for `Outer Continental Shelf`, `OCS`, `rents`, and `royalties`; do not answer from the legal definition alone.
2. Confirm the unit on the table. Modern receipts tables commonly report amounts in millions of dollars, so keep values as printed when the prompt asks for millions.
3. If the prompt asks for a calendar year, use the twelve monthly records in that calendar year, not fiscal-year totals or year-to-date columns.
4. If it asks for the `lowest amount` by `lowest absolute value`, compute `abs(value)` for each recorded monthly rent/royalty amount, then choose the minimum absolute value. Negative values can occur; report the absolute value when requested.

## On-Budget vs Off-Budget Receipts R-Square Pattern

Use this pattern for prompts asking for the relationship, correlation, or R-square between U.S. Treasury nominal `on-budget receipts` and `off-budget receipts` across fiscal years.

1. Use the Federal fiscal operations / budget results tables in the requested September Treasury Bulletins.
   - Search for exact labels `on-budget receipts`, `off-budget receipts`, `on-budget`, and `off-budget`.
   - When the prompt gives multiple September bulletins (for example 1996, 2001, 2006, 2011), use them to cover/verify the fiscal-year range in blocks. Later bulletins may restate or extend earlier years; prefer the bulletin that directly covers the needed years and cross-check overlapping years.

2. Extract fiscal-year annual nominal values, not monthly values.
   - Keep `on-budget receipts` and `off-budget receipts` as separate paired observations for each fiscal year.
   - Use fiscal years exactly as requested (e.g. FY 1991-2010 inclusive gives 20 paired observations).
   - Do not deflate by CPI and do not transform to real dollars unless explicitly asked. The prompt’s `nominal` means use printed current-dollar table values.

3. Units/scaling do not affect R-square.
   - Treasury tables commonly report these receipts in millions of dollars. Keep both series in the same printed units.
   - If one source is in billions and another in millions, normalize before calculations; otherwise scaling either variable by a positive constant leaves R-square unchanged.

4. Compute R-square as the squared Pearson correlation / simple OLS R² between the two receipt series.
   - Fit either `off_budget = a + b * on_budget` or compute `corr(on_budget, off_budget) ** 2`; for simple linear regression with intercept they are identical.
   - Do not round annual observations before computing the correlation/regression.
   - Round only the final R-square to the requested precision (often 4 decimals).

## Common Pitfalls

- For OCS prompts, 43 U.S.C. § 1331 is only the definition clue (`Outer Continental Shelf`); still extract the numeric values from Treasury receipt-source records labeled rents/royalties on the Outer Continental Shelf.
- For OCS `lowest amount` prompts that specify lowest absolute value, compare absolute values of monthly recorded rents/royalties and return the absolute value, not the most negative signed entry.
- Do not use `payments to the public` or net cash borrowing rows; the target row is receipts.
- Do not use fiscal-year columns for questions that ask for calendar months.
- For on-budget/off-budget relationship questions, do not combine the two series into total receipts; they are the two variables being compared.
- For receipts-by-source questions, do not confuse `individual income taxes, net of refunds` with total budget receipts or total receipts from the public.
- Do not convert millions to raw dollars if the answer is requested in millions after conversion.
- Do not invert USD/INR for USD-to-INR conversion; multiply by INR per USD.
- If the prompt explicitly says to use an exchange rate rounded to hundredths, round the exchange rate before multiplying, not only the final result.
- For OLS/trend questions, do not round observations or coefficients until the final requested formatting step.

## Verification Checklist

- [ ] Source row is exactly `Total receipts from the public`.
- [ ] Month columns match the requested calendar months and year.
- [ ] Units remain in millions throughout the currency conversion.
- [ ] Exchange-rate direction is INR per USD for USD-to-INR.
- [ ] Annual average rate is rounded to 2 decimals before conversion when requested.
- [ ] Final answer is rounded to nearest hundredths.
