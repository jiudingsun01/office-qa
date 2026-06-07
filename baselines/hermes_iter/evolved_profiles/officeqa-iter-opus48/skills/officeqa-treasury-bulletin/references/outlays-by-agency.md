# Federal Government Outlays by Agency (monthly) — exclude/include traps

Triggered by questions like: "Using the reported monthly outlay values for
individual federal agencies, calculate the total outlays in millions for
<MONTH YEAR> across all listed agencies EXCEPT <A>, <B>, <C>. Sum only the
agency-specific outlay entries and EXCLUDE all undistributed offsetting
receipts or other non-agency items."

## Where it lives
- Treasury Bulletin section "Federal Fiscal Operations" — a table of
  outlays broken out BY AGENCY/department (Legislative Branch, Judicial
  Branch, Agriculture, Commerce, Defense, Education, Energy, HHS, DHS, HUD,
  Interior, Justice, Labor, State, Transportation, Treasury, VA, Corps of
  Engineers, EPA, GSA, NASA, OPM, SBA, SSA (on/off-budget), International
  Assistance Programs, Other independent agencies, FEMA, etc.).
- Columns are typically: current month, prior period(s), fiscal-YTD. The
  question's month picks the COLUMN (e.g. "January 2003" = that calendar
  month column, NOT the fiscal-YTD total column).
- Units already in MILLIONS of dollars — no scaling needed when the question
  asks for millions. Do NOT divide by 1000.

## The critical trap: non-agency reconciliation lines
At/near the BOTTOM the table carries non-agency reconciliation rows that are
NOT agency outlays and MUST be excluded when the question says "sum only
agency-specific entries":
- "Undistributed offsetting receipts" — a LARGE NEGATIVE line (e.g. employer
  share of employee retirement, interest received by trust funds, rents/
  royalties on the OCS). Including it would substantially LOWER the sum.
- "Total outlays" / grand-total row — exclude (it's the sum, not a component).
- Any "Proprietary receipts", "Allowances", or footnote-only lines.

So the procedure is: sum ALL named agency/department rows, then SUBTRACT
(i.e. omit) the three agencies the question names for exclusion, and OMIT
the offsetting-receipts and total rows entirely. Result = a positive
agency-only subtotal.

## Procedure
1. Locate the by-agency outlays table; identify the column for the asked month.
2. List every agency row's value in that column (watch for parentheses =
   negative for individual agencies too, though most are positive outlays).
3. Sum all agency rows. Exclude any agencies the question names.
4. Do NOT include: undistributed offsetting receipts, Total outlays row,
   or any non-agency reconciliation line.
5. Report in millions as an integer (unless the question asks otherwise).

## Sub-table: OCS rents & royalties column (single-cell lookup, NOT a sum)
Question form: "According to the definition of OCS within 43 U.S. Code § 1331,
what was the lowest/highest amount of recorded rents and royalties attributed
to OCS ... in millions ... in calendar year YYYY? Report as absolute value."
- This is FFO-3 "On-Budget and Off-Budget Outlays by Agency" (continued page,
  ~page 22). The continued page has the "Undistributed offsetting receipts"
  group; the OCS column is "Rents and royalties on the Outer Continental Shelf
  lands" (e.g. col (33) in the 2016/2017 layout) — between "Interest received
  by trust funds" (32) and "Other" (34).
- NOT IN THE MARKDOWN PARSE — grep finds nothing. Use
  `pdftotext -layout -f 22 -l 24 <pdf> -` and read the column by position.
- CALENDAR-YEAR spans TWO bulletins: the December bulletin lists Jan–Aug of
  that year; the following-year June bulletin lists Sept–Dec. Collect all 12
  monthly cells (values are tiny, often negative, ~ -400..+60).
- "Lowest absolute value" = min(|cell|) across all 12 months. A small POSITIVE
  month (e.g. Jan +56) can beat the smallest-magnitude negative (e.g. Oct -61).
  Don't just pick the largest-looking negative. Report the absolute value.
- Verified CY2016 col(33): Jan 56, Feb -353, Mar -152, Apr -100, May -347,
  Jun -339, Jul -97, Aug -413, Sep -338, Oct -61, Nov -297, Dec -94
  -> lowest |value| = 56 (Jan).

## Multi-part bracket answer: PER-VALUE rounding rule OVERRIDES the blanket rule
Question form: "...average YoY growth rate ... rounded to the nearest HUNDREDTHS
place. Additionally, run OLS of ln(outlays) on FY index, return slope and
intercept. ... 3 comma-separated values ... ALL numbers rounded to the nearest
THOUSANDTHS place."
- This is a CONFLICT: the YoY value got a specific "hundredths" instruction
  early, but the closing sentence says "all numbers ... thousandths."
- RULE: the value-SPECIFIC rounding instruction WINS for that value. Round the
  YoY to hundredths (2 dp), round slope+intercept to thousandths (3 dp).
- WORKED FAIL: I returned [2.806,0.030,8.706]; gold [2.81,0.030,8.706]. Digits
  100% correct; only the YoY rounding place was wrong (used blanket 3dp instead
  of the YoY's own 2dp). Slope/intercept (no per-value rule) correctly used 3dp.
- Delimiter: every value has a decimal point -> MODE A (bare comma, NO space).
- Judicial Branch total = on-budget + off-budget outlays, FY column, FFO by-agency
  table. FY2007-2013 inclusive = 7 years -> 6 YoY ratios -> average them.

## OLD-STYLE 1940s-1950s "Budget expenditures by organization unit" table
Question form: "What was the amount spent in millions of nominal dollars by the
HIGHEST SPENDING U.S. Federal Department in the fiscal year of YYYY?" (or lowest,
or a named department). These pre-1970 bulletins use a DIFFERENT table than the
modern FFO-3 by-agency table — old department names, NOT DHS/HHS/NASA.

- Table title is roughly "Budget Receipts and Expenditures" / "Expenditures by
  organization unit (department or major agency)" in the Federal Fiscal
  Operations section. Rows are old departments: Legislative, Judiciary,
  Executive Office, Funds appropriated to the President, Agriculture, Commerce,
  Defense, Health Education & Welfare, Interior, Justice, Labor, Post Office,
  State, Treasury, Atomic Energy Commission, Veterans Administration, etc.
- Units already in MILLIONS — report the cell as-is, no scaling.
- Column = the asked fiscal year (these tables often show several FYs side by
  side, or you pick the right bulletin's FY column). Use the FY column, NOT a
  monthly column, when the Q says "in the fiscal year of YYYY".

### THE TRAP that cost FY1955 (answered 35532, gold 36080, ~548M short):
DEFENSE in 1950s tables is SPLIT into sub-rows:
  - "Department of Defense — Military functions"
  - "Department of Defense — Civil functions" (Corps of Engineers, Panama Canal,
    cemeterial, etc.), sometimes a separate "Mutual security / military
    assistance" piece.
The DEPARTMENT total = MILITARY functions + CIVIL functions (+ any "Office of
Secretary of Defense" subtotal line shown). I grabbed ONLY the Military
functions sub-row (~35532) and missed the Civil-functions add-on (~548M) that
brings the full Department of Defense to ~36080.
RULE: when a Q asks the spending of a DEPARTMENT (not a named sub-bureau), and
the department is broken into sub-rows, SUM all of that department's sub-rows
(or read the department's own subtotal/heading line if the table prints one).
Defense is ALWAYS the highest-spending department in 1950s-1960s peacetime FYs;
the contest is only "did you total Defense correctly," not "which department."

### Procedure for "highest spending department FY YYYY"
1. Open the bulletin covering FY YYYY's final data (the by-organization-unit
   expenditure table). pdftotext -layout the FFO pages; the table can be wide.
2. Defense is the answer department >99% of the time for 1950s-60s. Find its
   block and SUM Military functions + Civil functions (+ subtotal sub-lines).
3. Cross-check it really is the max vs Treasury (interest on debt sometimes
   lives elsewhere) and Veterans Administration.
4. Report the SUMMED department total in millions, integer. Delimiter MODE B
   (plain integer, no brackets needed unless multi-part).

## Sanity check
- If your sum is implausibly small or comes out near a round "total" figure,
  you likely either included the negative offsetting-receipts line or grabbed
  the Total row. Agency-only subtotals for a single month in the 2000s are
  typically ~150k–200k million. (Verified: Jan 2003, all agencies minus
  Commerce, FEMA, Interior, excluding offsetting receipts = 180681 million.)
- For OLD-style department-expenditure Qs: if your Defense figure is a few
  hundred million short of a round number, you probably took ONLY Military
  functions and dropped Civil functions. Add the Civil-functions sub-row.
