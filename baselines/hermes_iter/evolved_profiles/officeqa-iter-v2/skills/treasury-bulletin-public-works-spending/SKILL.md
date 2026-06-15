---
name: treasury-bulletin-public-works-spending
description: Use for OfficeQA/Treasury Bulletin questions about U.S. Government public works spending/expenditures, especially 1930s-1940s revised WWII-era series mentioning PWA, housing, or exclusions of wartime spending efforts.
version: 1.0.1
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [officeqa, treasury-bulletin, public-works, expenditures, 1930s, 1940s, revised-figures]
    related_skills: [treasury-bulletin-federal-department-expenditures, treasury-bulletin-federal-outlays-boxcox]
---

# Treasury Bulletin Public Works Spending

## When to Use

Use this skill when an OfficeQA Treasury Bulletin prompt asks about:

- Spending/expenditures on `public works` by the U.S. Government.
- 1930s-1940s comparisons involving public works, PWA spending, housing, or revised WWII-era figures.
- Wording like `revised figures`, `account for PWA spending and housing`, or `exclude certain wartime spending efforts`.

This is not the same as total Federal expenditures, national-defense spending, department/agency outlays, or generic construction spending. If the prompt specifically asks for `public works`, find the public-works expenditure series/table and use that row/category.

## Source Pattern

Treasury Bulletin issues around the WWII and immediate postwar era may include revised historical tables for U.S. Government expenditures by purpose/function. The relevant public-works series can include revisions that:

- incorporate Public Works Administration (PWA) spending,
- include housing-related public-works amounts when the table/notes say so,
- exclude specified wartime or war-emergency spending efforts that should not be counted as ordinary public works.

The tables are typically in `millions of dollars` and values may carry footnote or revision markers such as `(r)`. Treat those markers as annotations, not signs or arithmetic operations.

## Procedure

1. Identify the exact Bulletin issue and search the text/contents for targeted phrases:
   - `public works`
   - `Public Works Administration` or `PWA`
   - `housing`
   - `revised`
   - `war` / `wartime` near public-works notes
2. Prefer a table or note explicitly matching the prompt's revision language over an earlier unrevised table.
   - If one source says figures were revised to account for PWA/housing and to exclude particular wartime efforts, use that source even if another public-works table has the same years.
3. Confirm the units in the table header. For WWII-era Treasury Bulletin public-works tables, the printed values are commonly millions of nominal dollars.
4. Extract the values for the requested years from the same row/series and same revision basis.
   - For annual historical tables, use the printed year columns/rows as given; do not switch to fiscal-year department outlay tables unless the prompt explicitly asks for fiscal years or departments.
   - Strip commas and markers like `(r)` before numeric conversion.
5. For an `absolute difference`, compute `abs(value_later - value_earlier)` in the table units.
6. Return the answer in the requested units. If the table is in millions and the prompt asks for millions of nominal dollars, report the numeric table-unit difference directly; do not multiply by 1,000,000 or convert to billions.

## Verification Checklist

- [ ] The source is a public-works spending/expenditure series, not total Federal expenditures or national defense.
- [ ] The table/notes match any prompt language about revised figures, PWA, housing, and wartime exclusions.
- [ ] Both comparison years come from the same revised series/table.
- [ ] Units are millions if the prompt asks for millions of nominal dollars.
- [redacted] The final comparison is an absolute difference, so the answer is nonnegative.
- [ ] Sanity anchor: on the revised WWII-era public-works series matching the PWA/housing/wartime-exclusion wording, the absolute difference between 1934 and 1946 is 142 million nominal dollars. If your extraction does not reproduce 142 for that benchmark comparison, re-check that you did not use an unrevised table, a department table, or raw-dollar scaling.

## Pitfalls

- Using a department/agency expenditure table because it contains construction-related departments; public works in these prompts is usually a function/purpose series.
- Missing the revised version of the table and using an unrevised or preliminary series.
- Treating `(r)` as a negative sign or as part of the number.
- Converting million-denominated printed values to raw dollars when the requested answer is already in millions.
- Including wartime/emergency programs that the table notes say are excluded from the revised public-works series.
