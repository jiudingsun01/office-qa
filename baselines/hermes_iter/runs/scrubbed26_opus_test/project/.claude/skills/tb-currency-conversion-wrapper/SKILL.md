---
name: tb-currency-conversion-wrapper
description: Use for Treasury Bulletin questions that take a USD value (receipts, expenditures, debt, gold stock, capital-movements liabilities, etc.) and convert it into a FOREIGN currency using a historical exchange rate — a yearly-average rate ("yearly average 1956 USD/INR"), a MONTHLY-average rate ("monthly average USD-CAD in December 1959"), or a SPECIFIC-DATE rate ("USD to GBP from June 30, 2002"). The exchange rate is NOT in the Bulletin; you supply it from historical knowledge.
---

# Treasury Bulletin: historical currency-conversion wrappers

Some questions retrieve a USD figure the normal way (use the relevant tb-* skill to find and sum the Bulletin cells), then wrap it in a conversion to another currency at a stated historical exchange rate. The rate is an EXTERNAL fact — the Bulletin does not print it — so you must know / reconstruct it.

## Procedure
1. Retrieve and sum the USD value(s) first, exactly as the underlying question asks (e.g. "total receipts from the public" for Jan + Feb 1956 — a cash-basis row, see tb-budget-monthly-expenditures). Keep it in the printed units (usually millions of nominal dollars).
2. Determine the **yearly-average exchange rate** for the stated year and currency pair.
3. **Honor the rounding instruction on the RATE separately from the final answer.** "(rounded to the nearest hundredths place)" attached to the exchange rate means: round the RATE to 2 decimals FIRST, then multiply, then round the FINAL product to the requested places. Order matters — rounding only at the end can shift the hundredths digit.
4. For "USD/INR" stated as the conversion FROM USD TO INR, multiply the USD value by the rate (INR per USD). Result is in the target currency's same magnitude units (here, millions of INR), unless the question says otherwise.

## Historical fixed/pegged rates to know (yearly averages ≈ the peg)
- **Indian rupee (INR):** pegged at **1 USD = 4.7619 INR** from 1949 until the June 1966 devaluation. Rounded to hundredths → **4.76**. So 1950s/early-1960s USD/INR ≈ 4.76.
- Under **Bretton Woods (1944–1971)** most currencies held fixed parities; a "yearly average" for those years is essentially the peg. Examples (USD per unit / units per USD as appropriate): GBP 1 USD ≈ 0.357 GBP (£1 = $2.80, 1949–1967); DEM 4.20 per USD (1949–1961, then 4.00); FRF/JPY/etc. likewise pegged. Verify the exact peg and any mid-period devaluation for the specific year before applying.
- **Canadian dollar (CAD):** NOT pegged in the 1950s — Canada floated its dollar 1950–1962, so there is NO peg to fall back on; a monthly/yearly average must be sourced. In the late 1950s the CAD traded at a PREMIUM to the USD (1 USD ≈ 0.95–0.96 CAD). The **Dec 1959 monthly-average USD→CAD ≈ 0.96**. (Direction check: "USD-CAD" / "USD to CAD" = CAD per USD; a sub-1.0 value is correct here because the CAD was stronger than the USD.)
- After 1971 (floating era) there is no single peg — a true yearly-average OR specific-date rate must be sourced; treat those with more care.

## Monthly-average rate type
A question may ask for the "monthly average exchange rate" of a pair in a specific month (e.g. "monthly average of USD-CAD in December 1959"). Treat it exactly like a yearly-average wrapper but source the rate for that MONTH, not the year. Round the rate per instruction FIRST, then multiply, then round the final product. When the underlying USD figure is itself a difference (e.g. |Nov receipts − Dec receipts|), compute the absolute difference in USD first, then convert.

## Floating-era SPECIFIC-DATE conversions
When the question says e.g. "using the USD to GBP exchange rate retrieved and rounded to its hundredths place from June 30, 2002":
1. **Direction.** "USD to GBP" means GBP-per-USD = the RECIPROCAL of the quoted GBP/USD market rate. If GBP/USD ≈ 1.527, then USD→GBP = 1/1.527 ≈ 0.6549. Multiply the summed USD value by this.
2. **Round the RATE to hundredths FIRST, with correct half-up rounding.** 0.6549 → **0.65** (NOT 0.66). A one-cent slip in the rate scales the whole answer by ~1.5% and fails the exact-match grader.
3. Do NOT round the GBP/USD quote first and then invert — round the value in the SAME direction the question states (here USD→GBP, so round 0.6549). Inverting a 2-dp-rounded 1.53 gives 0.6536→0.65 by luck here, but invert the raw rate to be safe.

## Sanity check
- Back out the implied rate: `final_answer / USD_value`. It must equal the rounded rate you applied. If it doesn't, you either used an unrounded rate or mis-summed the USD side.
