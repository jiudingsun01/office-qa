---
name: treasury-bulletin-reserve-assets
description: Use for OfficeQA/Treasury Bulletin questions about U.S. reserve assets, including end-of-calendar-month values for gold, SDRs, IMF reserve position, and foreign currencies.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [officeqa, treasury-bulletin, reserve-assets, fraser]
    related_skills: []
---

# Treasury Bulletin U.S. Reserve Assets

## Overview

Use this skill when a Treasury Bulletin question asks about U.S. reserve assets, especially monthly values such as "end of calendar month July" across several years. These tables report U.S. reserve asset component values in millions of dollars; OfficeQA questions often ask for arithmetic or geometric aggregates over selected months and years.

## When to Use

- The question mentions U.S. reserve assets, reserve asset values, gold stock, SDR holdings, reserve position in the IMF, or foreign currencies.
- The question asks for values at the end of a calendar month (for example, July 2010-2013).
- The task asks for a mean, geometric mean, sum, ratio, or trend across reserve asset components.

Do not use for broader Treasury debt, exchange-rate, TIPS, trust-fund, or ESF balance-sheet questions unless U.S. reserve asset components are explicitly involved.

## Source/Table Pattern

- Search the relevant Treasury Bulletin for a table whose title includes "U.S. Reserve Assets" or similar wording.
- The usable rows are monthly observations, usually labeled by end-of-calendar-month month/year.
- Component columns are reserve asset categories, commonly including:
  - gold stock,
  - special drawing rights (SDRs),
  - reserve position in the International Monetary Fund (IMF),
  - foreign currencies.
- Values are reported in millions of dollars unless the table heading says otherwise. Preserve that unit through the calculation unless the question asks for billions or another unit.

## Extraction Procedure

1. Locate the U.S. reserve assets table in the Treasury Bulletin PDF/text.
   - Prefer table title search over page guessing.
   - Use layout-preserving extraction if columns are close together.
2. Identify the requested calendar month rows exactly.
   - "End of calendar month July across 2010-2013 inclusive" means the July row for each of 2010, 2011, 2012, and 2013.
   - Do not substitute fiscal-year rows or annual totals.
3. Select only the requested component columns.
   - If the question says "each of the 4 U.S. reserve asset values," use the four component values, not a grand total column.
   - Confirm whether the table includes a total column; exclude it unless explicitly requested.
4. Strip commas and footnote markers before converting to numbers.
5. Keep all selected values in the same unit. For Treasury Bulletin reserve asset component tables this is typically millions of dollars.

## Geometric Mean Convention

For a geometric mean across N positive reserve asset values:

```python
import math
values = [...]  # all selected positive numeric values, same unit
geo_mean = math.exp(sum(math.log(x) for x in values) / len(values))
answer = round(geo_mean + 1e-12, 2)
```

For a request like "geometric mean across each of the 4 U.S. reserve asset values in end of calendar month July across 2010-2013 inclusive," use 4 years x 4 component columns = 16 total positive values, then return one rounded value.

## Common Pitfalls

1. Including a total column. If four reserve asset values are requested, those are the component columns; a total column would make five values and distort the result.
2. Mixing units. Do not convert millions to billions unless the question explicitly requests a different output unit.
3. Using calendar-year annual rows. "End of calendar month July" refers to the monthly July observation for each year.
4. Arithmetic mean instead of geometric mean. Use logs/products over all selected values, not an average of yearly means unless the question asks for that.
5. Dropping a year endpoint. "2010-2013 inclusive" includes 2010, 2011, 2012, and 2013.

## Verification Checklist

- [ ] Table title is U.S. reserve assets or clearly equivalent.
- [ ] Rows match the requested month and all requested years.
- [ ] Number of selected values matches the wording (for example, 4 components x 4 years = 16).
- [ ] For phrases like "each of the 4 U.S. reserve asset values," treat the four component columns as one flat set across all requested months/years; do not compute per-year geometric means first unless asked.
- [ ] Total column excluded unless requested.
- [ ] Units kept consistent, usually millions of dollars.
- [ ] Geometric mean computed with logs or full product and rounded to nearest hundredth.
