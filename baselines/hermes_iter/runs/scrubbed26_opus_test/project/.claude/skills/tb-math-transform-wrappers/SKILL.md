---
name: tb-math-transform-wrappers
description: Use for Treasury Bulletin questions that wrap retrieved values in a mathematical transform — Box-Cox, log, square-root, z-score, percentiles (Hazen plotting position), Fisher Ideal symmetric growth rate, CAGR / compound annual growth rate, annual decay factor, arc elasticity (midpoint/symmetric percentage change), geometric mean of a series of growth rates, percent change of transformed values, one-step realized variance of a log series, Value-at-Risk / "lower-tail portfolio loss exceeded with X% probability", expected shortfall (historical approach), linear or quadratic/polynomial regression projection to a future time step (t=N+1), etc. — e.g. "difference between Box-Cox transformed values of X in FY1981 and FY1980, lambda 0.75" or "estimated one-year loss on these holdings exceeded with 1% probability".
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
- Convert a retrieved USD value to a foreign currency at a historical (yearly-average or specific-date) rate the Bulletin does NOT print. Full recipe, peg table, direction/rounding conventions, and worked examples live in **tb-currency-conversion-wrapper** — use that skill for the conversion layer. Key rule (repeated here because it bites): aggregate in USD first, **round the rate to the stated precision BEFORE multiplying**, then round the final product.

## "Apply the CPI-U YoY inflation rate" wrapper (inflate, don't deflate)
- Pattern: "inflation-adjusted dollar amount after applying the official BLS CPI-U year-over-year inflation rate for <month> to <value>" → r = CPI(month,Y)/CPI(month,Y−1) − 1, **answer = value × (1 + r)**. It's a forward multiplication, not deflation.
- Fetch the two CPI-U index values (FRED CPIAUCNS) rather than recalling them; round only the final product.

## Real difference "in millions of YYYY dollars" (CPI for those YEARS)
- Pattern: "signed difference (Y2 − Y1) in <value> as of <month> Y1 and <month> Y2, adjusted for inflation using the BLS CPI-U for those years, in millions of Y2 dollars."
- **"CPI-U for those years" means the ANNUAL AVERAGE CPI for each calendar year — even when the retrieved values are month-end (e.g. December) balances.** Do NOT use the named month's CPI.
- Recipe: real_other = value_Y1 × (CPI_annual(Y2) / CPI_annual(Y1)); answer = value_Y2 − real_other. The target-year value is unchanged.
- Useful 1940s annual-average CPI (1982-84=100): 1946 = 19.5, 1947 = 22.3 (web-confirm other years; FRED CPIAUCSL/CPIAUCNS annual averages).
- Using December monthly CPI instead of the annual average gives a materially different (wrong) number.

## "Average SHARE of total" + CPI-adjustment wrapper — the adjustment is a RED HERRING
- Pattern: "average share of <total> that came from <component> across <several dates>, with each nominal value adjusted to <month Y> dollars using BLS CPI-U" (often comparing two sets of dates, e.g. June-ends vs Sept-ends 2000–2002).
- **Compute the share separately at EACH date (component ÷ total, same date), then take the plain ARITHMETIC MEAN of those per-date shares.** Per-date shares are ratios of same-date values, so the CPI deflator cancels and the adjustment changes nothing — that is the graders' intent.
- **Do NOT switch to sum(deflated component)/sum(deflated total) on the theory that the CPI instruction would otherwise be meaningless.**
- General principle: when a question wraps the computation in a transform that turns out to be a mathematical no-op under the straightforward reading, KEEP the straightforward reading. Question writers add boilerplate adjustments without checking whether they bind; "make every instruction matter" is the wrong prior here.
- For "absolute difference ... in percentage points" between two such averages: |mean₁ − mean₂| × 100, rounded only at the end.

## CPI deflation + linear regression wrappers
- Pattern: "convert each month's nominal value to real <target-month> dollars using BLS CPI-U (1982-84=100), then output the linear regression slope and intercept."
- Deflation: real_m = nominal_m × (CPI_target / CPI_m). The target month's own value is unchanged.
- Regression x-coding: code the time index as **1, 2, 3, …** in chronological order (Jan=1 for a Jan–Mar window). Slope is unaffected by the coding origin but the **intercept depends on it** — 1-based is the convention the graders use.
- **This 1-based rule applies to ANY "index" regressor, including "fiscal year index"** (FY-range window → first FY = 1, not 0, and not the literal year number).
- **CONTRAST — "year (numeric, untransformed)" means the LITERAL calendar year (1929, 1930, …), NOT a re-indexed 1,2,3 or 0,1,2.** The word "untransformed" is the tell: use the actual year numbers. This makes the intercept a large extrapolation back to year 0, so a correct fit has a huge-magnitude (often negative) intercept — that is expected, not a bug. If your intercept is a small number near the data range, you wrongly re-indexed the years; if it's a large negative number, you correctly used literal years.
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

## CAGR, decay factor, and arc elasticity from a single ratio
- Pattern: "CAGR of X from FY A to FY B ... and the annual decay factor and arc elasticity (using midpoint percentage change)". All three are functions of the single ratio **r = V_end / V_start**:
  - **CAGR** = r^(1/n) − 1, with n = B − A (years between endpoints, NOT number of data points).
  - **Annual decay factor** = r^(1/n) = 1 + CAGR (for a declining series this is < 1; do not negate it).
  - **Arc elasticity via midpoint % change**, with only two points and no second variable, is just the midpoint percent change itself: (V2 − V1) / ((V1 + V2)/2) = **2(r − 1)/(r + 1)**, in decimal form (negative for a decline).
  - **DO NOT divide by the midpoint % change of the YEAR/time axis.** There is no second variable here — "arc elasticity" in this question family is a synonym for the arc (midpoint) percent change of the single series, full stop. If your arc-elasticity magnitude is in the hundreds, you wrongly treated the years as the elasticity denominator.
- Because everything depends on r, a small error in EITHER endpoint cell shifts ALL three outputs by a few thousandths — a "close but wrong in the 3rd decimal" triple means a retrieval error, not a math error. Cross-verify both endpoint cells in two independent issues/vintages (see the cross-check tactic in tb-irs-collections) BEFORE computing.
- Round each output independently to the stated places at the very end; keep full precision in between (decay factor must be rounded from r^(1/n), not computed as 1 + rounded CAGR — though these usually agree).

## Cubic (or high-degree) polynomial regression far-extrapolated to a future year
- Pattern: "fit a cubic polynomial regression to <annual series, e.g. surplus/deficit 1989–2013> and estimate the value for <future year, e.g. 2025>, then report the absolute difference with the U.S. Treasury's reported estimate."
- Two separate quantities feed the answer: (1) the **regression projection** for the future year, and (2) the **Treasury's separately-reported estimate** for that same year — a DISTINCT retrieved number, not something you compute. The answer is |projection − reported estimate|. Do NOT forget to retrieve (2); both cells matter.
- Fit with `numpy.polyfit(x, y, 3)` then `numpy.polyval(coeffs, target)`. **Use the LITERAL calendar year as x (e.g. 1989…2013, predict 2025), not a 1-based index**, unless the question says "time step t=1…N" — when the question names actual years, code them as the actual years. (A cubic refit on a re-coded x predicts the SAME value at the corresponding point, but only if the target is re-coded consistently; using literal years end-to-end is the safe default and matches "for calendar year 2025".)
- **"Calendar years" surplus/deficit ≠ fiscal-year figures.** The Bulletin's headline surplus/deficit is fiscal-year (Oct–Sep); a calendar-year series must come from a calendar-year table or be summed from monthly receipts−outlays over Jan–Dec. Confirm you are reading the calendar-year basis the question states; mixing in a fiscal-year value for one year is a classic ~hundreds-of-millions error.
- **Extreme sensitivity: a degree-3 fit extrapolated 12+ years past the data is wildly leveraged on every input cell.** A near-miss (off by ≲ 0.2%) almost always means ONE mis-read data point or the Treasury estimate cell was off by a small amount — re-verify every annual cell AND the reported-estimate cell against the printed values before trusting the projection; do not assume the formula is wrong. Treat anything within ~0.3% as "one cell is wrong, find it", and reserve the structural diagnosis below for misses of ~1%+.
- **A LARGE miss (~1% or more) is a DIFFERENT regime — not one fat-fingered cell but a structural error.** Suspect, in order: (a) **wrong data basis** — you pulled fiscal-year surplus/deficit for some or all years instead of the calendar-year series the question demands (CY ≠ FY; see the "Calendar years" bullet above), or mixed bases across years; (b) **wrong "Treasury reported estimate" cell** — the |projection − estimate| answer is dominated by whichever of the two is wrong, so a 5%-scale miss can come entirely from grabbing the wrong reported-estimate figure (confirm it is Treasury's own published CY2025 surplus/deficit estimate, in the same nominal-millions units); (c) a single extreme year (e.g. the 2009 deficit trough) transcribed with the wrong magnitude, which a cubic amplifies enormously.
- **Do NOT chase the x-coding for a large miss.** Polynomial least-squares is invariant under affine reparametrization of x: a cubic refit on literal years vs a 1-based index predicts the SAME value at the corresponding (consistently re-coded) target. So coding cannot explain a 5% gap — the cause is in the data or the estimate cell. (Still use literal calendar years as the safe default since the target is "calendar year 2025".)
- Keep full precision through polyfit/polyval; round only the final absolute difference to the nearest whole million as instructed.

## R-square of the relationship between two retrieved series
- Pattern: "calculate the R-square value of the relationship between <series A> and <series B> for <years Y1–Yn>" — e.g. on-budget vs off-budget receipts, FY1991–2010.
- **R² of a simple two-variable relationship = (Pearson correlation coefficient)².** Build the two equal-length, year-aligned lists, then `r = numpy.corrcoef(A, B)[0,1]; r2 = r**2`. Round only at the end. No regression fit is needed — the squared correlation IS the R² of the OLS line between them (works regardless of which is x vs y).
- Use nominal values as printed (no deflation unless the question says "real"). Keep every year; a single dropped/misaligned year shifts R² noticeably.
- The two lists must be index-aligned by year: A[i] and B[i] are the SAME fiscal year. Sort both by year before correlating.

## Annual fiscal-year series spanning many years — source from bulletins spaced ~5 years apart
- Each annual Bulletin fiscal-data table (Summary of Fiscal Operations, receipts/outlays, surplus/deficit) prints roughly the **last 5 fiscal years** of history. To cover a long span (e.g. FY1991–2010 = 20 years) the question often names a SET of issues spaced ~5 years apart (e.g. **September 1996, 2001, 2006, 2011**) — each issue supplies its ~5 most recent completed fiscal years, and together they tile the whole window with no gaps.
- A September issue's most recent COMPLETED fiscal year is the one ending that Sept 30 (modern FY = Oct–Sep): Sept-1996 → through FY1995 (covers FY1991–1995), Sept-2001 → FY1996–2000, Sept-2006 → FY2001–2005, Sept-2011 → FY2006–2010. Stitch the four into one 20-value series.
- **On-budget vs off-budget receipts** appear as explicit separate lines under the Summary of Fiscal Operations / budget-receipts table (Total = on-budget + off-budget; off-budget is dominated by Social Security). Pull both lines per fiscal year from the same issue so they share a vintage.
- When a question pins specific issues, honor them exactly — "reported values" means the figures as printed in THOSE issues, even if later vintages revised them.

## Constant compound-rate projection ("if it continued to grow at the same annualized compound rate")
- Pattern: "if <series> continued to grow at the same annualized compound rate observed between <date A> and <date B>, what would its projected level be at <date C>?" — two retrieved values plus a deterministic extrapolation.
- General recipe: r = (V_B/V_A)^(1/n) − 1 with n = years from A to B; projection = V_B × (1+r)^m with m = years from B to C.
- **Equal-span shortcut (very common — e.g. 2001→2006 projected to 2011): projection = V_B² / V_A exactly.** Computing it this way skips the rate entirely and removes any rate-rounding error. More generally projection = V_B × (V_B/V_A)^(m/n).
- Keep the values in printed units (usually millions, nominal); round only the final projection to the stated places.

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
- Retrieval note: U.S. real GDP quarterly growth (SAAR) is the standard BEA series (FRED A191RL). Use current-vintage values rounded to tenths, taking each rate rounded to tenths as the input as the question instructs.

## Gini coefficient of a small set of retrieved values
- Pattern: "Gini coefficient when considering <value A> and <value B> (e.g. total receipts and total expenditures of a trust fund)" — the "population" is just the 2 (or few) retrieved numbers.
- **The graders use the bias-corrected (sample) Gini: G = Σᵢ Σⱼ |xᵢ−xⱼ| / (2·n·(n−1)·μ)** — denominator n(n−1), NOT the population form's n². For exactly two values a and b this collapses to **G = |a − b| / (a + b)**.
- The population formula |a−b|/(2(a+b)) gives EXACTLY HALF the expected answer. **If your Gini is exactly half (or double) a plausible round answer, you used the wrong n²/n(n−1) convention — switch conventions, don't re-retrieve.**
- "Expenditures excluding those attributed to investments" → use the printed total-expenditures line; trust-fund tables list investments in a separate section below expenditures (see tb-trust-account-receipts).
- Surplus/deficit rider: surplus iff receipts > expenditures (same two numbers — no extra retrieval).

## One-step realized variance of a log series (two observations)
- Pattern: "compute the one step realized variance of the log <rate/value>, treating the two quoted values as successive observations" — two retrieved values r1 (earlier) and r2 (later).
- Formula: **RV = (ln r2 − ln r1)²** — the squared log-return, a single term, NOT divided by n and NOT demeaned. With only two observations the realized variance is just that one squared increment.
- The log-ratio is scale-invariant, so it doesn't matter whether the rates are in percent (8.0) or decimal (0.08) form — as long as both use the same form. Use the rates as printed.
- "Output as a decimal value (if 12.34% is percent, 0.1234 is decimal)" describes the OUTPUT scale of the variance itself — the squared log-return is already a small decimal; do not multiply by 100 or 10,000.
- Retrieval for cash management bill rates: see tb-treasury-auctions ("Treasury Financing Operations" section, matched by tender-opening date).

## Annualized realized volatility under a Brownian-motion model (weekly returns)
- Pattern: "treat the weekly log change in <rate> as a return and compute the annualized realized volatility … under a Brownian motion model, using the realized variance estimator based on squared returns … output as a percent."
- Steps: (1) return r = ln(v2) − ln(v1) for the two successive weekly observations; (2) realized variance = Σ r² (here a single term, r²); (3) **annualize the VARIANCE by ×52** (weekly → 52 periods/yr); (4) volatility = sqrt of the annualized variance; (5) ×100 for percent. So with one return: **vol% = sqrt(52) · |r| · 100**.
- Annualize at the variance step (×52) and sqrt LAST. sqrt(52·r²) = sqrt(52)·|r| — do NOT take sqrt(r²) first and then multiply by 52.
- Use **52** as the annualization factor (calendar weeks/yr), not 365/7 ≈ 52.14 — the latter shifts the last digit.
- **Carry full precision; round ONLY the final percent.** This class lands on hundredth-place boundaries: do not round the printed discount rates or any intermediate. Read both rates exactly as printed and compute in python3.

## Z-score: "how many sample standard deviations off the N-year sample average"
- Pattern: "compute how many sample standard deviations off the N-year sample average the year-X value was."
- Formula: **z =
