# Counting local maxima / minima / peaks on Treasury Bulletin chart pages

Some OfficeQA questions are VISUAL, not table-extraction:
  "On page N of the <month year> US Treasury Monthly Bulletin, how many local
   maxima are there on the line plots on that page?"

These ask you to look at the rendered chart page and count peaks across ALL line
series on the page. This is a vision task — render the PDF page to an image at
high DPI and count, do NOT try pdftotext.

## Procedure
1. Render the exact page to PNG at high resolution so individual peaks are
   distinguishable. Use ~200-300 DPI:
     pdftoppm -png -r 300 -f <page> -l <page> bulletin.pdf /tmp/chartpage
   (Page here is the PRINTED/document page as the question states; if off, the
   FRASER PDF page may differ from the printed page number — try both.)
2. Load the image with vision and count local maxima on EVERY line series on the
   page, then SUM across all series. A "local maximum" = a point where the line
   rises then falls (a visual peak/hump). The page often has multiple charts and
   multiple lines per chart; the answer is the total count over everything.

## Pitfalls (these cost real off-by-one errors)
- OFF-BY-ONE is the dominant failure mode. Got 17, gold was 18. Recount carefully.
- Count peaks on ALL lines, not just the most prominent one. Faint/secondary
  series (dashed, lighter color) each contribute their own maxima — easy to miss
  one, which produces exactly the -1 error.
- ENDPOINT rule: the first and last data points of a series are generally NOT
  local maxima (no neighbor on one side). But a sharp turn right at the visible
  edge can read as a peak — when undercounting, re-examine the left/right edges
  and any peak that sits near where a series starts/ends.
- Small "shoulders" / plateaus and tiny wiggles at chart resolution can each be a
  genuine local max in the underlying data. When your count is just below gold,
  zoom in (crop + upscale) on busy regions and look for shallow humps you skipped.
- Multiple stacked sub-charts on one page: process each sub-chart region
  separately, count its line(s), then add. Missing an entire small bottom chart
  is another way to land one short.
- If two readings disagree by one, prefer the HIGHER count — the systematic
  error here was undercounting (missing a faint/shallow/edge peak), not
  overcounting.

## Verification
- Re-render at higher DPI and crop into 2-3 horizontal bands; count each band
  independently and sum. Reconcile against the whole-page count before answering.
