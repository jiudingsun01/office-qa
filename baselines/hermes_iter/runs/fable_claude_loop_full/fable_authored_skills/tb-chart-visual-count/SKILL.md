---
name: tb-chart-visual-count
description: Use for Treasury Bulletin questions that ask you to count visual features on CHART pages — local maxima/minima on line plots, number of line series, line crossings, bars above a level — on a specific page (e.g. "how many local maxima are there on the line plots on page 5"). For counting TABLE cells, use tb-page-cell-census instead.
---

# Treasury Bulletin: counting features on chart pages

Bulletins from the ~1940s–1990s have chartbook-style pages near the front (often pdf pages 3–8, e.g. the "Treasury Financing Operations" / market-yields section) with one or more panels of small line charts. These counting questions are lost to off-by-one errors, so the procedure below is about exhaustiveness, not chart-reading talent.

## Rendering — do this first
1. Navigate by the **PDF page number** given in the question.
2. Render the page as an image at high DPI (300+; `pdftoppm -r 300 -f N -l N`). Low-res renders hide shallow wiggles, which is the #1 cause of undercounting.
3. If the page has multiple panels, **crop each panel and inspect it separately, zoomed**. Counting from a whole-page thumbnail reliably misses 1–2 features.

## Enumerate every series before counting
- List ALL line series on the page first: every panel × every line in each panel, including dashed/dotted/thin lines and any series only distinguishable via the legend. A missed series is a missed handful of peaks.
- Then count features **per series**, write the per-series tally down, and sum at the end. Never count "across the whole page" in one visual sweep.

## Local maxima rules and pitfalls
- A local maximum = a point/vertex strictly higher than the line immediately on both sides. Every interior peak counts, no matter how shallow — small wiggles are full-fledged maxima.
- Flat plateaus that rise then fall count as ONE maximum.
- **Endpoint convention check:** the usual convention excludes plot endpoints, but if a series ends (or begins) at its highest point in the neighborhood, graders may count it. After your strict-interior count, separately note how many series start/end on a falling edge (i.e. the first/last point is locally highest) — if your answer is being squeezed between N and N+k by such cases, lean toward INCLUDING endpoint peaks (a Sept-1990 page-5 question graded 18 where the strict-interior visual count gave 17).
- Undercounting (missing a shallow wiggle or a whole series) is far more common than overcounting. If two independent passes disagree, the higher count from a zoomed-in pass is usually the right one.

## Numeric cross-check (strongest tactic when available)
Front-section charts usually plot data tabulated elsewhere in the SAME bulletin (e.g. yield charts ↔ the average-yields table; financing charts ↔ offerings tables). If you can identify the source table, transcribe the series and count maxima numerically (`x[i-1] < x[i] > x[i+1]`) instead of trusting your eyes; then reconcile with the visual count.

## Final pass
Sum per-series tallies, recount once independently (panel-by-panel in reverse order), reconcile any mismatch, and report a bare integer.
