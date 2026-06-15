---
name: tb-esf-tables
description: Use for any Treasury Bulletin question about the Exchange Stabilization Fund (ESF) — locating its balance sheet (ESF-1) or income/expense (ESF-2) tables, handling the quarterly publication lag, or reading the balance-sheet structure.
---

# Exchange Stabilization Fund (ESF) tables

## Locating ESF data
- The Exchange Stabilization Fund has its own "ESF" section in the Treasury
  Bulletin: **ESF-1 = Balance Sheet** (assets; liabilities and capital),
  **ESF-2 = Income and Expense**.
- ESF data is **quarterly, as of quarter-end**, and is published with a lag
  of roughly one quarter: data "as of the last day of March YYYY" appears in
  the **June YYYY** (or later) bulletin, not the March one. If a date phrase
  like "as of the last day of <month>" is used, map it to the quarter-end
  column (Mar. 31, June 30, Sept. 30, Dec. 31).

## Balance-sheet structure (applies to ESF-1 and similar statements)
- The statement balances: **Total assets = Total liabilities and capital**.
- "Capital" subtotal (capital account + accumulated net income) is listed
  under the liabilities-and-capital side. A question asking for the
  difference between "total capital and liabilities" and "capital" is just
  asking for **total liabilities** — sanity-check your subtraction against
  the printed liabilities subtotal if available.
- "Total **nominal** capital" means the printed Capital subtotal as-is —
  "nominal" signals no inflation/real-dollar adjustment, not a different row.

## Units
ESF tables print **millions of dollars**. If the question asks for a
different unit or a rounded result, follow the unit-rescaling rules in the
`answer-format` skill (rescale/round only at the final step).
