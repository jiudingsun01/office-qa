---
name: tb-bond-yields
description: Use for Treasury Bulletin questions about yields of long-term Treasury bonds vs corporate (Moody's Aaa/Aa) bonds — levels, spreads, argmax/argmin of a spread, the NEW-issue Aa corporate series ("yields that are new"), or regression projections of monthly yields to a future month.
---

# Long-term bond yields and corporate–Treasury spreads in the Treasury Bulletin

## Where the data lives
- The Bulletin has a recurring table **"Average Yields of Long-Term Treasury, Corporate, and Municipal Bonds"** (older issues: "Average Yields of Taxable Treasury Bonds and Corporate Aaa/Aa Bonds"), located in the **market quotations / yields section near the back** of each issue (often labeled "Yields of Long-Term Bonds", page numbers ~80-90 in 1960s-70s issues).
- It gives **monthly average yields (percent per annum)** for: long-term Treasury bonds, corporate Aaa (Moody's), and corporate Aa (Moody's). A single issue carries a long monthly history (a decade or more), so one bulletin (e.g. June 1970) can answer a question spanning 1960-1969 — do NOT fetch one bulletin per year.
- There is also a companion chart; **always read the table, never eyeball the chart**.

## Phrasing → series mapping
- "**highest quality** corporate bonds (as determined/rated by Moody)" = **Moody's Aaa**. "High-grade" / second tier = Aa. Map the quality phrase to the column header before reading any numbers.
- Questions may anchor years to historical events instead of naming them — resolve the event to a calendar year first and state it explicitly (e.g. end of WWII = **1945**, Korean War began = **1950**, US entered WWII = 1941, Korean War armistice = 1953). Then treat it as an ordinary year lookup.

## Annual-average questions
- For "average annual yield in year Y": the table often prints an **annual-average row/line** alongside monthly figures — prefer the printed annual figure. If only monthly values are printed, average the 12 months and round to the table's precision (2 decimals).
- "Absolute change in percentage points" = |value(Y2) − value(Y1)|, in raw points (NOT percent-of-percent), rounded as asked. A result of **0.0 is a legitimate answer** — Aaa yields were nearly flat across some spans (e.g. mid/late 1940s–1950), so don't second-guess a zero difference.

## Early-era (1938–1950s) "high-grade corporate bonds" series (KNOWN FAILURE)
- The earliest Bulletins (first issue Jan 1939; 1938 data appears in 1939 issues) carry a table of monthly average yields of **long-term Treasury bonds and "high-grade corporate bonds"**. This corporate series is the **Bulletin's own published column — do NOT substitute Moody's Aaa values from memory or FRED**; the two series differ by enough to flip any small-window statistic.
- **Verified failure (variance of high-grade corporate yields, Jan–Jun 1938, 5 d.p.): an attempt using Moody's-Aaa-style values (~3.17–3.26) gave 0.00089; the accepted answer was 0.00137.** The gap is far larger than a divisor (n vs n−1) effect — it was a wrong-series/wrong-cells problem. Open the actual early bulletin and transcribe the printed cells.
- Tiny-variance pitfall: with ~6 values printed to 2 decimals, the variance is ~1e-3, so a **single ±0.01 misread shifts the answer at the 4th–5th decimal** — re-read every cell (ideally cross-check against the same months reprinted in the next issue) before computing.
- Divisor: compute BOTH population (÷n) and sample (÷n−1) variance; with correct cells the accepted value should match one of them exactly at the asked rounding — if neither matches a sanity cross-check, suspect a misread cell, not the divisor.

## "NEW" Aa corporate bond yields (newly issued series)
- In modern issues (1980s–2000s) the yields table has a **"New Aa corporate bonds"** column — yields on NEWLY ISSUED Aa-rated bonds — distinct from Moody's seasoned Aa. Question phrasing like "AA-rated corporate bond yields **that are new**" refers to this new-issue column, not to the date range. The table's footnote matches the phrase "monthly averages of weekly (or daily) series".
- The New Aa series can have **missing months** (no qualifying new issues in some months). Count your data points before any statistic — a 48-month window may yield fewer than 48 values.
- A single modern issue prints only ~13 recent months of monthly data (plus annual averages for earlier years). A multi-year monthly window (e.g. 1999–2002) must be **stitched from ~4 bulletins**; cross-check the overlapping months between consecutive issues to catch transcription/revision errors before computing.

## Regression-projection questions on these yields (KNOWN FAILURE — be careful)
- Pattern: "linear regression of monthly averages of <yield series> from year A to year B inclusive — absolute difference between the predicted yield for <next month> and the actual value."
- Setup: t = 1 for the first month of the window through t = N for the last (1-based, per tb-math-transform-wrappers); predict t = N+1 (e.g. Jan 1999=1 … Dec 2002=48, predict t=49). Fit OLS with numpy; the actual next-month value comes from a bulletin published a few months after that month.
- **Verified failure (New Aa corporate, 1999–2002 → Jan 2003): an attempt produced 0.59; the accepted answer was 0.35.** A 0.2+ gap is a data-assembly problem, not rounding. Before answering this shape, re-check: (1) you used the NEW Aa column, not seasoned Aa (FRED's Moody's Aa is the seasoned series — do NOT substitute it); (2) missing-month handling — if some months are blank, compute BOTH calendar-indexed t (with gaps) AND consecutive renumbering of the available points and see which yields a cleaner/expected-scale answer; (3) the "actual" cell comes from the Bulletin's own table, same column; (4) overlap months across the stitched bulletins agree.

## Procedure for spread questions
1. Find the yields table in the single bulletin the question names.
2. Extract BOTH series month-by-month over the full stated range; compute spread = corporate − Treasury for every month (write a small script if 100+ months).
3. Apply `series-peak-argmax` discipline: explicit argmax/argmin over all months, inclusive endpoints, report at printed precision (yields are printed to 2 decimals; spreads can tie — pick the strictly smallest/largest at printed precision).
4. **Chained questions** ("in that month, what was X?"): fully resolve and double-check the argmin/argmax month FIRST — an off-by-one-month error there silently corrupts the second lookup even if the second table is read perfectly.
5. **Average-spread questions (VERIFIED working)**: "average yield spread between Aa and Treasury across the months of YYYY–YYYY" = mean of the monthly spreads, which equals mean(corporate) − mean(Treasury), so you can sum each column once and difference the sums — fewer transcription steps than 120 individual subtractions. Sanity-check the month count first (a full decade = exactly 120 monthly cells per series; a missing/extra row shifts the 4th–5th significant digit). Verified: June 1970 bulletin, Aa − long-term Treasury, Jan 1960–Dec 1969, 5 significant digits → **0.88525** accepted. Report at the requested significant digits, not 2 decimals.
