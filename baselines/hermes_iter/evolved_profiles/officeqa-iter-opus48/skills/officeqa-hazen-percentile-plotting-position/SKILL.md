---
name: officeqa-hazen-percentile-plotting-position
description: OfficeQA Treasury Bulletin — compute the "Nth Hazen Percentile" / "Hazen Plotting Position" value of a small fiscal-year series (e.g. total nominal on-budget+off-budget outlays for an agency FY YYYY-YYYY). Covers the exact Hazen inverse formula, the dominant failure of emitting the MAX instead of the interpolated rank, the rank-lands-exactly-on-integer subtlety, and the agency-row-summing prerequisite (DoD = Military + Civil). FAILED DoD 85th Hazen FY2011-2020 by emitting 732852 (the max) vs GOLD 678077 (the 2nd-largest = rank 9.0 of 10).
category: research
---

# Hazen Percentile / Hazen Plotting Position (OfficeQA)

## Trigger
Q asks for "the Nth Hazen Percentile value (using the Hazen Plotting Position)
of <series>" — typically a 10-ish-value fiscal-year series of agency outlays or
receipts. The phrase "Hazen Plotting Position" is the tell. Output is one dollar
value in the series' stated unit (usually $ millions), rounded as asked.

## The Hazen convention (THE WHOLE GAME)
Hazen plotting position assigns to the i-th smallest of n sorted values the
cumulative probability:
    p_i = (i - 0.5) / n            (i = 1..n, ascending sort)

To find the VALUE at percentile P, INVERT it. The (1-indexed, ascending) rank
position r that corresponds to percentile P is:
    r = (P/100) * n + 0.5

Then:
- If r is an integer, the answer is EXACTLY the value at ascending rank r
  (the r-th smallest). NO interpolation, NO rounding up to the max.
- If r is fractional, linearly interpolate between floor(r) and ceil(r):
    answer = x[floor(r)] + (r - floor(r)) * (x[ceil(r)] - x[floor(r)])
  using 1-indexed ascending-sorted x. (Clamp r to [1, n].)

## THE FAILURE (why this ref exists)
Q: 85th Hazen percentile of total nominal on-budget+off-budget DoD outlays,
FY2011-2020 (n=10). I answered **732852.00** (the MAX of the series). GOLD =
**678077.00**. For n=10, P=85:  r = 0.85*10 + 0.5 = **9.0** — exactly rank 9 of
10, i.e. the **2nd-LARGEST** value, NOT the max (rank 10). The max is the 100th
percentile-ish tail; the 85th lands one rank below it.

GENERAL RULE OF THUMB: for n=10, the Hazen rank r = P/10 + 0.5. So
85th -> r=9.0 (2nd largest), 95th -> r=10.0 (the max), 75th -> r=8.0,
50th -> r=5.5 (interp between 5th and 6th). The MAX is only the answer when
r >= n, i.e. P >= (n-0.5)/n*100 = 95% for n=10. If you emitted the max for an
85th percentile, you almost certainly skipped the formula.

## GATE before submitting
1. Compute r = P/100*n + 0.5. State it explicitly.
2. The answer must be <= the max of the set, and unless r>=n it must be
   STRICTLY LESS than the max. If your candidate == max(series) but r < n,
   STOP — you grabbed the wrong rank.
3. If r is an integer, answer == the r-th smallest value verbatim (a value that
   actually appears in the table). If your "Hazen value" is not one of the
   actual data points and r was an integer, you interpolated wrongly.

## PREREQUISITE: build the per-year series CORRECTLY first
The Hazen math is worthless if the 10 yearly totals are wrong. For DoD
specifically, the Treasury "Outlays by Agency" table SPLITS Defense into
**Department of Defense — Military** AND **Department of Defense — Civil**
(plus sometimes a separate Military Retirement / Corps of Engineers civil line).
SUM the Military + Civil sub-rows for each year; Military-only undershoots.
(See memory note on highest-spending-department; same split trap.)

"total nominal on-budget AND off-budget outlays" = the combined agency outlay
total (on-budget + off-budget components added), in nominal (not inflation-
adjusted) $ millions. Most agency outlay tables already report the combined
figure; if on/off-budget are shown separately, add them per year.

Data source: modern bulletins' "Federal Fiscal Operations" / agency-outlay
tables, or pull the 10 annual values from successive September bulletins
(one fiscal year each) — same sourcing pattern as the R-square / on-vs-off
budget refs. Confirm each year's number before sorting.

## Worked procedure
1. Pull the 10 annual DoD total outlay values (Military + Civil summed) FY2011-2020.
2. Sort ascending.
3. r = (85/100)*10 + 0.5 = 9.0.
4. r is integer -> answer = 9th-smallest = 2nd-largest value.
5. Round to hundredths -> e.g. 678077.00.

```python
import numpy as np
def hazen_percentile(values, P):
    x = sorted(values)                  # ascending
    n = len(x)
    r = (P/100.0)*n + 0.5               # 1-indexed rank position
    r = min(max(r, 1.0), float(n))      # clamp
    lo = int(np.floor(r)); hi = int(np.ceil(r))
    if lo == hi:
        return x[lo-1]                  # exact integer rank
    frac = r - lo
    return x[lo-1] + frac*(x[hi-1] - x[lo-1])
# hazen_percentile(ten_dod_totals, 85) -> 678077.0
```
numpy not importable in the execute_code sandbox -> run via
`cd /home/azureuser/office-qa && python3 script.py`.

## Distinguish from other plotting positions
This is HAZEN specifically: p=(i-0.5)/n. Do NOT use Weibull p=i/(n+1) or the
California / Tukey / Blom variants unless the Q names them. The +0.5 offset is
what makes 85th land on rank 9.0 (not 9.35 as Weibull would give for n=10).
