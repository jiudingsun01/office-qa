---
name: tb-currency-in-circulation
description: Use for Treasury Bulletin questions about currency and coin in circulation (total or by kind — Federal Reserve notes, U.S. notes, silver certificates, coin) at a month-end or fiscal-month-end date, including questions that wrap the value in an inflation/CPI adjustment.
---

# Currency in circulation (Treasury Bulletin)

## Where it lives
- Each Bulletin issue has a money/currency statement (titled like "Currency in Circulation", "Status of United States Currency and Coin", or within the General Fund / money tables near the front). It reports END-OF-MONTH amounts in **millions of dollars**, broken down by kind: Federal Reserve notes, U.S. notes, silver certificates, standard silver dollars, fractional/minor coin, etc., plus a **Total** line.
- "By the end of the fiscal month" = the ordinary end-of-month figure; no special fiscal adjustment.

## THE pitfall — total vs. Federal Reserve notes
- **"Total currency in circulation" means the grand-total line (all kinds, including coin), NOT the Federal Reserve notes row.** FR notes are the largest component (~85-88% of the total in the late 1960s) and are easy to grab by mistake from a summary table.
- Magnitude anchor for sanity-checking: late-1969 total currency in circulation ≈ $53.0 billion, while FR notes alone ≈ $46.4 billion.
- Diagnostic: if your answer is ~12-14% LOW versus a graded/expected value, you used FR notes (or another subcomponent) instead of the total — re-read the table for the Total row rather than questioning the arithmetic.
- Conversely, "currency outside banks" (a Fed/FRB money-stock concept, smaller) is NOT the Bulletin's "currency in circulation" (which includes currency held by banks). Match the exact phrase to the exact table line.

## CPI inflation-adjustment wrapper
- Pattern: "inflation-adjusted dollar amount after applying the official BLS CPI-U year-over-year inflation rate for <month YYYY> to <value>".
- Recipe: rate r = CPI-U(month, year) / CPI-U(same month, year−1) − 1, using the official BLS CPI-U index (NSA, U.S. city average — FRED series CPIAUCNS; for 1969-era values the 1982-84=100 index is the one to use). Then **answer = value × (1 + r)** — a single multiplication, not deflation/division.
- Do NOT recall CPI index values from memory for the exact month — fetch them (e.g. `curl "https://fred.stlouisfed.org/graph/fredgraph.csv?id=CPIAUCNS&cosd=1968-11-01&coed=1969-11-01"`). A 0.1-index-point error shifts the YoY rate enough to break tenths-place rounding.
- Keep the base value in printed millions; round only the final product to the stated precision.

### Variant 2 — real month-over-month change ("adjust month A to month B dollars")
- Pattern: "month-over-month change in <series> in <month B> dollars, using the CPI-U to adjust the <month A> value to <month B> real dollars".
- Recipe: **answer = value(B) − value(A) × CPI-U(B) / CPI-U(A)**. The ratio of the two monthly CPI index LEVELS (not a YoY rate) converts month A into B-dollars; the month-B value is already in B-dollars and is NOT adjusted.
- Carry full precision through the CPI ratio; round only the final difference to the stated decimal places.
- The result is often small and NEGATIVE (monthly inflation outpaces the nominal rise) — e.g. May→June [redacted] Federal Reserve notes gave [redacted] (verified correct). A negative answer is expected, not a sign error; output a plain ASCII minus.

### Variant 3 — constant-year dollars via ANNUAL average CPI
- Pattern: "adjust to constant year-T dollars using the annual average CPI-U (1982-84=100, NSA)". Recipe and the critical use-published-ROUNDED-annual-averages rule (not unrounded means of the 12 monthly values) are in **tb-federal-debt-outstanding → "Constant-dollar (CPI deflation) wrapper"**; the same recipe applies regardless of which series is being deflated.

- Verified example: Nov [redacted] — total currency in circulation ≈ [redacted]XX (millions, Total line) × (1 + CPI-U YoY for Nov [redacted] ≈ [redacted][redacted]) = **[redacted]** (accepted). Using the FR-notes row (~[redacted]B) gave [redacted] → WRONG.
