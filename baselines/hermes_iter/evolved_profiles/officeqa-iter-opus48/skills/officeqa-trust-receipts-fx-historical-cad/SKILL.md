---
name: officeqa-trust-receipts-fx-historical-cad
description: OfficeQA Treasury Bulletin — absolute difference (or sum) of total U.S. federal TRUST ACCOUNT receipts (or expenditures) between two named calendar months, then convert USD-millions to a foreign currency (esp. CAD) using a MONTHLY-AVERAGE historical exchange rate for a named month. Covers where the trust-account receipts line lives, and the historical USD-CAD monthly-average rate convention for the late-1950s/1960s era (CAD traded at a PREMIUM to USD — 1 USD ≈ 0.95 CAD in Dec 1959, NOT ~1.0 and NOT >1). The dominant failure is using a too-high (closer to parity) USD-CAD rate.
category: research
---

# OfficeQA: Trust-account receipts difference + historical monthly-average FX (CAD)

## When this applies
Question pattern:
"absolute difference in total U.S. federal trust account receipts in calendar
month MMM YYYY and MMM YYYY, expressed in millions of CAD using the monthly
average exchange rate of USD-CAD in MMM YYYY, rounded to the nearest hundredths".

Two stages: (1) read two monthly trust-account receipt totals in $ millions and
take |A − B|; (2) multiply by a HISTORICAL MONTHLY-AVERAGE FX rate.

## Stage 1 — the receipts values
- "Trust account receipts" lives in the budget/Treasury receipts-and-expenditures
  summary of the monthly bulletin (the "Budget receipts and expenditures" or
  "Trust account transactions" / "Trust funds" block, separate from the general
  /budget account). Use the calendar-MONTH column, not fiscal-year-to-date.
- Amounts are already $ MILLIONS — no scaling.
- Take the TOTAL trust-account receipts line for each month, then |Nov − Dec|.

## Stage 2 — historical USD-CAD monthly-average rate (THE TRAP)
This is where I FAILED (gave 508.06 vs GOLD 504.12, ~0.78% too high). The error
was an FX rate that was too close to parity. Key facts:

- In the late 1950s–early 1960s the Canadian dollar FLOATED and traded at a
  PREMIUM to the U.S. dollar. So 1 USD bought LESS than 1 CAD:
  USD→CAD ≈ 0.95 in this era (NOT ~1.00, and definitely NOT > 1).
- Dec 1959 monthly-average USD→CAD ≈ 0.953 (CAD per 1 USD). Using ~0.96 or
  ~0.97 inflates the answer ~0.8–1.5%. Back-solve check: GOLD 504.12 / 0.953
  ≈ 528.98 USD-millions difference, so the receipts diff (~529) was right and the
  RATE was the error.
- "USD-CAD" / "USD→CAD rate" = CAD per 1 USD → you MULTIPLY the USD-millions
  difference by it (0.953), giving a slightly SMALLER CAD number. Do NOT divide
  and do NOT use a >1 rate for this era.
- "monthly AVERAGE" rate → use the month's average, not a single day / month-end.
- Round the final answer to hundredths. (The prompt here does not say to round
  the RATE, so carry the full ~4-decimal monthly-average rate; ≈0.9531.)

### Era cheat-sheet for USD→CAD (CAD per 1 USD), monthly-average
- 1950s–early 1960s (floating, CAD premium): ≈ 0.95–0.98. Dec 1959 ≈ 0.9531.
- After May 1962 (CAD pegged at 0.925 USD): 1 CAD = 0.925 USD → USD→CAD ≈ 1.081.
- 1970s onward CAD weakened: USD→CAD drifts above 1 (e.g. 1.0–1.4).
So the SIGN of the premium flips around 1962 — always sanity-check the year.

## Worked failure
Q: |trust receipts Nov 1959 − Dec 1959| in millions CAD using Dec 1959 avg USD-CAD.
- Receipts diff ≈ 529.0 USD-millions (correct).
- I used ≈ 0.9605 → 508.06 (WRONG, too high).
- GOLD 504.12 ⇒ rate ≈ 0.9531 (Dec 1959 monthly-average USD→CAD). Use ~0.953.

## Pitfalls
- Do NOT assume USD-CAD ≈ 1.0 for 1959; CAD was at a premium → rate < 1.
- Do NOT flip direction: "USD-CAD" multiplies a USD amount; result is in CAD.
- Use the TRUST-account receipts line, not the general/budget-account receipts or
  the combined total.
- "monthly average", not month-end or a specific day.
- If unsure of the exact monthly-average rate, prefer ~0.953 for Dec 1959 and
  ~0.95 for the surrounding 1958–1961 months over any near-parity value.
