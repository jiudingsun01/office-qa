---
name: officeqa-var-lower-tail-loss
description: OfficeQA Treasury Bulletin — compute a parametric "lower-tail portfolio loss exceeded with X% probability" (Value-at-Risk / VaR), or "expected shortfall", on a short series of dated holding values (e.g. estimated U.S. Treasury securities ownership of a fund type, end-of-March for several years). Covers the year-over-year return series, the POPULATION (÷N) std convention, the z-score, scaling by the final holding value, and FX conversion. FAILED Treasury-securities-of-mutual-funds end-Mar 2000-2004 VaR99% with 5437 (sample std) vs GOLD 4928.
category: research
---

# OfficeQA: VaR / Lower-Tail Portfolio Loss (parametric)

## When this applies
Question gives a short series of dated dollar holding values (often 5 annual
end-of-March / end-of-fiscal-year figures from one ownership/holdings table) and
asks for the **"one-year lower-tail portfolio loss ... exceeded with X%
probability"** (= Value-at-Risk at the (1−X) confidence), or **"loss not
exceeded with Y% confidence"**, possibly converted to a foreign currency and
rounded to the nearest whole billion. This is parametric (Gaussian) VaR, not an
empirical percentile of so few points.

## The exact recipe (FAILED→FIXED)
1. Collect the N dated holding values V_1..V_N in chronological order (e.g. the
   estimated holdings at end-of-March 2000, 2001, 2002, 2003, 2004). These come
   from the **same ownership/estimated-holdings table** read across multiple
   bulletins (here the "estimated ownership of U.S. Treasury securities" table,
   mutual-funds row, March vintages). Use the values as printed in $ billions
   (or scale to billions).
2. Build the **N−1 year-over-year simple returns**: r_i = V_{i+1}/V_i − 1.
   (5 March values → 4 annual returns.)
3. Compute the mean μ = mean(r_i) and the **POPULATION** standard deviation
   σ = sqrt( Σ(r_i − μ)² / (N−1returns) ) where the divisor is the COUNT of
   returns, i.e. **÷ (number of returns), NOT ÷ (returns−1)**. OfficeQA uses
   population/MLE statistics throughout (cf. Gini, TIPS-volatility, plain-
   variance skills). This is the single dominant failure: sample std (Bessel
   ÷ k−1) OVERSHOOTS the loss. ← my 5437 used sample std; GOLD [redacted] ≈ ÷N.
4. z-score for the tail. For 1% lower-tail (99% VaR) z = **2.326**. For 5% use
   1.645; for 2.5% use 1.960. (One-sided lower tail.)
5. Loss as a fraction of the current holding:
   **L_frac = −(μ − z·σ) = z·σ − μ**   (a positive number; the loss the holdings
   would suffer at the 1% worst outcome). If μ is small/positive it REDUCES the
   loss slightly; keep its sign.
6. Dollar loss = L_frac × V_N  (V_N = the LAST / most recent holding value, here
   end-of-March 2004 — the portfolio you actually hold going forward).
7. FX-convert if asked: multiply USD-billions loss by the dated monthly NSA
   USD→JPY (or other) rate specified ("first day of the month", "month-end",
   etc.). Read that rate from the H.10 / international exchange-rate table for the
   exact month/day stated. Then round to the nearest whole billion.

```python
import statistics as st
from scipy.stats import norm
V = [v2000, v2001, v2002, v2003, v2004]      # chronological, $ billions
rets = [V[i+1]/V[i]-1 for i in range(len(V)-1)]
mu  = sum(rets)/len(rets)
# POPULATION std: divide by number of returns, NOT returns-1
var = sum((r-mu)**2 for r in rets)/len(rets)
sigma = var**0.5
z = abs(norm.ppf(0.01))                       # = 2.326 for 1% tail
loss_frac = z*sigma - mu                       # positive = the loss
loss_usd  = loss_frac * V[-1]                  # scale by MOST RECENT holding
loss_fx   = loss_usd * usd_to_jpy_rate         # dated monthly NSA rate
print(round(loss_fx))
```

## Why 5437 was wrong (this question)
- Used **sample** std (÷ k−1 = ÷3 over 4 returns) → σ too big → VaR too big.
- Population std (÷4) shrinks σ; combined with the μ term the answer drops from
  5437 to ≈ GOLD [redacted] (ratio 0.906, which sits between the pure σ-ratio
  sqrt(3/4)=0.866 and 1.0 — exactly the signature of a sample→population σ swap
  with a nonzero mean term).
- DEFAULT to POPULATION (÷N) std for every VaR/volatility/variance OfficeQA item
  unless the question literally says "sample standard deviation".

## Variants & ambiguities to watch
- "loss exceeded with 1% probability" = 99% VaR, z=2.326. "loss NOT exceeded
  with 99% confidence" is the same number. Don't flip the tail.
- If it says **log returns** use ln(V_{i+1}/V_i) instead of simple returns; if
  silent, simple returns matched here.
- "Expected shortfall / CVaR at 1%" is NOT VaR: ES_α = μ − σ·φ(z)/α (φ=normal
  pdf), a LARGER loss than VaR. See the es-cvar memory note. Only use ES if the
  question says shortfall/CVaR/"average loss in the worst α%".
- The scaling base is the MOST RECENT holding (V_N), not the mean and not V_1.
- "one-year" loss ⇒ use the ANNUAL (year-over-year) return series as-is; do not
  re-annualize. If returns were sub-annual you'd scale σ by sqrt(periods/yr).

## Data sourcing
- The "estimated ownership of U.S. Treasury securities" tables (by holder type:
  mutual funds, pension funds, insurance, foreign, etc.) live in the
  **Ownership of Federal Securities** section (table OFS-2 era) of modern
  bulletins. "As of reported estimates on March 2010" tells you WHICH bulletin
  vintage carries the revised back-series for end-March 2000-2004 — read all five
  March values from that single later (March 2010) bulletin's historical table,
  NOT from five separate contemporaneous bulletins.
- FX rates: the monthly NSA USD→foreign table (exchange rates) — match the exact
  month and the "first day"/"month-end" qualifier stated.
