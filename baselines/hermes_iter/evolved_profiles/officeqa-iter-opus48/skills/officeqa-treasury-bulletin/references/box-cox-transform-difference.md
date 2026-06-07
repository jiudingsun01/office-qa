# Box-Cox transformed difference between two extracted values

## When this applies
Q says: "difference between **Box-Cox transformed values** of <metric> in
<period A> and the same category value for <period B> ... Assume Box-Cox lambda
value of <λ>." Two cells are pulled from the bulletin, each is Box-Cox
transformed, then subtracted. Rounding usually 4 dp.

WORKED: "difference between Box-Cox transformed values of net interest outlays
... FY1981 ... and the comparable 1980 fiscal period reported in November 1981,
λ=0.75" → gold 6.1596 CORRECT.

## The formula (memorize — do NOT call scipy and let it estimate λ)
λ is GIVEN. Apply the standard Box-Cox power transform to EACH raw value
(in the requested unit, here billions of nominal dollars):

    λ ≠ 0:   y(x) = (x**λ − 1) / λ
    λ == 0:  y(x) = ln(x)

Then the answer = y(x_A) − y(x_B), in the SAME order the question names them
(period A minus period B). Round to the stated dp with ROUND_HALF_UP.

Python:
    from decimal import Decimal, ROUND_HALF_UP
    lam = 0.75
    def bc(x): return (x**lam - 1)/lam if lam != 0 else math.log(x)
    diff = bc(x_A) - bc(x_B)
    print(Decimal(str(diff)).quantize(Decimal('0.0001'), ROUND_HALF_UP))

PITFALL: do NOT use scipy.stats.boxcox(data) — that ESTIMATES λ by MLE and
transforms an array. The question fixes λ, so use the closed-form per-value.

## Getting the two cells (the part that actually varies)
"net interest outlays by the federal government, FY1981, billions nominal $" and
"comparable 1980 fiscal period reported in November 1981".

KEY BULLETIN PATTERN — the NOVEMBER bulletin of year N closes FY-N (Oct N-1 →
Sep N) and reports it ALONGSIDE the comparable prior fiscal period (FY N-1). So
the Nov 1981 Bulletin's budget/outlays summary table carries BOTH:
  - "This fiscal year to date" / FY1981 full-year column
  - "Comparable prior period" / FY1980 full-year column
Both values come from the SAME table in the SAME bulletin — you do NOT need the
Nov 1980 bulletin. Find the federal budget receipts/outlays summary (Summary of
Federal Government finances / "Budget Results"), the net-interest line, take the
two year-to-date columns. Convert to billions (cells usually in $millions →
÷1000). Then transform & subtract.

This "Nov bulletin reports closed FY + comparable prior FY in adjacent columns"
layout recurs for any FY-vs-prior-FY question sourced from a November issue —
reuse it.
