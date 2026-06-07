---
name: officeqa-profile-economy-chart-quarterly-change
description: OfficeQA Treasury Bulletin — read a CHART in the "Profile of the Economy" section of modern (2000s) bulletins (e.g. payroll employment, unemployment rate, GDP, CPI) and compute a "mean of the average monthly change from end of QX to end of QY" across several years. Covers where the Profile of the Economy charts live, the per-month-change definition (divide the quarter-to-quarter delta by the number of months in the span), and the mean-across-years step. PASSED Sep 2007 payroll employment, end-Q1->end-Q2, 2004-2006 = 202.333.
---

# OfficeQA — "Profile of the Economy" chart quarterly-change questions

## When this applies
Question references:
- A CHART (not a table) in the **"Profile of the Economy"** section of a modern Treasury Bulletin (roughly 2000–2010 era).
- A named economic indicator chart: **payroll employment** (nonfarm), unemployment rate, real GDP, CPI / inflation, industrial production, etc.
- A phrase like "**mean of the average monthly change from end of QX to end of QY from YEAR1 - YEAR2**".

## Where the data lives
- The **Profile of the Economy** section sits near the FRONT of the bulletin, before the main statistical tables. In the Sep 2007 bulletin it is one of the first content sections.
- It contains a row of small charts (line plots) with accompanying data. The **payroll employment** chart shows total nonfarm payroll employment in thousands (or millions on the axis) over a multi-year window with monthly granularity.
- Render the relevant page(s) to a high-res image and/or pull the underlying monthly values. Quarter ends:
  - **End of Q1 = March**, **End of Q2 = June**, end of Q3 = Sept, end of Q4 = Dec.
- For "payroll employment in thousands", read the level at March and at June for each year.

## The calculation (THE WHOLE GAME)
"**Average monthly change from end of Q1 to end of Q2**" for a single year =
```
(value_at_June - value_at_March) / N_months
```
where **N_months = number of months spanning end-Q1 to end-Q2 = 3** (March→April→May→June is a 3-month change: Apr, May, Jun deltas). Use the span length the question implies; end-Q1 to end-Q2 is 3 months.

Then "**mean ... from YEAR1 - YEAR2**" = arithmetic mean of that per-year average-monthly-change across each year in the inclusive range.

```
for each year Y in [YEAR1 .. YEAR2]:
    amc[Y] = (june[Y] - march[Y]) / 3
answer = mean(amc over all years)
```

### Worked PASS — Sep 2007, payroll employment, end-Q1 -> end-Q2, 2004-2006
- Compute (June − March)/3 for 2004, 2005, 2006 (payroll employment in thousands).
- Mean of the three per-year average monthly changes = **202.333** (GOLD-VERIFIED). Report to nearest thousandth.

## Pitfalls
- **Divide by the right number of months.** End-Q1 to end-Q2 = 3 months. End-Q1 to end-Q3 = 6 months, end-Q2 to end-Q4 = 6, etc. The divisor is the count of monthly steps between the two quarter-end months, NOT the number of quarters and NOT the number of years.
- **"Average monthly change" then "mean across years" is a two-stage average.** First divide each year's quarter delta by months (stage 1), THEN average those per-year numbers across the year range (stage 2). Do not lump all months together into one big mean unless the question literally says so.
- **Inclusive year range.** "2004 - 2006" = three years {2004, 2005, 2006}.
- **Units are thousands.** Payroll employment is reported in thousands of jobs; keep the answer in thousands (e.g. 202.333 thousand). If the chart axis is in millions, scale to thousands before reporting.
- This is a CHART question but the values are precise levels — extract the actual monthly numbers (chart data / nearby table), don't eyeball off pixels if exact values are available.
- Report to the precision the question asks (here, nearest thousandth).
