---
name: officeqa-savings-bond-redemption-rate-avg-outstanding
description: OfficeQA Treasury Bulletin — compute a savings-bond / savings-note "redemption RATE out of the (average) amount outstanding" for one or more CALENDAR years, then often a relative/absolute difference between two years. Distinct from the accrued-discount-SHARE question. Covers the per-year rate = annual redemptions / average-amount-outstanding definition, the average-outstanding = (begin-of-year + end-of-year)/2 convention, and the "relative difference in percentage points" trap that is (rateB - rateA)/rateA * 100, NOT the bare rateB - rateA.
---

# OfficeQA: Savings Bond/Note Redemption RATE out of Average Amount Outstanding

## When this applies
A question about U.S. **savings bonds** OR **savings notes** (a.k.a. U.S. Savings
Notes / "Freedom Shares") that asks for a **redemption RATE** expressed as a share
of the **amount outstanding**, usually for one or more **calendar years**, e.g.:
- "saving note redemption rate out of the average amount outstanding for the
  1980 and 1981 calendar years"
- "what percent of the amount outstanding was redeemed in CY YYYY"

This is NOT the accrued-discount-share question (see
`officeqa-savings-bond-redemptions-accrued-discount`). Here the denominator is
**amount OUTSTANDING**, not total redemptions.

## The rate definition (this is the whole trick)
For each calendar year Y:

    redemption_rate_Y = (total redemptions during year Y) / (AVERAGE amount outstanding during year Y) * 100

- **Numerator** = the year's TOTAL redemptions (sum the 12 monthly redemption
  figures, or read the calendar-year total row if the table provides one).
- **Denominator** = the **AVERAGE amount outstanding**, NOT a single month's
  outstanding. Default convention:
      avg_outstanding_Y = (outstanding at START of year + outstanding at END of year) / 2
  i.e. (Dec-prev-year-end + Dec-year-end)/2, equivalently (Jan 1 + Dec 31)/2.
  If the question literally says "average amount outstanding" and the table gives
  month-end outstanding for all 12 months, the strict average = mean of the 12
  (or 13) month-end values — but the two-endpoint average is the usual gold
  convention and matches "average for the calendar year".

## The "relative difference in percentage points" trap (DOMINANT FAILURE)
When asked for "the relative difference ... of the rate for year A and year B":

    relative_difference = (rate_B - rate_A) / rate_A * 100

Base = the EARLIER year (A). This is a PERCENT-OF-A-PERCENT figure, so it can be
large (e.g. 17.69) even when the two underlying rates differ by only a few raw
percentage points. DO NOT report the bare absolute gap (rate_B - rate_A); that
undershoots by roughly a factor of 4-5 and is the recorded failure mode here
(emitted 3.85 — the absolute gap — vs GOLD 17.69 — the relative difference).

Decode "relative difference in percentage points": "relative" = divide by the
base rate; the result is itself reported in percentage points. See memory note
"RELATIVE diff" and skill if present.

## Where the data lives
- Savings-bond/note **redemptions** and **amounts outstanding** live in the
  Public Debt Operations / savings-securities detail tables of the Treasury
  Bulletin. Outstanding is reported as month-end balances; redemptions as
  monthly flows. Search extracted text for `savings notes`, `savings bonds`,
  `redemptions`, `outstanding`. Use `pdftotext -layout` (wide tables).
- For CY1980/1981 figures, the cleanest source is often a single later bulletin
  (e.g. early-1982) whose savings-securities table shows full-year 1980 and 1981
  redemptions plus year-end outstanding for 1979, 1980, 1981 — so you can build
  both averages from one table.
- "Savings notes" are a SEPARATE line from "savings bonds" — read the savings
  NOTES row, not the bonds row, when the question says notes.

## Procedure
1. Find the savings-notes (or -bonds) section; identify the redemptions column
   and the amount-outstanding column.
2. For each target year: total redemptions (numerator); avg outstanding =
   (prior-year-end + this-year-end)/2 (denominator). rate = num/den*100.
3. If a difference between two years is asked:
   - "relative difference" => (rate_later - rate_earlier)/rate_earlier*100.
   - plain "difference" / "percentage point difference" => rate_later - rate_earlier.
4. Round to the requested precision (here nearest hundredth).

## Pitfalls
- Denominator is AVERAGE outstanding, not end-of-year and not redemptions.
- "Relative" difference divides by the earlier year's rate — do not skip it.
- Notes vs bonds: pick the right security line.
- Calendar year (Jan-Dec), not fiscal year, when it says "calendar years".
