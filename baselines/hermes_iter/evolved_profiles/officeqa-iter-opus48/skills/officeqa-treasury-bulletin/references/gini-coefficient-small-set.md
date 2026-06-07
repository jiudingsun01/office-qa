# Gini coefficient on a fund's receipts vs expenditures (and other small value sets)

Trigger: Q asks for the "Gini coefficient" computed over a SMALL set of dollar
values pulled from a Treasury Bulletin fund statement — typically just TWO values
(total receipts and total expenditures of a trust fund), sometimes also a
surplus/deficit follow-up.

## THE CONVENTION OFFICEQA USES (critical)
OfficeQA grades against the SAMPLE (unbiased) Gini, which applies the n/(n-1)
correction — NOT the population Gini. For a 2-value set these differ by EXACTLY
a factor of 2, which is the single most common way to get this wrong.

For values x_1..x_n with mean μ:
- Population Gini  = ( Σ_i Σ_j |x_i − x_j| ) / ( 2 · n² · μ )
- SAMPLE   Gini    = ( Σ_i Σ_j |x_i − x_j| ) / ( 2 · n·(n−1) · μ )   ← USE THIS
  (sample = population × n/(n−1))

Closed forms for n=2 values a, b:
- Population: |a − b| / ( 2·(a + b) )          ← WRONG for OfficeQA
- SAMPLE:     |a − b| / ( a + b )              ← CORRECT (= 2× population)

## WORKED FAILURE (why this ref exists)
Q: Gini of total receipts vs total expenditures (excl. investments) of the
Federal Disability Insurance Trust Fund, fiscal month Sept 1975, to nearest
thousandth; plus surplus or deficit.
- Emitted [0.006, surplus] using population formula → WRONG.
- Gold [0.012, surplus]. 0.012 = |a−b|/(a+b) = sample formula = 2 × 0.006.
The surplus/deficit half was right (receipts > expenditures ⇒ surplus); only the
Gini convention was wrong.

## RECIPE
1. Pull the two dollar figures from the fund statement. "Excluding those
   attributed to investments" means use the receipts/expenditures totals that
   EXCLUDE interest-on-investments and the buying/selling of investments —
   read the labeled total row, not the grand total that folds investments in.
2. Compute Gini = |a − b| / (a + b) for two values (sample convention).
   For n>2 values use Σ Σ |x_i−x_j| / (2·n·(n−1)·μ).
3. Round to the requested place (here thousandths).
4. Surplus/deficit: receipts > expenditures ⇒ surplus; else deficit.
5. Output order exactly as asked: [gini, 'surplus'|'deficit'].

## PITFALLS
- DEFAULT TO THE SAMPLE FORMULA (÷ n(n−1)), not population (÷ n²). If unsure,
  remember the failure above: gold matched the 2× (sample) value.
- numpy/pandas naive Gini implementations and most online formulas give the
  POPULATION value — do not trust them; halving error follows.
- Scale cancels in Gini (ratio of differences to sum), so units (millions vs
  billions) don't matter for the Gini value — but DO matter for surplus/deficit
  sign only via which figure is larger (sign is scale-invariant too). The real
  risk is picking the wrong two rows (investment-inclusive vs exclusive).
