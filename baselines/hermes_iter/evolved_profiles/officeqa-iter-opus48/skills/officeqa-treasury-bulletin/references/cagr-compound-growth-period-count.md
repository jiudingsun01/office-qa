# CAGR / Compound Annual Growth Rate — period-count off-by-one trap

Trigger: "compound annual growth rate ... from FY/CY A to FY/CY B", "average
annual growth rate", "compounded ... per year".

## THE FATAL MISTAKE (cost a fail: answered 74.40, gold 108.01)
The exponent n is the SPAN BETWEEN ENDPOINTS, not the count of years/data points.

    n = end_year - start_year        # NOT (end_year - start_year + 1)
    CAGR = (value_end / value_start) ** (1/n) - 1
    answer_percent = CAGR * 100

FY1947 -> FY1950 : n = 1950 - 1947 = **3** (three one-year steps), NOT 4.
- Correct: (E/S)^(1/3) - 1
- Wrong (what I did): (E/S)^(1/4) - 1  -> understates the rate.

Sanity: if you list the years 1947,1948,1949,1950 you have 4 LABELS but only
3 INTERVALS. CAGR compounds over INTERVALS. Counting labels = the off-by-one.

Worked example (this exact question): expenditure transfers to the Federal
Old-Age & Survivors Insurance trust fund. value_end / value_start was ~9.0
(end ≈ 9x start). 9.0^(1/3)-1 = 1.0801 = **[redacted]**. 9.0^(1/4)-1 = 73.3%.

## Quick reverse-check trick
If your computed CAGR seems off, recompute the implied ratio (1+CAGR)^n and see
if it matches value_end/value_start cleanly. A clean ratio (like exactly 9.0x)
over the SMALLER n is a strong signal you have the right n.

## Identifying the fiscal year from a named historical event
Questions hide the year behind an event. The U.S. federal FY in this era runs
Jul 1 (prev cal yr) – Jun 30. Map event -> the FY in which the event DATE falls:
- **Korean War started** = June 25, 1950 -> falls in **FY 1950** (FY1950 = Jul 1949–Jun 1950).
- WWII U.S. entry (Pearl Harbor) = Dec 7, 1941 -> FY 1942.
- WWII end (V-J Day) = Aug/Sep 1945 -> FY 1946.
Always resolve the event to a calendar DATE first, then ask which FY contains it.

## Checklist
1. Resolve any event-named year to an explicit FY/CY (use event date + FY rule).
2. n = end - start (intervals, never +1).
3. Pull value_start and value_end in NOMINAL dollars if the question says
   "nominal" (do NOT deflate). Same unit/scale for both endpoints.
4. CAGR = (E/S)^(1/n) - 1, ×100, round as requested.
5. Reverse-check: (1+CAGR)^n ≈ E/S.
