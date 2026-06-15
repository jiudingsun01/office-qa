---
name: series-peak-argmax
description: Use for any question asking in which year/month a series peaked, bottomed, was highest/lowest, or first/last crossed a threshold over a stated range (e.g. "between 1950 and [redacted], when did the personal saving rate peak?"). Applies to Treasury Bulletin tables and to macro series (saving rate, deficits, yields) alike.
---

# Peak/trough-over-a-range questions: extract the series, never answer from memory

## The failure this prevents
Asked "between [redacted] and [redacted], in which year did the U.S. personal saving rate (household saving as % of after-tax income) peak?", an agent answered **[redacted]** from general knowledge ("saving rates were high in the early 80s"). The correct answer was **[redacted]** (the NIPA-vintage series peaks ~13% around [redacted]-74; the early-80s local high is lower). Memory-based priors reliably pick the *famous* episode, not the actual argmax.

## Procedure
1. **Locate the actual data table/chart in the source corpus** (Treasury Bulletin page, report appendix, statistical table). Do not skip retrieval because the question "sounds like general knowledge" — these questions are graded against a specific document's series.
2. **Extract EVERY year (or month) in the stated range** into a list, even if tedious. Partial extraction ("the 70s look high, the 80s look high") is where errors creep in.
3. **Compute the argmax/argmin programmatically or by explicit written comparison** — list year:value pairs and pick the extremum; do not eyeball a chart and guess.
4. **Check range endpoints inclusively**: "between 1950 and [redacted]" includes 1950 and [redacted] unless stated otherwise.
5. If the source document is unavailable and you MUST fall back on knowledge, prefer **historical/contemporaneous data vintages** over modern revised series, and prefer the structurally-known extremum over the most-famous episode. Known anchor: the U.S. personal saving rate (household saving / disposable income) **peaked in the early 1970s (~[redacted], ~13%)**, NOT the early 1980s (~10-11% local high), and declined steadily after the mid-1980s.

## Related pitfalls
- "Peak" on a *rate* vs peak on a *level*: a dollar series can peak in a different year than the same series as a percent of income/GDP. Match the exact measure named in the question.
- Ties or near-ties: if two years are within rounding of each other in the table, report the one the table shows as strictly highest at the printed precision.
