---
name: treasury-bulletin-federal-department-expenditures
description: Use for OfficeQA/Treasury Bulletin questions asking for U.S. Federal Department or agency spending/expenditures/outlays by fiscal year, including highest-spending department questions.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [officeqa, treasury-bulletin, federal-budget, expenditures, departments, agencies, fiscal-year]
    related_skills: [treasury-bulletin-federal-outlays-boxcox, treasury-bulletin-budget-deficit-projections]
---

# Treasury Bulletin Federal Department / Agency Expenditures

## When to Use

Use this skill when an OfficeQA Treasury Bulletin prompt asks about:

- Spending, expenditures, or outlays by U.S. Federal Department, bureau, or agency.
- The highest/lowest spending Federal Department in a fiscal year.
- A named fiscal year such as 1955, 1960, etc., where the answer is requested in nominal dollars or millions of nominal dollars.

Do not use aggregate deficit/surplus tables for these questions. The relevant source is the department/agency expenditure table, not the receipts/deficit summary and not functional categories unless the prompt explicitly asks for functions.

## Source Pattern

Treasury Bulletins include federal budget expenditure tables listing departments and agencies as rows and fiscal-year columns. In mid-century bulletins, these tables commonly report amounts in `millions of dollars`.

Typical rows can include Cabinet departments and subcategories such as:

- `Department of Defense` / `Military functions`
- `Department of Agriculture`
- `Department of Health, Education, and Welfare`
- other departments, independent agencies, legislative/judicial branches, and totals

For prompts asking for the highest-spending U.S. Federal Department, scan department/agency rows and exclude aggregate rows such as `Total`, `Total budget expenditures`, subtotals, and non-department summary lines. If a department is printed with multiple function subrows, compute the department total by summing those subrows unless the prompt asks for a specific function. Important mid-century example: Defense may appear as `Department of Defense—Military functions` and `Department of Defense—Civil functions`; a department-level prompt needs military + civil, not the military subrow alone.

## Procedure

1. Identify the exact Treasury Bulletin issue and locate the federal budget expenditures/outlays by department/agency table.
   - Use the contents/index when available; search for phrases like `expenditures by agencies`, `expenditures by department`, `budget expenditures`, `outlays by agency`, `budgetary and trust fund`, or the department name (for example `Department of Labor`).
2. Confirm the table units from the title/header/notes. Mid-century tables often use millions of dollars; modern fiscal-year outlay tables may still be in millions.
3. Select the requested fiscal-year column, not calendar-year months and not a later estimate unless the prompt asks for an estimate.
4. If the prompt says figures include both budgetary and trust-fund flows, use the combined/total outlays line or table section that includes both budgetary and trust-fund transactions. Do not use a budget-only column, a trust-fund-only column, or net budget authority.
   - In modern Treasury Bulletin `Federal Fiscal Operations` / budget results tables, `Department of Defense--Military` (or `Military programs`) is the agency row used for Department of Defense outlays. Do **not** substitute the functional `National defense` category; it includes non-DOD defense-related spending and can be much larger (for example about 732,852 in FY 2020, which is not the DOD agency value). Also do not add unrelated defense function rows unless the table explicitly presents them as Department of Defense subrows.
5. For highest-spending questions:
   - Extract all department/agency row values for the fiscal-year column.
   - Strip commas and footnote/revision markers such as `(r)` before numeric conversion.
   - Ignore totals, grand totals, and subtotal/summary rows that are not a Federal Department or agency.
   - If the same Federal Department is split across rows by function, sum those rows first (for example Defense military functions + Defense civil functions) before comparing against other departments.
   - Compare values in the table units after normalizing signs and missing values.
6. Return the amount in the unit requested by the prompt.
   - If the prompt asks for `millions of nominal dollars` and the table is in millions, report the table value directly, e.g. `36080 million` rather than converting to billions or raw dollars.

## Growth, Decay, Average YoY, and Regression Calculations

For questions comparing a department's outlays between fiscal years:

1. Let `start` be the earlier fiscal-year outlay and `end` be the later fiscal-year outlay, using the same row/table definition and units for both. Units cancel for rates.
2. Number of annual intervals is `n = later_fy - earlier_fy` (FY 2011 to FY 2019 means `n = 8`, not 9).
3. Compound annual growth rate: `CAGR = (end / start) ** (1 / n) - 1`.
4. Annual decay factor: `decay_factor = 1 + CAGR = (end / start) ** (1 / n)`. If outlays declined, this is less than 1.
5. Average Year-over-Year growth over an inclusive fiscal-year range is usually the arithmetic mean of each adjacent annual percentage change, not the CAGR: for values `v_2007 ... v_2013`, compute `mean([(v_t / v_{t-1} - 1) * 100 for t in 2008..2013])`. There are `last_fy - first_fy` YoY rates for an inclusive range.
6. For prompts that ask for `arc elasticity (using midpoint percentage change)` after computing CAGR/annual decay factor between two fiscal-year outlay values, treat the requested arc value as the midpoint percentage change in the outlay itself: `arc = (end - start) / ((end + start) / 2)`. Do **not** divide by the midpoint percentage change in the fiscal-year labels unless the prompt explicitly defines a second economic variable for elasticity. Example: FY 2011 to FY 2019 Department of Labor total outlays using budgetary + trust-fund flows has CAGR `-0.153`, annual decay factor `0.847`, and arc value `-1.162`; dividing by `(2019-2011)/((2019+2011)/2)` incorrectly gives about `-292.6`.
7. For OLS regressions of `ln(outlays)` on a fiscal-year index, use `ln` as the natural logarithm and treat the fiscal-year index as 1-based sequential positions (`1..n`) unless the prompt explicitly defines `0..n-1` or actual years. This affects the intercept by one slope; the slope is unchanged by shifting the index.
8. Keep full precision through all calculations; round only final requested outputs. If the prompt requests decimal-form rates in brackets, output like `[CAGR, decay_factor, arc_elasticity]`, not percentages. If the prompt gives conflicting rounding instructions (for example, says YoY percent to hundredths and later says all numbers to thousandths), follow the metric-specific rule attached to each metric rather than the later global sentence: YoY percent to hundredths, regression slope/intercept to thousandths. Example: Judicial Branch FY 2007-2013 average YoY `2.804...%` must be emitted as `2.81`, not `2.804`, while OLS values remain `0.030, 8.706`.

## Monthly Agency Outlay Summations

For prompts asking to sum reported monthly outlays for individual federal agencies (for example, January 2003):

1. Locate the agency/outlay table whose columns are months or fiscal-year-to-date periods. Confirm the unit, commonly `millions of dollars`.
2. Use only rows that are specific departments, agencies, or agency components listed by name.
3. Exclude rows that are not agency-specific even if they appear in the same table, especially:
   - `Undistributed offsetting receipts`
   - totals, subtotals, and grand totals
   - deficit/surplus or financing lines
   - other non-agency summary items
4. Apply any prompt-specified exclusions exactly. If the prompt says to exclude the Department of Commerce, FEMA, and the Department of the Interior, omit those rows in addition to the non-agency rows above.
5. Strip commas/footnote markers and preserve signs as printed for each included agency-specific outlay entry. Sum in table units; if the table is in millions and the answer asks for millions, report the integer sum directly.
6. Verify by independently checking that excluded named agencies and all undistributed offsetting receipt rows did not enter the arithmetic.

## Percentiles and Distribution Calculations

For prompts asking for a Hazen percentile of department/agency outlays across an inclusive fiscal-year range:

1. Extract one value per fiscal year from the same row/table definition, preserving the table units (modern outlay tables are commonly in millions of dollars).
2. Sort the values ascending before applying the percentile formula.
3. Hazen plotting positions are `p_i = (i - 0.5) / n` for sorted rank `i = 1..n`. To compute a requested percentile `p` as a quantile, use rank `h = p * n + 0.5`.
   - If `h` is an integer, return the sorted value at that 1-based rank.
   - Otherwise linearly interpolate between ranks `floor(h)` and `ceil(h)`.
   - Clamp only if `h < 1` or `h > n` (unusual for benchmark percentiles); do not use Excel `PERCENTILE.INC`/`EXC` unless the prompt asks for them.
4. Example: for FY 2011-FY 2020 there are `n = 10` values. The 85th Hazen percentile has `h = 0.85 * 10 + 0.5 = 9.0`, so it is exactly the 9th sorted value, not an interpolation between the 8th and 9th or 9th and 10th values.
5. Round only the final percentile to the requested precision (for example nearest hundredths) and keep the source units in the answer.

Recommended scratch pattern:

```python
vals = [ ... ]  # one value per FY, in table units
vals = sorted(vals)
p = 0.85
n = len(vals)
h = p * n + 0.5
if h <= 1:
    q = vals[0]
elif h >= n:
    q = vals[-1]
elif abs(h - round(h)) < 1e-12:
    q = vals[int(round(h)) - 1]
else:
    lo = int(h)          # 1-based floor rank
    frac = h - lo
    q = vals[lo - 1] + frac * (vals[lo] - vals[lo - 1])
print(round(q, 2))
```

## Unit and Rounding Rules

- Preserve nominal-dollar table values; do not inflation-adjust unless explicitly requested.
- If the source table is in millions and the prompt asks for millions, no scaling is needed.
- If the prompt asks for raw dollars, multiply million-denominated table values by 1,000,000.
- Keep full printed integer precision; do not add decimals unless the prompt requests them.
- Parenthetical markers such as revision notes are annotations, not negative numbers.

## Verification Checklist

- [ ] The column is the requested fiscal year, not a calendar year or month.
- [ ] The row set is department/agency expenditures, not functional outlays or deficit totals.
- [ ] Totals and subtotals are excluded from `highest department` comparisons.
- [ ] Units are read from the table and match the final answer wording.
- [ ] Footnote/revision markers have been removed without changing the numeric value.
- [ ] For mixed rounding prompts, apply the metric-specific precision even if a later sentence gives a global precision. Example: if YoY growth says nearest hundredths but slope/intercept are thousandths, output YoY with 2 decimals and OLS values with 3 decimals.

## Pitfalls

- Accidentally using total federal expenditures as the `highest department` value.
- Comparing functional categories such as `national defense` instead of department/agency rows when the prompt asks for a Federal Department.
- Converting a table already in millions into billions because the number looks large.
- Treating a fiscal year as the calendar year ending in December; use the fiscal-year column printed in the table.
- For prompts asking for `arc elasticity (using midpoint percentage change)` with only start/end outlay values, return the midpoint percentage change in outlays: `(end - start) / ((end + start) / 2)`. Do not divide by the midpoint percentage change in the year labels unless a second economic variable is explicitly specified.
