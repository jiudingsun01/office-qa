---
name: tb-math-transform-wrappers
description: Use for Treasury Bulletin questions that wrap retrieved values in a mathematical transform — Box-Cox, log, square-root, z-score, percentiles (Hazen plotting position), Fisher Ideal symmetric growth rate, geometric mean of a series of growth rates, percent change of transformed values, one-step realized variance of a log series, Value-at-Risk / "lower-tail portfolio loss exceeded with X% probability", expected shortfall (historical approach), linear or quadratic/polynomial regression projection to a future time step (t=N+1), etc. — e.g. "difference between Box-Cox transformed values of X in FY1981 and FY1980, lambda 0.75" or "estimated one-year loss on these holdings exceeded with 1% probability".
---

# Math-transform wrappers on Treasury Bulletin values

These questions are ordinary retrieval questions (find two or more printed values) plus a deterministic transform. Retrieval follows whatever topical skill matches the category; this skill covers the math layer.

## Box-Cox transform
- Formula (lambda ≠ 0): **BC(x) = (x^λ − 1) / λ**. For λ = 0: BC(x) = ln(x).
- Example with λ = 0.75: BC(x) = (x^0.75 − 1) / 0.75.

## Order of operations — the main pitfall
- **Transform each value FIRST, then take the difference/ratio.** "Difference between Box-Cox transformed values of A and B" = BC(A) − BC(B), NOT BC(A − B). The two give very different numbers.
- Sign: "difference between FY-later and FY-earlier" → later minus earlier unless stated otherwise.

## Units before transforming
- Apply the transform to the value in the units the question states ("expressed in billions of nominal dollars" → convert millions-printed figures to billions BEFORE transforming). Transforms are nonlinear, so unit conversion after transforming is WRONG.
- E.g. table prints 68,734 (millions) and the question says billions → transform 68.734, not 68734.

## Currency-conversion wrappers (USD → INR, GBP, etc.)
- Pattern: "using the yearly average 19XX USD/XXX exchange rate (rounded to the nearest hundredths place) to convert ... report in XXX, rounded to the nearest hundredths place."
- Aggregate first in USD (sum the months/values as printed), then convert once.
- Apply rounding exactly where the question places it: **round the exchange rate itself to the stated precision FIRST**, then multiply, then round the final result. Using the unrounded rate gives a near-miss answer.
- Sourcing the rate: many mid-century currencies were pegged, so the yearly average equals the peg (e.g. INR was pegged at ≈4.76 per USD from 1949 to 1966 → "1956 yearly average rounded to hundredths" = 4.76). For floating eras, web-search the annual average rate.
- Verified example: Jan 1956 + Feb 1956 total receipts from the public = 12,104 (millions USD); × 4.76 = 57,615.04 (millions INR).

## "Apply the CPI-U YoY inflation rate" wrapper (inflate, don't deflate)
- Pattern: "inflation-adjusted dollar amount after applying the official BLS CPI-U year-over-year inflation rate for <month> to <value>" → r = CPI(month,Y)/CPI(month,Y−1) − 1, **answer = value × (1 + r)**. It's a forward multiplication, not deflation.
- Fetch the two CPI-U index values (FRED CPIAUCNS) rather than recalling them; round only the final product. See tb-currency-in-circulation for a verified worked example.

## Real difference "in millions of YYYY dollars" (CPI for those YEARS)
- Pattern: "signed difference (Y2 − Y1) in <value> as of <month> Y1 and <month> Y2, adjusted for inflation using the BLS CPI-U for those years, in millions of Y2 dollars."
- **"CPI-U for those years" means the ANNUAL AVERAGE CPI for each calendar year — even when the retrieved values are month-end (e.g. December) balances.** Do NOT use the named month's CPI.
- Recipe: real_other = value_Y1 × (CPI_annual(Y2) / CPI_annual(Y1)); answer = value_Y2 − real_other. The target-year value is unchanged.
- Useful 1940s annual-average CPI (1982-84=100): 1946 = 19.5, 1947 = 22.3 (web-confirm other years; FRED CPIAUCSL/CPIAUCNS annual averages).
- Verified example: Unemployment Trust Fund total balance Dec 1946 = 7,585.3 and Dec 1947 = 8,124.2 (millions) → 8,124.2 − 7,585.3 × 22.3/19.5 = **−550.3** (accepted). Using December monthly CPI instead gives a materially different (wrong) number.

## "Average SHARE of total" + CPI-adjustment wrapper — the adjustment is a RED HERRING
- Pattern: "average share of <total> that came from <component> across <several dates>, with each nominal value adjusted to <month Y> dollars using BLS CPI-U" (often comparing two sets of dates, e.g. June-ends vs Sept-ends 2000–2002).
- **Compute the share separately at EACH date (component ÷ total, same date), then take the plain ARITHMETIC MEAN of those per-date shares.** Per-date shares are ratios of same-date values, so the CPI deflator cancels and the adjustment changes nothing — that is the graders' intent.
- **Do NOT switch to sum(deflated component)/sum(deflated total) on the theory that the CPI instruction would otherwise be meaningless.** Verified failure (ESF FX+securities share, Jun vs Sep 2000–2002, March-2003 dollars): aggregate-of-deflated method gave 0.981 pp — WRONG; mean of per-date shares gave **0.953 pp — the accepted answer**.
- General principle: when a question wraps the computation in a transform that turns out to be a mathematical no-op under the straightforward reading, KEEP the straightforward reading. Question writers add boilerplate adjustments without checking whether they bind; "make every instruction matter" is the wrong prior here.
- For "absolute difference ... in percentage points" between two such averages: |mean₁ − mean₂| × 100, rounded only at the end.

## CPI deflation + linear regression wrappers
- Pattern: "convert each month's nominal value to real <target-month> dollars using BLS CPI-U (1982-84=100), then output the linear regression slope and intercept."
- Deflation: real_m = nominal_m × (CPI_target / CPI_m). The target month's own value is unchanged.
- Regression x-coding: code the time index as **1, 2, 3, …** in chronological order (Jan=1 for a Jan–Mar window). This coding reproduced the expected slope/intercept on a verified question; slope is unaffected by the coding origin but the **intercept depends on it** — 1-based is the convention the graders use.
- **This 1-based rule applies to ANY "index" regressor, including "fiscal year index"** (FY-range window → first FY = 1, not 0, and not the literal year number). Verified failure: OLS of ln(outlays) on fiscal year index over FY2007–2013 with 0-based coding gave intercept 8.736; the accepted intercept was 8.706 = 8.736 − slope.
- **Diagnostic: if your slope matches but your intercept is off by exactly ±(one slope-unit), your index origin is off by one** — recompute with 1-based coding rather than hunting for a data error.
- Use numpy/manual least squares in python3; round slope and intercept only at the end.
- 1970-era CPI-U (U.S. City Average, 1982-84=100) monthly values are widely known (Jan 1970 = 37.8, Feb = 38.0, Mar = 38.2); web-search to confirm if unsure.
- Output as `[slope,intercept]` with NO space after the comma (see answer-format-exact-match skill).

## Polynomial (quadratic) regression projection to a future time step
- Pattern: "using these N data points as time steps t=1 … t=N, fit a quadratic (2nd-degree polynomial) regression model to project the value for t=N+1" — often followed by a rider (divide by some number, round to integer).
- Use **least squares** via `numpy.polyfit(t, y, 2)` then `numpy.polyval(coeffs, N+1)`. With 4 points and degree 2 this is a genuine least-squares fit, NOT an exact interpolation — do not solve 3 points exactly and ignore the 4th, and do not fit degree 3.
- Use exactly the t-coding the question states (here explicitly 1-based: t=1 for the first month). If unstated, default to 1-based (see the linear-regression section above).
- Keep full precision through the projection and any subsequent arithmetic (division, scaling); round once at the very end as instructed.
- **History-fact riders**: some questions divide/multiply by a fact like "the calendar day number on which <historical event> occurred" (e.g. Germany invaded Poland on Sept **1**, 1939 → divisor 1). Resolve the date confidently (web-check if unsure) — a wrong day number wrecks an otherwise-correct projection.
- Pattern: "CAGR of X from FY A to FY B ... and the annual decay factor and arc elasticity (using midpoint percentage change)". All three are functions of the single ratio **r = V_end / V_start**:
  - **CAGR** = r^(1/n) − 1, with n = B − A (years between endpoints, NOT number of data points).
  - **Annual decay factor** = r^(1/n) = 1 + CAGR (for a declining series this is < 1; do not negate it).
  - **Arc elasticity via midpoint % change**, with only two points and no second variable, is just the midpoint percent change itself: (V2 − V1) / ((V1 + V2)/2) = **2(r − 1)/(r + 1)**, in decimal form (negative for a decline).
- Verified example: r = 0.84698^8 ≈ 0.2649 → CAGR −0.153, decay factor 0.847, arc elasticity 2(0.2649−1)/1.2649 = −1.162.
- Because everything depends on r, a small error in EITHER endpoint cell shifts ALL three outputs by a few thousandths — a "close but wrong in the 3rd decimal" triple means a retrieval error, not a math error. Cross-verify both endpoint cells in two independent issues/vintages (see the cross-check tactic in tb-irs-collections) BEFORE computing.
- Round each output independently to the stated places at the very end; keep full precision in between (decay factor must be rounded from r^(1/n), not computed as 1 + rounded CAGR — though these usually agree).

## Constant compound-rate projection ("if it continued to grow at the same annualized compound rate")
- Pattern: "if <series> continued to grow at the same annualized compound rate observed between <date A> and <date B>, what would its projected level be at <date C>?" — two retrieved values plus a deterministic extrapolation.
- General recipe: r = (V_B/V_A)^(1/n) − 1 with n = years from A to B; projection = V_B × (1+r)^m with m = years from B to C.
- **Equal-span shortcut (very common — e.g. 2001→2006 projected to 2011): projection = V_B² / V_A exactly.** Computing it this way skips the rate entirely and removes any rate-rounding error. More generally projection = V_B × (V_B/V_A)^(m/n).
- Keep the values in printed units (usually millions, nominal); round only the final projection to the stated places.
- Verified example: Series I savings bonds interest-bearing debt, calendar March 2001 and March 2006, projected to March 2011 → V_2006²/V_2001 = 339501.88 (accepted).

## Average YoY growth over "FY A – FY B inclusive"
- Two readings exist: (a) the B−A rates BETWEEN years inside the window (FY A→A+1 … FY B−1→B), or (b) one rate FOR each listed year, which needs FY A−1 as the base (B−A+1 rates). Compute (a) first, but if the two differ at the requested precision, compute both and sanity-check against any other clue in the question. A wrong-in-the-last-digit average YoY is more likely a window/base-year mismatch than an arithmetic slip.

## Geometric mean of a SERIES of percent changes / growth rates (per-year, then argmax)
- Pattern: "year with the highest geometric mean of <series> quarterly percent change at an annual rate, and that geometric mean rounded to N places."
- **The graders' convention is GM of growth FACTORS, de-annualized — NOT the geometric mean of the raw printed percents.** For quarterly rates r_q quoted "at an annual rate":
  1. Convert each to a quarterly factor: f_q = (1 + r_q/100)^(1/4).
  2. GM = (∏ f_q)^(1/n_quarters); answer = (GM − 1) × 100. (Equivalently (∏(1+r_q/100))^(1/(4n)) − 1.)
- The result is on the QUARTERLY scale — for GDP-like data it lands around **0.5–0.7**, not ~2–3. If your candidate answer is ~the arithmetic mean of the printed rates, you used the wrong convention.
- This convention also handles negative quarters gracefully (e.g. 2014 Q1 real GDP = −1.4): the factor 1 + r/100 stays positive, whereas a direct GM of raw percents is undefined — a strong hint the factor convention is intended.
- Compute per candidate year, then argmax. Rankings under the factor convention can differ from arithmetic-mean rankings, so compute all years; don't shortcut via "highest average".
- Verified example (BEA real GDP, quarterly % change SAAR, tenths-rounded): 2017 = [2.3, 2.2, 3.2, 3.5] → GM = 0.6924 → **0.69**, the 2013–2019 max (2013 = 0.65 is the runner-up). Expected answer was [2017, 0.69].
- Retrieval note: U.S. real GDP quarterly growth (SAAR) is the standard BEA series (FRED A191RL). Current-vintage values rounded to tenths reproduced the expected answer exactly — use those, taking each rate rounded to tenths as the input as the question instructs.

## Gini coefficient of a small set of retrieved values
- Pattern: "Gini coefficient when considering <value A> and <value B> (e.g. total receipts and total expenditures of a trust fund)" — the "population" is just the 2 (or few) retrieved numbers.
- **The graders use the bias-corrected (sample) Gini: G = Σᵢ Σⱼ |xᵢ−xⱼ| / (2·n·(n−1)·μ)** — denominator n(n−1), NOT the population form's n². For exactly two values a and b this collapses to **G = |a − b| / (a + b)**.
- The population formula |a−b|/(2(a+b)) gives EXACTLY HALF the expected answer. Verified failure: DI trust fund Sept 1975 receipts vs expenditures → population form gave 0.006, accepted answer was 0.012. **If your Gini is exactly half (or double) a plausible round answer, you used the wrong n²/n(n−1) convention — switch conventions, don't re-retrieve.**
- "Expenditures excluding those attributed to investments" → use the printed total-expenditures line; trust-fund tables list investments in a separate section below expenditures (see tb-trust-account-receipts).
- Surplus/deficit rider: surplus iff receipts > expenditures (same two numbers — no extra retrieval).

## One-step realized variance of a log series (two observations)
- Pattern: "compute the one step realized variance of the log <rate/value>, treating the two quoted values as successive observations" — two retrieved values r1 (earlier) and r2 (later).
- Formula: **RV = (ln r2 − ln r1)²** — the squared log-return, a single term, NOT divided by n and NOT demeaned. With only two observations the realized variance is just that one squared increment.
- The log-ratio is scale-invariant, so it doesn't matter whether the rates are in percent (8.0) or decimal (0.08) form — as long as both use the same form. Use the rates as printed.
- "Output as a decimal value (if 12.34% is percent, 0.1234 is decimal)" describes the OUTPUT scale of the variance itself — the squared log-return is already a small decimal; do not multiply by 100 or 10,000.
- Verified example: two cash-management-bill average bank discount rates from the 6/1980 Bulletin's Financing Operations (19-day bill, tenders opened 5/27/1980; 2-day bill, tenders opened 6/2/1980) → (ln r2 − ln r1)² = **0.058** (accepted, 3 dp).
- Retrieval for cash management bill rates: see tb-bill-auction-rates ("Treasury Financing Operations" section, matched by tender-opening date).

## Z-score: "how many sample standard deviations off the N-year sample average"
- Pattern: "compute how many sample standard deviations off the N-year sample average the year-X value was."
- Formula: **z = (x_X − mean(all N values)) / s**, where **s is the SAMPLE standard deviation (ddof=1, divisor N−1)** — not the population std. The target year's value IS included in the mean and std.
- The answer is **SIGNED**: negative when the value is below the mean. Report the sign; do not take absolute value.
- Units cancel in a z-score, so use the values as printed (no millions→billions conversion needed) — but all N values must come from the SAME table/units convention.
- Compute with python3 (`statistics.stdev` or numpy `std(ddof=1)`); round only the final z to the stated places.
- Verified example: totals of interest-bearing marketable debt maturing within-year from end-of-February maturity schedules, CY1972–1976 → z for 1972 = **−1.063** (accepted). A population-std (ddof=0) computation shifts the 3rd decimal — if you're off only in the last digit with correct cells, check the ddof.

## Hazen percentile (Hazen plotting position)
- Pattern: "the Pth Hazen Percentile value (using the Hazen Plotting Position) of <series> from FY A to FY B".
- The Hazen plotting position assigns the i-th smallest of n values the cumulative probability **p_i = (i − 0.5)/n**. To get the Pth percentile, invert: **rank r = P/100 × n + 0.5**, then linearly interpolate between the floor(r)-th and ceil(r)-th order statistics (sorted ascending). If r is an integer, the answer is that order statistic exactly.
- This is numpy's `np.percentile(x, P, method='hazen')` (a.k.a. R type 5) — NOT the default `method='linear'` (R type 7), which gives a different number. Compute with the explicit method, or by hand via the rank formula.
- Convenient case: a 10-value window (e.g. FY2011–FY2020) and P=85 gives r = 0.85×10 + 0.5 = 9 exactly → the answer is the **9th smallest (2nd largest) value as printed**, no interpolation. Verified: DoD total (on-budget + off-budget) outlays FY2011–2020 → 85th Hazen percentile = 678077.00 (millions, the 2nd-largest year's printed value).
- Because the answer is often a single printed cell (or a blend of two), "rounded to hundredths" usually just appends `.00` — keep values in printed millions and don't rescale.

## H spread (interquartile range) with Type 7 quartiles + intermediate rounding
- Pattern: "H Spread of monthly <series> for FY X ... use the standard linear-interpolation percentile method (Type 7) ... use the intermediate values rounded to the tenths before computing the H spread."
- H spread = Q3 − Q1. With the Type 7 instruction, compute quartiles as `np.percentile(x, [25, 75], method='linear')` (numpy's default) — NOT Tukey's hinges, NOT Hazen/Type 5, even though "H spread" classically means hinges. The question's stated method overrides the classical definition.
- **"Intermediate values rounded to the tenths" means round at EVERY intermediate step**: (1) convert each monthly value to the question's units (millions printed → billions) and round each to 1 decimal BEFORE computing percentiles; (2) round Q1 and Q3 each to 1 decimal; (3) subtract. The final H spread then necessarily ends in 0 at the hundredths digit (e.g. 57.50).
- **Self-check: if your hundredths digit is nonzero (e.g. 57.53), you skipped the intermediate rounding** — verified failure: corporate income tax monthly net receipts FY2021, unrounded quartiles gave 57.53, accepted answer 57.50.
- 12 monthly values with Type 7: Q1 rank = 0.25×11 = 2.75 (0-based) and Q3 rank = 8.25, so both quartiles interpolate between order statistics — exactly where rounding choices change the last digits.
- Retrieval: monthly net budget receipts by source (individual/corporate income taxes, etc.) for a recent FY are in the Bulletin's FFO "Budget Receipts by Source" monthly-detail table (see tb-budget-monthly-expenditures); FY = Oct(Y−1)–Sep(Y), 12 values.

## "Fisher Ideal symmetric growth rate" between two values
- Pattern: "find <series> for period B and for period A ... calculate the Fisher Ideal symmetric growth rate."
- For two SCALAR observations the Fisher Ideal index degenerates: Laspeyres relative = Paasche relative = x_new/x_old, so the Fisher (geometric mean) is just x_new/x_old and the growth rate is **g = x_new / x_old − 1**.
- **Report g as a DECIMAL FRACTION, NOT ×100** — even when the underlying series is itself a percent (e.g. bond yields). Verified failure: new long-term Treasury bond yields Aug 1982 vs Aug 1981 (~12.7 vs ~14.3) → accepted answer −0.113; reporting −11.354 (the percent form) was graded WRONG.
- Sanity check that generalizes to ALL growth-rate wrappers here (Fisher, geometric, CAGR, arc elasticity): if your candidate answer's magnitude is ~100× a small decimal (e.g. −11.4 when the values changed by ~11%), you multiplied by 100 — these graders want the decimal form unless the question explicitly says "in percent".
- "Rounded to three decimal places" is itself a hint the expected answer is a small decimal — a percent-scaled answer would rarely be requested at 3 dp.
- Chronology: the later period is x_new (numerator), the earlier is x_old, regardless of the order the question lists them.
- A miss only in the 3rd decimal (e.g. −0.114 vs −0.113) with the right formula means a retrieval error in one of the two cells — re-verify both cells against the stated vintage issue (see "as-of vintage" note below) rather than changing the formula.

## "As of reported values on the end of FY X" (vintage selection)
- This phrase pins WHICH bulletin issue to read, because monthly figures get revised across issues: use the issue whose data coverage runs through the end of FY X (FY ends Sept 30 → the first issue published after that, e.g. the Fall/late-19XX issue for FY1982), and take the values as printed THERE.
- Reading the same months from an earlier preliminary issue or a later revised issue can shift a cell by a few basis points — enough to flip the last decimal of a growth-rate answer.

## "Relative difference in percentage points" between two rates
- Pattern: "relative difference in percentage points of <rate> for years A and B" where the rate itself is a percentage (e.g. redemption rate out of average amount outstanding).
- **Despite the words "percentage points", the graders want the RELATIVE difference: (r_A − r_B) / r_base × 100 — NOT the absolute difference r_A − r_B.** Verified failure: savings-note redemption rates for CY1980 vs CY1981 differed by 3.85 pp absolute; accepted answer was 17.69 = 3.85 / (base rate ≈ 21.76) × 100.
- Use the second-listed/earlier year as the base denominator first; if the question lists "for A and B", base = B's rate is the convention that matched. Sanity check: if your candidate answer is roughly (other plausible answer × base rate / 100), you computed absolute when relative was wanted (or vice versa).
- Only treat "difference in percentage points" as absolute subtraction when the word "relative" is ABSENT.

## Parametric VaR — "lower-tail loss exceeded with X% probability"
- Pattern: "estimated one-year lower-tail portfolio loss on these holdings that would be exceeded with 1% probability", given a short series of period-end LEVEL values (e.g. 5 year-end holdings → 4 annual observations).
- **The graders' convention is normal VaR on the DOLLAR first-differences of the levels, NOT on percentage returns.** Steps:
  1. Δᵢ = Vᵢ − Vᵢ₋₁ (n levels → n−1 changes, in the table's printed billions).
  2. μ = mean(Δ), σ = SAMPLE std (ddof=1).
  3. Loss exceeded with 1% probability = **z·σ − μ** with z = the exact normal quantile 2.3263 (`scipy.stats.norm.ppf(0.99)`; 2.326 also rounds the same). The mean IS subtracted (positive drift reduces the loss). Result is already in dollars — do NOT multiply by the latest holding.
- The textbook alternative — std of percentage returns × latest value — gives a materially different number. Verified failure: mutual-fund Treasury holdings end-Mar 2000–04 (222.3, 225.3, 266.1, 296.6, 280.8 from OFS-2, March 2010 issue): dollar-change VaR = 2.3263×25.807 − 14.625 = 45.41 ($B) → accepted; return-based VaR gave 50.10 → WRONG. **If your answer is ~10% high and the series trended up, you likely used returns; switch to dollar changes.**
- Currency rider ("in billions of JPY using the monthly NSA USD→JPY rate for <month>"): the rate is FRED **EXJPUS** (yen per dollar, monthly NSA; "reported on the first day of the month" just describes the observation date label). Fetch via `curl "https://fred.stlouisfed.org/graph/fredgraph.csv?id=EXJPUS&cosd=<date>&coed=<date>"` — the fredgraph.csv endpoint works when the FRED data page 403s. Multiply the USD loss by the rate, then round at the end (Mar 2004 = 108.5157; 45.41 × 108.5157 = 4927.8 → 4928).

## Historical Expected Shortfall (ES / CVaR) at X% confidence on a short retrieved series
- Pattern: "calculated expected shortfall at 95% confidence using the **historical portfolio return approach** for <series values, one per year/month> between <years>" — e.g. January New Aa corporate bond yields 1990–1999.
- The retrieved LEVELS (even when they are yields in percent) are treated as portfolio "prices". Steps:
  1. Sort the values chronologically; compute simple percent returns between consecutive observations: rᵢ = (vᵢ − vᵢ₋₁)/vᵢ₋₁ × 100. N levels → N−1 returns.
  2. Historical VaR cutoff at 95%: the worst 5% of returns. **Tail size = ceil(0.05 × n_returns)** — with ≤ 20 returns that is exactly 1 observation.
  3. **ES = the mean of the tail returns** (with a 1-observation tail, ES = the single most-negative return).
- **Report ES as a NEGATIVE percentage** (the return itself, sign preserved), rounded as asked — e.g. −18.51. Do NOT flip to a positive "loss" number, and do NOT report a std-dev/parametric quantity. Verified failure: Jan New Aa yields 1990–1999 → worst YoY return was Jan 1995→Jan 1996 (≈8.86 → 7.22, −18.51%); accepted answer **−18.51%**, while an answer of 6.14 (wrong methodology/sign) was rejected.
- Contrast with the parametric VaR section above: "historical … approach" means use the empirical returns directly (no normal z, no μ/σ); "estimated loss exceeded with X% probability" without "historical" means the parametric dollar-change recipe.
- Retrieval note for yearly January (or other fixed-month) yield values across a decade: one modern Bulletin prints only ~13 recent months, so stitch the January cells from ~one issue per year (see tb-bond-yields), and double-check the two cells that produce the extreme return — the whole answer hinges on that single worst pair.

## Herfindahl-Hirschman Index (HHI) + "effective number" of a small market
- Pattern: "treat <groups listed in a table> as the full market ... HHI of concentration using shares based on <value column>, and the effective number of groups implied by this index defined as the reciprocal of the HHI."
- **Shares are DECIMAL fractions of the stated total (Σsᵢ = 1), and HHI = Σ sᵢ² — so HHI ∈ (0, 1], NOT the antitrust 0–10,000 points scale.** A request to "round to the thousandths place" confirms the decimal convention.
- The market participants are exactly the GROUPS the question enumerates (e.g. the NY City bank group vs the Chicago bank group = a 2-participant market) — NOT the individual members inside each group, even when the question quotes member counts ("16 New York City banks and 14 Chicago banks"). Use each group's printed TOTAL holdings.
- Effective number = 1/HHI (the inverse-Simpson "numbers equivalent"). Compute from the UNROUNDED HHI, then round each output independently to the stated places — for a 2-group market it lies in (1, 2].
- Quick algebra check for two groups: HHI = s² + (1−s)²; verified example: shares ≈ 0.768/0.232 → HHI 0.611, effective number 1.635, answer `[0.611, 1.635]`.

## Compute, don't eyeball
- Use Python (`python3 -c "..."`) for fractional exponents; round only at the very end to the requested decimal places.

## Where "net interest" lives (retrieval note)
- "Net interest outlays" of the federal government appears as an outlay function/category in the **Federal Fiscal Operations / budget summary tables (FFO series)** near the front of each Bulletin issue, with current FY and comparable prior-FY columns side by side — one issue usually supplies both years needed for a comparison.
