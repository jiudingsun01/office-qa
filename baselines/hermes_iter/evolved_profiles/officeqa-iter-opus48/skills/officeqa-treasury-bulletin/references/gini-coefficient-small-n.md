# Gini coefficient of a few extracted values (n=2, n small)

## When this fires
Q asks for the **Gini coefficient** of a small set of figures pulled from a
trust-fund / receipts-expenditures table — e.g. "Gini coefficient considering
the total receipts and total expenditures (excluding investments) of the
Federal Disability Insurance Trust Fund, month X, rounded to thousandths."
Plus often a second sub-answer: surplus vs deficit.

## THE DENOMINATOR TRAP (the #1 fail here)
OfficeQA's gold uses the **sample / bias-corrected mean-absolute-difference**
form (denominator n(n-1)), NOT the population form (denominator n²).
The population form gives a Gini that is **exactly (n-1)/n of the gold** — for
n=2 that is exactly HALF. Fail seen: returned 0.006, gold 0.012 (digits all
correct, only the normalization constant wrong, off by factor 2).

### For n=2 (receipts vs expenditures), use the closed form:
    Gini = |a - b| / (a + b)
where a = total receipts, b = total expenditures. That's it — absolute
difference over the sum. Do NOT divide by 2 again.

Worked: receipts 1018, expenditures 994 -> |1018-994|/(1018+994)
       = 24/2012 = 0.011928 -> round 0.012.   (population form would give
       0.006 — WRONG.)

### General small-n formula (gold convention)
    mu  = mean(vals)
    MAD = sum_{i,j} |x_i - x_j| / (n*(n-1))    # sample, n(n-1) NOT n^2
    Gini = MAD / (2*mu)
Equivalently the standard sorted form WITHOUT the population shrink:
    Gini = ( 2*sum_{i=1..n} i*x_sorted_i ) / (n*sum) - (n+1)/n
(both give the same; for n=2 both reduce to |a-b|/(a+b)).

RULE OF THUMB: if your Gini comes out suspiciously small and you used numpy's
`mean abs diff / (2*n*mu)` or any n² normalization, multiply by n/(n-1).

## "excluding those attributed to investments"
Read the trust-fund statement's "Total receipts" and "Total expenditures"
rows but use the variants that EXCLUDE the interest/investment line — i.e. the
table usually breaks out "Receipts: ... interest on investments" and
"Expenditures: ... investments"; subtract or pick the row labeled total
receipts/expenditures net of investment account transactions. Use the two
totals that the question scopes (net of investments), not the gross totals.

## Surplus vs deficit (second sub-answer)
Compare the two net totals used for the Gini:
  - receipts > expenditures  -> "surplus"
  - receipts < expenditures  -> "deficit"
(The fund-statement also often shows a "net increase/decrease in the fund"
line; positive net increase = surplus. Cross-check sign.)

## Output format
Two answers, Gini first then word: `[0.012, surplus]`
Gini has a decimal point so by the delimiter rule the value side is a decimal,
but here the second element is a WORD, so a comma-space `[0.012, surplus]` is
correct (mixed value+word brackets take ", ").
