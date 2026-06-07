---
name: treasury-bulletin-nonbanking-foreign-currency-positions
description: Use for OfficeQA/Treasury Bulletin questions about U.S. nonbanking firms' foreign-currency positions by currency, including comparisons, correlations, or calculations across quarterly/monthly dates.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [officeqa, treasury-bulletin, foreign-currency-positions, nonbanking-firms, correlation]
    related_skills: [treasury-bulletin-capital-movements]
---

# Treasury Bulletin: Nonbanking Firms' Foreign-Currency Positions

## When to Use

Use this skill when an OfficeQA/Treasury Bulletin prompt mentions:
- the U.S. Treasury report on nonbanking firms' foreign-currency positions
- U.S. nonbanking business firms/enterprises and their foreign-currency positions
- positions denominated in Belgian francs, Canadian dollars, Swiss francs, Deutsche marks, Japanese yen, pounds sterling, etc.
- calculations over calendar months such as December 1975, March 1976, June 1976, September 1976
- Pearson correlation, ratios, changes, or comparisons between currency columns

This is distinct from Capital Movements liabilities/claims tables: these tables are denominated in current foreign-currency units, usually millions, not U.S. dollars or thousands of dollars.

## Source/Table Pattern

The relevant Treasury Bulletin material is a special report/table series for nonbanking firms' foreign-currency positions. Rows are reporting months (often quarter-end months) and columns are currencies. The column labels may use currency names rather than country names, e.g. "Belgian francs" and "Canadian dollars".

For the mid-1970s questions, look for quarter-end calendar months such as:
- Dec. 1975
- Mar. 1976
- June 1976
- Sept. 1976

Values are in "millions of current foreign-currency units". Keep the printed values as-is for correlations and ratios unless the prompt explicitly asks for another unit. Do not convert to U.S. dollars.

## Procedure

1. Locate the exact report/table.
   - Search the PDF/text for: `nonbanking`, `foreign-currency positions`, `Belgian`, `Canadian`, or the requested currency names.
   - Use layout-preserving extraction (`pdftotext -layout`) or rendered page inspection because currency columns can be dense and easy to shift.

2. Match the requested dates exactly.
   - Treat months like "December 1975" as the row labeled `Dec. 1975` (or equivalent), not a fiscal-year period.
   - If the table reports quarter-end months, use only the specified month rows; do not interpolate missing intervening months.

3. Match the requested currency columns exactly.
   - Use `Belgian francs` for Belgian-franc positions and `Canadian dollars` for Canadian-dollar positions.
   - Do not use country totals, U.S.-dollar equivalents, or all-currency totals unless the prompt asks for them.

4. Preserve signs and units.
   - Positions may be positive or negative; keep the sign in any arithmetic.
   - Values are in millions of current foreign-currency units. For Pearson correlation, multiplying a column by a constant would not change the result, but converting currencies is still wrong and may introduce errors.

5. Compute requested statistics directly from the paired rows.
   - For Pearson correlation across N selected months, create paired vectors in the same date order and compute the standard sample Pearson correlation:
     `r = sum((x_i-mean(x))*(y_i-mean(y))) / sqrt(sum((x_i-mean(x))^2) * sum((y_i-mean(y))^2))`
   - Python verification example:
     `python - <<'PY'\nimport numpy as np\nx=[...]\ny=[...]\nprint(np.corrcoef(x,y)[0,1])\nPY`
   - Round only the final result to the requested precision (usually four decimal places).

## Common Pitfalls

- Confusing these tables with Capital Movements tables denominated in dollars/thousands of dollars.
- Converting foreign-currency values to U.S. dollars when the prompt asks for current foreign-currency units.
- Dropping negative signs in positions.
- Using a total/all-currency column instead of the named currency column.
- Misreading `Dec. 1975` as a fiscal-year endpoint rather than a calendar month row.
- Misaligning dense/wrapped currency columns. In layout text, headers can wrap across multiple lines; do not count columns from a single header line. Reconstruct the full header stack and verify each numeric token against the intended currency.
- Using the wrong table/panel when several nonbanking foreign-currency-position panels appear. Prefer the panel whose title/units match the prompt exactly: "positions" in "millions of current foreign-currency units" for the named currencies and months.
- Manually computing correlation with inconsistent rounding; keep full table values and round only the final coefficient.

## Correlation Workflow Guardrails

For Pearson-correlation prompts, add a transcription audit before finalizing:

1. Build a 2-column table with exactly one row per requested date, e.g. `date | Belgian francs | Canadian dollars`.
2. Record the source page/table/panel for those values and confirm the units line says current foreign-currency units, normally millions.
3. Check that the two vectors are paired by the same dates in the same order; sorting by value or dropping a date changes the answer.
4. Compute Pearson once with an explicit formula and once with `numpy.corrcoef`; investigate any mismatch before rounding.
5. If the coefficient differs from an expected benchmark or sanity check, first suspect column drift caused by wrapped headers or a nearby similarly named panel, not the correlation formula.

## Verification Checklist

- [ ] The source text/table explicitly concerns nonbanking firms' foreign-currency positions.
- [ ] The selected panel/table title and units match the prompt, not merely a nearby report with the same currencies.
- [ ] Rows match the requested calendar months exactly.
- [ ] Columns match the requested currencies exactly after reconstructing wrapped headers.
- [ ] Units are kept as millions of current foreign-currency units; no FX conversion was applied.
- [ ] Signed values are preserved.
- [ ] Pearson correlation is computed on paired values and rounded only at the end.
