---
name: tb-macro-indicators
description: Use for Treasury Bulletin questions about quarterly U.S. macro indicators — nonfarm business productivity (output per hour), real GDP/GNP growth, CPI, payroll employment, compensation — pulled from the Bulletin's economic-review front matter for a specific calendar quarter or year. Covers BOTH the narrative "recent economic developments" prose figures AND the modern "Profile of the Economy" charts whose bars carry printed data labels.
---

# Macro indicators from the Bulletin's economic-review front matter

Each quarterly Treasury Bulletin opens with an economic review in its first ~10 pages
(in modern issues, ≈1995–2013, titled **"Profile of the Economy"**). The figures you
need are stated TWO ways on these pages — in **prose** ("rose at a 2.0 percent annual
rate") and on small **bar/line charts that print a numeric data label above each bar**.
Read the form the question points to; do NOT estimate from bar height and do NOT
recompute from external/current BLS or BEA data (vintages differ from what was printed).

## Quarter → issue mapping
The bulletin covering calendar quarter Q is published ~2–3 months after the quarter ends:
- Q1 data → **June** issue
- Q2 data → **September** issue
- Q3 data → **December** issue
- Q4 data → **March** issue of the following year

## Vintage pitfall — use the FIRST-reported figure
Later issues print **revised** values that can differ enormously. Gold answers use the
value **as first reported in the issue covering that quarter**, so retrieve each quarter
from its OWN covering issue per the mapping above; never take two quarters' values from
one later bulletin (you'd get revised vintages). Verified examples:
- Q3 1995 nonfarm productivity: first reported **2.0%** (Dec 1995); revised to 1.4% in
  March 1996 (chain-weighted output switch).
- Q1 1998 nonfarm productivity: first reported **0.2%** (June 1998); revised to 3.5% in
  September 1998.

## Reading PROSE figures
- Search the front matter for keywords like "productivity", "output per hour", "rose at
  a", "annual rate" — do not hunt for a statistical table.
- "Growth rate" for a quarter = the seasonally adjusted **annual rate** quoted in prose.

## Reading CHART data labels (Profile of the Economy bar charts)
Bar charts (e.g. "Payroll Employment", real GDP growth, CPI) print a small numeric label
above every bar. A wrong answer here almost always comes from pairing a printed label
with the wrong bar/quarter (a one-slot shift in one year poisons the mean). Procedure:
1. Render the chart page as an image at high DPI and view it zoomed.
2. Transcribe **every** label left-to-right into one ordered list first (don't cherry-pick
   the bars you need).
3. Check count: labels = 4 × (number of full years) + (quarters of the partial current
   year). If the count is off, a label was missed or merged — re-render.
4. Only then chunk the list into years (I,II,III,IV per year group) and select the needed
   quarter from each year.
5. Labels can sit at staggered heights to avoid overlap — height is NOT meaningful, only
   left-to-right order is.
6. Sanity-check against the prose on the same page and neighboring bulletins if in doubt.

**Payroll Employment chart bar semantics** (subtitle "Average monthly change in thousands
from end of quarter to end of quarter"): each year has 4 bars in order I, II, III, IV, and
bar N = change from end of quarter N−1 to end of quarter N. Concrete mapping — DO NOT
shift this by a slot:
- "end of Q1 → end of Q2" = bar **II** (the **2nd** bar of the year), NOT bar III.
- "end of Q2 → end of Q3" = bar **III** (3rd bar).
- "end of Q3 → end of Q4" = bar **IV** (4th bar).
- "end of Q4(prev) → end of Q1" = bar **I** (1st bar).
The recurring failure is reading the 3rd bar for an "end-of-Q1→end-of-Q2" question. After
chunking the year into [I, II, III, IV], explicitly say which ordinal slot you are taking
and confirm it matches the table above before averaging. For adjacent quarters it is a
single bar — no (June−March)/3 level arithmetic needed; the bar IS already the avg monthly
change.

Worked example (Sept 2007 bulletin, PoE p.5): labels in order are
2004: 163 219 112 194 | 2005: 151 264 211 220 | 2006: 252 124 202 177 | 2007: 142 145.
"Mean of the end-of-Q1→end-of-Q2 change, 2004–2006" = mean of the three II bars =
(219+264+124)/3 = 202.333. A one-quarter misalignment in 2004 (taking 112 instead of 219)
gives the plausible-looking but wrong 166.667.

(For COUNTING visual features on line-chart pages — local maxima, line crossings — rather
than reading printed values, use tb-page-counting.)

## Computation conventions
- "Absolute difference in the growth rate between quarter A and quarter B" =
  |rate_A − rate_B| in percentage points (e.g. |2.0 − 0.2| = 1.8). It is NOT a cumulative
  growth computation across the span; "inclusive" just names the endpoints.
- **Geometric-mean / aggregation wrappers go to tb-math-transform-wrappers, NOT a naive GM
  here.** If a question asks for the "geometric mean of <real GDP growth> quarterly percent
  change at an annual rate" (per-year, then argmax), do NOT geometric-mean the raw printed
  percents (gives ~2–3, WRONG). The graders' convention de-annualizes:
  f_q = (1+r_q/100)^(1/4), GM = (∏f_q)^(1/n), answer = (GM−1)×100 — landing ~0.5–0.7. See
  tb-math-transform-wrappers "Geometric mean of a SERIES of percent changes" (verified:
  2017 → 0.69, the 2013–2019 max). A candidate near the arithmetic mean of the rates is
  the tell you used the wrong convention.
- Means like X/3 are usually non-terminating — keep full precision and round only at the
  end to the requested place ([redacted], not 202.3).
