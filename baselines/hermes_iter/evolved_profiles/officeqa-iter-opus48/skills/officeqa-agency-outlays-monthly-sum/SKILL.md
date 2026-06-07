---
name: officeqa-agency-outlays-monthly-sum
description: OfficeQA Treasury Bulletin — sum monthly OUTLAYS across individual federal agencies for a given month, excluding named agencies and all undistributed offsetting receipts / non-agency items. Covers the "Budget Results" / Monthly Treasury Statement style outlay table found in modern bulletins.
category: research
---

# OfficeQA: Sum Monthly Agency Outlays (with exclusions)

## When this applies
Question says something like: "Using the reported monthly outlay values for
individual federal agencies, calculate total outlays in millions of dollars for
[Month Year] across all listed agencies except [Agency A], [Agency B], [Agency C].
Sum only the agency-specific outlay entries and exclude all undistributed
offsetting receipts or other non-agency items."

Answer is a single integer in millions of dollars. PASSED: Jan 2003 = 180681.

## Where the table lives
This is the "Budget Receipts and Outlays" / Monthly Treasury Statement summary
table reproduced in modern Treasury Bulletins (~2000s). It lists each
DEPARTMENT/AGENCY as a row with columns for the current month and fiscal-year-to-date,
typically split into Receipts | Outlays sections (or a "Budget Results" /
"Outlays by agency" block). Outlays are already in MILLIONS — no scaling needed.

## Procedure
1. Find the agency-level outlays table for the target month. Search the PDF text
   for agency names (e.g. "Department of Defense", "Health and Human Services",
   "Social Security Administration", "Veterans Affairs"). pdftotext -layout works.
2. Identify the CURRENT-MONTH outlay column (not fiscal-YTD). The header usually
   has "This Month" / the month name vs "Fiscal Year to Date" / "Current Fiscal
   Year to Date". Use the monthly column.
3. Take EVERY agency row's current-month outlay. Then:
   - SUBTRACT (i.e. drop) the rows for each agency named in the exclusion list.
   - DROP "Undistributed Offsetting Receipts" entirely (it is negative; it is the
     classic non-agency item the prompt tells you to exclude).
   - DROP any "Total" / subtotal rows, "Other Defense Civil Programs" only if it's
     a non-agency line (usually it IS an agency line — keep it), and any
     interest/allowance non-agency aggregate that isn't an agency.
4. Sum the remaining agency outlays. Report as an integer in millions.

## Pitfalls
- "Exclude all undistributed offsetting receipts" is the key instruction. That
  row is negative; if you accidentally include it your sum is too LOW. If you
  forgot to exclude an excluded agency your sum is too HIGH.
- Do NOT use the printed grand "Total outlays" line — you must rebuild the sum
  from individual agency rows minus exclusions, because the total includes the
  offsetting receipts and the excluded agencies.
- Watch for negative agency entries (rare) — keep them with their sign unless the
  prompt says exclude.
- Verify your reconstructed sum is plausible vs the printed total: 
  printed_total = your_sum + excluded_agencies + offsetting_receipts.
  This cross-check catches missed/double-counted rows.
