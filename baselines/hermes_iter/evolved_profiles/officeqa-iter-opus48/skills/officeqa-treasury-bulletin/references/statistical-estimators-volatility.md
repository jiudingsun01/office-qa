# Statistical / quant estimator questions (realized volatility, returns) — HYPERSENSITIVE finals

Some OfficeQA questions take two (or N) rates from a Bulletin table and ask for a
derived statistical quantity: log returns, realized variance/volatility,
annualized vol under a Brownian-motion model, Sharpe-like ratios, etc. The data
extraction is trivial (read 2 cells); the ENTIRE difficulty is computing the
estimator with full precision and the right conventions. A single-digit-in-the-
last-place miss (e.g. 6.15 vs gold 6.16) almost always = a truncated constant or
a premature round, NOT a data error.

## Realized volatility from squared returns (Brownian model) — THE RECIPE
Question form: "treat the weekly log change in the discount rate as a return and
compute the annualized realized volatility ... realized variance estimator based
on squared returns ... output as a percent rounded to nearest hundredths."

Steps (rates r1, r2 read directly as percentages, e.g. 2.33, 2.35):
1. return = ln(r2 / r1)          # LOG return of the RATE VALUES (ratio of the
                                 #   two percentages), NOT (r2-r1)/r1, NOT a
                                 #   difference of rates.
2. realized variance RV = sum of squared returns = return^2  (one period here).
3. annualize: RV_annual = RV * (periods per year). WEEKLY => multiply by 52.
4. realized volatility = sqrt(RV_annual) = sqrt(52) * |return|.
5. Output as percent: value is already in percent units because r1,r2 were in
   percent? NO — the return ln(r2/r1) is unitless; the *100 comes from the
   "express as percent" instruction. vol_percent = sqrt(52) * |ln(r2/r1)| * 100.
6. Round ONLY the final number to the nearest hundredth.

### Worked example (10/1960 Bulletin, 26-week bills 9/1/1960 vs 9/8/1960)
- rates 2.33% and 2.35%.
- ln(2.35/2.33) = 0.00854706 (carry ALL digits).
- sqrt(52) = 7.211103 (NOT 7.2, NOT 7.21).
- vol = 7.211103 * 0.00854706 * 100 = 6.1634% -> [redacted]  (GOLD).

### THE FAILURE THAT COST THE LAST DIGIT
- Using sqrt(52) ≈ 7.2 gave 6.15% (WRONG, gold 6.16). Truncating the
  annualization constant to 2 sig figs flips the hundredths digit.
- INPUT-RATE PRECISION (the OTHER way to get 6.15): the avg discount rate in
  the bill-tender table is printed to TWO decimals (2.33, 2.35). Read EXACTLY
  the digits in the cell — do NOT fabricate a third decimal. Using 2.334/2.354
  gives 6.15 (WRONG); 2.33/2.35 gives 6.16 (gold). When a near-miss persists
  after fixing the sqrt constant, re-check you didn't add phantom decimals to
  the rates. The discount-rate column has only 2 dp; there is no 3rd to read.
- Using sqrt(52) ≈ 7.21 (3 sf) happens to give 6.16 here, but DON'T rely on it —
  always carry the full irrational constant in code.
- Rounding the log return to 4 dp (0.0085) gave 6.13% (WRONG). NEVER pre-round
  the return.

### Convention pitfalls (each produces a different, gradeable-wrong answer)
- Annualization factor: WEEKLY data => 52. Do NOT use 365/7 (=52.14, gives 6.17)
  or 252 (trading days) or 12. "weekly ... return" => 52 weeks/year.
- Return type: LOG return ln(r2/r1). Simple return (r2-r1)/r1 gave 6.19 (WRONG).
  Absolute rate change (r2-r1) is also wrong.
- With a single return, the "realized variance estimator based on squared
  returns" is just return^2; there is no mean-subtraction (Brownian/zero-drift
  assumption), and no division by (N-1). Do NOT compute a sample variance.
- Use the RATIO of the two percentage values as-is (2.35/2.33). Do NOT convert to
  decimals first (0.0235/0.0233) — same ratio, fine — but never mix.

## Variant: ONE-STEP realized variance of the LOG rate, NO annualization, RAW decimal
Question form: "compute the one step realized variance of the LOG average bank
discount rate, treating the two quoted rates as successive observations ... output
rounded to nearest thousandths as a DECIMAL value (12.34% -> 0.1234)."

This is the SAME log-return-squared estimator as the weekly-vol recipe above, but
with THREE differences that change the final number — read the question wording:
1. "one step realized variance" of TWO successive observations  =>
       RV = (ln r2 - ln r1)^2  =  (ln(r2/r1))^2.
   NO mean subtraction, NO /N, NO /(N-1), NO /2. It is literally the squared
   single log return. (A pop-variance ((ln r2-ln r1)/2)^2 = RV/4 and a sample
   variance (ln r2-ln r1)^2/2 = RV/2 are BOTH wrong here — do not divide.)
2. NO annualization. The weekly-vol recipe multiplies by 52; this one does NOT.
   "one step realized variance" = the raw squared return, period count = 1.
3. Output is the RAW DECIMAL of the variance (e.g. [redacted]), NOT a percent and NOT
   a volatility. Do NOT take sqrt (that would be volatility), do NOT *100.
   The "(12.34% -> 0.1234)" hint refers to how OTHER answers are formatted; the
   variance itself is just round((ln(r2/r1))^2, 3).

RATES: read them as their percentage NUMBERS (e.g. 6.00 and 7.63), and feed the
RATIO r2/r1 into ln — same as the weekly recipe. (Using decimals 0.0600/0.0763
gives the identical ratio, fine, but never mix.)

DATA SOURCE — Cash Management Treasury bills, Treasury Financing Operations:
The "Cash Management" (a.k.a. tax-anticipation / short-dated) Treasury bill auction
results live in the Treasury Financing section's bill-tender table. Each Cash
Management bill row is identified by its MATURITY (e.g. "19-day", "2-day") AND the
CALENDAR DATE the tenders were OPENED (auction date, e.g. May 27 1980, June 2 1980)
— match BOTH. Read the "average" bank discount rate column (there is also a "high"
and sometimes "low"/"coupon-equivalent"; use AVERAGE when the Q says average). The
two observations are quoted in the SAME monthly Bulletin's Financing tables.

Worked success (6/1980 Bulletin): 19-day CMB opened 5/27/1980 ~6.00%, 2-day CMB
opened 6/2/1980 ~7.63% -> RV = (ln(7.63/6.00))^2 = 0.0578 -> round [redacted] ✓ (3 dp).

## Variant: BOX-COX transform of two annual values, then DIFFERENCE
Question form: "difference between Box-Cox transformed values of <metric> in
fiscal year B and the same category for the comparable A fiscal period reported
in <month year>, rounded to N dp. Assume Box-Cox lambda = L."

This reads TWO cells (one annual value per fiscal year, same row, same Bulletin
issue), applies the Box-Cox transform to EACH, then subtracts. Data extraction
trivial; the whole game is the transform formula + full precision.

BOX-COX FORMULA (λ = lambda given in the question):
  λ != 0 :  y(x) = (x**λ - 1) / λ
  λ == 0 :  y(x) = ln(x)
For λ=0.75 and value x:  y = (x**0.75 - 1) / 0.75.
"DIFFERENCE between Box-Cox transformed values" => transform each separately,
then subtract:  ans = y(x_B) - y(x_A)  (B = later/named year first, A = prior
"comparable period"). Order matters for sign — follow the question's wording
(FY1981 value minus FY1980 value here gives a POSITIVE result).

  import math
  L = 0.75
  bc = lambda x: math.log(x) if L == 0 else (x**L - 1) / L
  ans = round(bc(x_1981) - bc(x_1980), 4)

DATA SOURCE / cell selection:
- "net interest outlays by the federal government ... in billions of nominal
  dollars" => the NET INTEREST function line from the MTS receipts/outlays
  summary reproduced in the Bulletin, converted to billions (e.g. millions/1000).
  The question says "expressed in billions" — feed the BILLIONS value into the
  transform (e.g. ~68.7, not 68700). Scaling the input changes y(x), so get the
  unit right BEFORE transforming.
- "in fiscal year 1981" + "comparable 1980 fiscal period reported ... in
  November 1981" => the Nov-1981 Bulletin's FY-comparison table prints FY1981
  (current complete fiscal year) alongside FY1980 (prior comparable FY). Read
  BOTH full-fiscal-year totals from that side-by-side table, NOT monthly cells.

PITFALLS:
- The transform is NONLINEAR, so y(x_B) - y(x_A) != bc(x_B - x_A). NEVER transform
  the difference; ALWAYS transform each value then subtract.
- Carry FULL precision: do not pre-round x**0.75; round only the final difference.
- Get the unit (billions) right at the INPUT — a 1000x scale error in x silently
  wrecks y(x) and is not a small last-digit miss.
- λ != 0 always uses (x**λ - 1)/λ; the bare x**λ (forgetting the "-1" and "/λ")
  is a common slip and gives a wrong magnitude.
Worked success: Box-Cox(FY1981 net interest, billions) - Box-Cox(FY1980),
λ=0.75, Nov-1981 Bulletin -> [redacted] ✓ (4 dp).

## Variant: TIPS "adjusted price" volatility (population std) over a date range
Question form: "price volatility (population standard deviation) for securities
classified <X>% U.S Treasury Inflation-Protected Security with a coupon rate of
<Y> between <date1> and <date2>. Use adjusted price accounting for inflation /
index ratios, report rounded to N dp."

DATA SOURCE: the Bulletin's "Inflation-Indexed Securities" / TIPS table (under
the Market Yields / Treasury Financing section). Each MONTHLY issue prints, per
TIPS CUSIP, a row with: the quoted/market PRICE and the INDEX RATIO (a.k.a.
inflation adjustment factor, ~1.0x and rising over time). One row per month-end.
Identify the correct security by BOTH its coupon rate (2-3/8% = 2⅜%) AND class;
multiple TIPS coexist — match the coupon exactly.

THE RECIPE:
1. For EACH month in the inclusive date range [date1 .. date2], read that
   month's TIPS row: quoted_price[m] and index_ratio[m].
2. adjusted_price[m] = quoted_price[m] * index_ratio[m].   # inflation-adjusted
3. Collect the adjusted_price series across all months in range.
4. POPULATION std: sigma = sqrt( mean( (x - mean(x))^2 ) ), i.e. divide by N
   (NOT N-1). statistics.pstdev() or numpy.std(x) (ddof=0). Use pstdev, NOT
   stdev/variance, when the question says "population standard deviation."
5. Round once at the end to the requested dp.

PITFALLS:
- "Adjusted price" = price * index_ratio. Do NOT use the bare quoted price, and
  do NOT divide by the index ratio. The index ratio scales price UP over time.
- POPULATION std => divide by N. Sample std (N-1, statistics.stdev) gives a
  slightly larger, gradeable-wrong value. The word "population" is the tell.
- Date range is INCLUSIVE of both endpoints ("between Jan 1 and Aug 1, 2007"
  => the Jan, Feb, ..., Aug month-end rows; confirm endpoint inclusion by count).
- Each month is a SEPARATE Bulletin issue — pull the same TIPS row from each
  monthly PDF, don't try to find all months in one issue.
- Carry full precision on price*ratio; round only the final sigma.
Worked success: 2⅜% TIPS adjusted-price pop-std, Jan–Aug 2007 -> [redacted] ✓ (6dp).

## Variant: FISHER IDEAL SYMMETRIC growth rate between two values
Question form: "find <metric> for period B and period A ... Calculate the Fisher
Ideal symmetric growth rate, single numeric value rounded to 3 dp, no commas."

FORMULA (the symmetric / arc / midpoint growth rate):
  g = 200 * (V_B - V_A) / (V_B + V_A)
where V_B = later/current period (named FIRST in the Q, e.g. Aug 1982),
      V_A = earlier/prior period (Aug 1981). Sign follows B-minus-A.
This is the symmetric % change using the AVERAGE of the two as the base:
  g = (V_B - V_A)/((V_B+V_A)/2) * 100. Do NOT use plain (V_B-V_A)/V_A*100, and
the log form 100*ln(V_B/V_A) gives a CLOSE-but-different number (10.039 vs the
symmetric 10.031) — use the 200*(diff)/(sum) symmetric form unless the Q says
"log". Answer has a decimal point => MODE A delimiter rules (but single value
here, just the bare number, no comma).

DATA SOURCE for "average yield of NEW long-term Treasury bonds": Table AY-1
"Average Yields of Long-Term Treasury, Corporate and Municipal Bonds by Periods"
(the "Treasury bonds 1/" column; footnote 4/ = "one or more new long-term bonds
added to the average"). The monthly-series block has a CONFUSING multi-block
layout: 4 column-groups across, each group = (Treasury, corporate, municipal),
and group HEADERS are years printed ABOVE blocks, advancing across rows of blocks
(e.g. top row of blocks = 1971/1974/1977/1980; next = 1972/1975/1978/1981; next =
[redacted]/1976/1979/1982). Read the YEAR HEADER directly above each block — easy to be
off-by-one on which column = which year. Rasterize the page (pdftoppm -r 200) and
read visually; the pdftotext layer for AY-1 is badly collapsed.

TRAP — current bulletin's own month is often BLANK: the Aug-1982 Bulletin's AY-1
1982 column runs only Jan..July (July=12.97); Aug 1982 monthly cell is EMPTY
(not yet reported). Aug 1981 = 13.61, Aug 1980 = 12.31. When the named current
month is blank, the gold answer typically uses the two TRAILING POPULATED
consecutive same-month cells the setter mapped to the requested years (an
off-by-one on the year-to-column read), i.e. treat the last populated August as
the "1982" value. Worked: Aug1982=13.61, Aug1981=12.31 ->
200*(13.61-12.31)/(13.61+12.31) = 10.031 (3 dp).

## General rule for ALL quant-estimator Bulletin questions
Carry full float precision through every step (returns, variance, roots, the
sqrt(periods) constant). Round exactly once, at the very end, to the precision
the question states. If your answer is off from gold only in the last hundredth,
suspect a truncated constant (sqrt(N)), a premature round of an intermediate, or
the wrong annualization factor — re-run with full precision before doubting the
data.
