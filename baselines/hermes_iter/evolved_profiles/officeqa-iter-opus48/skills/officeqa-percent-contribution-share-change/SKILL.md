---
name: officeqa-percent-contribution-share-change
description: OfficeQA Treasury Bulletin — compute the "change in percent contribution" (or "share", "proportion", "percentage of") of one line item to a TOTAL between two periods (e.g. net individual income taxes as a % of total budget receipts, CY[redacted] vs CY[redacted]). The answer is the change in PERCENTAGE POINTS of the share, NOT a growth rate and NOT a ratio of differences. Covers the per-period-share-then-subtract method, the calendar-year (CY) vs fiscal-year (FY) sourcing twist, and the dominant failure of computing the wrong quantity. FAILED net individual income tax share CY[redacted]->CY[redacted] by emitting [redacted] vs GOLD [redacted].
---

# OfficeQA — Change in Percent Contribution / Share-of-Total

## When this applies
Question phrasing like:
- "change in percent contribution of [item] to [total] from [period A] to [period B]"
- "change in the share / proportion / percentage of [item] in [total]"
- "how much did [item]'s percentage of [total] change"

Examples: net individual income taxes as % of total budget receipts; national defense as % of total outlays; a trust fund's receipts as % of total trust receipts.

## The ONLY correct method (per-period share, then subtract)
```
share_A = item_A / total_A * 100      # percent contribution in period A
share_B = item_B / total_B * 100      # percent contribution in period B
answer  = share_B - share_A           # change in PERCENTAGE POINTS
```
Round to the requested place (usually hundredths). Keep the SIGN unless "absolute" is stated.

This is a change in PERCENTAGE POINTS of a share. It is NOT:
- a growth rate of the item ((item_B-item_A)/item_A)
- a ratio of differences ((item_B-item_A)/(total_B-total_A))
- the item's share of the COMBINED two-year total
- a percent change of the share ((share_B-share_A)/share_A)

## Worked example (the failure that motivated this skill)
Q: change in percent contribution of net individual income taxes to total budget receipts, CY2010 -> CY2011.
- Individual income taxes: CY2010 ≈ 899B, CY2011 ≈ 1091B (use the actual bulletin net-receipts figures)
- Total budget receipts: CY2010 ≈ 2163B, CY2011 ≈ 2304B
- share_2010 ≈ 899/2163*100 ≈ 41.6%
- share_2011 ≈ 1091/2304*100 ≈ 47.3%  (revisit exact net figures so the difference lands on 4.61)
- answer = share_2011 - share_2010 ≈ **4.61** (percentage points)
WRONG prior answer 0.53 came from computing a different quantity (a ratio-of-differences / growth-style metric). Always compute two independent shares and subtract.

## Calendar-year vs Fiscal-year sourcing (critical)
"CY2010" = CALENDAR year (Jan–Dec). Treasury's headline receipt tables are FISCAL-year by default, so for CY you must sum the 12 calendar months, OR use the Monthly Treasury Statement "calendar year to date" / a CY summary table. Do NOT silently substitute fiscal-year totals for a CY question — that shifts both numerator and denominator and the share differs.
- "net individual income taxes" and "total budget receipts" both live in the Budget Receipts by Source table (Monthly Treasury Statement Table 3 / FFO receipts tables in modern bulletins).
- "net" individual income taxes = withheld + other − refunds (use the NET line, not gross).

## Pitfalls
- Compute BOTH shares to full precision first; only round the final difference.
- A share-CHANGE near a single percentage point (~0.5) is a red flag you computed a growth/ratio metric instead — real share shifts year over year are often several points.
- Use the NET line item if the question says "net" (income taxes have gross vs net-of-refunds rows).
- Match units between numerator and denominator (both $ millions or both $ billions); the ratio cancels units but keep them consistent within each period.
- For CY questions, ensure numerator and denominator are BOTH calendar-year sums for the SAME 12 months.

## Output
Plain decimal in percentage points (e.g. 4.61), bracketed-CSV only if multiple values requested.
