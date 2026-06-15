---
name: series-peak-argmax
description: Use for any question asking in which year/month a series peaked, bottomed, was highest/lowest, or first/last crossed a threshold over a stated range (e.g. "between 1950 and [redacted], when did the personal saving rate peak?"). Applies to Treasury Bulletin tables and to macro series (saving rate, deficits, yields) alike.
---

# Peak/trough-over-a-range questions: extract the series, never answer from memory

## The failure this prevents
Memory-based priors reliably pick the *famous* episode, not the actual argmax. When asked which year a series peaked over a range, an agent tends to name a well-known high-profile period from general knowledge rather than computing the true extremum from the document's series.

## Procedure
1. **Locate the actual data table/chart in the source corpus** (Treasury Bulletin page, report appendix, statistical table). Do not skip retrieval because the question "sounds like general knowledge" — these questions are graded against a specific document's series.
2. **Extract EVERY year (or month) in the stated range** into a list, even if tedious. Partial extraction ("the 70s look high, the 80s look high") is where errors creep in.
3. **Compute the argmax/argmin programmatically or by explicit written comparison** — list year:value pairs and pick the extremum; do not eyeball a chart and guess.
4. **Check range endpoints inclusively**: "between 1950 and [redacted]" includes 1950 and [redacted] unless stated otherwise.
5. If the source document is unavailable and you MUST fall back on knowledge, prefer **historical/contemporaneous data vintages** over modern revised series, and prefer the structurally-known extremum over the most-famous episode.

## Related pitfalls
- "Peak" on a *rate* vs peak on a *level*: a dollar series can peak in a different year than the same series as a percent of income/GDP. Match the exact measure named in the question.
- Ties or near-ties: if two years are within rounding of each other in the table, report the one the table shows as strictly highest at the printed precision.
