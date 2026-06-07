---
name: officeqa-savings-bond-redemptions-accrued-discount
description: OfficeQA Treasury Bulletin — questions about U.S. savings bond redemptions that ask what share of total redemptions came from "accrued discount" / "value buildup from the original price markdown" / "interest accrued" vs the principal (original issue/purchase price). Covers the terminology decode and where the savings-bond redemption breakdown table lives.
---

# OfficeQA: Savings Bond Redemptions — Accrued Discount Share

## Sibling question family (don't confuse them — THREE variants)
1. If the question asks for a redemption RATE out of the (average) amount
   OUTSTANDING (not the accrued-discount SHARE of redemptions), that is a
   different computation — see officeqa-savings-bond-redemption-rate-avg-outstanding.
   Denominator there is amount outstanding; here it is total redemptions.
2. If it asks for the SHARE of total redemptions accounted for by ONE named
   SERIES (Series I / EE / HH), and/or the CHANGE in that share between two
   months — see officeqa-savings-bond-series-share-of-redemptions. Numerator
   there is a single series' redemption line, not the accrued-discount line.

## When this applies
A question about **U.S. savings bonds** (Series E, H, etc., "all series combined")
that asks for the **percent of total redemptions** attributable to a portion
described with obfuscated language, e.g.:
- "redemptions that elapsed **value buildup from the original price markdown**"
- "the interest/value that **accrued** since purchase"
- "the portion above the original purchase price"

## The key terminology decode (this is the whole trick)
Savings bonds were sold at a **discount** (markdown) from face value; they
accrue value over time toward redemption value. In Treasury Bulletin savings-bond
tables, total redemptions are split into TWO components:

1. **Principal / original issue (purchase) price** — what the buyer paid.
2. **Accrued discount** (sometimes "accrued interest" / "interest") — the
   value buildup ABOVE the original markdown price that accumulated until redemption.

So the obfuscated phrase **"value buildup from the original price markdown"
= the ACCRUED DISCOUNT line**, NOT principal, NOT total.

Answer = accrued_discount / total_redemptions × 100.

## Where the table lives
- Look in the **Public Debt Operations / savings-bond detail** tables of the
  Treasury Bulletin for the relevant month. The savings-bond section reports
  sales, redemptions, and amounts outstanding, often broken out by series
  (A-D, E, F, G, H, J, K, etc.) plus an "all series" / total line.
- The redemption breakdown into **principal of accrued-discount bonds /
  accrued discount / current-income bonds** appears as separate columns or
  sub-rows. Find the column explicitly labeled **"accrued discount"** (or
  "redemption of accrued discount").
- Search the extracted text for `accrued discount`, `savings bonds`,
  `redemptions`. Use `pdftotext -layout` for these wide tables.

## Procedure
1. Locate the savings-bond redemptions table for the target month.
2. Read **total redemptions, all series** for that month (denominator).
3. Read the **accrued discount** redemption value (numerator).
4. pct = numerator / denominator × 100; round to nearest hundredth.

## Verified example
- Oct 1961, all-series total redemptions → accrued-discount share = **14.04%**.
  (matched gold exactly).

## Pitfalls
- Do NOT use total sales or amount outstanding — the denominator is **total
  REDEMPTIONS**, all series combined.
- Do NOT confuse "accrued discount" with the principal/original-price line; the
  question's obfuscation ("value buildup from the markdown") points at accrued
  discount, which is the SMALLER of the two components (typically ~10-20%).
- "All series combined" means use the total row, not a single series.
