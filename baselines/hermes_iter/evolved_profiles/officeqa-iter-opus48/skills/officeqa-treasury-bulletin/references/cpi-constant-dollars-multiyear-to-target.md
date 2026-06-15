# Inflation-adjust MULTIPLE prior years to a COMMON target year (constant-$)

## Trigger
Q: "calculate [debt/value] at end of FY Y1, Y2, ... TARGET. Adjust the values
for Y1 and Y2 for inflation to constant <TARGET> dollars using the ANNUAL
AVERAGE BLS CPI-U index. What is the absolute difference between the
inflation-adjusted Y2 value and the inflation-adjusted Y1 value, in millions?"

This is a THIRD CPI pattern, distinct from the two in
`cpi-yoy-applied-to-single-value.md`:
- Pattern A = single value scaled by a YoY rate.
- Pattern B = consecutive-month ASYMMETRIC real-$ MoM change.
- Pattern C (THIS) = several nominal values each rescaled to ONE common
  target-year price level, then compared. SYMMETRIC, static base.

## Formula (do this per prior year, independently)
    real_Yk = nominal_Yk * CPI(TARGET) / CPI(Yk)
Each prior year gets the SAME numerator CPI(TARGET). The target year's own value
is already in target dollars (factor = 1) and is usually NOT in the final answer.

Then:
    answer = | real_Y2 - real_Y1 |
           = | nominal_Y2*CPI(T)/CPI(Y2) - nominal_Y1*CPI(T)/CPI(Y1) |
           = CPI(T) * | nominal_Y2/CPI(Y2) - nominal_Y1/CPI(Y1) |

## CPI index source — ANNUAL AVERAGE, not monthly
- Use BLS CPI-U, U.S. city average, ALL items, NSA, base 1982-84=100.
- The Q says "ANNUAL AVERAGE" -> use the calendar-YEAR average index (the 13th
  "Annual" column on BLS), NOT a single month. Do not grab a monthly value.
- These are EXTERNAL constants (not in the Bulletin). Annual-avg CPI-U:
  1960 = 29.6, 1961 = 29.9, 1962 = 30.2, 1963 = 30.6, 1964 = 31.0,
  1965 = 31.5, 1966 = 32.4, 1967 = 33.4, 1968 = 34.8, 1969 = 36.7,
  1970 = 38.8, 1971 = 40.5, 1972 = 41.8, [redacted] = 44.4, 1974 = 49.3,
  1975 = 53.8, 1976 = 56.9, 1977 = 60.6, 1978 = 65.2, 1979 = 72.6.
  (Cross-check against `external-historical-constants.md` if present.)

## Debt figure — which row, which issue
- "public debt outstanding as of end of Federal Fiscal Year YYYY" -> the
  TOTAL PUBLIC DEBT OUTSTANDING line at fiscal-year-end. US federal FY ended
  June 30 in this era (pre-1977), so "end of FY1960" = June 30 1960. Read the
  June column / the FY-end issue.
- If the Q adds an "include agency/FHA securities" clause, switch to the GRAND
  TOTAL gross debt row instead (see gross-federal-debt-multiyear-list.md).

## Arithmetic discipline
- Carry FULL precision through the rescale; round ONLY the final difference.
- The answer is a DECIMAL value -> MODE A delimiter: bare value, no commas
  ("no commas" is stated explicitly). Round to the requested place (thousandths).
- Absolute value -> answer is POSITIVE regardless of which year is larger.

## Worked CORRECT (FY1960/61/62 public debt, constant 1962 $, |Δ|)
Nominal end-of-FY public debt (June 30, $millions):
  FY1960 = 286,331  FY1961 = 288,971  (FY1962 not needed in the diff)
real_1960 = 286,331 * 30.2/29.6
real_1961 = 288,971 * 30.2/29.9
answer = |real_1961 - real_1960| = [redacted]  (gold = [redacted], CORRECT)

## SIGNED variant + target-is-one-of-the-compared-years (IMPORTANT sub-case)
Some Qs ask for the SIGNED difference in a stated order, e.g. "signed difference
(1947 - 1946) ... in millions of 1947 dollars". TWO things change vs the |Δ| case:
1. Do NOT take absolute value. Compute in the stated order. Sign can be negative.
   real(Y_first) - real(Y_second), exactly as written in the parentheses.
2. The TARGET year is often ONE of the two compared years (deflate "to 1947
   dollars", comparing 1946 vs 1947). Then real_1947 = nominal_1947 (CPI factor
   = CPI(1947)/CPI(1947) = 1); only the OTHER year (1946) gets rescaled:
       real_1946 = nominal_1946 * CPI(1947)/CPI(1946)
       answer = nominal_1947 - real_1946   (order 1947 - 1946)
   Rounding here = ONE decimal place (Q-specified), not thousandths. Always read
   the Q's own rounding clause; it overrides any blanket rule.

## Annual-average CPI-U (1982-84=100) for 1940s (extend the table above)
  1946 = 19.5, 1947 = 22.3, 1948 = 24.1, 1949 = 23.8.
(So CPI(1947)/CPI(1946) = 22.3/19.5 = 1.14359.)

## Worked CORRECT (Unemployment Trust Fund, signed 1947-1946, 1947 dollars)
Total balance ($millions, from the Trust-fund statement): Dec1946 nominal and
Dec1947 nominal. Deflate Dec1946 to 1947 $: real_1946 = nom_1946 * 22.3/19.5.
answer = nom_1947 - real_1946 = [redacted]  (gold = [redacted], CORRECT).
Negative because the 1946 balance, inflated into 1947 dollars, exceeds 1947.

## Takeaway
Same-numerator CPI(target) on every prior year; annual-average index; round only
the final difference. SIGNED Qs keep the parenthesized order and can be negative;
when target = one of the years, that year's factor is 1. Decimal answer = bare
value, no commas; honor the Q's stated decimal place.
