# VISUAL chart questions: counting features on line plots / charts

This is a distinct OfficeQA category: the question asks you to COUNT visual
features on the charts of a specific page — NOT to read values or do arithmetic.
Examples:
- "how many local maxima are there on the line plots on that page?"
- "how many local minima / peaks / troughs / inflection points ..."
- "how many lines / series / data points / gridlines are on the chart"

The answer is an INTEGER (no brackets-with-decimals, no units). Output the bare
count, e.g. `18`.

## Procedure (this is a VISION task, not a text-layer task)
The text layer is useless for chart shapes. You MUST render the page to an image
and look at the pixels.

1. Resolve the page number. Treasury Bulletin questions usually mean the PRINTED
   page label, which may differ from the PDF page index (FRASER front matter
   offset). Find the page: render a few candidate pages or search the text layer
   for the printed page number / section title, then confirm by eye.

2. Render at high DPI so thin plot lines and small wiggles are visible:
       pdftoppm -png -r 300 -f <pdfpage> -l <pdfpage> bulletin.pdf /tmp/p
   (300 dpi minimum; bump to 400 if lines are faint or close together.)

3. vision_analyze the PNG. Ask a SPECIFIC question, e.g. "Count the local maxima
   (points where the line rises then falls) across ALL line plots on this page.
   List each chart and its count, then total."

## Counting conventions (match OfficeQA gold)
- "local maximum" = an interior point where the line goes UP then DOWN (a peak).
  Endpoints of the series are NOT local maxima even if they are the highest point
  (a max needs neighbors on BOTH sides). Same logic for local minima (valleys).
- Count across EVERY line plot on the page and SUM them. A page often has
  multiple stacked charts and/or multiple series per chart — include them all
  unless the question names one specific chart.
- Each distinct series (line) is counted independently; overlapping lines each
  get their own peaks.
- Be deliberate: zoom/crop if charts are dense. Small secondary bumps still count
  as local maxima if the line genuinely reverses direction.

## Worked example
Sep [redacted] Bulletin, page 5: counted local maxima across all line plots on the
page = 18. CORRECT. (Multiple charts on the page; summed peaks across all of
their plotted series.)

## Pitfalls
- Do NOT count series endpoints as maxima/minima.
- Do NOT confuse "line plots" with bar charts on the same page — read the
  question's wording (it may restrict to line plots only).
- Render high-dpi; at low dpi adjacent peaks merge and you undercount.
- The answer is a plain integer — do not wrap in brackets or add a decimal.
