---
name: treasury-bulletin-shipping-tonnage
description: Use for OfficeQA/Treasury Bulletin questions about vessel tonnage cleared from the United States for foreign ports, especially American-vessel shares and correlations with grand totals.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [officeqa, treasury-bulletin, shipping, tonnage, correlation]
    related_skills: []
---

# Treasury Bulletin Shipping Tonnage Tables

## Overview

Some Treasury Bulletin benchmark questions use shipping/commerce tables rather than fiscal dollar tables. The table wording may be like "net registered tonnage cleared from the United States for foreign ports" and values are usually labelled "in thousands of tons". Treat these as physical tonnage series, not dollars, even if the question accidentally says "nominal dollars".

## When to Use

Use this skill when the question asks about:

- net registered tonnage cleared from the United States for foreign ports;
- American vessels vs foreign vessels;
- a grand total series for monthly vessel clearances;
- shares/percentages of total tonnage or correlations between vessel categories and totals.

Do not use this for Treasury debt, receipts, outlays, exchange rates, or vessel counts unless the source table explicitly says registered tonnage cleared.

## Source Pattern

Look for a monthly table with columns similar to:

- calendar month/date;
- American vessels;
- foreign vessels;
- grand total / total.

The unit header "thousands of tons" applies to the numeric entries. Keep all series in the same printed units for shares and correlations; scaling cancels for percentages and Pearson correlation.

## Calculation Recipe

1. Identify the exact calendar months requested. For "January, February, and March of 1941", use the three monthly rows Jan 1941, Feb 1941, and Mar 1941; do not convert to fiscal year or quarterly aggregates unless the question explicitly asks.
2. Extract the monthly values for `American vessels` and `Grand total` from the same table and same unit header.
3. For the American-vessel percentage of total over multiple months, aggregate first:

   `percentage = 100 * sum(American vessels for requested months) / sum(Grand total for requested months)`

   Do not average the individual monthly percentages unless the prompt explicitly asks for a mean of monthly shares.
4. For Pearson correlation between American vessels and grand total, use the paired monthly raw values over the requested months:

   `corr = pearsonr([American Jan, American Feb, ...], [Grand total Jan, Grand total Feb, ...])`

   Multiplying both series by 1,000 to convert from thousands of tons to tons is unnecessary and will not change the correlation.
5. Round only at the end. If the requested format is one decimal for the share and nearest thousandth for correlation, compute with full precision and output e.g. `[34.4, 0.391]`.

## Common Pitfalls

1. Treating "calendar months" as fiscal months. Use the printed month rows directly.
2. Treating the table as dollars because the prompt says "nominal dollars". For this table the unit is physical net registered tonnage, usually in thousands of tons.
3. Averaging monthly shares instead of summing American tonnage and grand total tonnage before dividing.
4. Using American and foreign vessels only and forgetting that the grand total column is the required comparison series.
5. Rounding extracted values or intermediate percentages before computing Pearson correlation.

## Verification Checklist

- [ ] The source table says net registered tonnage / cleared for foreign ports.
- [ ] Values came from the requested calendar months, not a fiscal quarter.
- [ ] American-vessel share used sums over the requested months.
- [ ] Pearson correlation used paired monthly American-vessel and grand-total values.
- [ ] Final rounding matches the prompt exactly.
