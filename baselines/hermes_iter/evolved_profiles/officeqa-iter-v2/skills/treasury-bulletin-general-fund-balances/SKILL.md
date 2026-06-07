---
name: treasury-bulletin-general-fund-balances
description: Use when answering OfficeQA/Treasury Bulletin questions about the U.S. Treasury General Fund balance, working balance, total balance, or ratios/rates of change between dated General Fund balances.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [officeqa, treasury-bulletin, general-fund, working-balance, geometric-rate, fraser]
    related_skills: [ocr-and-documents]
---

# Treasury Bulletin General Fund Balance Questions

## Overview

OfficeQA questions about the U.S. Treasury Bulletin may ask for a ratio involving the Treasury's General Fund working balance and total balance at two dates, then a rate of change between those ratios. Treat this as a two-step extraction-and-arithmetic task: first read the two line items for each requested period end, then compute ratios and the requested growth/decline rate.

The ratio is unitless, so values can stay in the source table's unit as long as the numerator and denominator come from the same table/unit. Do not convert millions to dollars unless the final answer asks for a currency amount.

## When to Use

Use this skill when the question mentions any of:

- U.S. Treasury Bulletin plus General Fund / general fund of the Treasury.
- Working balance, total balance, balance ratio, or General Fund balance.
- Periods ending in month/year form, such as `December 1938` and `December 1940`.
- Geometric annual rate of change, CAGR, annual rate, or average annual change between two General Fund ratios.

Do not use this skill for Exchange Stabilization Fund balance sheets; use `treasury-bulletin-esf-balance-sheets` for ESF-specific questions.

## Source-Finding Procedure

1. Find the Treasury Bulletin PDF or extracted text for the requested date range.
   - Search the OCR/layout text for combinations of: `General Fund`, `working balance`, `total balance`, `Assets and liabilities in the general fund`, and the requested month/year labels.
   - In older Treasury Bulletins, the relevant table is often a General Fund balance table rather than a narrative paragraph. Prefer table extraction over prose snippets.

2. Use layout-preserving extraction for column alignment.
   - Run `pdftotext -layout` on the relevant PDF pages when available.
   - If columns wrap or date headers are ambiguous, inspect the visual PDF page or rerun extraction for a narrower page range.
   - Confirm that `working balance` and `total balance` are read from the same date column/period-end row family.

3. Record the unit, but do not over-convert.
   - Treasury Bulletin tables commonly report in dollars, thousands, or millions depending on the period/table.
   - For a ratio such as `working balance / total balance`, scaling cancels if both values use the same unit.
   - If the final output is only a decimal rate, avoid unnecessary currency conversion.

## Ratio and Geometric Rate Procedure

For each requested period ending date:

1. Extract the General Fund `working balance` value.
2. Extract the corresponding `total balance` value.
3. Compute the ratio:

```text
ratio_at_date = working_balance_at_date / total_balance_at_date
```

Then compute the geometric annual rate of change between the start and end ratios:

```text
years = elapsed_years_between_period_ends
geometric_annual_rate = (end_ratio / start_ratio) ** (1 / years) - 1
```

For December 1938 to December 1940, the elapsed time is 2 years, so use:

```text
((ratio_Dec_1940 / ratio_Dec_1938) ** 0.5) - 1
```

Round only the final decimal to the precision requested by the question, commonly nearest thousandth. A decline should remain negative.

## Arithmetic Checks

Use Python or another exact calculator rather than mental arithmetic:

```python
start_ratio = start_working_balance / start_total_balance
end_ratio = end_working_balance / end_total_balance
years = 2
answer = (end_ratio / start_ratio) ** (1 / years) - 1
print(round(answer, 3))
```

If the requested output is a decimal value, return `-0.119`, not `-11.9%` or `-0.1190`, unless the prompt asks for a specific number of digits.

## Common Pitfalls

1. Reversing the ratio: the phrase `working balance to total balance ratio` means `working balance / total balance`, not `total balance / working balance`.

2. Using arithmetic average change: `geometric annual rate of change` requires `(end/start)^(1/years)-1`, not `(end-start)/years` or `(end-start)/start/years`.

3. Using the wrong time span: period ending December 1938 to period ending December 1940 is 2 years, not 3 observations or 24 monthly intervals divided by 12 plus one.

4. Rounding early: do not round the two ratios before computing the annual rate. Round only the final result.

5. Sign mistakes: if the ratio falls over the period, the geometric annual rate is negative.

6. Unit distraction: for same-table ratios, thousands/millions/dollars cancel. Only currency outputs need unit scaling.

## Verification Checklist

- [ ] The source is a Treasury Bulletin General Fund table, not an ESF or unrelated balance sheet.
- [ ] Start and end dates match the requested period endings exactly.
- [ ] `working balance` and `total balance` values are from matching date columns/rows.
- [ ] Ratio formula is `working balance / total balance`.
- [ ] Geometric annual formula uses the elapsed years between the dates.
- [ ] No intermediate rounding was used.
- [ ] Final answer is a decimal rounded to the requested place, with the correct sign.
