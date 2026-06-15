---
name: tb-savings-bonds-sales
description: Use for any question about U.S. savings bonds sales or redemptions — phrases like "all series combined", "Series E", "Series E and H" — for one or more CALENDAR years. The savings-bonds tables print annual calendar-year rows directly, so no month-by-month summation is needed.
---

# U.S. savings bonds sales/redemptions tables ("all series combined")

Verified: "arithmetic mean of total sales (millions of nominal dollars) of
all series combined for calendar years 1949–1953" → averaging five annual
rows from the savings-bonds table gave [redacted] (CORRECT).

## 1. Where the data lives
Every Treasury Bulletin issue has a **"United States Savings Bonds"**
section containing tables titled like *"Sales and Redemptions of Series
E–K (All Series Combined)"* plus per-series breakouts (Series E and H;
Series F, G, J and K; etc.). Search the parsed text for
`savings bonds` / `all series combined` / `Sales and Redemptions`.

## 2. Calendar-year rows are printed directly — do NOT sum months
Unlike the budget receipts/expenditures tables (fiscal-year organized,
see tb-calendar-year-monthly-sums), the savings-bonds tables have a
stub column listing **annual calendar-year rows** (e.g. `1949`, `1950`,
…) followed by recent monthly rows. For a calendar-year figure, read the
annual row verbatim — summing 12 monthly values is unnecessary and risks
OCR errors compounding.

## 3. One late issue covers many years
The annual rows go back a decade or more, so a single issue published in
~mid YYYY+1 or later contains ALL the calendar years asked about (e.g.
1949–1953 are all in one table of a 1954+ issue). Pick one issue, pull
every year from the same table, then spot-check 1–2 values against an
adjacent issue (tb-cross-issue-ocr-check) since they are reprinted
identically for years.

## 4. Column pitfalls
- Units are **millions of dollars**; "Sales" are at **issue price** —
  distinct columns exist for "Accrued discount", "Sales plus accrued
  discount", and "Redemptions". Take the plain *Sales* column unless the
  question says otherwise.
- "All series combined" is its own table/column group — do not add up
  the per-series tables yourself (rounding in the source makes your sum
  differ from the printed combined figure).

## 5. Arithmetic
Mean of N annual values: sum the verbatim table values, divide by N,
round to the requested decimals, and format per the answer-format skill
(bare number, no separators).
