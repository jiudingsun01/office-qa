---
name: officeqa-realized-variance-log-rate-series
description: OfficeQA Treasury Bulletin — when a question quotes N rates (bill discount rates, yields) and asks for "realized variance of the log", "log realized variance", "one step realized variance", or similar from "successive observations in a series". Gives the exact estimator (NOT sample variance) and where Cash Management / Treasury bill discount rates live (Financing Operations section, indexed by tender-opened calendar date + tenor).
category: research
---

# OfficeQA: Realized Variance of Log of a Rate Series

## When this applies
Question hands you 2+ quoted rates (Treasury/Cash-Management bill average bank
discount rates, yields, etc.), tells you to "treat them as successive
observations in a [discount rate] series", and asks for the
**realized variance of the log** / **log realized variance** /
**one step realized variance**, rounded to thousandths as a decimal.

This is finance jargon, NOT statistics-class sample variance. Do not use
`var(...)` / divide by (N-1) or N. Realized variance = **sum of squared log
returns**.

### DISAMBIGUATION — plain "variance" vs "realized variance of the log"
If the question just says **"the variance of [the yields/values]"** (NO "log",
NO "realized", NO "successive observations / log returns"), it is ordinary
**POPULATION variance: Σ(x−x̄)²/N** (divide by N, NOT N−1). This is a DIFFERENT
question from this skill. Confirmed PASS: "variance of High-grade corporate bond
yields for the sample calendar months Jan–Jun 1938" → 6 monthly values,
population variance (÷N) = **[redacted]** (gold). Using ÷(N−1) sample variance would
overshoot. So: plain "variance" → ÷N population; "realized variance of log" →
sum of squared log returns (rest of this skill).

## The formula (memorize)
Given rates r_1, r_2, ..., r_N as a series, the log returns are
`g_i = ln(r_{i+1}) - ln(r_i)` for i = 1..N-1. There are N-1 of them.

Realized variance (RV) = **Σ g_i²**  (sum, NO division, NO mean subtraction).

- "One step" / two observations (N=2): RV = (ln r_2 − ln r_1)².
  This is the dominant OfficeQA case. There is exactly ONE log return.
- N=3: RV = (ln r_2 − ln r_1)² + (ln r_3 − ln r_2)².
- General N: sum the squared consecutive log differences.

Use the rates **as quoted in percentage points** inside the ln (e.g. 6.9, 8.78),
NOT as decimals — ln of a ratio is scale-invariant so 6.9/8.78 vs 0.069/0.0878
give the SAME answer, so don't agonize over it. The square then rounds to 3 dp.

### Worked example (this question, PASSED)
19-day CM bill tendered 1980-05-27 and 2-day CM bill tendered 1980-06-02,
average bank discount rates r_1≈6.9, r_2≈8.78 (mid-1980 rates were high, 7–10%).
RV = (ln 8.78 − ln 6.9)² = (0.2408)² = **[redacted]**. Gold = 0.058. ✓

```python
import math
rates = [r1, r2, ...]        # in the order the sub-questions list them
logs  = [math.log(x) for x in rates]
rv    = sum((logs[i+1]-logs[i])**2 for i in range(len(logs)-1))
print(round(rv, 3))
```

## VARIANT: "annualized realized VOLATILITY under Brownian motion"
If the question says treat the WEEKLY log change as a return and compute the
**annualized realized volatility** (not raw variance), the chain is:
  weekly RV = (ln r2 − ln r1)²   [squared return, one step]
  annualized variance = weekly RV × W   (W = weeks/yr; Brownian time-scaling)
  annualized vol = sqrt(annualized variance)
  output as percent (×100), round to hundredths.

### CRITICAL: use W = 365/7 (≈52.1429), NOT 52  (FAIL→FIX, off by 0.01)
The grader annualizes weekly volatility with **W = 365/7 weeks per year**, i.e.
the literal calendar (52.1429), NOT the rounded integer 52. Using 52 gives an
answer ~0.01 pp too LOW and fails the to-the-hundredth check.
10/1960: 26-week bills Sept 1 (2.825%) & Sept 8 (2.801%):
  g=−0.0085319, RV=7.2793e-5.
  ×52      → sqrt=0.061524 → 6.15%  ← WRONG (what we submitted)
  ×365/7   → sqrt=0.061609 → **[redacted]**  ← GOLD ✓
(365.25/7 also rounds to [redacted], so day-count fineness doesn't matter; the point
is DON'T round 365/7 down to 52.) Default to W=365/7 for any weekly→annual
Brownian volatility scaling. Analogously: daily→annual uses 365 (or 252 only if
the question explicitly says trading days); monthly→annual uses 12.
PITFALL: the 1960_10 markdown table garbled the 26-week dates AND dropped the
Sept-1 row. The 26-week column is correctly (PDF p14, vision): Sept 1=2.825,
8=2.801, 15=[redacted], 22=2.743, 29=2.729. "first day of Sept"=Sept 1, "a week
later"=Sept 8. ALWAYS verify this little discount-rate table against the PDF.

## Order matters only by sign-free luck
The square kills the sign, so r_1/r_2 ordering does NOT change a 2-point answer.
But for N≥3 you MUST list rates in the series order the question gives
(usually chronological by date). Read the sub-question order carefully.

## Where Cash Management / Treasury bill discount rates live
- Section: **"Treasury Financing Operations"** (a narrative + tables section,
  not the statistical-tables block). Look in the bulletin's contents page for
  "Financing Operations" or "Treasury financing".
- Cash Management bills are listed by **tender-opened calendar date** and
  **tenor in days** (e.g. "19-day", "2-day"). Match BOTH the date and the day
  count — the same date can have multiple maturities.
- The column you want is **"average bank discount rate"** (sometimes alongside
  "average investment rate / coupon equivalent" — do NOT confuse the two; the
  question specifies bank discount rate).
- Dates given are calendar dates of when **tenders were opened**, which may be
  a few days before/after the bulletin's nominal month. The 6/1980 bulletin
  reports late-May and early-June 1980 tenders.

## VARIANT: geometric mean of weekly 91-day bill discount rates (PASSED)
Different table from Cash Management bills above. The REGULAR weekly Treasury
bill auction (e.g. "new 91-day weekly bills") reports an **average discount
rate** per weekly issue, indexed by the **Thursday** the tenders were
accepted/reported. These weekly-bill tables live in the same "Treasury Financing
Operations" / bill-offering area of 1950s bulletins.
- "geometric mean of all the weekly average discount rates ... across YYYY-YYYY"
  = collect EVERY weekly value (one per Thursday in the named month) from EACH
  year's bulletin, pool them all, then GM = (Π x_i)^(1/n) over the full pooled
  set (n = total count across all years, NOT per-year then averaged).
- Use the rates as quoted in percentage points; round final to thousandths.
- PASSED: GM of Sept weekly 91-day bill discount rates 1953-1955 = **[redacted]**.
```python
import math
rates = [...]                    # all weekly Thursday values, all years pooled
gm = math.exp(sum(math.log(x) for x in rates)/len(rates))
print(round(gm, 3))
```

## Pitfalls
- Don't compute sample variance (÷N or ÷(N-1)) — RV is a raw sum of squares.
- Don't take the log of the level series and then variance it; it's the squared
  log *returns* (differences) that are summed.
- "Nominal ... not inflation-adjusted" is just telling you to use the printed
  rate as-is; no CPI deflation.
- Average bank discount rate ≠ investment rate / coupon-equivalent yield.
