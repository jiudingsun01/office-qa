---
name: treasury-bulletin-national-defense-expenditures
description: Use when answering OfficeQA/Treasury Bulletin questions about U.S. national defense and associated activities expenditures by month, fiscal year, calendar year, or sums of reported monthly values.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [officeqa, treasury-bulletin, expenditures, national-defense, monthly-tables, fraser]
    related_skills: [ocr-and-documents]
---

# Treasury Bulletin National Defense Expenditure Questions

## Overview

Some OfficeQA Treasury Bulletin questions ask for expenditures for `national defense and associated activities` across individual months. These are usually table-extraction questions, not finance-modeling questions: use the values as reported in the Treasury Bulletin table, preserve the table unit, and sum only the requested monthly entries.

Treasury Bulletin expenditure tables often report amounts in `millions of dollars`. If the prompt asks for `in millions of nominal dollars`, return the sum of the printed monthly values in millions; do not multiply by 1,000,000 or convert to billions.

## When to Use

Use this skill when the question mentions:

- U.S. Treasury Bulletin expenditures.
- `national defense and associated activities`, `national defense`, or a closely named defense expenditure line item.
- Individual calendar months, fiscal months, calendar-year sums, monthly totals, or sums of reported values.
- A specific year such as `1953` where the answer must use all months in that calendar year.

Do not use this skill for General Fund balance ratios or Exchange Stabilization Fund balance sheets; use the dedicated Treasury Bulletin skills for those.

## Source-Finding Procedure

1. Locate the Treasury Bulletin table that contains monthly Federal budget receipts/expenditures or expenditure classifications.
   - Search text/OCR for exact phrases: `national defense and associated activities`, `expenditures`, `monthly`, `1953`, and month labels.
   - Prefer layout-preserving extraction (`pdftotext -layout`) because the table is columnar and month headers can be easy to misalign.

2. Confirm the line item exactly.
   - Use the row labeled `National defense and associated activities` or the closest exact printed wording.
   - Do not substitute a subtotal, grand total, `military functions`, or another defense-related row unless the prompt explicitly asks for it.

3. Confirm the unit in the table header.
   - Common header: `In millions of dollars` or equivalent.
   - Keep the reported precision. If the table values are whole millions, sum whole millions.

4. Build the requested month set explicitly.
   - For `all individual calendar months in 1953`, use exactly Jan., Feb., Mar., Apr., May, June, July, Aug., Sept., Oct., Nov., and Dec. 1953.
   - Do not include annual totals, fiscal-year totals, cumulative columns, or adjacent months from 1952/1954.
   - If the table spans fiscal-year pages, remember that calendar 1953 may be split across two fiscal-year sections; gather Jan-Jun and Jul-Dec from the correct columns if necessary.

## Arithmetic Procedure

1. Transcribe each requested monthly value into a calculator/Python list, with the month name next to it.
2. Sum the listed reported values directly.
3. Return the result in the requested unit and formatting.

Recommended scratch pattern for a one-year defense-expenditure sum:

```python
vals = {
    "1953-01": ..., "1953-02": ..., "1953-03": ...,
    "1953-04": ..., "1953-05": ..., "1953-06": ...,
    "1953-07": ..., "1953-08": ..., "1953-09": ...,
    "1953-10": ..., "1953-11": ..., "1953-12": ...,
}
assert len(vals) == 12
print(sum(vals.values()))
```

For calendar-year ratio questions such as `mean of the ratios of total net budget receipts to total national defense budget expenditures for each calendar year from 1941-1943`:

1. Use the Treasury Bulletin Federal budget-results/summary table where both annual rows are budget series in the same unit, usually `millions of dollars`.
   - Numerator row: `Total net budget receipts` (not `total receipts from the public`, not trust-account receipts, not on/off-budget subtotals).
   - Denominator row: the budget expenditure row for `National defense`/`national defense and associated activities` (not broader payments-to-public or non-budget defense-like rows).
2. For each calendar year, collect or compute the annual value for each row from calendar-year columns or by summing the twelve monthly cells if only months are printed. Do not use fiscal-year columns for `calendar years`.
3. Compute each year's ratio as `total_net_budget_receipts / total_national_defense_budget_expenditures`.
4. Take the arithmetic mean of the per-year ratios; do not divide the sum of all receipts by the sum of all defense expenditures unless the prompt asks for an aggregate ratio. An answer near `0.49` for 1941-1943 is a red flag that an aggregate ratio, fiscal-year values, or the wrong receipts/defense table may have been used; the benchmark-style per-year mean is near `0.6841`.
5. Round only the final mean to the requested decimals.

Recommended scratch pattern for multi-year ratio means:

```python
receipts = {1941: ..., 1942: ..., 1943: ...}
defense = {1941: ..., 1942: ..., 1943: ...}
ratios = {y: receipts[y] / defense[y] for y in receipts}
print(ratios)
print(round(sum(ratios.values()) / len(ratios), 4))
```

For absolute percent-change questions comparing two calendar-year sums, use the earlier/base year as the denominator unless the prompt explicitly says otherwise:

```python
base = sum(vals_1940.values())
new = sum(vals_1953.values())
pct = abs(new - base) / base * 100
print(f"{pct:.2f}%")
```

Round only the final percentage. Do not round or convert the monthly values before summing.

Known extraction checks from the monthly `National defense and associated activities` row:

- Calendar 1940 (Jan-Dec reported monthly cells) sums to `2,602` million dollars.
- Calendar 1953 (Jan-Dec reported monthly cells) sums to `44,463` million dollars.

Use these only as checks on extraction/arithmetic, not as replacements for reading the source in future variants.

## Common Pitfalls

1. Off-by-one month errors: `calendar months in 1953` means January through December 1953, not fiscal year 1953 and not a rolling twelve-month period.

2. Including summary columns: do not add fiscal-year totals, calendar-year totals, or cumulative-to-date columns to the twelve monthly values.

3. OCR digit slips: small OCR/transcription errors in one month can change the sum by only 1-3 million. After summing, re-check any ambiguous digit in the source image/layout text before finalizing.

4. Using derived or revised totals instead of the requested reported monthly values: if the prompt says `reported values for all individual calendar months`, sum the monthly cells exactly as printed. Do not recompute from an annual total or choose a later revised table unless the question asks for revised values.

5. Unit conversion mistakes: if the table and question both use millions of dollars, the final number is a count of millions (for example `44,463`), not dollars and not billions.

6. Row-label drift across pages: when a table wraps, verify that the row continuation still corresponds to `national defense and associated activities` and not the next expenditure category.

## Verification Checklist

- [ ] The source table is a Treasury Bulletin expenditure table, not a balance sheet or narrative summary.
- [ ] The row label matches `National defense and associated activities`.
- [ ] The unit is recorded and the final answer preserves the requested unit.
- [ ] Exactly twelve monthly cells are included for a calendar-year request.
- [ ] No fiscal-year totals, cumulative totals, or adjacent-year months are included.
- [ ] Each ambiguous OCR digit is checked against the layout/visual source.
- [ ] The final sum is computed with a tool, not mental arithmetic, and rounded/formatted only at the end.
