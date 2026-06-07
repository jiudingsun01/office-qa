# Continuously compounded (CC) average annual growth rate

## Trigger
Q asks for the "continuously compounded average annual growth rate" of some
nominal-dollar series between two calendar years (e.g. Seigniorage on coins from
end of CY 1945 to 1955), "rounded to the nearest thousandths place and reported
as a decimal value."

## THE FORMULA (do NOT use CAGR)
Continuously compounded != geometric/CAGR. They differ.

  CC  rate = ln(V_end / V_start) / n          <- THIS is what "continuously compounded" means
  CAGR     = (V_end / V_start) ** (1/n) - 1   <- WRONG for this phrasing

where n = the number of YEARS BETWEEN the two endpoints = end_year - start_year.
  "end of CY 1945 to 1955"  ->  n = 1955 - 1945 = 10   (NOT 11, not a count of labels)

```python
import math
def cc_growth(v_start, v_end, n_years):
    return math.log(v_end / v_start) / n_years
# round(cc_growth(V1945, V1955, 10), 3)
```

## Worked example (CORRECT, gold 0.063)
Seigniorage on coins (silver+minor), end CY1945 -> 1955, n=10.
Answer 0.063. The CC rate and CAGR are close for small rates but diverge enough
to flip the thousandths digit — always use ln(ratio)/n when the word
"continuously" appears.

## Output convention
"reported as a decimal value (12.34% -> 0.1234)": report the bare rate, NOT
times 100. 0.063 means 6.3%. Single decimal value -> MODE A bare format, no
brackets-with-comma issue (single number). Round to requested place (thousandths).

## Quick decision
- phrase contains "continuously compounded" -> ln(V_end/V_start)/n
- phrase contains "compound annual growth" / "CAGR" / "average annual growth"
  WITHOUT "continuously" -> (V_end/V_start)**(1/n) - 1
- n = end_year - start_year (the time SPAN, not the number of data points)
