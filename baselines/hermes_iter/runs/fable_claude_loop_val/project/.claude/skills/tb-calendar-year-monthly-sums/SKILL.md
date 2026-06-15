---
name: tb-calendar-year-monthly-sums
description: Use when a Treasury Bulletin question sums or averages the reported values for the individual calendar months of a year from a monthly series (budget receipts/expenditures, national defense spending), or otherwise needs month-by-month data spanning a calendar year — fiscal-year table layout means the 12 months come from two fiscal-year tables.
---

# Summing 12 calendar-month values from Treasury Bulletin monthly tables

Verified pattern: "total of the reported values for all individual calendar
months in 1953 of expenditures for national defense and associated
activities" → sum of 12 monthly figures = 44463 (millions). The procedure
below is what makes this class of question reliable.

## 1. Calendar year ≠ fiscal year: data spans TWO fiscal years
Treasury Bulletin budget tables ("Budget Receipts and Expenditures") are
organized by **fiscal year (July–June)**. A calendar year YYYY therefore
spans fiscal years YYYY (Jan–Jun) and YYYY+1 (Jul–Dec). No single table
in one issue shows all 12 calendar months — plan to pull from more than
one issue/section.

## 2. Pick issues by publication lag
Monthly figures for month M appear in bulletins published **1–2 months
after M**. Practical issue choices for calendar year YYYY:
- Jan–Jun YYYY: an issue from ~Aug–Dec YYYY (its fiscal-year-YYYY table
  lists all months through June).
- Jul–Dec YYYY: an issue from ~Feb–Apr YYYY+1 (its fiscal-year-YYYY+1
  table lists months through December).
A single late issue (e.g. Feb/Mar YYYY+1) often contains BOTH fiscal-year
tables (current FY monthly detail + prior FY by month or totals) — check
it first before opening a second file.

## 3. Use per-month columns, not cumulative-to-date
Budget tables frequently print, side by side, the **monthly** figure and a
**cumulative fiscal-year-to-date** figure (or a "corresponding period prior
year" column). Read the column headings; summing cumulative columns
massively overstates the total. If only cumulative values exist, recover
month M as `cum(M) - cum(M-1)` — and remember the cumulation resets at
July (fiscal year start).

## 4. "Reported values" = take figures as printed
The question wording "specifically only the reported values" means: take
each month's figure exactly as printed in the table (these are often later
revised in subsequent issues — use the values from the issue(s) you pulled,
do not mix revised and unrevised series mid-year, and prefer pulling each
half-year from one consistent table).

## 5. Checklist before answering
- Exactly **12 monthly values** listed out (print them) — Jan through Dec.
- Same row/series for all months ("National defense and related/associated
  activities" — match the row label across both fiscal-year tables; the
  label may vary slightly between issues but refers to the same line).
- Same unit throughout (these tables are in **millions of dollars**;
  values may be printed with decimals — sum at full printed precision,
  round only at the end).
- Sanity check: total ≈ 12 × typical monthly value.
- Format per the answer-format skill (bare number, no commas).
