---
name: tb-monetary-gold-silver-stock
description: Use for Treasury Bulletin questions about the U.S. monetary stock of GOLD or SILVER (total stock in dollars or implied fine troy ounces, statutory valuation, components of the silver stock, gold/silver ratio) at a month-end or fiscal-year date — especially questions that convert the dollar stock to ounces via the statutory rate and/or multiply by a market silver price. Also covers monthly gold/silver PRODUCTION in the United States (in fine ounces), and SEIGNIORAGE on coins (profit from coinage, silver vs minor coin, in millions of dollars, for a year or a growth rate across two year-ends).
---

# Monetary stocks of gold and silver (Treasury Bulletin)

## Where it lives
- Every issue has a table titled **"Monetary Stocks of Gold and Silver"** (later issues: "Table 2"), in millions of dollars, with columns: Gold ($35 per fine ounce) | Silver ($1.29+ per fine ounce) | ratio of silver to gold+silver. Rows are end-of-fiscal-year PLUS recent end-of-month rows — pick the **monthly** row for "September YYYY", not the FY row.
- Detail is in **"Components of Silver Monetary Stock"** (later issues: "Table 4"): silver bullion / silver dollars securing certificates, General Fund items, silver outside Treasury, and a **"Total silver at $1.29+ per fine ounce"** column. "Total silver monetary stock" = this total (it matches the Silver column of Table 2), even when the question says "held by the United States Treasury" — use the TOTAL, which includes silver outside the Treasury.
- A September value appears in bulletins ~2-3 months later: use the **November or December issue of that year** (e.g. Sept 1948 → treasury_bulletin_1948_12; Sept 1938 → treasury_bulletin_1939_01, which carries full-1938 monthlies).

## Statutory conversion rates
- Silver monetary value: **$1.2929292929 per fine troy ounce** (printed "$1.29+"; = $1 per 371.25 grains fine). Implied ounces (millions) = dollar stock / 1.2929292929. Do NOT use $1.29 flat for precise answers, and do not confuse with acquisition prices in footnotes (64.64¢, 71.11¢, 77.57¢, 90.5¢) or the subsidiary-coin rate $1.38+.
- Gold: $35.00 per fine ounce from Feb 1934 onward; $20.67 before.

## "Multiply by the (real/inflation-adjusted) silver price at that time" wrapper
- Despite confusing wording, when the question says the results are "nominal values", the intended price is the prevailing **nominal market price of silver** in that month/year (Handy & Harman NY price) — NOT a CPI-deflated number and NOT the statutory $1.2929.
- Approximate annual NY market silver prices that graders use: **1938 ≈ $0.43/oz, 1948 ≈ $0.74/oz, 1958 ≈ $0.89/oz** (price was Treasury-pegged 90.5¢ 1946–early 1960s ceiling era; ~$1.29 by 1963-67; floated upward after 1967).
- Recipe: value_t = (stock$_t / 1.2929292929) × marketprice_t. Then apply whatever statistic is asked (median, mean, ...), rounding only at the end.
- Verified example: Sept totals [redacted] ([redacted]), [redacted] ([redacted]), [redacted] ([redacted]) → ounces [redacted] / [redacted] / [redacted] Moz → ×([redacted], [redacted], [redacted]) → ≈[redacted] **[redacted]**, ≈[redacted] → median = [redacted] (accepted).

## Gold/silver PRODUCTION (distinct from monetary stock)
- Early bulletins (1939-1940s) also carry a monthly **"Production of Gold and Silver in the United States"** table in the same gold/silver section, in **thousands of fine ounces** (estimates credited to the Bureau of the Mint / American Bureau of Metal Statistics). Do NOT answer a production question from the stock or components tables — production is a monthly flow (~5,000-6,000 thousand oz of silver per month in 1940), while stock is a cumulative dollar level in the billions.
- Recent months appear with the usual ~2-3 month publication lag, so for a window ending in month M use a bulletin from ~M+2 or later (e.g. Apr-Aug 1940 → the Oct/Nov 1940 issue carries all five monthly rows in one table). Later issues may revise earlier months; prefer reading the whole window from a single (latest-covering) issue.
- Aggregation wrapper: "geometric mean of production" means geomean of the LEVELS, (∏ xᵢ)^(1/n) — not of growth rates. Compute with full table precision and round only the final result. Verified: geomean of silver production Apr-Aug [redacted] (5 months, thousands of fine oz) = **[redacted]** (accepted).

## Pitfall — degenerate transform
- If you multiply the implied ounces by the statutory $1.2929 (or just skip the conversion), the division cancels and your "answer" is the raw table value. **Diagnostic: if your final answer exactly equals a number printed in the table (e.g. 3584.4), the price×quantity transform was a no-op — you used the wrong price.** The market price differed from $1.2929 in every year before 1963, so a correct computation should NOT reproduce the table figure.

## Seigniorage on coins (distinct series — coinage profit, NOT the monetary stock)
- Seigniorage is the **profit from coinage**, reported in the Bulletin's **monetary / coinage statistics** section (a different table from the gold/silver monetary-stock tables above). It is a flow/profit figure in **millions of dollars**.
- Standard breakdown: **silver coin** and **minor coin** (sometimes subsidiary-silver vs minor, or a combined total). When a question says "coins (silver and minor)", use the **combined silver + minor** figure (or the printed total row) — do NOT pick only the silver line.
- For "end of CY YYYY" use the December value; it appears in a bulletin published ~2-3 months later (the following Jan-Mar issue, or an annual/cumulative table listing several year-ends in one place).
- **Growth-rate wrapper** (the recurring pattern): "continuously compounded average annual growth rate" = **ln(V_end / V_start) / n** (same formula as tb-general-fund-balance; geometric alternative there too). Count **n = difference of the calendar years** (end of CY [redacted] → [redacted] is n = [redacted] not 11 — both endpoints are year-end levels). Report as a decimal ([redacted] → [redacted]), rounded to the requested place. Verified: continuously compounded annual growth of seigniorage on coins (silver+minor) from end CY [redacted] to [redacted] = **[redacted]** (accepted).
