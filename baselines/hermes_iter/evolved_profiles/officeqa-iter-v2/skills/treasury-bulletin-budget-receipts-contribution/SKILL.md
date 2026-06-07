---
name: treasury-bulletin-budget-receipts-contribution
description: Use for OfficeQA/Treasury Bulletin questions asking for percentage contributions/shares of receipt categories such as net individual income taxes relative to total budget receipts, especially CY-to-CY changes.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [officeqa, treasury-bulletin, federal-finance, receipts, budget-receipts, tax-receipts, shares]
    related_skills: [treasury-bulletin-federal-receipts-exchange-rates]
---

# Treasury Bulletin Budget Receipts Contribution Questions

## When to Use

Use this skill for OfficeQA/Treasury Bulletin questions that ask for:

- The percent contribution/share of a named budget receipt category to total budget receipts.
- Receipt categories such as `net individual income taxes`, `corporation income taxes`, `employment taxes`, etc.
- A change in contribution between two calendar years (`CY2010` to `CY2011`) or other annual periods.
- Ordinary least squares regressions or summaries over annual fiscal-year receipt series, including `individual income tax receipts, net of refunds`.
- H-spread/interquartile-range questions over monthly nominal net budget receipt categories such as `corporation/corporate income taxes`.
- Nominal values from Treasury Bulletin budget receipt tables.

## Procedure

1. Locate the correct budget receipts table.
   - Search the bulletin/OCR/data for phrases like `budget receipts`, `total budget receipts`, `individual income taxes`, and the requested years.
   - Do not substitute `total receipts from the public`, `net receipts`, `trust fund receipts`, or cash-flow receipt tables unless the prompt explicitly asks for those. `Total budget receipts` is the denominator for contribution questions.

2. Identify the exact numerator row.
   - For prompts saying `nominal net individual income taxes`, use the row/category for `net individual income taxes`.
   - Avoid nearby gross/withheld/nonwithheld/refund rows if present. The requested numerator is the net category.

3. Match the period convention.
   - `CY2010` and `CY2011` mean calendar-year annual totals, not fiscal-year totals and not monthly values.
   - If source tables provide monthly columns, compute CY as January-December for that year unless an explicit annual CY column is available.
   - Keep both numerator and denominator in the same nominal unit; scaling cancels in the percentage share.

4. Compute each year's contribution percentage.
   - Formula: `contribution_pct_year = 100 * net_individual_income_taxes_year / total_budget_receipts_year`.
   - Preserve precision through the ratio calculation. Do not round the individual annual contributions before computing their change unless the question explicitly instructs intermediate rounding.

5. Compute the change.
   - For wording like `change in percent contribution ... from CY2010 to CY2011`, compute the percentage-point difference:
     `change = contribution_pct_2011 - contribution_pct_2010`.
   - Report with a percent sign if the benchmark/gold format includes one. Example formatting: `4.61%`.

6. For OLS regression questions over annual receipt series:
   - Use the named annual period exactly (`FY` means fiscal year; do not substitute CY or monthly receipt-from-the-public series).
   - Use the named net row exactly. For `individual income tax receipts, net of refunds`, use the net-of-refunds/individual-income-tax receipt series, not gross collections or total internal revenue.
   - Convert units only if the prompt requests it. If it asks for `billions of nominal dollars`, divide printed millions by 1,000 before fitting; do not CPI-adjust.
   - Fit `receipts = intercept + slope * year` using the year number untransformed (e.g. 1929, 1930, ...), not an index starting at 0 and not a centered year, unless explicitly requested.
   - Preserve full precision through the regression; round only final slope/intercept to the requested decimals.
   - For benchmark output rounding, use conventional decimal half-up / away-from-zero at the requested place rather than Python's binary floating `round()`/banker's rounding. This matters for intercepts very near a .0005 boundary (e.g. an intercept ending in `...1425` should report `...143` in magnitude). Use `Decimal(str(value)).quantize(Decimal('0.001'), rounding=ROUND_HALF_UP)` or equivalent on the final full-precision coefficient, and never recompute the intercept from the displayed/rounded slope.

7. For R-square/correlation questions between annual on-budget and off-budget receipts:
   - Use the `on-budget` and `off-budget` receipt rows/columns from the fiscal-year budget receipts table, not monthly `receipts from the public` and not total budget receipts.
   - `FY1991-2010` means one paired annual observation for each fiscal year 1991 through 2010, inclusive.
   - The September 1996, 2001, 2006, and 2011 bulletins together provide the needed fiscal-year spans; combine them by fiscal year and use the later bulletin when overlapping years have revised values.
   - Keep the data nominal. Do not CPI-adjust or convert to real dollars. Unit scaling does not affect R-square if both series are scaled consistently.
   - Compute `R-square` as the square of the Pearson correlation between the paired on-budget and off-budget nominal receipt series, or equivalently the R² from a simple OLS regression with intercept of one series on the other.
   - Preserve full precision in the paired data and round only the final R-square to the requested decimals.

8. For H-spread questions over monthly nominal net budget receipts:
   - Interpret `H Spread` as the interquartile spread `Q3 - Q1`.
   - Use the monthly `budget receipts` table and the exact named receipt category row, e.g. `corporation income taxes` / `corporate income taxes`. Do not use gross internal-revenue collection tables or `receipts from the public` unless the prompt explicitly says so.
   - `FY 2021` means the 12 fiscal-year months October 2020 through September 2021, not calendar-year 2021.
   - Convert printed monthly values from millions to billions when requested by dividing by 1,000.
   - If the prompt says to round intermediate values to tenths of billions before computing H spread, first round each monthly observation to one decimal billion, then compute quartiles on those rounded observations.
   - Use the standard linear-interpolation percentile method (`Type 7`, NumPy/R default): with sorted values `x[0..n-1]`, percentile `p` uses `h=(n-1)*p`, `lo=floor(h)`, `hi=ceil(h)`, and `Q=(1-frac(h))*x[lo]+frac(h)*x[hi]`. For quartiles use `p=0.25` and `p=0.75`.
   - Round only the final H spread to the requested precision after subtracting `Q1` from `Q3`.

## Common Pitfalls

- `Budget receipts` and `receipts from the public` are different Treasury concepts; use `total budget receipts` when that exact denominator is requested.
- Do not use fiscal-year (`FY`) data for `CY` questions. If the easy table is fiscal-year, keep looking for a CY annual table or sum Jan-Dec monthly data; for modern Treasury Bulletin receipt-share questions, using FY instead of CY can shift the answer by more than a full percentage point.
- Do not use gross individual income tax rows when the prompt asks for `net individual income taxes`.
- The requested change is a difference in contribution percentages (percentage points), not a percent growth rate of the contribution ratio. Compute `100*numerator/denominator` for each year at full precision, then subtract; do not subtract raw receipt totals or divide the change in numerator by the change/level of total receipts.
- Scaling (millions vs billions) cancels in the share only if numerator and denominator use the same units.
- For H-spread tasks, fiscal-year monthly windows run Oct-Sep; using Jan-Dec changes the quartiles.
- For prompts requiring intermediate tenths, round each monthly billion-dollar observation to one decimal before Type 7 quartiles; do not compute quartiles from full-precision millions and round afterward.

## Verification Checklist

- [ ] Denominator row is exactly `total budget receipts`.
- [ ] Numerator row is exactly `net individual income taxes` or the named net receipt category.
- [ ] Years are calendar years, not fiscal years.
- [ ] Contribution is computed as numerator / denominator * 100 for each year.
- [ ] Change is later year contribution minus earlier year contribution.
- [ ] For H-spread tasks, values are the 12 FY monthly observations (Oct-Sep), converted to requested units.
- [ ] If instructed, monthly values are rounded to tenths before Type 7 Q1/Q3 are computed; H spread is `Q3 - Q1`.
- [ ] Final answer is rounded to requested precision and includes `%` when appropriate.
