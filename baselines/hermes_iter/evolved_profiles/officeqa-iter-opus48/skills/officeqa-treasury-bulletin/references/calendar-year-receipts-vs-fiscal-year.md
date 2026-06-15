# Calendar-year vs fiscal-year receipts/outlays + "national defense" function line

## Trigger
Question asks for "**calendar year(s)**" totals of budget receipts / outlays, OR
ratios involving a named **budget function** ("national defense", "international
affairs", etc.) over a span of years. Classic phrasing: "ratio of total net
budget receipts to total national defense budget expenditures for each of the
**calendar years** 1941-1943."

## The trap (this is what cost a wrong answer)
The Treasury Bulletin headline summary tables ("Summary of Fiscal Operations",
"Budget Receipts and Outlays") are organized by **FISCAL YEAR** (Jul 1 - Jun 30)
by default. If you grab the row labeled "1942" from a fiscal-year table you get
FY1942 = Jul-1941..Jun-1942, which is NOT calendar 1942. Mixing fiscal-year
figures into a "calendar year" question produces a systematically wrong ratio.
A worked fail: answer 0.4802 vs gold [redacted] (ratio of mine/gold = 0.70), i.e.
wrong year-aggregation, digits not random — the hallmark of fiscal-vs-calendar
or wrong-12-months aggregation.

## How to get a CALENDAR-year total correctly
Calendar-year = sum of the 12 MONTHLY values Jan..Dec of that year. The Bulletin
publishes monthly receipts & outlays; for a calendar-year aggregate you must
either:
  (a) find a table that explicitly carries a **"Calendar year"** column/section
      (some Bulletin summary tables print BOTH "Fiscal year" and "Calendar year"
      blocks — read the CALENDAR-year block), or
  (b) sum the 12 monthly cells Jan-1941..Dec-1941, etc., yourself.
Do NOT use the fiscal-year row as a shortcut.

## "National defense" expenditures
"National defense" is a **budget FUNCTION line** in the outlays-by-function
breakdown, NOT a single agency. In 1940s Bulletins it appears as a major outlay
category line ("National defense" / "War activities"/"War Department + Navy"
depending on year — for 1941-1943 the WWII buildup means this line balloons).
- Confirm you are reading the function/category line, not a department total.
- Match the SAME period basis (calendar year) as the receipts numerator.

## Procedure
1. Confirm period basis: the word "calendar" => calendar year, sum Jan-Dec.
2. Numerator = total net budget receipts for that calendar year.
3. Denominator = total national-defense outlays for the SAME calendar year.
4. ratio_year = receipts / defense_outlays; compute for 1941, 1942, 1943.
5. Answer = mean of the three ratios, round to 4 dp.
   NOTE: "mean of the ratios" = arithmetic mean of per-year ratios
   = (r1941 + r1942 + r1943)/3. Do NOT compute (sum receipts)/(sum defense).
6. Delimiter: single decimal value, plain number.

## Sanity check
Receipts/defense in wartime 1941-43 should fall ~0.5-1.0 and DECLINE as defense
spending explodes faster than receipts (1941 highest, 1943 lowest). Gold mean
[redacted] is consistent. If your mean lands near ~0.48 you likely used fiscal-year
rows or summed the wrong 12 months.
