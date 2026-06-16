---
name: tb-general-fund-balance
description: Use for Treasury Bulletin questions about the U.S. Treasury General Fund — its working balance, total balance, components, or ratios/rates of change between period-end dates. Also contains the generic annual rate-of-change recipes (geometric AND continuously compounded) used by many Bulletin questions.
---

# Treasury Bulletin: General Fund of the Treasury

## Where the data lives
- Recurring table titled "General Fund of the Treasury" (sometimes "Status of the General Fund") near the front of each issue, in the fiscal/budget section alongside budget receipts-and-expenditures tables.
- Reported **as of end-of-month dates**; figures **in millions of dollars** in early (1939-1941) issues.
- A given month-end (e.g. December 1938) appears in the issue published 1-2 months later, AND as a comparison row/column in later issues. Period-end rows for several months/years are often printed together in one table — prefer reading both needed dates from a SINGLE issue so vintages match.

## Key line items
- **"Working balance"** is a specific printed line (the freely available balance in the General Fund, i.e. balance excluding amounts earmarked/held for specific purposes like gold-reserve, trust, and special accounts). Use the printed line — do not derive it.
- **"Total balance"** (total General Fund balance) is the table's grand-total balance line.
- Ratio questions: ratio = working balance ÷ total balance, both from the same date column/row. Keep full precision; do not round the ratio before later steps.

## Annual rate of change (generic — applies across Bulletin questions)
Read the question's wording carefully — two different formulas appear in this benchmark:
- **Geometric / compound annual rate**: rate = (V_end / V_start)^(1/n) − 1.
- **"Continuously compounded" average annual growth rate**: rate = ln(V_end / V_start) / n. Do NOT use the geometric formula here — the results differ (e.g. ratio 2.0 over 10 yrs: geometric 0.072 vs continuous 0.069).
- In both: n = number of YEARS between the dates (Dec 1938 → Dec 1940 ⇒ n = 2; end of CY 1945 → 1955 ⇒ n = 10), not the number of data points.
- When the quantity is itself a ratio, compute each date's ratio first at full precision, then apply the formula to the two ratios.
- A declining series gives a **negative** rate — keep the sign.
- "Rounded to the nearest thousandths place ... as a decimal value" ⇒ round to 3 decimals and output e.g. `[redacted]`, NOT `-11.9%` and NOT a 4-decimal value.
