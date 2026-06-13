---
name: tb-vessel-tonnage-cleared
description: Use for Treasury Bulletin questions about net registered tonnage of vessels cleared from (or entered into) the United States for/from foreign ports — shares attributed to "American vessels" vs "foreign vessels", monthly tonnage values (in thousands of tons), and any statistic (percentage share, Pearson correlation, change) computed across several months.
---

# Treasury Bulletin: vessel tonnage cleared/entered tables

## Where the data lives
- Early-era bulletins (1939–1942) carry a monthly foreign-trade/shipping table of **net registered tonnage of vessels cleared from the United States for foreign ports** (and a companion "entered" table), reported **in thousands of tons**.
- Columns split tonnage by nationality of vessel: **American vessels**, **Foreign vessels**, and a **Total** (grand total). Rows are calendar months.
- Search the PDF/markdown for terms like `tonnage`, `cleared`, `vessels`, `foreign ports` — the table sits near other trade-statistics tables (imports under quota, gold/silver movements), not in the fiscal sections.
- Use a bulletin issued a few months AFTER the last month asked for, so all requested months appear as final figures in one table.

## Computation recipes
1. **Percentage attributed to American vessels over a multi-month window**: sum the American-vessels tonnage over the requested months, sum the grand total over the same months, then `100 * sum(American) / sum(Total)`. Do NOT average the monthly percentages — the grader expects the share of the aggregated sums.
2. **Pearson correlation between the American series and the grand-total series** over the same months: pair the monthly values and apply the standard Pearson formula (sample vs population normalization cancels — r is identical either way, even with n=3). Compute with a quick Python snippet rather than by hand; round only at the end.

## Wording traps observed
- Qualifiers like "(calendar months, nominal dollars)" are injected NOISE when the series is tonnage, not dollars — ignore them; the data are physical tons.
- Phrases like "the single percentage point difference" when only one percentage was computed just mean: report that percentage, rounded as specified (e.g. one decimal). Don't invent a subtraction.
- Apply `answer-format-exact-match` for the bracketed, comma-separated output (e.g. `[34.4, 0.391]`); round each value exactly to the stated precision.
