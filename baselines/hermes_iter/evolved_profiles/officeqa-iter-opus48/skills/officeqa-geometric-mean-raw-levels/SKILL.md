---
name: officeqa-geometric-mean-raw-levels
description: OfficeQA Treasury Bulletin — compute the "geometric mean" of a series of RAW LEVEL values over a span of months/years (e.g. "Silver production in thousands of fine ounces from April 1940 to August 1940"). Unlike growth-rate geometric means, raw-level values are NOT converted to (1+r/100) factors — you take the plain nth root of the product of the actual numbers. Distinguishing raw-level vs growth-rate geomean is the whole game.
---

# OfficeQA — Geometric Mean of RAW LEVEL Values

## When this applies
Question asks for the **geometric mean** of a series of plain quantity/level
observations read directly from a table — e.g. silver production (fine ounces),
gold stock, monthly receipts, debt outstanding, a price level — over a date span.

Trigger phrases: "geometric mean of <quantity> from <month/year> to <month/year>",
where <quantity> is a LEVEL (a stock or flow amount), NOT a percent-change or
growth rate.

## THE CORE DISTINCTION (decide this first)
There are TWO different "geometric mean" question types in OfficeQA. Pick correctly:

1. RAW LEVELS (this skill): the quoted/looked-up values are actual amounts
   (ounces, dollars, counts). Compute the plain geometric mean:

       G = (prod x_i)^(1/n)

   Do NOT add 1, do NOT divide by 100, do NOT build factors. The numbers ARE the
   data points.

2. GROWTH RATES (see officeqa-geometric-mean-growth-rates): the quoted values are
   percent changes / rates (real GDP growth %, inflation %). There you MUST convert
   to factors (1+r/100), take the geomean of factors, convert back to percent.

If you apply the factor method to raw levels, your answer is catastrophically
wrong (you'd compute ~1.0). If you apply the raw method to growth rates, also
wrong. Read the units in the question: "thousands of fine ounces" / "$ millions" /
a count => RAW LEVELS. "percent change" / "growth" / "rate" => GROWTH RATES.

## Procedure (raw levels)
1. Identify the N months/periods in the inclusive span. "April 1940 to August
   1940" => Apr, May, Jun, Jul, Aug = 5 data points. Inclusive of BOTH endpoints.
2. Read each period's value from the table in the EXACT units the question states
   (e.g. "in thousands of nominal fine ounces" — use the column already in
   thousands; do not rescale). Keep them as-is, no deflation unless asked.
3. Geometric mean:
       G = (x1 * x2 * ... * xn) ** (1.0/n)
   For numerical stability prefer: G = exp( mean( ln(x_i) ) ).
4. Round to the stated precision (here two decimal places).

## Worked example (PASSED)
Q: "Geometric mean (rounded to two decimal places) of Silver production (in
thousands of nominal fine ounces) in the United States from April 1940 to
August 1940."
- 5 monthly values, plain geometric mean of the raw thousands-of-ounces numbers.
- Answer: [redacted]  (CORRECT)
No factor conversion, no rounding of intermediates, full-precision product then
round final to 2dp.

## Multi-dimensional grids (N is a PRODUCT, not a span)
Some questions take the geomean over a 2-D grid, not a single time span. Example
(PASSED): "geometric mean across each of the 4 U.S. reserve asset values in end
of calendar month July across 2010-2013 inclusive (geometric mean across 16 total
values)." Here N = 4 asset categories x 4 years = 16. Read all 16 raw level values
(the 4 reserve-asset line items — gold, SDRs, IMF reserve position, foreign
currencies — for each of the 4 Julys), take the plain 16th-root geomean. The
question usually states the total count explicitly ("16 total values") — use it
to verify you collected the right cells. Answer there: 29347.01.

## Pitfalls
- Off-by-one on N: a month span is INCLUSIVE of both endpoint months. Apr..Aug = 5,
  not 4. For grids, N = (rows) x (periods); cross-check against any stated total.
- Don't rescale units that are already given (if the column is "thousands of fine
  ounces" and the question asks in thousands, leave it).
- Don't round each monthly value before multiplying; round only the FINAL geomean.
- Confirm all values are POSITIVE (raw production/stock levels are; if any value
  is 0 or negative the geomean is undefined/zero — re-check you're reading the
  right column).

## Output format
Bare number to the stated precision, e.g. `[redacted]`. (Single-value answer; no
brackets unless the question asks for multiple values.)

## Checklist
- [ ] Classified as RAW LEVEL (not growth rate) — no (1+r/100) factors
- [ ] N counted inclusive of both endpoint months
- [ ] Values read in the stated units, not rescaled
- [ ] G = (prod x)^(1/n); intermediates kept full precision
- [ ] Final rounded to stated decimals
