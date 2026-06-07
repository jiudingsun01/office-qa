---
name: treasury-bulletin-chart-local-maxima
description: Use for OfficeQA/Treasury Bulletin questions that ask for counts of local maxima, peaks, turning points, or similar visual features on line plots/charts in a Treasury Monthly Bulletin page.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [officeqa, treasury-bulletin, charts, line-plots, local-maxima, visual-counting]
    related_skills: [ocr-and-documents]
---

# Treasury Bulletin Chart Local-Maxima Counting

## Overview

Some OfficeQA Treasury Bulletin questions are visual chart questions, not table-extraction questions. A typical prompt asks: `On page X of the September 1990 US Treasury Monthly Bulletin, how many local maxima are there on the line plots on that page?`

For these, text extraction will not answer the question. Render the exact PDF page, identify every line plot and every separate plotted line/series on the page, then count visible interior peaks. The September 1990 Monthly Treasury Bulletin page 5 case exposed the main pitfall: an eyeballed count can miss several peaks when a page has dense front-matter chart panels and multiple visible line styles/series; a count that only follows the most obvious black lines can undercount by several peaks. Do a visual inventory first, crop/zoom each panel, trace each plotted polyline separately (including faint/dashed/secondary series inside the plot area), then peak-count from left to right.

## When to Use

Use this skill when the prompt asks about Treasury Bulletin charts/plots and visual features such as:

- `how many local maxima are there on the line plots on that page?`
- `count the peaks`, `count the troughs`, `turning points`, `local minima`
- chart/graph questions where the answer is not a table value
- pages with line plots in Monthly Treasury Bulletins, including front-matter chart pages

Do not use this skill for numeric table lookup, leading-digit counting, fiscal-year arithmetic, or PDF text extraction questions unless a chart must also be interpreted.

## Procedure

1. Resolve the exact source page.
   - If the prompt says `page 5` without saying `PDF page`, inspect the rendered PDF page 5 and nearby pages if the page content does not match the prompt.
   - Treasury Bulletins often have cover/front matter and printed page numbers that differ from PDF indices; do not assume report page and PDF page are identical.
   - Verify visually that the page contains line plots before counting.

2. Render the page as an image.
   - Use a high-resolution render (at least 200-300 DPI) so thin grayscale lines and small panels are visible.
   - Prefer `pdftoppm -r 300 -f PAGE -l PAGE -png input.pdf outprefix` or an equivalent PDF renderer.
   - If the page image is dense, crop each chart/panel separately and zoom. Do not rely on `pdftotext`; chart lines are not text.

3. Make a plot inventory before counting.
   - List every separate line-plot panel on the page.
   - Within each panel, identify every distinct plotted series/line. A single chart may contain multiple overlaid lines or several small multiples.
   - Exclude axes, gridlines, legends, arrows, labels, borders, and decorative rules.
   - If a line is repeated in a legend swatch only, do not count legend swatch peaks.

4. Count local maxima per plotted series.
   - Work panel-by-panel from a crop/zoomed image; for dense front-matter chart pages, make a left-to-right peak tally on each crop rather than estimating from the full page.
   - Count an interior point/vertex/rounded crest where the line rises before it and falls after it.
   - For monthly/quarterly connected line charts, count each visible peak in the polyline, not each year label or tick.
   - Do not count endpoints as local maxima unless the prompt explicitly says to include endpoints.
   - For a flat-topped plateau, count it as one maximum only if the line rises into the flat segment and falls after it.
   - For noisy jagged lines, count visible turning peaks; use the plotted line path, not inferred underlying data.
   - When two lines cross, follow each line separately across the crossing before deciding peaks.
   - Treat dashed/dotted/gray lines as real plotted series if they are data lines in the plot area; do not drop them just because they are visually lighter than a solid black line.

5. Sum with an audit trail.
   - Record counts as `panel/series -> peak count` and then sum them.
   - For dense pages, make a temporary marked-up copy or written tick list for each crop: mark every accepted interior crest, then compare the marks against the raw image. Do not finalize from an unmarked mental count.
   - Independently recount from the page image after summing. A second pass should confirm that every plot panel and every series was included.
   - If counts differ between passes, crop/zoom the ambiguous panel and resolve it visually before finalizing.
   - Treat a surprisingly low count on a multi-panel chart page as a warning sign: the common miss is not definition of “local maximum” but omitted faint/short/secondary data series or small crests in crowded panels. If an initial pass is off by several peaks, redo the page as an explicit annotation task: number each accepted crest on the crop, maintain a per-series tally, and compare against the raw crop. Do not trust an unmarked mental count on dense chart pages.

## Practical Commands

Example page render workflow:

```bash
# Render one PDF page at high resolution. PAGE is 1-indexed.
pdftoppm -r 300 -f PAGE -l PAGE -png bulletin.pdf page

# Optionally crop/inspect with ImageMagick if installed.
magick page-PAGE.png -crop WIDTHxHEIGHT+X+Y crop.png
```

If using Python for manual assistance, display the rendered page or crops with matplotlib and optionally trace approximate line coordinates. Automated image processing is risky on old scanned Bulletins because axes, gridlines, labels, and anti-aliased text are often mistaken for plotted data; use it only as a helper, not as the sole evidence.

## Common Pitfalls

- Returning no answer because `pdftotext` has no chart geometry. Chart maxima questions require visual page rendering.
- Counting only the first chart on a page; front-matter pages can contain several line plots/panels.
- Counting only one line in a multi-series chart.
- Treating endpoints as local maxima. Unless specified, local maxima are interior peaks where the line changes from rising to falling.
- Counting legend sample lines, axes, gridlines, or decorative chart borders.
- Losing a line at crossings or where black/gray series overlap; trace each series continuously.
- Counting every wiggle in a thick scanned line without checking whether it is a real plotted vertex versus scan noise.

## Verification Checklist

- [ ] The exact PDF/report page mapping was checked visually.
- [ ] The page was rendered as an image at sufficient resolution.
- [ ] Every line-plot panel on the page was inventoried.
- [ ] Every plotted series in each panel was counted separately.
- [ ] Endpoints, legend swatches, axes, gridlines, and labels were excluded.
- [ ] Ambiguous crossings or flat peaks were resolved by zoom/crop.
- [ ] Final answer is the sum of per-panel/per-series peak counts, not an eyeballed page-level guess.
