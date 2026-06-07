---
name: treasury-bulletin-esf-balance-sheets
description: Use when answering OfficeQA/Treasury Bulletin questions about U.S. Treasury Exchange Stabilization Fund balance sheets, especially questions asking for nominal capital, total capital and liabilities, or date-column values.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [officeqa, treasury-bulletin, exchange-stabilization-fund, balance-sheet, fraser]
    related_skills: [ocr-and-documents]
---

# Treasury Bulletin ESF Balance Sheet Questions

## Overview

Treasury Bulletin questions about the U.S. Treasury's Exchange Stabilization Fund (ESF) often ask for values from a balance sheet table at a specific month-end or quarter-end date. The table is usually titled similar to "Exchange Stabilization Fund Balance Sheet" and reports values in millions of dollars. Treat the table as an accounting statement: identify the exact date column, read the labeled row, preserve signs, and scale to billions only at the final answer.

## When to Use

Use this skill when the question mentions any of:

- U.S. Treasury Bulletin and Exchange Stabilization Fund / ESF.
- ESF Balance Sheet.
- Nominal capital, capital account, total capital and liabilities, total assets.
- A requested date such as "as of the last day of March 1989".
- Output in billions even though the source table is in millions.

Do not use this skill for non-ESF Treasury Bulletin tables except as a reminder to check units and date-column alignment.

## Procedure

1. Find the source Treasury Bulletin PDF or OCR text.
   - Search inside extracted text for `Exchange Stabilization Fund Balance Sheet`, `Stabilization Fund`, `Nominal capital`, `Foreign exchange holdings`, `Special drawing rights`, `Securities`, `Total assets`, and `Total capital and liabilities`.
   - If text extraction loses columns, use `pdftotext -layout` on the relevant PDF pages and compare against the visual PDF page.

2. Confirm the table unit before extracting numbers.
   - ESF balance sheet tables may state values in `millions of dollars`, while later/underlying balance sheets or question wording may use `thousands of dollars`.
   - Keep all source values in the stated unit while doing row/column extraction.
   - Convert units only at the end if the final answer requests a different unit. For shares/percentages, common unit scaling cancels if numerator and denominator use the same unit.

3. Map the requested date to the exact column.
   - Phrasing like "as of the last day of March 1989" corresponds to the `Mar. 31, 1989` column, not fiscal-year totals.
   - Balance sheet tables may include multiple columns for adjacent month/quarter ends; do not read a nearby date such as Dec. 31 or June 30.
   - If OCR wraps headers, reconstruct date columns from the visual or layout text before reading row values.

4. Read the required rows.
   - For `nominal capital held`, use the row labeled `Nominal capital` when present. Do not substitute `capital account` or `total capital` unless the question explicitly asks for those.
   - For `total capital and liabilities`, use the final liability-side total row labeled `Total capital and liabilities`.
   - In March 1989 ESF Balance Sheet format, `Nominal capital` is reported as an individual line item in the capital section and the statement total is a separate `Total capital and liabilities` line.

5. Perform arithmetic only after values are aligned.
   - If asked for absolute difference, compute `abs(total capital and liabilities - nominal capital)` in the same source unit.
   - Convert the result to billions after subtraction when the output unit requires it.
   - Round final outputs to the requested precision, commonly nearest thousandth.

6. For asset-share questions, compute the share per date before averaging.
   - Rows such as `Foreign exchange holdings` and `Securities` are asset components; the denominator is `Total assets` for the same exact date column.
   - If wording asks for the share of assets that came from `foreign-exchange holdings and securities`, combine those rows in the numerator for each date: `(foreign exchange holdings + securities) / total assets`. Do not treat them as alternative labels or average the two component shares.
   - If the question says values are adjusted to a common-dollar date with CPI-U, NSA, apply the CPI factor consistently to each nominal value for that same statement date. In a within-date share, the CPI factor cancels: `(component * factor) / (total assets * factor) = component / total assets`.
   - For wording like `average share ... for June 2000-2002` versus `September for those same years`, calculate each date's percentage share first, then take the arithmetic average of the three shares for each month set. Do not compute a pooled ratio such as `sum(adjusted components) / sum(adjusted total assets)` unless the question explicitly asks for an aggregate share.
   - Express the final absolute difference between average shares in percentage points: `abs(avg_share_A - avg_share_B) * 100`, then round to the requested precision.

## Worked Pattern: March 31, 1989

For questions using the ESF Balance Sheet as of the last day of March 1989:

- Source rows are in millions of dollars.
- `Nominal capital` at `Mar. 31, 1989` = 8,124 million dollars -> 8.124 billion dollars.
- `Total capital and liabilities` at `Mar. 31, 1989` = 20,976 million dollars.
- Absolute difference = `abs(20,976 - 8,124) = 12,852` million dollars -> 12.852 billion dollars.

This worked pattern is included to show the extraction/scaling convention; do not reuse these numbers for other dates.

## Common Pitfalls

1. Unit mismatch: source table values may be in millions or thousands depending on the ESF table/source vintage and question wording. Preserve the source unit during extraction; unit scaling cancels for shares and should be applied exactly once for currency outputs.

2. Date drift: "last day of March 1989" means the March 31, 1989 column. Do not use the nearest fiscal year-end or calendar year-end column.

3. Row substitution: `Nominal capital` is not the same thing as `Total capital and liabilities`. For asset composition questions, `Foreign exchange holdings` and `Securities` are numerator components and `Total assets` is the denominator.

4. Arithmetic order: calculate absolute differences in source units first, then scale and round for currency answers. For average share questions, calculate each date's share first and average the shares; do not pool adjusted dollars across dates unless explicitly requested.

5. CPI-adjusted share trap: a CPI factor for a given date cancels inside that date's numerator/denominator share. CPI adjustment can change pooled dollar ratios across dates, but it should not change a per-date share that is averaged afterward.

6. OCR/layout errors: the final total row can be far from the `Nominal capital` line, and PDF extraction may wrap row labels. Verify the row label and column alignment visually or with `pdftotext -layout`.

## Verification Checklist

- [ ] The exact ESF Balance Sheet table was found.
- [ ] The table unit was recorded and applied exactly once, or confirmed irrelevant because a share/percentage cancels common scaling.
- [ ] The requested date column was mapped to the correct month-end/quarter-end date.
- [ ] Values came from the explicitly named rows, not nearby subtotals.
- [ ] Absolute differences used `abs(a - b)`.
- [ ] For average share questions, each date's share was computed before averaging and before taking the between-set difference.
- [ ] Final answers are in the requested units (currency, percentage, or percentage points) and rounded to the requested thousandth place.
