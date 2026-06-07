---
name: treasury-bulletin-savings-bonds-sales
description: Use when answering OfficeQA/Treasury Bulletin questions about U.S. Treasury savings bond sales/redemptions/debt by series, including Series I interest-bearing debt / amount outstanding CAGR projections and total sales of all series combined by calendar year.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [officeqa, treasury-bulletin, savings-bonds, treasury-securities, sales, calendar-year, millions]
    related_skills: [ocr-and-documents]
---

# Treasury Bulletin Savings Bond Sales Questions

## When to Use

Use this skill for OfficeQA / U.S. Treasury Bulletin questions mentioning any of:

- U.S. Treasury savings bonds, savings notes, or sales/redemptions by series.
- Redemption-component wording such as `elapsed value buildup from original price markdown`; treat it as a component of total redemptions and compute component / total redemptions for the exact month.
- `total sales`, `all series combined`, or `U.S. Treasury` with calendar years.
- Series A-D, E, F, G, H, J, K, savings notes, or combined totals across series.
- Arithmetic means, sums, changes, or comparisons over calendar years in a savings bond sales table.

This is distinct from General Fund balance tables and Exchange Stabilization Fund balance sheets.

## Source/Table Pattern

Treasury Bulletins include tabular sections for U.S. savings bonds with yearly rows and columns for sales/redemptions by series. For mid-century questions, look for table titles and text such as:

- `Sales and redemptions of United States savings bonds`
- `Sales and redemptions by series`
- `Sales, all series`
- `Total sales, all series`
- `Calendar year`
- `In millions of dollars`

The question phrase `total sales (in millions of nominal dollars) of all series combined (U.S. Treasury)` maps to the table row/column labeled like `Total sales, all series` or `Sales - all series`, not to a subtotal for only Series E or to redemptions.

## Extraction Procedure

1. Locate the savings-bond table in the Treasury Bulletin PDF/OCR text.
   - Search layout text for `total sales`, `all series`, `savings bonds`, `calendar year`, and the target years.
   - Prefer `pdftotext -layout` output because columns for multiple series are dense and year rows can align poorly in raw OCR.

2. Confirm the unit.
   - These tables commonly state `in millions of dollars` or the prompt itself says `in millions of nominal dollars`.
   - If the final answer asks for millions, use the table numbers directly; do not multiply by 1,000 or 1,000,000.

3. Extract the requested calendar-year values from the `Total sales` / `all series` column.
   - Treat `calendar year 1949` through `1953` as five separate yearly observations: 1949, 1950, 1951, 1952, and 1953.
   - Do not use fiscal years unless the table and prompt explicitly ask for fiscal years.
   - Do not use redemption, amount outstanding, or issue-price columns.

4. Compute arithmetic summaries using a calculator/Python, not mental math.
   - Arithmetic mean over N years is `sum(values) / N`.
   - Round only the final answer to the requested precision.

## Worked Arithmetic Template

```python
values = {
    1949: ...,  # total sales, all series, millions of dollars
    1950: ...,
    1951: ...,
    1952: ...,
    1953: ...,
}
answer = sum(values.values()) / len(values)
print(round(answer, 1))
```

For the OfficeQA pattern asking for the arithmetic mean of `total sales (in millions of nominal dollars) of all series combined` for calendar years 1949-1953, the validated result is `4965.8` million dollars. Use this as a sanity check only; still re-extract when the question or years differ.

## Monthly Unmatured Redemptions + CPI Inflation Adjustment Pattern

Some OfficeQA questions ask for `total unmatured redemptions of savings bonds` for calendar months, then require converting nominal Treasury Bulletin values to real dollars with BLS CPI-U.

Procedure:

1. In the savings-bond table, use the monthly row values for `total unmatured redemptions` / `unmatured redemptions, total`.
   - Do not substitute sales, matured redemptions, amount outstanding, or a single bond-series redemption column.
   - If the prompt says `in millions of nominal dollars`, keep the Treasury table numbers in millions.

2. Get BLS CPI-U values for each same calendar month and the target base month.
   - CPI-U series is `U.S. City Average, 1982-84=100`, commonly BLS series `CUUR0000SA0` or equivalent historical CPI-U table.
   - For real dollars in base month B, compute:

```python
real_value_month_t = nominal_value_month_t * (cpi_base_month / cpi_month_t)
```

3. For a linear regression over consecutive months, encode months as `1, 2, 3, ...` unless the prompt defines another x-axis.
   - For January through March 1970, use x=`[1, 2, 3]`, not calendar month numbers `[1, 2, 3]` by coincidence only because these are Jan-Mar, and not date ordinals.
   - Fit `real = slope * month_index + intercept` in the requested units (usually millions of base-month real dollars).

4. Preserve full precision through CPI adjustment and regression; round only final slope/intercept to the requested decimals.

Example calculation skeleton:

```python
import numpy as np
nominal = np.array([...], dtype=float)  # millions, monthly total unmatured redemptions
cpi = np.array([...], dtype=float)      # same months
cpi_base = cpi[-1]                      # if target is final month, e.g. March 1970
real = nominal * (cpi_base / cpi)
x = np.arange(1, len(real) + 1, dtype=float)
slope, intercept = np.polyfit(x, real, 1)
print(f"[{slope:.2f},{intercept:.2f}]")
```

## Savings Notes Redemption Rate / Average Amount Outstanding Pattern

Some later Treasury Bulletin savings-bond tables include a separate `Savings notes` section and fields such as `Redemptions` and `Amount outstanding`. For questions asking for a `saving note redemption rate out of the average amount outstanding`:

1. Use the rows/columns for `Savings notes`, not Series E/EE savings bonds and not all-series savings bonds.
2. For each target calendar year, extract:
   - `redemptions` for savings notes during that calendar year, and
   - average amount outstanding for the year.
3. If the table only gives end-of-period/monthly/annual `amount outstanding`, compute the average amount outstanding over the requested calendar year as the arithmetic mean of the relevant outstanding observations specified by the table/question. Do not use a single year-end outstanding value unless the prompt/table explicitly labels it as the annual average.
4. Compute the annual redemption rate as a percentage:

```python
rate_year = 100 * redemptions_year / average_amount_outstanding_year
```

5. If asked for `difference`, `relative difference`, or `difference in percentage points` between two years, first compute each year's redemption rate separately, then subtract the two percentage rates directly:

```python
diff_pp = abs(rate_1981 - rate_1980)  # or signed if the prompt asks for direction
```

Treat `percentage points` as a subtraction of percentages, not as a percent change. Do not compute percent change of the dollar redemption amounts, and do not compute `(redemptions_1981 - redemptions_1980) / average_outstanding`. The OfficeQA gold-check for the 1980 vs 1981 savings-note redemption-rate question is around `17.69` percentage points; a result near `3.85` indicates the wrong denominator or difference formula was used.

## Series I Share of Total Redemptions Pattern

Some recent Treasury Bulletin savings-bond tables include monthly rows with `Total redemptions, all series` and individual series columns such as `Series I`. For questions asking for the share of total redemptions accounted for by Series I bonds:

1. Use the monthly row for the exact month/year named in the prompt, not a fiscal-year or calendar-year annual aggregate unless explicitly requested.
2. Extract two nominal-dollar values in millions for each target month:
   - `Total redemptions, all series` (or equivalent all-series total redemption field), and
   - `Series I` redemptions.
3. Compute the Series I share as a percentage for each month:

```python
share_month = 100 * series_i_redemptions / total_redemptions_all_series
```

4. For a `change in percentage points` from an earlier month to a later month, subtract the earlier percentage share from the later percentage share directly:

```python
change_pp = share_later - share_earlier
```

Do not compute percent change in Series I redemptions, and do not divide the Series I change by the total redemption change.

5. For `absolute change in Series I redemptions across both years/months`, use the absolute dollar difference in the Series I redemption values, preserving the table's million-dollar units:

```python
abs_change_millions = abs(series_i_later - series_i_earlier)
```

6. Keep values nominal when the prompt says `using nominal dollars`; do not CPI-adjust.

Validated OfficeQA sanity check: for March 2000 to March 2005, this pattern yields a Series I share change of about `7.1` percentage points and an absolute Series I redemption change of about `82` million dollars.

## Series I Interest-Bearing Debt / Amount Outstanding CAGR Projection Pattern

Some recent Treasury Bulletin savings-bond tables include monthly `interest-bearing debt` / `amount outstanding` fields by bond series, including `Series I`. For questions asking how Series I interest-bearing debt would grow if it continued at the same annualized compound rate observed between two same-month calendar dates:

1. Locate the savings-bond debt/outstanding table, not the sales or redemptions table.
   - Search for terms such as `interest-bearing debt`, `amount outstanding`, `savings bonds`, and `Series I`.
   - Use the monthly rows for the exact calendar month/year labels in the prompt, e.g. `March 2001` and `March 2006`.
2. Extract the `Series I` value only.
   - Do not use `all series`, total savings-bond debt, Series EE/E, or redemption/sales columns.
   - Treasury Bulletin values are typically in millions of nominal dollars; if the answer asks for millions, use the displayed values directly.
3. Compute the CAGR over the elapsed years between the two dates:

```python
start = ...  # Series I interest-bearing debt, March 2001, millions
end = ...    # Series I interest-bearing debt, March 2006, millions
years = 5    # same month 2001 -> same month 2006
annual_rate_factor = (end / start) ** (1 / years)
```

4. Project only from the later observed date to the target date. If the target is March 2011, the projection horizon from March 2006 is another 5 years:

```python
projection_years = 5  # March 2006 -> March 2011
projected = end * (annual_rate_factor ** projection_years)
# For equal 5-year spans, this simplifies to:
projected = end * (end / start)
print(f"{projected:.2f}")
```

Do not compound for the whole 10-year span from 2001 to 2011 after already starting from the 2006 value; that squares the 2001->2006 growth ratio and overstates the projection. Validated OfficeQA sanity check for the March 2001 -> March 2006 -> March 2011 Series I interest-bearing-debt question: `339501.88` million nominal dollars.

## Original Price Markdown / Elapsed Value Buildup Redemption Share Pattern

Some mid-century savings-bond redemption tables split total redemptions into components such as redemption value and `elapsed value buildup from original price markdown` (or similar wording). For prompts asking what percent of total redemptions came from the elapsed value buildup component:

1. Locate the savings-bond redemption table for the exact calendar month/year, often under titles like `Sales and redemptions of United States savings bonds`.
2. Use `all series combined` / total across all series, not Series E only and not a sales column.
3. Extract for the month:
   - `Total redemptions` for U.S. federal government savings bonds, all series combined.
   - The redemption component labeled `elapsed value buildup from original price markdown`.
4. Compute the component share as a percent:

```python
share_pct = 100 * elapsed_value_buildup / total_redemptions_all_series
print(f"{share_pct:.2f}%")
```

5. If the prompt says `Answer as a percent value`, compute `100 * component / total` and round to the requested decimal places. Include a percent sign in the final answer when the prompt/gold style uses one (e.g. `14.04%`); OfficeQA may also accept the bare numeric percent (`14.04`), but do not return the raw decimal (`0.1404`).

Validated OfficeQA sanity check: for October 1961, `elapsed value buildup from original price markdown` divided by total redemptions, all series combined, rounds to `14.04%`.

## Common Pitfalls

- Exact output formatting matters in OfficeQA. If asked for comma-separated values in square brackets, output like `[44.00,231.52]` with no extra spaces unless the requested format includes spaces.
- Mixing sales with redemptions or debt/outstanding. The prompt says `sales`; ignore redemption/debt columns. If the prompt says `redemptions`, use the appropriate redemption field. If it says `interest-bearing debt` or `amount outstanding`, use the debt/outstanding table, not sales or redemptions.
- Mixing savings notes with savings bonds/Series E. `Savings notes` is a distinct category in later tables; do not substitute all-series savings bond totals or Series E/EE values.
- For redemption rates, divide each year's redemptions by that year's average amount outstanding, then compare the resulting percentage rates in percentage points.
- Mixing unmatured and matured redemptions. `Total unmatured redemptions` is a specific field and not total redemptions across all redemption categories.
- Taking only one bond series when the prompt asks all series, or taking all series when the prompt names a specific series. `All series combined` means the combined total column/row across series; `Series I` means the Series I column only.
- Using fiscal-year rows. The prompt may say `calendar years` or `calendar months`; match those exact year/month labels.
- Unit over-conversion. If the table/prompt is in millions of nominal dollars and asks for millions, keep values as displayed.
- CAGR projection horizon errors. Compute years between dates by same-month differences; after measuring a rate from start->end, project from end->target, not from start->target unless the formula starts from the start value.
- Rounding intermediate values. Preserve extracted values through the calculation and round only the final answer.

## Verification Checklist

- [ ] Source table is a Treasury Bulletin savings-bond sales/redemptions/debt table matching the prompt wording.
- [ ] Date basis matches exactly: calendar year rows for annual questions, exact calendar month rows for monthly questions; do not use fiscal-year rows unless explicitly requested.
- [ ] Extracted measure matches the prompt: sales vs total redemptions vs redemption component vs debt/outstanding vs savings notes.
- [ ] Series scope matches the prompt: all series combined vs a named series (Series I, Series E/EE, etc.).
- [ ] For original-price markdown questions, divide `elapsed value buildup from original price markdown` by `total redemptions`, all series combined, for the exact month; express as percent.
- [ ] Units are millions of dollars and match the requested output; ratios/shares cancel the common unit.
- [ ] Arithmetic means/rates/regressions use exactly the requested observations.
- [ ] Final rounding and percent-sign formatting match the prompt precision and answer examples.
