---
name: officeqa-chart-local-maxima-counting
description: OfficeQA Treasury Bulletin — VISUAL questions that ask "how many local maxima are there on the line plots on page N?" (or peaks/humps on charts). These are answered by rendering the page to a high-res image and visually counting peaks across ALL line series on the page, then SUMMING. Not a table/arithmetic question. Covers the render pipeline, the all-series-summed rule, and the dominant undercount failure mode. PASSED Sep1990 pdf p5 = 18.
---

# OfficeQA — Counting Local Maxima on Treasury Bulletin Chart Pages

## When to use
Question wording like:
- "how many local maxima are there on the line plots on that page?"
- "how many peaks / humps / turning points on the chart(s) on page N?"
- Any VISUAL counting question over CHART pages (not tables).

These are NOT arithmetic or table-lookup questions. There is no text extraction
that helps — you must RENDER the page and look at it.

## Pipeline (proven)
1. Resolve the PDF for the given bulletin (e.g. September [redacted] Monthly Treasury
   Bulletin). The "page N" in the question is the PRINTED/visual page; chart
   pages in early-1990s bulletins are usually near the front (charts precede the
   tabular sections). If page N is ambiguous, render a few candidate pages and
   pick the one that actually contains line plots.
2. Render that page to a high-resolution image:
   ```
   pdftoppm -png -r 300 -f <pdfpage> -l <pdfpage> "<bulletin>.pdf" /tmp/p
   ```
   300 dpi is the floor — faint/thin lines and small peaks get lost at lower
   resolution and cause undercounts.
3. Load the rendered PNG with vision and count peaks.

## Counting rule — the whole game
- A "local maximum" = a point where the line goes UP then DOWN (a peak / crest).
  Endpoints that are merely high are NOT local maxima unless the curve turns.
- Count peaks on EVERY line series on the page and **SUM across all series**.
  A chart page often stacks multiple panels (e.g. receipts, outlays, deficit)
  and/or multiple lines per panel. Each line contributes its own peaks; total =
  sum over all lines on the page.
- Count every distinct crest, including small secondary bumps between larger
  peaks — they each count.

## Dominant failure mode: UNDERCOUNT
The off-by-one error here is almost always an UNDERCOUNT — a faint peak, an
edge/near-boundary peak, or a small secondary bump gets missed. When torn
between two counts, **prefer the HIGHER count**. Re-scan each line left-to-right
specifically hunting for: (a) peaks near the left/right plot edges, (b) faint or
thin lines you may have skipped, (c) tiny bumps riding on a larger trend.

## Verification checklist before answering
- Did you count ALL lines on the page, not just the most prominent one?
- Did you sum across panels if the page has multiple stacked charts?
- Did you re-scan edges and faint lines for missed crests?
- Is your count biased toward the higher side when uncertain?

## Track record
- PASSED: Sep [redacted] bulletin, pdf page 5, answer = 18 (sum of peaks across all
  line series on the page).

## Output format
A single integer (bracketed-CSV not required for a lone scalar, but follow the
question's stated format). No units.
