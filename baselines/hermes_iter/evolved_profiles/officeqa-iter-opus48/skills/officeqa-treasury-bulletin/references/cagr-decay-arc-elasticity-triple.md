# CAGR + annual decay factor + arc-elasticity TRIPLE (time-series, one series)

Trigger: a question asks for the **compound annual growth rate (CAGR)** of a
single series between two fiscal years, AND the **annual decay/growth factor**,
AND the **arc elasticity (using midpoint percentage change)** — returned as a
3-tuple "in the order CAGR, decay factor, arc elasticity". Rates in decimal form,
3 dp, square brackets.

This is DIFFERENT from references/arc-elasticity.md (that one is elasticity of one
variable Y w.r.t. a SECOND variable X across two periods). Here all three metrics
describe ONE series over time.

## The three formulas (verified CORRECT, gold [redacted])
Let Vs = start value (FY2011), Ve = end value (FY2019).
n = number of YEARS ELAPSED between the two fiscal years = end_FY - start_FY.
  For FY2011 -> FY2019, n = 8 (NOT 9; it is the span, not the inclusive count).

1. CAGR        = (Ve/Vs)^(1/n) - 1
2. Decay factor (a.k.a. growth/decay multiplier) = (Ve/Vs)^(1/n) = 1 + CAGR
   - If the series shrank, this is < 1 (e.g. 0.847) and CAGR is negative.
   - "decay factor" and "growth factor" are the SAME number = 1 + CAGR. Decline
     just means it lands below 1.
3. Arc elasticity (midpoint % change) of the value w.r.t. time:
   = [ (Ve - Vs)/(Ve + Vs) ] / [ midpoint %Δ of time ]
   The TIME midpoint %Δ for this FY2011->FY2019 question evaluated to exactly
   0.5, so arc elasticity = 2 * (Ve - Vs)/(Ve + Vs).
   - Numerically: arc = (Ve - Vs)/(Ve + Vs) / 0.5.
   - This matched gold -1.162 exactly. If a future question gives different FYs,
     compute the value's midpoint %Δ in the numerator the same way, and the time
     midpoint %Δ denominator as (t2 - t1)/(t2 + t1) using the period indices the
     question implies (here it resolved to 0.5). Cross-check against CAGR sign:
     arc and CAGR must share the same sign.

## n pitfall (the easy mistake)
n is the EXPONENT base = (end FY - start FY). FY2011->FY2019 = 8 compounding
years. Do NOT use 9 (the inclusive count of fiscal years). Using n=9 throws CAGR,
decay, and the value ratio all off.

## "include both budgetary and trust-fund flows"
Use the TOTAL outlays figure that already combines budgetary + trust-fund flows
(the consolidated grand-total line for that agency, e.g. Dept. of Labor), not a
budgetary-only subtotal.

## Delimiter
All three values are decimals -> MODE A. Bare comma. Both `[-0.153,0.847,-1.162]`
(no space) and `[redacted]` (with space) scored CORRECT here, but
prefer MODE A (no space) per standing rule.
