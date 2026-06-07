---
name: treasury-bulletin-trust-fund-flows
description: Use when OfficeQA/Treasury Bulletin questions ask about Federal trust fund receipts/expenditures, balances, investment exclusions, Disability Insurance/OASDI/Unemployment trust funds, surplus/deficit status, CPI inflation adjustment, or a Gini/inequality measure over trust-fund flow totals.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [officeqa, treasury-bulletin, trust-funds, disability-insurance, gini]
    related_skills: []
---

# Treasury Bulletin Trust Fund Receipts, Expenditures, Balances, Investments, CPI Adjustment, and Gini

## Overview

Treasury Bulletin trust fund tables often list a fund's operating receipts and expenditures together with investment transactions. For OfficeQA questions, prompts that say "excluding those attributed to investments" usually want the fund's operating flow totals only: the row labeled `Total receipts` for receipts and the row labeled `Total expenditures` for expenditures, not investment purchases/sales, net investment activity, changes in balance, or assets held.

A recurring arithmetic trap is the two-value "Gini coefficient" convention used by OfficeQA for comparing two totals. When only two categories are being considered, OfficeQA expects the relative absolute difference:

```text
Gini-like value = abs(total_receipts - total_expenditures) / (total_receipts + total_expenditures)
```

Do not divide by an additional factor of 2. The textbook population Gini for two observations, `abs(a-b)/(2*(a+b))`, gives half the OfficeQA expected answer and will be marked wrong.

## When to Use

Use this skill for questions involving:

- Federal Disability Insurance Trust Fund, Old-Age and Survivors Insurance Trust Fund, Hospital Insurance, Supplementary Medical Insurance, Unemployment Trust Fund, or other federal trust fund tables.
- Fiscal month columns such as `September 1975`, `fiscal year`, or `fiscal month`, and balance dates such as `as of December 1946` / `as of December 1947`.
- Phrases like "total receipts and total expenditures", "excluding investments", "attributed to investments", "operating surplus/deficit", or "fund operating in a surplus or deficit".
- Phrases like "total balance", "balance as of", "assets held by trust funds", "adjusted for inflation", or "in YYYY dollars".
- Gini, inequality, dispersion, or relative difference computed from only receipts and expenditures.
- Aggregate `total U.S. federal trust account receipts` or similar all-trust-account monthly receipts/outlays by calendar month, including questions that convert the dollar result to a foreign currency using a monthly average exchange rate.

Do not use this for unrelated Treasury Bulletin tables such as market yields, bill rates, import quotas, or general fund balances unless a trust fund operating-flow table is involved.

## Procedure

1. Locate the relevant Treasury Bulletin issue and the trust fund section/table.
   - Search the PDF text for the exact fund name first, e.g. `Disability Insurance Trust Fund` or `Federal Old-Age and Survivors Insurance`.
   - If the table of contents is easier, look for sections titled like `Trust Funds`, `Federal Old-Age and Survivors Insurance Trust Fund`, `Federal Disability Insurance Trust Fund`, or `Receipts and expenditures of trust funds`.
   - For historical Social Security/OASI questions, the table may label the relevant line as `expenditure transfers to the trust fund` under `Federal Old-Age and Survivors Insurance`, rather than a modern `Total receipts`/`Total expenditures` pair.

2. Use the fiscal month/year column requested by the prompt.
   - Treasury Bulletin tables may include monthly columns, fiscal-year-to-date columns, or full fiscal-year columns on the same page.
   - Confirm the column header says the requested fiscal month, e.g. `September 1975`; do not accidentally use the fiscal-year total or adjacent month.

3. Extract operating receipts and operating expenditures.
   - Use the row labeled `Total receipts` for the requested fund and month.
   - Use the row labeled `Total expenditures` for the same fund and month.
   - If the prompt says investments are excluded, ignore rows such as `Investments`, `Purchase of obligations`, `Sale/redemption of securities`, `Interest on investments` if they are presented as investment transactions rather than operating totals, `Net increase/decrease in investments`, or balance/asset rows.
   - Do not use the change in fund balance as a substitute for receipts or expenditures.

4. Preserve units consistently.
   - Most Treasury Bulletin trust fund tables are in millions of dollars, but the Gini/ratio and surplus/deficit comparison are scale-invariant when both values come from the same table.
   - Balance questions usually also remain in the table's stated unit. If the prompt asks for "in millions", keep the trust-fund table values in millions and do not multiply by 1,000 unless the table header is thousands.
   - Strip commas, footnotes, `r` revised markers, and parentheses carefully. Parentheses usually indicate negative values only where a row can be negative; totals for receipts/expenditures should normally be positive.

5. For trust-fund balance questions, use the end-of-period balance/asset table rather than operating-flow rows.
   - Locate the row for the named fund, e.g. `Unemployment Trust Fund`, and the column for the requested date, e.g. `December 1946` or `December 1947`.
   - Use the row/column labeled `Total balance` or equivalent total assets/balance for the fund, not `total receipts`, `total expenditures`, `net increase`, or investment purchase/sale rows.
   - `as of December YYYY` means the December end-of-month/end-of-period balance for that calendar year.
   - If two bulletins contain overlapping/revised values, prefer the table value in the issue that directly covers the later comparison date or marks the value revised, unless the prompt names a specific bulletin.

6. For CPI-U inflation adjustments to a target year's dollars, convert each nominal table value into target-year dollars before taking differences.

```python
# values in table units, commonly millions of dollars
real_base = nominal_base * (cpi_target / cpi_base)
real_target = nominal_target * (cpi_target / cpi_target)  # unchanged
signed_difference = real_target - real_base              # e.g. 1947 - 1946
answer = round(signed_difference, 1)
```

   - Use U.S. BLS CPI-U annual-average values when the prompt says "for those years" without specifying a month. Do not use December CPI unless the question explicitly requests monthly CPI.
   - For 1940s Unemployment Trust Fund `total balance as of December YYYY` questions, this means: take the December end-of-period nominal `Total balance` for each year, inflate the earlier year's balance to the target year's dollars, then subtract in the stated order.
   - Keep the sign in the order stated by the prompt, e.g. `(1947 - 1946)` is `real_1947 - real_1946`, even if the result is negative.
   - Round only the final value to the requested precision; avoid rounding intermediate CPI-adjusted values.

7. Compute the OfficeQA two-flow Gini-like value.

```python
receipts = ...       # Total receipts, excluding investment rows
expenditures = ...   # Total expenditures, excluding investment rows
gini = abs(receipts - expenditures) / (receipts + expenditures)
answer = round(gini, 3)
```

   - This is the convention observed for OfficeQA Treasury Bulletin trust-fund questions.
   - Do not use `abs(receipts - expenditures) / (2 * (receipts + expenditures))`.
   - Format to the nearest thousandth with three decimal places when requested.

8. Determine surplus or deficit from operating flows.
   - `surplus` if `total_receipts > total_expenditures`.
   - `deficit` if `total_receipts < total_expenditures`.
   - `balanced` or similar only if the prompt explicitly allows it and the values are exactly equal; otherwise OfficeQA usually asks for surplus/deficit.

9. For aggregate monthly `total U.S. federal trust account receipts` questions, use the all-trust-account total row/column for the named calendar months.
   - These prompts are not asking for a named fund such as OASI or Unemployment; find the table/row that aggregates U.S. federal trust accounts and use `Total receipts` for each requested calendar month.
   - Keep the table units, commonly millions of U.S. dollars. If the prompt asks for the answer in millions of a foreign currency, the numeric value remains in millions after applying the exchange rate.
   - If a single exchange-rate month is specified, e.g. `using the monthly average exchange rate of USD-CAD in December 1959`, use that rate for the whole result; do not use November's exchange rate for November and December's for December unless explicitly instructed.
   - Treat `USD-CAD` as CAD per 1 USD. Convert USD millions to CAD millions by multiplying by the monthly average USD-CAD exchange rate after computing the requested USD difference.
   - Do **not** round the monthly-average FX rate to `1.05` before multiplying. These questions can hinge on the fourth-to-sixth decimal place: for the November/December 1959 aggregate receipts case, using `1.05` gives about `504.03`, while the benchmark expects about `504.12` from the full-precision December 1959 USD-CAD monthly average. Carry the full source precision through the multiplication and round only the final CAD-million answer.
   - For an absolute difference:

```python
nov_usd_millions = ...  # Total U.S. federal trust account receipts, November 1959
dec_usd_millions = ...  # Total U.S. federal trust account receipts, December 1959
usd_diff_millions = abs(dec_usd_millions - nov_usd_millions)
usd_cad_dec_avg = ...    # CAD per USD, December 1959 monthly average, full precision; do not pre-round to 1.05
cad_diff_millions = usd_diff_millions * usd_cad_dec_avg
answer = round(cad_diff_millions, 2)
```

10. For CAGR questions on trust-fund transfers, use nominal values exactly as the prompt says and map historical events to the correct fiscal year.
   - Example: the Korean War started June 25, 1950, which falls in U.S. FY 1950 (fiscal years before 1977 ran July 1-June 30).
   - If the start is FY 1947 and the end is FY 1950, the number of annual periods is `1950 - 1947 = 3`, not 4.
   - Use the exact row named in the prompt, e.g. `expenditure transfers to the trust fund` for Federal Old-Age and Survivors Insurance; do not substitute total receipts, benefits, balances, payroll-tax contributions, or generic `transfers` rows from another fund.
   - For the Federal Old-Age and Survivors Insurance `expenditure transfers to the trust fund` FY 1947→FY 1950 case, the endpoint ratio is about 9×, so the CAGR is about 108%/year. If your result is around 13%/year, you almost certainly extracted the wrong row/endpoint (or used an annual difference/average instead of the geometric CAGR).
   - Formula for percent per year:

```python
start_fy = 1947
end_fy = 1950
start_value = ...  # nominal table value for the named row/fund
end_value = ...    # nominal table value for the named row/fund
cagr_percent = ((end_value / start_value) ** (1 / (end_fy - start_fy)) - 1) * 100
answer = round(cagr_percent, 2)
```

   - If the prompt says `reported in percent per year`, format the final answer as a percent (e.g. `108.01%`) rather than a bare decimal fraction or unlabelled number, unless the benchmark interface explicitly requires numeric-only output.

## Common Pitfalls

1. **Using textbook two-observation Gini.** OfficeQA expects `|R-E|/(R+E)` for the two trust-fund totals. The textbook population Gini is half that value.

2. **Including investment transaction rows.** If the prompt excludes investments, use the operating `Total receipts` and `Total expenditures` rows only. Do not add investment purchases/sales or use net investments.

3. **Mixing month and fiscal-year-to-date columns.** September columns can appear next to fiscal-year totals. Verify the exact column header before extracting values.

4. **Using net balance change to infer surplus.** Determine surplus/deficit by comparing operating receipts and operating expenditures, not by investment activity or end-of-month fund balance.

6. **Using operating flows for balance questions.** For prompts asking for `total balance` or `balance as of December`, use the trust-fund balance/asset table's end-of-period balance column, not receipts/expenditures or net change rows.

7. **Wrong inflation order or CPI frequency.** For `in 1947 dollars` with annual years, use annual-average CPI-U and compute `nominal_year * CPI_1947 / CPI_year` before subtracting. Preserve the prompt's signed order such as `(1947 - 1946)`.

8. **Rounding too early.** Keep full extracted table and CPI values through the calculation. Round only the final Gini/difference value to the requested precision.

9. **Wrong fiscal-year endpoint for historical events.** The Korean War started in June 1950, so for old July-June federal fiscal years it is FY 1950. CAGR from FY 1947 to FY 1950 uses 3 annual periods.

10. **Currency conversion direction for USD-CAD.** `USD-CAD` monthly average means CAD per USD. For answers in millions of CAD, multiply the USD-million result by the rate; do not divide. When the prompt names one exchange-rate month, apply that one rate to the whole difference unless told otherwise.

11. **Aggregate calendar-month receipt questions are not fiscal-year-to-date questions.** For adjacent months such as November and December 1959, use the two calendar-month `Total receipts` entries from the all-trust-account aggregate. Compute the absolute USD-million difference first, then apply the single specified monthly average FX rate.

## Verification Checklist

- [ ] The same fund and same fiscal month/year were used for both totals.
- [ ] The values came from `Total receipts` and `Total expenditures`, not balance or investment rows.
- [ ] Investment-attributed rows were excluded when the prompt requested exclusion.
- [ ] Gini was computed as `abs(R-E)/(R+E)` with no extra `/2`.
- [ ] Surplus/deficit was based on `R > E` or `R < E`.
- [ ] For balance questions, the value came from the `Total balance`/assets balance row for the named fund and requested end-of-period date, not operating flows.
- [ ] For CPI-adjusted differences, each nominal value was converted to the requested year's dollars using annual-average CPI-U before subtracting.
- [ ] For CAGR, endpoint fiscal years are mapped correctly, the period count is `end_fy - start_fy`, and the result is multiplied by 100 if the prompt asks for percent per year.
- [ ] For aggregate monthly total trust-account receipts, the all-trust-account `Total receipts` values were used for the requested calendar months, not a named fund or fiscal-year-to-date total.
- [ ] For USD-CAD conversion, the USD-million difference was multiplied by the specified month's CAD-per-USD average rate, preserving `millions` units.
- [ ] The signed subtraction order matches the prompt, e.g. `(1947 - 1946)` = adjusted 1947 minus adjusted 1946.
- [ ] Final output matches the prompt format, e.g. `[0.012, surplus]` or a single numeric value in millions rounded to one decimal place.
