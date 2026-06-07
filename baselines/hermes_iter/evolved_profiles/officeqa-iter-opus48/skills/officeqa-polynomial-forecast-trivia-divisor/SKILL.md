---
name: officeqa-polynomial-forecast-trivia-divisor
description: OfficeQA Treasury Bulletin — fit a POLYNOMIAL (quadratic/cubic) regression to a SHORT monthly series (e.g. 4 consecutive months as t=1..N), project the next time step, then divide or multiply the projection by a HISTORICAL-FACT number embedded in the prose (e.g. calendar day Germany invaded Poland in Sept 1939 equals 1). Two stages — (1) exact polyfit forecast on tiny data, (2) decode the trivia divisor. Also covers the 1939 international flows of liquid banking funds grand-total table in the Capital Movements section. PASSED May-Aug1939 liquid banking funds quadratic to Sept divided by 1 equals 566840.
---

# OfficeQA — Polynomial Forecast / Historical-Trivia Divisor

## When this applies
The question has TWO distinct stages glued together:
1. "Fit a quadratic (2nd-degree polynomial) / cubic regression to these N monthly data points (t=1..N) and project the value for the next month (t=N+1)."
2. "Identify [some historical fact that resolves to a NUMBER] and divide/multiply your projection by it. Report a single integer."

The historical fact is deliberately obscured trivia. Examples seen / likely:
- "calendar day number in September 1939 on which Germany invaded Poland" = **1** (Sept 1, 1939). Dividing by 1 is a no-op — the projection IS the answer (after rounding).
- Any "day Germany invaded Poland" / "VE Day" / "Pearl Harbor day" etc. -> resolve to the day-of-month integer.

DO NOT skip stage 2 thinking it's filler — but also recognize when the divisor is 1 (no-op). Sept 1, 1939 = invasion of Poland -> divisor 1.

## The data table (1939 liquid banking funds)
"Aggregate international flows of liquid banking funds (excluding brokerage balances and security transactions)" lives in the **Capital Movements / International Capital** section of the 1939 Treasury Bulletins. It's the table of net movements of short-term banking funds; the row wanted is the **monthly GRAND TOTAL** (net inflow/outflow), NOT a sub-component, NOT brokerage balances, NOT security-transaction lines.
- One value per calendar month. For "May through August 1939" you need the May, Jun, Jul, Aug grand totals.
- Units are typically $ thousands in these 1939 capital-movement tables — KEEP the raw units the table uses; the final answer is a large integer (~hundreds of thousands), consistent with thousands-of-dollars magnitude. Do NOT rescale.
- Sourcing: the monthly grand totals for May–Aug 1939 appear across the mid/late-1939 bulletins (the bulletin reporting a given month publishes a few months later). Pull each month's grand total from the bulletin that reports it.

## Exact computation (stage 1)
Use numpy polyfit with the literal time index t = 1,2,3,...,N (NOT calendar dates).

```python
import numpy as np
t = np.array([1,2,3,4])              # May=1 ... Aug=4
y = np.array([v_may, v_jun, v_jul, v_aug])  # raw grand totals
coeffs = np.polyfit(t, y, deg=2)     # quadratic. deg=3 if "cubic"
proj = np.polyval(coeffs, 5)         # t=5 = September
```

With 4 points and deg=2 the fit is over-determined (least squares) — that is correct, use polyfit's LSQ solution. With exactly deg+1 points it interpolates exactly. Match `deg` to the wording: "quadratic / 2nd-degree" = 2, "cubic / 3rd-degree" = 3.

## Stage 2 and rounding
```python
divisor = 1   # Sept 1 1939 = day Germany invaded Poland
answer = round(proj / divisor)   # nearest whole number
```
Round ONLY at the very end, to the nearest integer.

## Pitfalls
- Wrong `deg` (using linear when "quadratic" asked) -> wrong projection.
- Using calendar-month numbers (5,6,7,8) as t instead of 1..4: the intercept/curvature change and the t=5 projection drifts. Use t=1..N as the question instructs ("t=1 (May) through t=4 (August)").
- Forgetting / mis-resolving the trivia divisor. Germany invaded Poland **September 1, 1939** -> 1.
- Rescaling units: don't. The answer magnitude (~5.7e5) matches the table's native thousands; output the raw projected number divided by the trivia integer.
- Picking a sub-row (e.g. just one country, or "exclusive of" lines) instead of the monthly GRAND TOTAL of net liquid-banking-fund movements.
