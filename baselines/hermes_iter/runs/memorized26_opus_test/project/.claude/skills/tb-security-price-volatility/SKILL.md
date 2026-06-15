---
name: tb-security-price-volatility
description: Use for Treasury Bulletin questions about price statistics of a SPECIFIC Treasury security (a named note/bond/TIPS identified by coupon rate) over a date window — volatility/standard deviation, mean price, min/max — especially TIPS questions mentioning "adjusted price" or "index ratio".
---

# Price volatility / statistics for a single Treasury security

## Locating the data
- Per-security prices live in the Bulletin's **market quotations table on Treasury securities** (lists every outstanding issue with its coupon, maturity, and end-of-period bid price; TIPS rows also carry an **index ratio** column and are labeled "inflation-protected"/"inflation-indexed").
- Identify the security by matching the coupon exactly — coupons are printed as vulgar fractions ("2-3/8%", "2⅜"). Convert to decimal (2.375) when matching. If several issues share a coupon, disambiguate by maturity date or the type stated in the question (TIPS vs nominal).
- One observation per period-end per issue ⇒ to cover a multi-month window you typically need quotes from SEVERAL consecutive Bulletin issues. Pull each period-end quote separately; don't assume one issue contains the whole series.

## TIPS adjusted price — the key formula
- **Adjusted (inflation-accreted) price = quoted price × index ratio.** When the question says "use adjusted price accounting for inflation / index ratios", multiply each period's quoted price by that SAME period's index ratio before doing any statistics. Do not use the raw quoted price, and do not apply a single index ratio to all periods.

## Date-window inclusion
- "Between <Month1> 1st and <MonthN> 1st" with period-end quotes ⇒ include every quote whose date falls inside the window: month-ends of Month1 through Month(N−1). E.g. Jan 1 → Aug 1, 2007 with month-end data = Jan 31 … Jul 31 (7 observations). Count your observations explicitly before computing.

## Computing the statistic
- "Population standard deviation" ⇒ divide by N, not N−1. Use `python3 -c "import statistics; print(statistics.pstdev([...]))"` — NOT `statistics.stdev` (sample, ÷(N−1)), and NOT numpy's default only if you set `ddof=0`.
- Watch price notation: Treasury quotes are sometimes in 32nds ("99-16" or "99:16" = 99 + 16/32 = 99.5). Convert to decimal before multiplying/averaging.
- Keep full precision throughout; round once at the very end to the requested decimal places.

## Verified example
- 2⅜% TIPS, adjusted price (price × index ratio) at each month-end Jan–Jul 2007, population std dev → [redacted] (6 dp). Confirmed correct.
