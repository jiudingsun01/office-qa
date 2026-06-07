---
name: treasury-bulletin-agency-outlays
description: Use for OfficeQA/Treasury Bulletin questions that ask for monthly or annual outlays/expenditures by individual federal agency, including sums across agencies with exclusions.
---

# Treasury Bulletin agency outlays

Use this when a question asks for outlays/expenditures for individual federal agencies in a Treasury Bulletin table, especially monthly values such as a single month across all listed agencies.

## Procedure

1. Locate the Treasury Bulletin table that reports outlays/expenditures by agency and month. These tables are normally in millions of dollars unless the table heading says otherwise.
2. Extract the column for the requested month/year exactly. For recent bulletins, monthly agency outlay tables can include both department/agency rows and separate non-agency subtotal/receipt rows.
3. Include only agency-specific rows when the question says “individual federal agencies” or “agency-specific outlay entries.”
   - Include department and named agency rows such as Department of Agriculture, Department of Defense, Department of Education, etc.
   - Apply any explicitly requested exclusions before summing, e.g. exclude Department of Commerce, Federal Emergency Management Agency, Department of the Interior.
4. Exclude non-agency rows even if they appear in the same table:
   - undistributed offsetting receipts
   - other offsetting receipts or receipt adjustments
   - totals/subtotals such as total outlays, total receipts, on-budget/off-budget totals
   - financing, deficit/surplus, or other memorandum lines
5. Preserve signs as printed for agency outlays. Negative agency entries are part of the sum unless the question says otherwise.
6. Sum the selected values in the printed units. If the table is in millions of dollars, the final answer is already in millions.

## Annual fiscal-year agency questions

- For questions asking about an agency's FY total on-budget and off-budget outlays, use the fiscal-year agency outlays table (usually units are millions of dollars) and the row for the named branch/agency. Do not use monthly receipt/deficit totals or undistributed offsetting receipt rows.
- "Total on-budget and off-budget outlays" means the combined printed total outlays for that agency/branch for each fiscal year. If separate on-budget/off-budget columns are printed, add them; if the table already prints a combined total column, use that.
- YoY growth from FY A-B inclusive is computed between adjacent fiscal years only: `(outlays[t] / outlays[t-1] - 1) * 100`, then take the arithmetic mean of those annual percentage rates unless the question explicitly asks for CAGR/geometric mean.
- For OLS of `ln(outlays)` on fiscal year index, use natural log and a simple 1-based sequential index over the selected fiscal years unless the prompt defines another index. Regression uses the unrounded outlay values.
- If the prompt gives conflicting rounding instructions (e.g. says the YoY percentage is rounded to hundredths but later says all numbers to thousandths), follow the field-specific rounding instruction for the YoY percentage and the general instruction for the remaining regression fields. OfficeQA gold has used `[2.81, slope, intercept]` rather than forcing YoY to three decimals in this case.

## Verification

- Reconcile by computing: printed total agency-like rows minus explicitly excluded agency rows, but do not use a grand total that includes undistributed offsetting receipts or other non-agency items unless you have separately removed those lines.
- Check that every included row names a specific agency/department and every excluded row is either explicitly named by the question or is a non-agency accounting line.

## Pitfalls

- Do not include “undistributed offsetting receipts” when asked for all listed agencies; it is not an agency.
- Do not accidentally subtract excluded agencies twice if starting from a subtotal.
- Do not convert millions to dollars unless the question asks for dollars rather than millions.