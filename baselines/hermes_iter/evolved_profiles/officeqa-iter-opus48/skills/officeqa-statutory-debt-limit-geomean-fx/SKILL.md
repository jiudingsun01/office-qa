---
name: officeqa-statutory-debt-limit-geomean-fx
description: OfficeQA Treasury Bulletin — questions over the "Statutory Debt Limitation" table that compute, for several fiscal-year-end dates, the RATIO of total interest-bearing securities subject to the limit to total public debt subject to the limit, take the GEOMETRIC MEAN of those ratios, multiply by a specific debt-limit line item (e.g. "U.S. Government securities issued under the Second Liberty Bond Act, as amended, subject to the limitation") as of the last date, then convert USD-millions to GBP/foreign currency via an ANNUAL-AVERAGE FX rate. Covers the table location, the exact ratio/geomean/FX chain, the 1964 GBP divisor, and the FULL-PRECISION rule (never round intermediates). FAILED 4x; closest fail 109523 vs GOLD 109625 (off 0.093% = rounded-geomean signature).
---

# Statutory Debt Limitation: ratio → geometric mean → FX conversion

## When this fires
Question mentions ALL of: "statutory debt limitation" (or "subject to statutory debt limit"),
multiple fiscal-year-END dates (e.g. Feb 29 1960, Feb 28 1961, Mar 31 1962/63/64),
a RATIO of "total interest-bearing securities subject to limit" to "total public debt subject to limit",
a GEOMETRIC MEAN of those ratios, a MULTIPLY by a debt-limit line item (often the
"Second Liberty Bond Act, as amended" securities subject to the limitation), and a CONVERT to GBP
(or other currency) via an annual-average exchange rate.

## Where the data lives
The "Statutory Debt Limitation" / "Public Debt Subject to Limitation" table is in the
Federal Debt section of the Treasury Bulletin (table family FD / "Statutory Debt Limit").
Each fiscal-year-end date is a COLUMN. Rows include:
  - "Total interest-bearing securities" (subject to limit)  <- numerator
  - "Total public debt subject to statutory debt limitation" (or "Total amount subject to limitation") <- denominator
  - line item "U.S. Government securities issued under the Second Liberty Bond Act, as amended" (subject to limit) <- the multiplier
All in $ millions, nominal. Use the bulletin reporting each fiscal-year-end; "fiscal year ending
<date>" means use that date's column (the FY-end balance), NOT a calendar average.

## The computation chain (do EVERY step at full float precision)
1. For EACH of the N dates: ratio_i = (total interest-bearing subject to limit) / (total public debt subject to limit).
   These ratios are each just UNDER 1.0 (e.g. ~0.997), so small truncation compounds — keep ALL digits.
2. geomean = (prod of ratio_i) ** (1/N).  Do NOT round geomean; do NOT round any ratio_i.
3. usd_product = geomean * <multiplier line item as of the LAST date> (e.g. Second Liberty Bond Act amount).
4. fx_value = usd_product / <annual-average exchange rate for the FX year>.
   - For 1964 GBP: divide by 2.7926 (USD per GBP, 1964 annual average). NOT 2.7912 (that is a different year).
     Other notes in this family used a different rate; ALWAYS use the year the question names.
5. Round ONLY the final fx_value to the nearest whole number. Output bare integer, no commas.

## Worked anchor (GOLD-verified)
Feb29-1960, Feb28-1961, Mar31-1962, Mar31-1963, Mar31-1964 ratios -> geomean ->
* Second Liberty Bond Act amount as of Mar31-1964 -> usd_product = 306138.775 (millions USD) ->
/ 2.7926 = 109625 (millions GBP). GOLD = 109625.

## Failure modes (this question has failed 4x)
- ROUNDING THE GEOMEAN OR THE RATIOS mid-stream. The dominant fail. 109523 (off -102, -0.093%)
  vs GOLD 109625 is the exact signature of carrying too few digits in the geomean/ratios.
  RULE: store every ratio and the geomean as full-precision floats; the ONLY round() is the final integer.
- Wrong FX divisor: use 2.7926 for 1964 GBP, not 2.7912.
- Using grand total public debt instead of the "subject to statutory debt limitation" total
  (there are two totals — pick the "subject to limitation" one for BOTH numerator and denominator,
  and for the multiplier line item use the "subject to the limitation" variant).
- Multiplying by the wrong-date multiplier: use the LAST date's (Mar31-1964) Second Liberty Bond Act figure.

## Verification
usd_product / divisor should round cleanly; if you land ~0.09% below an obvious round target,
you almost certainly rounded an intermediate — recompute keeping full precision.
