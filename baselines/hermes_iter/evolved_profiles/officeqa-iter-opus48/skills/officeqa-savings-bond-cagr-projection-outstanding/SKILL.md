---
name: officeqa-savings-bond-cagr-projection-outstanding
description: OfficeQA Treasury Bulletin — project the INTEREST-BEARING DEBT (amount outstanding) of a single savings-bond series (Series I, EE, HH, E, H) forward at the compound annual growth rate observed between two CALENDAR-month endpoints (e.g. Mar 2001 -> Mar 2006 -> projected Mar 2011). Covers the correct DATA SOURCE (savings-bond amount-outstanding line, NOT redemptions/sales), the per-series isolation trap (do NOT use combined EE/I or "savings bonds total"), and the projection formula V_future = V_mid*(1+CAGR)^h = V_mid^2/V_start for a symmetric horizon.
category: research
---

# OfficeQA: Savings-Bond Series CAGR Projection of Amount Outstanding

## When this applies
Phrasing like: "if the **interest-bearing debt for Series I savings bonds**
continued to grow at the same **annualized compound rate** observed between
calendar <MonthA YearA> and <MonthB YearB>, what would its **projected level**
be in calendar <MonthC YearC>?" Answer = single $-millions value, 2 dp.

Series I launched Sept 1998, Series EE 1980 — so these are late-1990s/2000s
bulletins. Same family also asks the question for Series EE, HH, E, H.

## DATA SOURCE — the dominant trap (this question FAILED: 560682.94 vs GOLD 339501.88)
"**Interest-bearing debt for Series I**" = the **AMOUNT OUTSTANDING** of the
Series I line at that month-end. It is NOT redemptions, NOT sales, NOT
accrued discount, NOT the combined Series EE/I line, NOT the all-savings-bonds
total.

In 2000s bulletins this lives in the Public Debt section, table
**"United States Savings Bonds"** / **"Savings Bonds and Notes"** (sometimes the
"Public Debt Securities by Issue" / savings-securities detail). It reports, by
series (E, H, EE, HH, I, savings notes) and a TOTAL: sales, redemptions, and
**amount outstanding**. Use the **amount-outstanding column for the Series I ROW**
at the exact MONTH stated (Mar 2001, Mar 2006).

Isolation checklist before reading a value:
1. Right SERIES row? (Series I only — its own line, not "EE/I" combined, not
   "Total savings bonds", not "Series EE".) In some layouts Series EE and
   Series I share a block header "Series EE/I" but list SEPARATE outstanding
   sub-rows — take the I sub-row, not the block subtotal.
2. Right COLUMN? Amount outstanding (a.k.a. "interest-bearing debt"), NOT
   redemptions/sales/sales-less-redemptions.
3. Right MONTH? The literal calendar month (March), from the bulletin that
   tabulates that month-end. Don't grab a fiscal-year-end or a different month.
4. Right UNITS? $ millions (these tables are in millions; no extra scaling).

A ~1.65x overshoot like this one usually means a wrong/larger line was read at
the EARLY endpoint (smaller V_start inflates V_mid^2/V_start) OR the combined
EE/I figure was used. Re-verify the Series-I-only outstanding at BOTH months.

## The projection formula
Let V0 = outstanding at start month (Mar 2001), V1 = outstanding at mid month
(Mar 2006). The CAGR is over n1 = (YearMid - YearStart) years.

    r = (V1 / V0)^(1/n1) - 1            # n1 = 2006-2001 = 5

Project forward h = (YearTarget - YearMid) years (Mar 2006 -> Mar 2011, h = 5):

    V_target = V1 * (1 + r)^h
             = V1 * (V1/V0)^(h/n1)

When h == n1 (here both 5), this simplifies to the clean symmetric form:

    V_target = V1^2 / V0          # ONLY when projection horizon == CAGR window

n convention = END_year - START_year (same as all CAGR skills): Mar2001->Mar2006
=> n = 5, NOT 6, NOT count of monthly points.

## Worked check (Python)
    V0 = <Series I amount outstanding, Mar 2001, $M>
    V1 = <Series I amount outstanding, Mar 2006, $M>
    n1, h = 2006-2001, 2011-2006          # = 5, 5
    r = (V1/V0)**(1/n1) - 1
    V_target = V1*(1+r)**h                 # == V1**2/V0 when h==n1
    print(round(V_target, 2))
Sanity: Series I outstanding grew through the 2000s, so r>0 and
V_target > V1. If your V_target looks implausibly large vs V1, you likely read
V0 from the wrong (too-large) line — recheck the early endpoint.

## Pitfalls
1. "Interest-bearing debt for Series X" = amount OUTSTANDING of that series, not
   a flow (redemptions/sales). DENOMINATOR/numerator confusion with the
   redemption-rate and redemption-share siblings is the #1 source-pick error.
2. Isolate the single series; never use the EE/I combined block subtotal or the
   savings-bonds grand total.
3. n = END - START for the CAGR window; project the stated horizon explicitly.
4. Output: bare numeric, 2 dp, period decimal, no commas (e.g. 339501.88).
