---
name: tb-poe-data-label-charts
description: Use for Treasury Bulletin questions that read VALUES off the "Profile of the Economy" (PoE) charts in modern bulletins (~1990s-2010s) — e.g. the quarterly "Payroll Employment (average monthly change in thousands)" bar chart, real GDP growth bars, CPI bars — where each bar has a small printed data label. Distinct from tb-chart-visual-count (which counts visual features, not values).
---

# Reading values off Profile-of-the-Economy charts

## Where the data lives
Modern bulletins (≈1995–2013) open with a "Profile of the Economy" section
(first ~10 PDF pages). Each topic page pairs narrative prose with 1–2 small
charts. Bar charts there print a **small numeric data label above every bar** —
read those labels; do NOT estimate from bar height and do NOT recompute from
external/current BLS or BEA data (vintages differ from what the bulletin printed).

## The Payroll Employment chart (recurring)
- Title: "Payroll Employment", subtitle: "(Average monthly change in thousands
  from end of quarter to end of quarter)".
- X-axis: quarters labeled with roman numerals I II III IV, grouped under year
  labels (e.g. 2004, 2005, 2006, plus a partial current year).
- **Bar semantics:** the bar labeled "II" of year Y IS the "average monthly
  change from end of Q1 to end of Q2" of year Y — i.e. (June level − March
  level)/3. Generally: bar N = change from end of quarter N−1 to end of
  quarter N, averaged over that quarter's 3 months. The question's
  "from end of QX to end of QY" phrasing maps directly to bar(s) X+1..Y;
  for adjacent quarters it is a single bar — no level arithmetic needed.

## Label→bar alignment procedure (the failure mode)
A wrong answer here almost always comes from pairing a printed label with the
wrong bar/quarter (a one-slot shift in one year poisons the mean). Procedure:
1. Render the chart page as an image at high DPI and view it zoomed.
2. Transcribe **every** label left-to-right into a single ordered list first
   (don't cherry-pick the bars you need).
3. Check count: labels = 4 × (number of full years) + (quarters of the partial
   current year). If the count is off, a label was missed or merged — re-render.
4. Only then chunk the list into years (I,II,III,IV per year group) and select
   the needed quarter from each year.
5. Cross-check labels can sit at staggered heights to avoid overlap — height of
   the label is NOT meaningful, only left-to-right order is.
6. Sanity-check against the prose on the same page (it quotes recent monthly
   job numbers) and against neighboring bulletins if in doubt.

Worked example (Sept 2007 bulletin, PoE p.5): labels in order are
2004: 163 219 112 194 | 2005: 151 264 211 220 | 2006: 252 124 202 177 |
2007: 142 145. "Mean of the end-of-Q1→end-of-Q2 change, 2004–2006" = mean of
the three II bars = (219+264+124)/3 = 202.333. A one-quarter misalignment in
2004 (taking 112 instead of 219) gives the plausible-looking but wrong 166.667.

## Output
Means like X/3 are usually non-terminating — keep full precision and round only
at the end to the requested place ([redacted], not 202.3).
