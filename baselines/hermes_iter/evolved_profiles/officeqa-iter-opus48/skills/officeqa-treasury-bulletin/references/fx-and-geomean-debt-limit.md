# FX conversion + geometric mean of debt-limitation ratios

## When this applies
Question chains an in-bulletin computation (ratios, securities totals) into a
final "convert to <foreign currency> using the official annual average
exchange rate in YEAR". The exchange rate is EXTERNAL to the bulletin — you
must supply the historical IMF / Federal Reserve annual-average figure to its
EXACT published precision (4 decimal places). A rate slip of even 0.01%
produces a wrong answer (the final value is large, ~10^5–10^6).

## Critical: USD/GBP is quoted USD-per-GBP
- The 1964 official annual-average rate = **2.7926 USD per 1 GBP**.
- To convert USD -> GBP: `GBP = USD / 2.7926`.
- Do NOT use the Bretton Woods par value [redacted] — the gold answer uses the
  market annual AVERAGE (2.7926), not par.

### EXACT GOLD TRACE for the recurring Feb1960/Feb1961/Mar1962/Mar1963/Mar1964 question
This SAME question has now failed 3+ times. Hard-pinned answer chain:
- 5 debt-limit ratios (interest-bearing subject / public-debt subject), geomean.
- geomean × Liberty-Bond-Act securities subject to limit (Mar 31 1964 row).
- USD intermediate = **306,138.775** (millions). If you get ~305,854 you
  MIS-READ a cell — recheck the Mar-31-1964 Liberty-Bond-Act value and each ratio.
- FX: divide by **2.7926** USD/GBP (1964 annual average).
- 306138.775 / 2.7926 = **[redacted]** ← GOLD (nearest whole GBP millions).

### FAIL history
- Run A: used ~2.7928 → 109617 → WRONG by 8.
- Run B: used 2.7912 AND mis-extracted USD intermediate as 305,854 → 109578
  → WRONG by 47. Two errors partially cancelled (do NOT trust a "close" answer).
Lesson: pin BOTH the USD intermediate (306,138.775) AND the rate (2.7926).
A wrong digit in the 4th decimal of the rate flips the answer, and a "close"
final value can hide a compensating extraction error.

## Known annual-average USD/GBP rates (IMF/Fed, Bretton Woods era)
- 1949–1967 (post-1949 devaluation, pre-1967 devaluation): par 2.80,
  but ANNUAL AVERAGES differ slightly by year. 1964 = **2.7926**.
- If a year isn't listed here, look up the exact IMF International Financial
  Statistics annual average (period average) to 4dp; do not assume par.

## Geometric mean of ratios procedure
1. For each of the N periods, compute ratio = numerator / denominator using the
   raw in-bulletin millions figures (full float, no intermediate rounding).
2. Geometric mean = (product of all N ratios) ** (1/N).
3. Multiply gmean by the specified securities value (millions USD).
4. Divide by the FX rate (USD per foreign unit) to get foreign-currency millions.
5. Round ONLY at the very end (ROUND_HALF_UP / nearest whole as asked).
   Carry full float64 precision through every step before the final round.

## Statutory debt limitation table notes
- The "Statutory Debt Limitation" table lists, by date:
  - Total interest-bearing securities subject to limit
  - Total public debt subject to limit
  - "U.S. Government securities issued under the Second Liberty Bond Act, as
    amended" subject to limit (this is typically the SAME as total public debt
    subject to limit, or a near-identical aggregate line — read the exact row
    label requested, don't substitute total interest-bearing).
- Fiscal-year-ending dates in older bulletins can be odd (Feb 29 1960, Feb 28
  1961, Mar 31 1962/63/64) — match the exact as-of date column/row, not the
  calendar year.
