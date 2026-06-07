---
name: treasury-bulletin-federal-outlays-boxcox
description: Use for OfficeQA/Treasury Bulletin questions that compare Box-Cox transformed U.S. federal outlay categories such as net interest across fiscal years or comparable fiscal periods.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [officeqa, treasury-bulletin, federal-budget, outlays, net-interest, box-cox, transformations]
    related_skills: [treasury-bulletin-budget-deficit-projections]
---

# Treasury Bulletin Federal Outlays and Box-Cox Transformations

## When to Use

Use this skill when an OfficeQA Treasury Bulletin prompt asks about:

- U.S. federal government outlays by category or function, especially `net interest`.
- Fiscal-year comparisons in a named Treasury Bulletin issue, e.g. “reported by the US Treasury in November 1981.”
- A “comparable 1980 fiscal period” or similar prior-year column in the same fiscal/outlays table.
- Box-Cox transformed values with a specified lambda.

This is distinct from deficit-projection questions: here the source values are outlay category amounts, not total deficit forecasts.

## Source Pattern

Treasury Bulletin issues around 1981 can contain federal fiscal/outlays tables that report categories such as `Net interest` for the current fiscal year and a comparable prior fiscal period. The prompt may say values are “expressed in billions of nominal dollars,” even when the underlying Bulletin table or extraction has values in millions. Always inspect the table title, notes, and column headers before transforming.

For November 1981 style questions:

1. Use the specifically named publication month/year.
2. Locate the federal budget receipts/outlays or outlays-by-category table containing `Net interest`.
3. Select the fiscal-year current-period column and the `comparable` prior-year fiscal-period column from that same table; do not substitute a later historical revision.
4. Normalize both numbers to billions of nominal dollars before Box-Cox transformation.

## Box-Cox Procedure

For positive source value `x` and lambda `λ`:

- If `λ != 0`: `BC(x, λ) = (x^λ - 1) / λ`
- If `λ == 0`: `BC(x, 0) = ln(x)`

For a difference between two transformed positive values using the same nonzero lambda, the `-1` terms cancel:

`BC(a, λ) - BC(b, λ) = (a^λ - b^λ) / λ`

Still keep the full formula in mind for audits and for cases where the prompt asks for a single transformed value.

## Unit and Rounding Rules

1. Convert source amounts to the unit requested by the prompt before applying Box-Cox.
   - If the table is in millions and the prompt asks for billions, divide by `1000` first.
   - Do not transform millions and then relabel the result as billions; Box-Cox is nonlinear, so that changes the answer.
2. Strip table annotations such as footnote markers, commas, `(r)` revised markers, or em dashes before numeric conversion.
3. Keep full precision through the exponentiation and subtraction.
4. Round only the final transformed difference to the requested decimal places unless the prompt explicitly says source values were rounded before use.
5. Report the result in the prompt’s requested transformed-unit wording; for Box-Cox-transformed billions, the arithmetic uses billion-denominated inputs.

## Verification Checklist

- [ ] Publication month/year exactly matches the prompt.
- [ ] The row is the requested outlay category, e.g. `Net interest`, not gross interest, total outlays, or deficit.
- [ ] The prior value comes from the `comparable` prior fiscal period column in the same table if the prompt uses that wording.
- [ ] Both source values are in billions before transformation.
- [ ] Lambda is applied as specified; for `λ = 0.75`, compute `(a**0.75 - b**0.75) / 0.75` for a difference.
- [ ] Final rounding is performed after all arithmetic.

## Common Pitfalls

- Using total outlays or deficit instead of the `Net interest` row.
- Comparing fiscal-year totals to calendar-year or month-only values.
- Applying Box-Cox to table values in millions when the question asks for billions.
- Rounding source values or intermediate transformed values before the final difference.
- Pulling values from a later annual table rather than the specifically named Treasury Bulletin issue.
