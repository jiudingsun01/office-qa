---
name: officeqa-silver-monetary-stock-physical-quantity
description: OfficeQA Treasury Bulletin — questions that take the TREASURY SILVER (or gold) MONETARY STOCK dollar values ($ millions, nominal) at several dated months, back out the implied PHYSICAL quantity (fine troy ounces) via the FIXED STATUTORY monetary rate per fine ounce, then multiply by a "real inflation-adjusted" silver price and take a median/mean across the dates. Covers the statutory $1.2929/oz silver rate, the gold $35/oz rate, the "real" = CPI-deflated price trap, and the median-of-three selection. FAILED Sep1938/1948/1958 silver median by emitting 3584.40 vs GOLD 2051.51.
category: research
---

# OfficeQA: Treasury Silver/Gold Monetary Stock → Physical Quantity → Real-Price Value

## When this applies
Question gives "total silver monetary stock values (in millions of dollars,
nominal) held by the United States Treasury" at several dated months (e.g.
Sep 1938, Sep 1948, Sep 1958), and asks to:
1. Back out the IMPLIED PHYSICAL QUANTITY (fine troy ounces) using "the defined
   fixed statutory conversion rate per fine troy ounce".
2. Multiply that quantity by the "real inflation-adjusted silver price at that
   time".
3. Return median (or mean) of the three computed values.

Same shape can appear for GOLD (gold monetary stock).

## Where the data lives
- The Treasury Bulletin has a long-running "MONETARY STATISTICS" / "Monetary
  Stock of Gold and Silver" / "Stock of Money" table (early/mid-century
  bulletins). The silver MONETARY stock (a.k.a. "silver held by Treasury",
  "silver bullion + silver dollars + subsidiary coin" valued at monetary
  value) is reported in $ millions. Index by month-end.
- For Sep-of-year sourcing, use the bulletin whose monthly column reports that
  September (often the Oct/Nov bulletin of that year, or a retrospective
  multi-year column).

## The fixed STATUTORY conversion rates (memorize)
- SILVER monetary value = **$1.2929292929 per fine troy ounce**
  (= 100/77.34; the statutory monetary value of silver = $1.29+ per fine oz,
  NOT the $0.50/oz subsidiary coinage figure and NOT the market price).
  Many sources round to $1.29. Treasury monetary silver was carried at
  $1.29292+ per fine ounce. → ounces = (stock $ millions × 1e6) / 1.2929.
- GOLD monetary value (post-1934, pre-1972) = **$35.00 per fine troy ounce**.
  (Pre-1934 = $20.67.) → ounces = ($ × 1e6) / 35.

PITFALL: do NOT use the market price of silver as the "statutory conversion
rate". The statutory rate is fixed by law; the MARKET / real price is the
second multiplier. Confusing the two is the #1 error.

## "real inflation-adjusted silver price at that time" — the key trap
- "Real" = CPI-DEFLATED to a base year, NOT the nominal market price.
  real_price(year) = nominal_market_price(year) × (CPI_base / CPI_year).
- The question's odd phrasing ("compute NOMINAL values ... using the REAL
  inflation-adjusted price") means: value_i = ounces_i × real_price_i, and the
  three results are the "computed values" you take the median of.
- If your answer is HIGH by a CPI-deflator-sized factor (~1.5–1.8×), you most
  likely used the NOMINAL market price instead of the REAL (deflated) price.
  FAILED case: emitted 3584.40 (≈1.747× too high) vs GOLD 2051.51 — consistent
  with skipping the inflation deflation step (or deflating to the wrong base).
- Decide the CPI base year from the question wording; if it says "in constant
  <YEAR> dollars" use that CPI as the base. If unspecified, the deflation is
  still required — pick the base implied (often the latest of the three dates,
  or a stated base). The point is: DO deflate.

## Median selection
- Three computed values → median = the MIDDLE one after sorting (the 2nd of 3),
  NOT the mean, NOT the max. Double-check you sorted before picking.

## Procedure
1. Read silver monetary stock $M for each dated month from the Monetary Stock
   table.
2. ounces_i = stock_i($) / 1.2929  (silver) or / 35 (gold).
3. Get the nominal market silver price for each year; deflate to real using CPI
   (real = nominal × CPI_base/CPI_year).
4. value_i = ounces_i × real_price_i.
5. Sort the three value_i; output the median, rounded to nearest hundredth.

## Output
Single number, nearest hundredth (or bracketed CSV if multiple sub-answers).
