---
name: officeqa-esf-asset-share-cpi-cancels
description: OfficeQA Treasury Bulletin — compute the SHARE of the U.S. Exchange Stabilization Fund's (ESF) total assets that come from a subset of line items (e.g. foreign-exchange holdings + securities), averaged across dated period measurements (e.g. end-of-June vs end-of-September for several years), and take the absolute difference between the two period-sets. KEY TRAP — when the question says to adjust each nominal value to a base month with CPI-U but the final answer is a SHARE/RATIO/percentage of total, the CPI factor CANCELS in numerator and denominator so applying it changes nothing; it is a red herring for any pure share question. PASSED ESF FX+securities share, June vs Sept 2000-2002, March 2003 CPI = 0.953.
category: research
---

# OfficeQA: ESF Asset Share (and the "CPI cancels in a ratio" trap)

## When this applies
Question asks for the SHARE / PROPORTION / PERCENTAGE of a fund's TOTAL ASSETS
(or total of anything) that comes from one or more line items, and then:
- averages that share across several dated period measurements, and/or
- takes an absolute difference between two SETS of periods (e.g. "the June
  measurements" vs "the September measurements" for CY 2000-2002), and
- (often) tacks on "...with each nominal value in thousands of dollars adjusted
  to MMM YYYY dollars using the BLS CPI-U, not seasonally adjusted."

The fund here is the **Exchange Stabilization Fund (ESF)**. Its statement of
financial position / "Statement of Assets and Liabilities" lives in the
Treasury Bulletin (modern bulletins have an ESF section; search the PDF for
"Exchange Stabilization Fund" or "ESF"). Line items typically include:
**U.S. dollar assets** (cash, special drawing rights certificates, U.S.
Government securities) and **foreign-exchange-denominated assets** (foreign
currency holdings, investments denominated in FX). "Total assets" is the row
sum.

## THE KEY INSIGHT — CPI adjustment CANCELS in a share

A SHARE is a ratio: share = (sum of selected items) / (total assets).

If the question says "adjust EVERY nominal value to a common base month
(e.g. March 2003) using CPI-U," every dollar figure for a given period gets
multiplied by the SAME factor f = CPI[Mar2003] / CPI[period]. That factor
appears in BOTH numerator and denominator and CANCELS:

  share = (f*A + f*B) / (f*Total) = (A + B) / Total

So the CPI adjustment is a **NO-OP for any pure share/ratio/percentage answer.**
Compute the shares straight from the raw nominal table values. The CPI clause is
a deliberate red herring designed to make you waste effort (or introduce an
error) deflating numbers that don't matter.

CAVEAT — the CPI does NOT cancel if the final asked quantity is a DOLLAR LEVEL
(deflate then compare/sum/average dollar amounts — see
officeqa-cpi-inflation-adjusted-dollar-amount). Even a multi-period AVERAGE of
shares is CPI-invariant, because each period's share is self-canceling (one
common factor per period). Confirm the final asked quantity is a share, not a
level — if share, ignore the CPI clause entirely.

## Method (worked, PASSED = 0.953)
Question: "average share of the ESF's total assets coming from its
foreign-exchange holdings AND securities, end-of-June CY2000-2002 vs
end-of-September CY2000-2002, CPI-adjusted to March 2003; absolute difference in
the two averages, percentage points, nearest thousandth."

1. Identify the two line items in the numerator: **foreign-exchange holdings** +
   **securities** (U.S. Government securities / investments). Read each, plus
   **total assets**, from the ESF statement.
2. For each of the 6 period-dates (Jun 2000, Jun 2001, Jun 2002, Sep 2000,
   Sep 2001, Sep 2002) compute share = (FX + securities) / total_assets * 100.
   Use RAW nominal values — CPI cancels.
3. avg_June = mean of the 3 June shares; avg_Sept = mean of the 3 Sept shares.
4. answer = |avg_June - avg_Sept|, percentage points, nearest thousandth. = 0.953.

## Where to find the ESF balances
- ESF data appears in the Treasury Bulletin's ESF/International section AND in
  standalone Treasury ESF reports. For "as of the last day of June / Sept" a
  given year, use the **month-end (last business day)** balance for that month.
- A June-CY2000 value is reported in the bulletin issued mid/late-2000 (or the
  Sept bulletin's "as of June 30" column); a Sept value in the following
  bulletin. Match the AS-OF date, not the publication date.
- Values may be in **thousands of dollars** (question states it). Units cancel
  in the share anyway.

## Pitfalls
- Do NOT deflate by CPI for a share answer — wasted effort and an error source.
  Reserve the CPI machinery for dollar-LEVEL questions.
- "foreign-exchange holdings AND securities" = TWO line items summed in the
  numerator; don't forget the securities row.
- "two SETS of period measurements" = average WITHIN each set first (the 3
  Junes, the 3 Septembers), THEN difference the two averages.
- Answer is absolute difference in percentage points (shares already in %),
  nearest thousandth.
- NSA / not-seasonally-adjusted CPI is specified but irrelevant for a share.
