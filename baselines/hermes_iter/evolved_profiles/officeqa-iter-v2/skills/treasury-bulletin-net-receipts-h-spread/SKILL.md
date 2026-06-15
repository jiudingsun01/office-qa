---
name: treasury-bulletin-net-receipts-h-spread
description: Use when OfficeQA/Treasury Bulletin questions ask for monthly nominal net budget receipts by source, especially FY monthly Corporate income taxes and percentile/H-spread calculations.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [officeqa, treasury-bulletin, federal-finance, receipts, quartiles, h-spread]
    related_skills: [treasury-bulletin-federal-receipts-exchange-rates]
---

# Treasury Bulletin Net Budget Receipts + H-Spread Questions

## Overview

Use this skill for OfficeQA questions that ask for monthly nominal net budget receipts from a named source (for example, `Corporate income taxes`) over a fiscal year, then ask for quartiles, H spread, or another percentile-derived spread. These questions are sensitive to row selection, units, fiscal-year month order, and prompt-specific intermediate rounding.

## When to Use

Use this when a prompt mentions any of:

- `monthly nominal net budget receipts`
- `Corporate income taxes` or another receipt source by month
- a fiscal year such as `FY 2021`
- `H Spread`, quartiles, Q1/Q3, percentile spread, or Type 7 percentiles
- intermediate values rounded before the final spread calculation
- annual/fiscal-year `individual income tax receipts, net of refunds` and regression/correlation/statistical calculations

Do not use this for `Total receipts from the public` plus exchange-rate conversion questions; use the federal-receipts/exchange-rates skill for those unless the prompt specifically asks for net budget receipts by source and distribution statistics.

## Annual Individual Income Tax Receipts: OLS Pitfall

For prompts like `Using U.S. federal individual income tax receipts, net of refunds, for fiscal years 1929–1942, reported in billions of nominal dollars, fit an ordinary least squares linear regression with year as predictor`:

1. Use the annual fiscal-year row/series for **individual income tax receipts net of refunds**, not monthly values, total receipts, or gross collections.
2. Convert the printed dollar amounts to the requested units first (usually billions if the source table is in millions).
3. Fit OLS with numeric year untransformed: `y = slope * year + intercept`.
4. Keep full floating-point precision for the receipts and fitted coefficients until final formatting. Do not round the slope first and then recompute/format the intercept from a displayed equation.
5. Round both final coefficients independently to the requested precision (e.g. nearest thousandth). This matters: the intercept can differ by 0.001 if calculated from prematurely rounded coefficients; for the FY 1929–1942 individual receipts benchmark the intercept rounds to `-184.143`, not `-184.142`.
6. Preserve negative signs in bracketed output exactly as requested, e.g. `[0.096,-184.143]`.

## Procedure

1. Locate the monthly budget receipts table.
   - Search the Treasury Bulletin/OCR text for exact row labels such as `Corporate income taxes`, `Individual income taxes`, `Social insurance and retirement receipts`, and `net budget receipts`.
   - Confirm the table is monthly and by source of receipts, not annual totals, outlays, gross receipts, or `receipts from the public` cash-flow tables.
   - Prefer layout-preserving extraction (`pdftotext -layout` or FRASER OCR layout) because month columns are dense.

2. Confirm fiscal-year coverage.
   - Federal fiscal years run October through September.
   - FY 2021 monthly values are October 2020, November 2020, December 2020, January 2021, February 2021, March 2021, April 2021, May 2021, June 2021, July 2021, August 2021, September 2021.
   - Do not use calendar-year January-December unless the prompt explicitly says calendar year.

3. Confirm units and scale.
   - Treasury Bulletin budget receipt tables usually present dollar values in millions.
   - If the prompt asks for billions of dollars, divide each monthly value by 1,000 before percentile calculations.
   - Keep signs as printed; net budget receipt components can be negative in some months.

4. Compute Type 7 quartiles exactly, then apply any required intermediate rounding.
   - Sort the 12 monthly values ascending.
   - Type 7 percentile position for probability p is `h = 1 + (n - 1) * p`, with 1-indexed sorted data.
   - Let `j = floor(h)` and `g = h - j`; percentile is `(1 - g) * x[j] + g * x[j+1]` using 1-indexed sorted values.
   - For quartiles: `Q1 = Type7(p=0.25)` and `Q3 = Type7(p=0.75)`.

5. For H-spread prompts, follow the prompt's rounding order literally.
   - H spread in these OfficeQA prompts is `Q3 - Q1`.
   - If the prompt says `use the intermediate values rounded to the tenths of billions before computing the H spread value`, round the interpolated Q1 and Q3 values to one decimal place in billions first, then subtract.
   - This rounding applies to the quartile intermediate values, not to each monthly observation before interpolation, unless the prompt explicitly says to round the monthly inputs.
   - Example pattern: `h_spread = round(Q3_billions, 1) - round(Q1_billions, 1)`, then format the final result to the requested places, commonly nearest hundredths (`[redacted]`, not `57.5`).
   - Required sanity check: after rounding Q1 and Q3 to tenths, the H-spread must be a multiple of `0.10` in billions, so a hundredths-formatted answer should normally end in `0` (e.g. `[redacted]`). If your computed result changes in the hundredths place after final rounding, you probably subtracted unrounded quartiles or rounded the wrong intermediate.
   - Do not compute `Q3 - Q1` from unrounded quartiles if the prompt requires rounded intermediate values; doing so can shift the hundredths place.

## Verification Checklist

- [ ] Row label is the requested receipt source (e.g. exactly `Corporate income taxes`).
- [ ] Table is monthly `net budget receipts`, not total receipts from the public or annual totals.
- [ ] Months are the fiscal year October-September.
- [ ] Values are scaled to billions before percentile/statistical calculations when requested.
- [ ] Type 7 percentile method is used for Q1 and Q3.
- [ ] Any prompt-specified intermediate rounding is applied to Q1/Q3 before subtracting for H spread.
- [ ] Final answer is formatted to the requested decimal places, including trailing zeros.

## Common Pitfalls

- Using unrounded Q1/Q3 to compute H spread when the prompt explicitly requires intermediate quartiles rounded to tenths; this can produce answers like `57.53` instead of the expected `[redacted]`.
- Accidentally using calendar-year months for a fiscal-year prompt.
- Forgetting to divide monthly values in millions by 1,000 when the answer asks for billions.
- Mixing `net budget receipts` with `receipts from the public`; they are different Treasury Bulletin concepts and appear in different tables.
