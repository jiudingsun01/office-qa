---
name: treasury-bulletin-seigniorage-coins
description: Use for OfficeQA/Treasury Bulletin questions about seigniorage on coins, especially silver and minor coins across calendar years and growth rates.
---

# Treasury Bulletin: Seigniorage on Coins

Use this skill when a question asks about seigniorage on coins, silver coins, minor coins, or combined coin seigniorage in a U.S. Treasury Bulletin.

## Source/table pattern

1. Look for the Treasury Bulletin table/section containing `Seigniorage on coins` or similar wording.
2. The relevant rows may be split by coin type, commonly including:
   - `Silver coins`
   - `Minor coins`
   - sometimes a combined/total row
3. Values for historical Treasury Bulletin seigniorage tables are commonly labeled in `millions of dollars`; preserve that unit unless the question asks for another unit. For growth rates, scaling cancels as long as start and end use the same units.
4. If the question says `end of CY YYYY to YYYY`, use the annual calendar-year/end-of-year values for those exact years, not fiscal-year totals or monthly observations.
5. If it asks for `coins (silver and minor)`, combine the silver and minor coin values for each endpoint before computing growth, unless the table explicitly provides a matching combined total row.

## Continuous compounded average annual growth

For a start value `S` at end of CY `Y0` and end value `E` at end of CY `Y1`:

```python
import math
rate = math.log(E / S) / (Y1 - Y0)
```

Report as a decimal, not a percent. For example, 6.3% should be `0.063`, not `6.3`.

## Rounding

- If asked for nearest thousandths place, round the decimal rate to 3 places.
- Do not multiply by 100 before rounding when the requested output is a decimal value.

## Silver monetary stock / physical quantity conversion

Use this section when a question asks about `total silver monetary stock`, `silver stock`, `fine troy ounces`, statutory conversion rates, or multiplying implied physical silver quantities by market/real silver prices.

1. Find the `Total silver monetary stock` row/column in the Treasury Bulletin table. These values are usually nominal book values in `millions of dollars`.
   - Match the exact observation date in the prompt (for example, September 1938/1948/1958). Do not substitute fiscal-year, calendar-year, annual-average, or nearby end-of-year values just because they are easier to locate.
2. Convert book value to physical quantity before applying any silver price:

```python
# stock_value_millions is the printed Treasury Bulletin value in millions of dollars
# statutory_rate is dollars per fine troy ounce, e.g. 1.292929... when defined by the prompt/source
fine_oz_millions = stock_value_millions / statutory_rate
computed_value_millions = fine_oz_millions * real_or_market_price_per_fine_oz
```

3. The result is still in `millions of dollars` if the stock input was in millions and the price is dollars per ounce.
4. If the price source gives cents per ounce, divide by 100 before multiplying. If it gives dollars per ounce, do not rescale.
5. For silver prices described as `real`, `inflation adjusted`, or CPI-adjusted, first identify the base/unit of the price series. Do **not** add a second CPI multiplier or convert the result to present-day dollars unless the prompt explicitly asks for that base year. In OfficeQA silver-stock questions, the expected operation is still statutory ounces × the provided per-ounce price after its own unit conversion; an accidental extra inflation factor can make the answer about an order of magnitude too large.
6. For three dates and a requested median, compute the three converted values first, then take the numeric median and round only the final median as requested.

## Monthly silver production

Use this section when a question asks for U.S. `silver production`, `nominal fine ounces`, or monthly production across calendar months.

1. Locate the Treasury Bulletin silver production table/row for the United States; it may be near monetary stock / silver sections rather than seigniorage.
2. Values labeled `in thousands of nominal fine ounces` should be used as printed. Do not convert to dollars, statutory ounces, or millions.
3. For a date range such as `from calendar month April 1940 to August 1940`, include every monthly observation in the inclusive range: Apr, May, Jun, Jul, Aug.
4. For a requested geometric mean, compute the nth root of the product of the n monthly values, equivalently:

```python
import math
values = [apr, may, jun, jul, aug]  # printed monthly values, thousands of nominal fine ounces
geo_mean = math.exp(sum(math.log(v) for v in values) / len(values))
```

5. Round only the final geometric mean to the requested number of decimal places.

## Pitfalls

- `Silver production` is not the same as silver monetary stock, seigniorage, receipts, expenditures, coinage face value, or mined-value dollars; use the exact physical-production row requested by the prompt.
- `Seigniorage` is not the same as receipts, expenditures, coinage face value, or total silver monetary stock; use the exact row requested by the prompt.
- For silver monetary stock questions, do not multiply the printed nominal stock value directly by a silver price. First divide by the fixed statutory dollars-per-fine-troy-ounce conversion rate to recover implied ounces.
- Keep track of dollars-versus-cents silver prices; using cents as dollars inflates answers by 100x.
- Do not average annual percentage changes arithmetically when the prompt says continuously compounded average annual growth rate.
- Do not treat `from end of CY 1945 to 1955` as 11 periods; it is `1955 - 1945 = 10` annual intervals.
- If silver and minor are separate rows, add them at each endpoint first, then take the log ratio.