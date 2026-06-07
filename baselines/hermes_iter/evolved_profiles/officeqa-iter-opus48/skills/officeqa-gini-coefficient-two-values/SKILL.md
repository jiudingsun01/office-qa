---
name: officeqa-gini-coefficient-two-values
description: OfficeQA Treasury Bulletin — compute the "Gini coefficient" of a SMALL set of fund-statement values, most often exactly TWO values (total receipts vs total expenditures of a trust fund). Covers the closed-form, the population-vs-sample n/(n-1) doubling trap that halves the answer for n=2, the surplus/deficit second-answer, and where the trust-fund receipt/expenditure statements live. FAILED Disability Insurance Trust Fund Sep1975 by emitting 0.006 (population) vs GOLD 0.012 (sample).
---

# OfficeQA — Gini coefficient of trust-fund receipts vs expenditures

## When this applies
Question asks for the "Gini coefficient value as a decimal" over a fund's
total receipts and total expenditures (sometimes "excluding investments"),
usually for a single fiscal month, plus a second answer of "surplus" or "deficit".
Output format: [gini_rounded, surplus|deficit].

The set being measured is almost always just TWO numbers: receipts R and
expenditures E. Occasionally 3-4 line items — same formulas, general n below.

## THE CRITICAL TRAP (this is why I failed)
For exactly two sorted values a <= b there are two Gini conventions that differ by
a factor of 2. OfficeQA's gold uses the SAMPLE (unbiased) convention:

    POPULATION Gini  G_pop    = (b - a) / (2*(a+b))     <- WRONG for OfficeQA (too small by 2x)
    SAMPLE Gini      G_sample = (b - a) / (a + b)       <- CORRECT (matches gold)

Concrete fail: Disability Insurance Trust Fund, fiscal month Sep 1975.
  I emitted 0.006 = population. GOLD = 0.012 = sample = exactly 2x.
RULE: emit the SAMPLE Gini. If you computed the population value, DOUBLE it for n=2.

## General-n formulas (use when 3+ values)
Sort values x_1 <= ... <= x_n, mean mu = (sum x)/n.
  Mean-absolute-difference numerator: MAD_sum = sum_i sum_j |x_i - x_j|.
  G_pop    = MAD_sum / (2 * n^2 * mu)
  G_sample = MAD_sum / (2 * n*(n-1) * mu)   = G_pop * n/(n-1)
For n=2 these reduce to the two boxed formulas above (n/(n-1) = 2).
Emit G_sample.

Equivalent rank formula (sample): with ascending sorted x_i (i=1..n),
  G_sample = ( 2*sum_i (i * x_i) ) / (n * sum x_i)  -  (n+1)/n

## Surplus vs deficit (second answer)
Compare the SAME two figures used for the Gini:
  receipts > expenditures  -> "surplus"
  receipts < expenditures  -> "deficit"
"excluding those attributed to investments" means use the receipt/expenditure
subtotals that already net out interest-on-investments / investment lines —
read the fund statement's own "excluding investments" or net operating rows,
do NOT add interest received on investments back in. The surplus/deficit sign
follows from those same excluded-investment figures.

## Where the data lives
Trust-fund receipt/expenditure statements (Disability Insurance, OASI, Highway,
Unemployment, etc.) are in the "Trust Funds" / "Federal Trust Funds" section of
the bulletin (a "Status of ... Trust Fund" or "Receipts and Expenditures" table).
Find the named fund, then the rows "Total receipts" and "Total expenditures"
(or the "excluding investments" variants). Figures are in thousands or millions —
scaling is irrelevant to the Gini (it is scale-invariant) but DOES matter for any
surplus/deficit magnitude if asked; the sign does not.

## Rounding
Round the Gini to the requested place (thousandths -> 3 dp) only at the END.
Gini is already a ratio; keep full precision through the division.

## Verification checklist
1. Did you pull BOTH the receipts and expenditures figure for the exact fund + month?
2. Are you using the "excluding investments" variant if the question says so?
3. Did you emit the SAMPLE Gini (= (b-a)/(a+b) for two values), NOT population?
4. Sanity: for two values the sample Gini = |R-E|/(R+E); a small relative gap
   gives a small Gini (e.g. R,E within ~1% -> Gini ~0.005-0.01).
5. surplus iff receipts > expenditures.
