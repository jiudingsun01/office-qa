---
name: tb-macro-narrative-indicators
description: Use for Treasury Bulletin questions about quarterly U.S. macro indicators quoted in prose — nonfarm business productivity (output per hour), real GDP/GNP growth, employment, CPI, compensation — for a specific calendar quarter (e.g. "growth rate of non-farm business productivity in Q3 1995"). These come from the narrative economic-review section, NOT a statistical table.
---

# Quarterly macro indicators from the Bulletin's narrative section

## Where the data lives
Each quarterly Treasury Bulletin opens with a narrative review of recent economic
developments (first few pages, before the statistical tables). Quarterly figures for
nonfarm business productivity, GDP growth, inflation, employment, etc. are stated in
**prose**, e.g. "nonfarm productivity (real output per hour worked) rose at a 2.0
percent annual rate in the third quarter." Search the front matter for keywords like
"productivity", "output per hour", "rose at a", "annual rate" — do not hunt for a table.

## Quarter → issue mapping
The bulletin covering calendar quarter Q is published ~2-3 months after the quarter ends:
- Q1 data → **June** issue
- Q2 data → **September** issue
- Q3 data → **December** issue
- Q4 data → **March** issue of the following year

## Vintage pitfall — use the FIRST-reported figure
Later issues print **revised** values that can differ enormously. Verified examples:
- Q3 1995 nonfarm productivity: first reported **2.0%** (Dec 1995 issue); revised to
  1.4% in the March 1996 issue (chain-weighted output switch).
- Q1 1998 nonfarm productivity: first reported **0.2%** (June 1998 issue); revised to
  3.5% in the September 1998 issue.

Gold answers use the value **as first reported in the issue covering that quarter**.
So retrieve each quarter from its OWN covering issue per the mapping above; never take
both quarters' values from one later bulletin (you'd get revised vintages).

## Computation conventions
- "Growth rate" for a quarter = the seasonally adjusted **annual rate** quoted in prose.
- "Absolute difference in the growth rate between quarter A and quarter B" =
  |rate_A − rate_B| in percentage points (e.g. |2.0 − 0.2| = 1.8). It is NOT a
  cumulative growth computation across the span; "inclusive" just names the endpoints.
- Round only at the end, to the precision the question asks for.
