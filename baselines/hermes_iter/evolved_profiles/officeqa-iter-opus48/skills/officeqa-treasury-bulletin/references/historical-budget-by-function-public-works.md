# Historical budget-by-function tables: "public works" & WWII-era revised columns

Treasury Bulletin (and the historical-tables supplement it reproduces) carries
long-run "Budget receipts and outlays by FUNCTION / major class" tables spanning
the 1930s–1940s. These are the source for questions like:

  "absolute difference in spending on PUBLIC WORKS between 1934 and 1946.
   Use revised WWII-era figures that should account for PWA spending and
   housing and exclude certain wartime spending efforts."  -> gold 142.

## The qualifier phrasing PICKS THE COLUMN (do not ignore it)
These historical functional tables print SEVERAL variant series for the same
function across different vintages/footnotes. The narrative qualifier is not
decoration — it tells you which exact column/footnote-row to read:

- "REVISED WWII-era figures" -> use the column flagged revised / (r), NOT the
  original contemporaneous figure. WWII-era functional outlays were re-stated
  post-war; revised and original differ materially.
- "account for PWA spending and HOUSING" -> the broader "public works" series
  that FOLDS IN Public Works Administration + housing programs (not the narrow
  general-public-works line).
- "EXCLUDE certain wartime spending efforts" -> use the peacetime/public-works
  variant that strips war-construction; do NOT grab a war-activities aggregate.

So the right cell is: the REVISED, PWA+housing-inclusive, war-EXCLUSIVE
"public works" outlay for each year. 1934 vs 1946 revised public-works outlays
differ by 142 (millions, nominal).

## Why this matters (failure family)
This is the SAME trap as the defense-spending phrasing fails (see memory +
calendar-year-from-monthly ref): a single function name maps to multiple
columns, and the qualifier opposite-selects which one. Grabbing the headline /
contemporaneous / narrow line gives a plausible-but-wrong number. Always map
EACH qualifier clause ("revised", "include X", "exclude Y") to a column/footnote
choice before reading the cell.

## Mechanics
- Units: these historical functional tables are in MILLIONS of nominal dollars.
  "in millions of nominal dollars" in the prompt = no scaling, report the raw
  millions difference. Do NOT scale to billions here (unlike the modern
  balance-sheet questions).
- "absolute difference between YEAR_A and YEAR_B" = |outlay_A - outlay_B|,
  sign-stripped.
- Locate the table by searching the PDF text layer for "Public works" /
  "Public Works Administration"; if the grid garbles, pdftoppm 300dpi + vision
  the function-outlay page.
