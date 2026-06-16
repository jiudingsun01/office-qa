---
name: tb-statutory-debt-limit
description: Use for Treasury Bulletin questions about the STATUTORY DEBT LIMITATION table — debt/securities "subject to statutory debt limitation", securities issued under the Second Liberty Bond Act, interest-bearing vs total subject to limit, guaranteed obligations under the limit, or ratios/products built from these rows at month-end dates.
---

# Statutory Debt Limitation table

## Where it is
- Every bulletin has a table titled **"Statutory Debt Limitation"** (often a "Status under limitations" / "Debt subject to limitation" layout; labeled FS-2 in later bulletins). In 1950s–60s issues it sits in the public-debt/Federal Securities section, near the "Summary of Federal Securities" table.
- It shows status **as of ONE month-end date per bulletin** (the latest available, ~2 months before the bulletin's cover month). For N as-of dates you need N different bulletins: e.g. status as of Feb 29, 1960 → April or May 1960 bulletin; Mar 31, 1964 → May/June 1964 bulletin.
- Questions may dress these dates up as "fiscal years ending Feb 29, 1960 / Mar 31, 1962" etc. — they are NOT fiscal years, just the as-of month-end dates of the table. Don't go hunting June-30 figures.

## Row taxonomy — map question phrases to the right row
The outstanding section is structured as:

1. **Public debt obligations issued under the Second Liberty Bond Act, as amended:**
   - Interest-bearing (broken out by class) → **Total interest-bearing**
   - Matured, interest-ceased
   - Bearing no interest
   - → **Total** (sum of the three)
2. **Guaranteed obligations (not owned by the Treasury):** interest-bearing + matured → total (a few hundred $M in the 1960s)
3. **Grand total outstanding (total debt subject to limitation)** = (1)+(2)

Phrase mapping:
- "total interest-bearing securities subject to statutory debt limitation" → row 1's **Total interest-bearing**.
- "total public debt subject to statutory debt limitation" → row 1's **Total** (SLBA total incl. matured + no-interest, **EXCLUDING guaranteed obligations**).
- "securities issued under the Second Liberty Bond Act, as amended, subject to limitation" → the same row-1 **Total**.
- "total debt subject to limitation" (no "public") → the grand total **including** guaranteed obligations.

## Pitfalls (this is where answers go wrong)
- The three candidate totals differ by only [redacted]–[redacted] (matured/no-interest ≈ $[redacted]–[redacted]M; guaranteed ≈ $[redacted]–[redacted]M, vs ~$[redacted]–[redacted]B totals). When the question then multiplies a ratio of these rows by a ~$[redacted]B figure, picking the wrong total shifts the final answer by hundreds of millions — enough to be graded wrong while looking plausible. Verified failure: a ratio question over Feb [redacted]–Mar [redacted] came out [redacted] low from total-row confusion (correct final [redacted], wrong [redacted]).
- A "ratio of interest-bearing to total subject to limitation" is ≈ 0.998, NOT ≈ 1.000 — do not shortcut it to 1; the small deficit is exactly what the question is testing.
- Carry each ratio at full precision (≥8 significant digits) through geometric means; round only the final answer.
- This table's totals are NOT the same as "total gross public debt" in the Summary of Federal Securities — some old debt is exempt from the limit. Don't substitute one for the other (see tb-federal-debt-outstanding for the summary table).

## Currency conversion (Bretton Woods era)
- "Official annual average USD/GBP exchange rate in 1964" → the fixed parity **$2.80 per £1** (in force 1949–Nov 1967). GBP value = USD millions ÷ 2.80. (Market annual averages like 2.7926 give answers ~0.3% off the graded value — use the $2.80 parity unless the question explicitly cites a market-rate source.)
- Other parities if needed: post-Nov 1967 devaluation £1 = $2.40.
