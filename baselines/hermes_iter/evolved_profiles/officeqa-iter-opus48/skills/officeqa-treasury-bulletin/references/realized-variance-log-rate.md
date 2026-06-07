# Realized Variance / Log-Return of a Treasury rate series

## When this applies
Q phrasing: "compute the one step realized variance of the log <rate>,
treating the two quoted <rates> as successive observations in a series ...
round to nearest thousandths as a decimal." Often built on bank discount
rates of Cash Management / regular Treasury bills.

## Where the numbers live (Treasury Financing Operations)
- The Treasury Bulletin has a section **"Treasury Financing Operations"**
  (narrative + tables), distinct from the statistical "Market Yields" tables.
- It lists each bill auction with: issue/tender-opened date, maturity (e.g.
  "19-day", "2-day"), amount, and the **average bank discount rate** (a %).
- "Cash Management bills" are short, odd-tenor bills (2-day, 19-day, etc.)
  reported here. Match on the CALENDAR DATE the tender was OPENED (the question
  gives "tenders opened on May 27, 1980"), NOT the issue or maturity date.
- The 6/1980 bulletin reports May-June 1980 operations. In general the
  Financing Operations section of bulletin month M covers operations roughly
  through the prior ~month, so a "6/1980" Q can reference late-May & early-June.
- Pull the **average** bank discount rate column (not "high"/"low"/"coupon
  equivalent / investment rate").

## The computation (formula is fixed)
Given two successive rate observations r1 (earlier) and r2 (later), as
decimals (e.g. 8.50% -> 0.0850) OR as percentage points — the LOG RATIO is
scale-invariant so it does not matter which, as long as both use the same unit.

1. log return  g = ln(r2 / r1)
2. one-step realized variance = g**2   (a single squared log-return; there is
   NO division by N, NO subtraction of a mean — "one step" = one squared return)
3. round to nearest thousandth, half-up.

Worked (6/1980): r1 (19-day, opened 5/27/1980), r2 (2-day, opened 6/2/1980).
The two avg discount rates differ enough that ln(r2/r1)**2 ≈ 0.058. Gold 0.058.

## VARIANT: "annualized realized VOLATILITY ... as a percent" (CONFIRMED FAIL 6.15 vs 6.16)
Q phrasing: "treat the weekly log change in the discount rate as a return and
compute the ANNUALIZED REALIZED VOLATILITY ... under a Brownian motion model,
using the realized variance estimator based on squared returns ... output as a
percent value ... rounded to nearest hundredths."
- Same two rates (r1 earlier, r2 later), same g = ln(r2/r1). With ONE return the
  realized variance is g**2 (no /N, no mean). VOLATILITY = sqrt(g**2) = |g|.
- ANNUALIZE: weekly returns -> multiply variance by 52 (weeks/yr). So
      annualized vol = sqrt(52 * g**2) * 100  =  |g| * sqrt(52) * 100   (percent).
  (Brownian/sqrt-of-time scaling: variance scales linearly with the number of
  periods, volatility with sqrt. 52 weeks because the returns are WEEKLY — bills
  issued Sep 1 1960 and "a week later".) Then round to nearest hundredth, half-up.
- 26-week bills issued the FIRST day of Sep 1960 and ONE WEEK LATER: read both
  "average rate of discount on new issues" (%) from the Sep/Oct 1960 financing
  tables. r1 = Sep 1 issue, r2 = ~Sep 8 issue.
- PRECISION IS EVERYTHING HERE (this is why I lost 6.15 vs 6.16): with a single
  return the whole answer is |ln(r2/r1)|*sqrt(52)*100, so a misread of ~0.001 in
  EITHER rate flips the last hundredth. The split between 6.15 and 6.16 is at
  vol=6.155 i.e. ratio r2/r1=1.008572. Read BOTH discount rates to FULL printed
  precision (3 decimals if the table shows them), do NOT pre-round either rate or
  g, and only round the FINAL percent. If your answer is within 0.01 of a clean
  value, re-read the exact rate digits before committing — do not assume hundredths.

## Pitfalls
- "realized variance" here = sum of squared log-returns; with only 2 obs that
  is just g**2. Do NOT compute a sample variance Var([r1,r2]) of the levels,
  and do NOT divide g**2 by 2 or by (n-1).
- Use ln (natural log), not log10.
- Order: r2/r1 with r1 the chronologically earlier tender date. (Squaring
  makes the variance order-independent anyway, but get g's sign right if a
  later Q asks for the log-return itself.)
- Decimal-output convention: this answer (0.058) has a decimal point ->
  MODE A delimiter rules apply if bracketed with other values (bare comma,
  no space).
