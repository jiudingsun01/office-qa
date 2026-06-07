---
name: treasury-bulletin-real-gdp-growth
description: Use when OfficeQA/Treasury Bulletin questions ask about U.S. real GDP growth quarterly percent change at an annual rate, annual summaries, or geometric means across quarters. Convert annualized rates to per-quarter growth before geometric averaging unless the prompt explicitly asks to average annualized rates themselves.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [officeqa, treasury-bulletin, gdp, geometric-mean, annualized-rates]
    related_skills: []
---

# Treasury Bulletin Real GDP Growth

## Overview

Treasury Bulletin OfficeQA questions may use U.S. real GDP growth series described as "quarterly percent change at an annual rate" for calendar years. The printed values are annualized quarter-over-quarter rates, not the actual one-quarter percentage changes. A common trap is to take the geometric mean directly over the printed annualized percentages, which produces an annual-rate answer (around 2-3%) instead of a quarter-rate answer (around 0.5-0.8%).

## When to Use

Use this skill when the question mentions:

- U.S. real GDP growth
- quarterly percent change at an annual rate
- CY ranges with quarterly observations
- highest/lowest annual geometric mean over quarters
- converting Treasury Bulletin or FRED-style GDP annualized quarterly growth into a calendar-year value

Do not use this for nominal GDP levels, annual real GDP growth already reported as annual values, or unrelated Treasury tables.

## Procedure

1. Extract the four quarterly annualized percent rates for each candidate calendar year.
   - Keep signs and decimal points.
   - Use revised values if the source marks revisions and the question does not request original vintage values.
   - Group by calendar year, not fiscal year.

2. Convert each annualized quarterly percent rate `r` into an actual one-quarter growth factor:

   ```text
   q_factor = (1 + r / 100) ** (1/4)
   q_percent = (q_factor - 1) * 100
   ```

   This reverses annualization. For small positive rates, a 2.8% annualized rate becomes about 0.69% for the quarter.

3. Compute the geometric mean across the four quarterly growth factors for the year:

   ```text
   gm_factor = (product(q_factor_i for the 4 quarters)) ** (1/4)
   gm_percent = (gm_factor - 1) * 100
   ```

   Equivalent shortcut:

   ```text
   gm_percent = ((product(1 + r_i/100) ** (1/16)) - 1) * 100
   ```

   The `1/16` exponent appears because there are four annualized rates and each must first be deannualized by `1/4`, then geometrically averaged across four quarters by another `1/4`.

4. Rank years by the unrounded `gm_percent` value. Only round after selecting the year unless the question explicitly says to round before comparison.

5. Format exactly as requested. For OfficeQA answers, if the prompt asks for square brackets and comma-separated values, return for example:

   ```text
   [2017, 0.69]
   ```

## Worked Sanity Check

If a year has quarterly annualized rates roughly around 2-4%, the geometric mean of actual quarterly growth should be around 0.5-1.0%, not 2-4%. A result near 2.80 for 2017 means you probably averaged annualized rates directly and missed the deannualization step; the expected scale is about 0.69.

## Common Pitfalls

1. Averaging printed annualized percentages directly.
   - Wrong: `geomean(1 + r_i/100) - 1` reported as percent.
   - Right: convert each annualized rate with `**(1/4)` first, then average growth factors.

2. Treating percent values as decimal values twice.
   - Use `r / 100` to make a decimal growth rate, then multiply the final result by 100 for percent.

3. Rounding before ranking.
   - Rank using unrounded `gm_percent`; round only for display.

4. Mixing annual and quarterly labels.
   - "At an annual rate" describes the scale of each quarterly change. It does not mean the quarter itself lasted a year.

## Verification Checklist

- [ ] Four quarterly observations per calendar year were used.
- [ ] Annualized quarterly rates were converted with exponent `1/4` before geometric averaging.
- [ ] The final value is on a quarterly percent scale, typically under 1% for annualized rates around 2-4%.
- [ ] Ranking used unrounded values.
- [ ] Final answer follows the requested bracket/comma/rounding format.
