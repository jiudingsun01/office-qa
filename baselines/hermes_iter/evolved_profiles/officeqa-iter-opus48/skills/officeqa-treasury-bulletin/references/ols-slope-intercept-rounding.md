# OLS slope + intercept: the intercept last-digit rounding trap

## Trigger
Q asks: "fit an ordinary least squares linear regression with YEAR (numeric,
untransformed) as predictor and X as outcome. Return slope and intercept ...
rounded to the nearest thousandth." The predictor is the raw calendar year
(e.g. 1929..1942), NOT 0/1/2... or year-1929.

## The failure (observed)
Q: US individual income tax receipts (net of refunds) FY1929-1942, billions
nominal, OLS on untransformed year.
- Submitted: [0.096,-184.142]   Gold: [0.096, -184.143]   WRONG by 0.001 on
  intercept only; slope perfect.

## Root cause — INTERCEPT IS ~mean_x TIMES MORE SENSITIVE THAN SLOPE
With untransformed year, intercept = mean_y - slope*mean_x, and mean_x ~= 1935.
So a slope error of just 5e-7 becomes a 5e-7 * 1935 ~= 0.001 intercept error —
exactly one unit in the thousandths place. Verified: [redacted] * 5e-7 = [redacted]e-4.

Therefore: ANY use of a rounded/truncated slope, or fitting with float32, or
a centered-then-uncentered hand computation, can shift the intercept's last
digit even when the slope still rounds to the same 3 dp.

## DO THIS (robust recipe)
1. Fit ONCE at full float64 precision; never round an intermediate.
   `import numpy as np; m, b = np.polyfit(years, y, 1)`
   (or `from scipy.stats import linregress; r = linregress(years, y)` then
   `r.slope, r.intercept`). Both give the SAME full-precision intercept.
2. Round slope and intercept INDEPENDENTLY from the full-precision fit:
   `round(m, 3)`, `round(b, 3)`. Do NOT compute intercept from the rounded
   slope. Do NOT do `mean_y - round(m,3)*mean_x`.
3. Keep the predictor as the literal years given; do not re-base to 0/1.
   (For the SLOPE, re-basing is invariant; for the INTERCEPT it is NOT —
   re-basing changes the intercept entirely. Use the years the Q specifies.)
4. Use Python's banker's rounding via `round()` OR numpy default; for a value
   like -184.1425xx both agree. If the unrounded intercept is a near-exact
   half (…xxx5000), prefer the full-precision value's natural rounding — do not
   hand-round.

## Self-check before submitting slope+intercept
- Recompute intercept two independent ways (polyfit b vs mean_y - m_full*mean_x
  using FULL m). They must agree to >6 dp. If they differ in the 3rd dp you
  rounded the slope somewhere.
- Predict y at mean_x: should equal mean_y to full precision
  (m_full*mean_x + b_full == mean_y). If off, the fit is wrong.

## Data note
FY1929-1942 individual income tax receipts (net of refunds) regress to
slope ~= 0.096, intercept ~= -184.143 (billions, year untransformed). The
slope being tiny (~0.1) with mean_x~1935 is precisely what makes the intercept
fragile — a general property of any "untransformed year" regression where the
slope is small.
