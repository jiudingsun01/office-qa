---
name: officeqa-savings-bond-series-share-of-redemptions
description: OfficeQA Treasury Bulletin — compute the SHARE of total savings-bond redemptions (all series, $ millions) accounted for by ONE specific series (e.g. Series I, Series EE, Series HH) for a given month, and the CHANGE in that share between two dated months, plus often the absolute change in that series' redemptions. Distinct from the accrued-discount-share and redemption-rate-out-of-outstanding siblings. PASSED Series I share Mar2000 vs Mar2005 = [7.1, 82].
---

# OfficeQA: Savings Bond — One Series' Share of Total Redemptions (+ change)

## Sibling question family (don't confuse the three)
This savings-bond family has THREE distinct denominators/answers:
1. **Accrued-discount SHARE of redemptions** — numerator = accrued-discount line,
   denominator = total redemptions all series. See
   officeqa-savings-bond-redemptions-accrued-discount.
2. **Redemption RATE out of amount OUTSTANDING** — denominator = average amount
   outstanding. See officeqa-savings-bond-redemption-rate-avg-outstanding.
3. **THIS one — ONE SERIES' SHARE of TOTAL redemptions** — numerator = redemptions
   of a single named SERIES (Series I, EE, HH, E, H...), denominator = total
   redemptions all series combined. Often asked as a CHANGE in that share between
   two months/years, plus the absolute change in the series' redemption $.

## When this applies
Phrasing like: "the **share of total redemptions** (all series, in millions of
dollars) **accounted for by Series I bonds**", and "the **change, in percentage
points**, ... from <Month YYYY> to <Month YYYY>", often bundled with "and what is
the **absolute change in Series I redemptions** ... in millions of dollars".

Series I and Series EE are MODERN series (Series I launched Sept 1998), so these
questions live in late-1990s/2000s bulletins, not the 1940s-60s ones.

## Where the table lives
- Savings-bond detail table, broken out by series with an "all series" / total
  line. In 2000s bulletins this is in the Public Debt / **"United States Savings
  Bonds" or "Savings Bonds and Notes"** section. It reports sales, redemptions,
  and amount outstanding by series (E, H, EE, HH, I, ...) plus a total.
- Use `pdftotext -layout` — these are wide multi-column tables.
- Search extracted text for `Series I`, `redemptions`, `Savings`, `Total`.
- "March 2000" / "March 2005" → use the bulletin REPORTING that month's
  redemption figure (the question gives the month directly; pick the bulletin
  issue that tabulates that month's savings-bond redemptions).

## Procedure
1. For the FIRST month (e.g. Mar 2000): read total redemptions (all series) =
   D1, and Series-I redemptions = S1. share1 = S1 / D1 × 100.
2. For the SECOND month (e.g. Mar 2005): read total redemptions = D2, and
   Series-I redemptions = S2. share2 = S2 / D2 × 100.
3. **Change in share (percentage points)** = share2 − share1. Round to nearest
   tenth (per the question's "first value rounded to the nearest tenths place").
4. **Absolute change in Series-I redemptions** = |S2 − S1| (or S2 − S1 per
   wording; "absolute change" → magnitude). Round to nearest whole number ($ M).
5. Output bracketed CSV: `[Δshare_tenths, Δredemptions_whole]`.

## Verified example
- Series I share of total redemptions, Mar 2000 → Mar 2005:
  answer = **[redacted]** (matched gold exactly).

## Pitfalls
- Denominator is **total redemptions ALL SERIES**, not amount outstanding, not
  sales — same denominator pitfall as the accrued-discount sibling.
- The first value is **percentage POINTS** (share2 − share1), NOT a relative
  percent change. Do not divide by share1.
- "Absolute change in Series I redemptions" is a raw $-millions difference of the
  series line (S2 − S1), NOT a share difference. Keep it in $ millions and round
  to a whole number.
- Series I redemptions in the early 2000s are small (the series was new), so the
  share starts near zero and grows — a positive Δshare is expected.
