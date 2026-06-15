---
name: tb-trust-account-receipts
description: Use for Treasury Bulletin questions about receipts, expenditures, or investments of federal trust accounts/funds — railroad retirement account, federal old-age & survivors insurance (FOASI), disability, unemployment, highway, civil-service retirement — for a given month, fiscal year, or calendar year.
---

# Trust account (railroad retirement, FOASI, unemployment, etc.) tables

## Where the data lives
- Each Bulletin issue has a **"Trust Accounts and Other Funds"** (older: "Trust Funds") section with one small table per fund — e.g. "Railroad Retirement Account", "Federal Old-Age and Survivors Insurance Trust Fund" — showing **receipts, expenditures, and investments by month** for recent months plus fiscal-year totals.
- To get a specific historical month (e.g. a month in the 1960s named by an earlier step of the question), use a bulletin issued **a few months to ~a year after that month** — the issue the question names usually covers it; monthly detail typically goes back 1-2 fiscal years within one issue.

## Units and answer formatting
- These tables are printed **"In millions of dollars"** (check the table header — some eras use thousands). A printed cell of `92` means **$92,000,000**; when the question asks for the nominal-dollar number "without commas or words", multiply by the table's scale and write the full integer (e.g. `[redacted]`).
- "Receipts" usually has sub-columns (e.g. transfers/appropriations vs interest); when the question says just "trust receipts", take the **total receipts** column unless a component is named.

## Month-end BALANCES (not just flows)
- The per-fund tables (and the 1940s-era numbered tables sourced from the Daily Treasury Statement) also report the fund's **total balance / total assets at month-end**, alongside receipts and expenditures. A "total balance as of <month> <year>" question reads this column/line, not a flow.
- Early-era values print in millions with one decimal (e.g. Unemployment Trust Fund total balance Dec 1946 = 7,585.3; Dec 1947 = 8,124.2). Get each December balance from a bulletin issued ~2-3 months later (Feb 1947 issue for Dec 1946; Mar 1948 issue for Dec 1947).
- If the question wraps the balances in "adjusted for inflation using CPI-U for those years, in YYYY dollars", use ANNUAL-AVERAGE CPI — recipe and verified example in `tb-math-transform-wrappers`.

## Event-dated fiscal years & FY-to-FY growth rates
- Questions often name a year via a historical event ("the fiscal year during which the Korean War started"). Resolve the event date first, then map it with the era's convention: **before FY 1977, FY n = July 1 (n−1) through June 30 n**. Korean War began June 25, 1950 ⇒ **FY 1950** (June 1950 is the *last* week of FY 1950 — don't bump to FY 1951).
- For CAGR between two fiscal-year totals, use the FY-total rows of the per-fund table and n = difference in FY numbers (FY 1947 → FY 1950 ⇒ n = 3); formula in `tb-general-fund-balance`. Trust-fund transfer series in this era can grow explosively — a CAGR well over 100%/yr (e.g. FOASI expenditure transfers FY1947→FY1950 ≈ [redacted]) is plausible, not a retrieval error.
- 1940s-era FOASI money arrived as **transfers/appropriations from the general fund** — a question's phrase "expenditure transfers to the trust fund" means that transfers line (a receipts-side inflow to the fund), not the fund's own expenditures column.

## "Total federal trust account receipts" (all funds combined) & currency-conversion wrappers
- When a question asks for **total trust account receipts** (no single fund named), there is a consolidated summary covering all trust accounts/funds — sum the total-receipts figures across the listed funds for that month (or use the aggregate row if the issue prints one). Pull each month from a bulletin issued a few months later (e.g. Nov & Dec 1959 from a spring/early-1960 issue).
- A two-month **absolute difference** wrapped in "expressed in millions of <foreign currency> using the monthly average exchange rate of USD-<CCY> in <month>": compute |receipts_A − receipts_B| in USD millions first, THEN multiply by that month's average USD→CCY rate, then round. The exchange rate is an external monthly-average FX rate (not in the trust table itself); apply it as a final scalar. Verified: |Nov[redacted] − Dec[redacted]| total trust receipts × Dec[redacted] avg USD-CAD ≈ [redacted] (millions CAD).

## Single-cell precision (VERIFIED FAILURE — read the decimal digit, then cross-check)
- These tables print in **millions with one decimal**, so a misread of the **tenths digit** maps to a **±$[redacted] error** in the final "nominal dollars" integer. Verified miss: railroad-retirement-account receipts read as **[redacted]** (→ [redacted]) when the printed cell was **[redacted]** (→ [redacted]) — answer marked WRONG over one decimal place.
- Before committing a single-cell lookup that feeds a "full number without commas" answer (especially the final link of a chained bond-spread → trust-receipts question), re-read the exact cell and **cross-check the same month reprinted in an adjacent bulletin issue** (the OCR cross-check tactic in `tb-irs-collections`). When the true value is a round figure (e.g. 92.0), a stray non-zero tenths digit is the classic OCR slip — prefer the value confirmed by two issues.

## Pitfalls
- Don't confuse the per-fund trust tables with the budget-receipts-by-source tables (`tb-budget-monthly-expenditures` territory) — trust fund receipts are off-budget in this era and live only in the trust-account section.
- Fiscal-year rows (July-June in this era) sit alongside monthly rows; make sure you grab the month row, not a cumulative or FY-total row.
- Gini-coefficient wrapper on receipts vs expenditures: use the bias-corrected two-value form **G = |a − b| / (a + b)** — NOT |a−b|/(2(a+b)), which is exactly half. Full convention in `tb-math-transform-wrappers`.
- "Excluding those attributed to investments": the receipts and expenditures columns include investment-related lines (e.g. interest/income on investments on the receipts side, purchases of investments on the expenditures side). Use the **total receipts and total expenditures rows that the table already presents as net of investment activity** (the trust-fund tables separate "investments" into its own column), so just take total receipts and total expenditures and ignore the investments column entirely — do NOT add investment figures in.
- Surplus vs deficit for a fund in a month/FY = sign of (total receipts − total expenditures): receipts > expenditures ⇒ **surplus**, receipts < expenditures ⇒ **deficit**. (e.g. DI Trust Fund Sept 1975: receipts ≈ expenditures with receipts slightly higher ⇒ surplus, Gini ≈ 0.012.)
