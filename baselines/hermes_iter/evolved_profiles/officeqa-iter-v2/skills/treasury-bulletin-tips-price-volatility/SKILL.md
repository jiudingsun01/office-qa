---
name: treasury-bulletin-tips-price-volatility
description: Use when OfficeQA/Treasury Bulletin questions ask about Treasury Inflation-Protected Securities (TIPS) prices, inflation/index ratios, adjusted prices, or price volatility over date ranges.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [officeqa, treasury-bulletin, tips, volatility, prices]
    related_skills: []
---

# Treasury Bulletin TIPS Adjusted-Price Volatility

## Overview

Treasury Inflation-Protected Securities (TIPS) price questions require applying the table's inflation/index ratio to the quoted price before doing any statistics. OfficeQA prompts may describe the same coupon in different formats, for example `2-3/8% U.S. Treasury Inflation-Protected Security` and `2⅜ percent`.

## When to Use

Use this skill for Treasury Bulletin questions asking for:

- TIPS / Treasury Inflation-Protected Security prices.
- Coupon-matched securities with fractional coupons such as `2-3/8%`, `2 3/8%`, or `2⅜ percent`.
- Adjusted price accounting for inflation or index ratios.
- Price volatility over a date range, especially population standard deviation.

Do not use this for nominal Treasury securities unless the prompt explicitly identifies the security as inflation-protected or asks for index-ratio adjustment.

## Procedure

1. Locate the Treasury Bulletin table that lists market prices for Treasury securities and the applicable TIPS index ratio or inflation adjustment factor.
2. Match the target security by both:
   - security type/name: Treasury Inflation-Protected Security or TIPS, and
   - coupon: normalize Unicode and ASCII fractions so `2-3/8%`, `2 3/8%`, and `2⅜ percent` all compare equal.
3. Keep only observations in the requested date range. Treat date ranges like `between January 1st, 2007 and August 1st, 2007` as inclusive unless the prompt says otherwise.
4. Convert every quoted price to a decimal price before adjustment. If a price is printed in Treasury 32nds or mixed fractional notation, convert the fraction rather than treating it as a decimal string.
5. Compute adjusted price for each observation:

```python
adjusted_price = quoted_price_decimal * index_ratio
```

6. Compute volatility from the adjusted prices. When the prompt says `population standard deviation`, use population SD:

```python
from statistics import pstdev
volatility = pstdev(adjusted_prices)  # divides by n, not n-1
print(f"{volatility:.6f}")
```

`numpy.std(adjusted_prices, ddof=0)` is equivalent. Do not use `statistics.stdev` or `numpy.std(..., ddof=1)` for population-standard-deviation prompts.

## Common Pitfalls

1. Using quoted prices directly. For TIPS adjusted-price questions, multiply each price by its index ratio first.
2. Selecting a nominal Treasury row with the same coupon. Require the TIPS/Treasury Inflation-Protected Security classification.
3. Missing coupon-format equivalence. Normalize Unicode fractions such as `⅜` and ASCII forms such as `3/8`.
4. Treating an inclusive date endpoint as excluded. Include endpoint observations if present.
5. Using sample standard deviation. `population standard deviation` means divide by `n`, not `n-1`.
6. Rounding intermediate adjusted prices. Keep full precision and round only the final answer.

## Verification Checklist

- [ ] Security row is explicitly TIPS / Treasury Inflation-Protected Security.
- [ ] Coupon matches after fraction normalization.
- [ ] Date filtering matches the prompt and includes endpoints when applicable.
- [ ] Every input price is converted to decimal before multiplying by index ratio.
- [ ] Volatility uses population SD (`ddof=0`).
- [ ] Final answer is rounded/formatted to the requested decimal places.
