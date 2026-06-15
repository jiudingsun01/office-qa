# Summing all 12 monthly cells from a Treasury Bulletin expenditure/receipt table

TRIGGER: Q says "sum of the reported values for all individual calendar months
in <YEAR>" for some expenditure/receipt line (e.g. "national defense and
associated activities", "interest on the public debt", a given agency). You must
read 12 monthly cells from ONE row of a "Budget Receipts and Outlays by Month"
(or similar monthly-detail) table and add them.

## The dominant failure: single-cell transcription error
On a 12-cell sum, getting the answer off by a smallish amount (exactly 100, 70,
50, a clean digit-place amount) almost always means ONE month's cell was misread
— NOT an arithmetic mistake across all 12. This OCR-heavy 1950s table flips
digits constantly (4↔It, 7↔1, 8↔3, 0 dropped).

Real fails on THIS SAME question (1953 national defense, gold = [redacted]):
  - Attempt A summed to 44,363 (off 100).
  - Attempt B summed to 44,393 (off 70).
Both were single-cell OCR misreads. The protocol existed but the agent never
actually pulled clean per-month values from BOTH source bulletins and never
cross-checked. Don't repeat that — use the confirmed table below.

## ★ CONFIRMED GROUND TRUTH: 1953 national defense monthly TOTAL column (millions)
This recurs. The answer column is the LEFTMOST number column of
"Table 3.- Expenditures for National Defense and Related Activities" (the
all-in total per month, NOT the Air Force/Army/Navy sub-columns).

  Jan 3632, Feb 3501, Mar 3789, Apr 3891, May 3746, Jun 4056,
  Jul 3890, Aug 3519, Sep 3787, Oct 3647, Nov 3540, Dec 3465
  → 12-month CALENDAR sum = [redacted]  (THE ANSWER)

SOURCE MAPPING (data lives across TWO bulletins — neither has all 12 months):
  - Jan–Jun 1953: treasury_bulletin_1953_10.pdf, Table 3 (months listed
    Jan..Jun then Jul/Aug). Note OCR: Jun renders as "It, 056" = 4,056.
  - Jul–Dec 1953: treasury_bulletin_1954_03.pdf, Table 3 (fiscal-YTD format,
    rows "1953 -July" through "December").
  In-doc control: Table 3's "1953" row = 44,584 = FISCAL year (Jul'52–Jun'53),
  NOT the calendar sum — use only as a magnitude/ballpark check (within ~120).

WHY: -layout pdftotext can shear a column so a hundreds digit reads from the wrong
visual row, or a faint scanned digit (4 vs 3, 8 vs 3, 9 vs 4) flips. The total of
the misread = a clean offset because only the hundreds (or thousands) place moved.

## Verification protocol (DO THIS before answering any 12-cell sum)
1. Extract all 12 monthly cells into an explicit list, labeled Jan..Dec. Write
   them out — do not sum in your head from the raw text.
2. SANITY-CHECK against an in-document control total. Monthly-detail tables
   almost always carry a fiscal-year or calendar-year total column/row, OR the
   annual figure appears in a companion summary table elsewhere in the bulletin.
   - If a CALENDAR-year total exists, your 12-month sum must match it. If it
     doesn't, the difference (e.g. 100) tells you exactly how much one cell is off
     — go find which month is wrong.
   - If only a FISCAL-year total exists (Jul prior yr – Jun this yr), it won't
     equal the calendar sum, but it's still a magnitude check: your sum should be
     in the same ballpark.
3. Re-read each cell a SECOND time directly from the layout text, comparing digit
   counts. A value like "3,453" vs "3,553" differs only in one digit — these are
   the cells that flip. Pay special attention to the hundreds and thousands digit.
4. Re-add with a script (sum the explicit list), don't trust mental arithmetic.

## Parsing tips for monthly-detail outlay tables
- DATA SPLIT ACROSS TWO BULLETINS (1950s "Table 3" national-defense layout): a
  single bulletin's Table 3 lists months in FISCAL-year order (Jul→Jun) plus a
  few recent calendar months, so NO single bulletin shows all 12 calendar months
  of a year. To cover Jan–Dec YYYY you need an Oct-YYYY bulletin (gives Jan–~Aug)
  AND a ~Mar-(YYYY+1) bulletin (gives Jul–Dec). Pull both, take the cleaner copy
  of each month, and reconcile any month that appears in both.
- COLUMN TRAP: Table 3 has many columns (Office of Sec Def TOTAL, Air Force,
  Army, Navy, Armed Forces Leave, surplus disposal, strategic materials, Other).
  The question's "national defense and associated activities" = the LEFTMOST
  per-month TOTAL column, NOT a service sub-column. Don't accidentally grab the
  Army or Navy column.
- These tables are wide (12 month columns + total). -layout mode often misaligns
  the rightmost/total column or shears one value up/down a row. If columns look
  sheared, also try `pdftotext -nopgbrk` raw mode and cross-check the suspect cell.
- The "national defense" / function rows in early-1950s bulletins are in the
  Budget Receipts/Outlays detail (functional classification). Values are already
  in MILLIONS of dollars — no further scaling for a "millions of nominal dollars"
  answer; just sum and report the integer.
- Answer is a bare integer in millions (no decimal). Per memory MODE B: plain
  number, and if the answer is a single value, no brackets/delimiter issues arise.

## Checklist
[ ] All 12 cells listed and labeled by month?
[ ] Cross-checked sum against an in-doc calendar-year (or fiscal-year ballpark) total?
[ ] If off by a clean round number, hunted down the ONE misread cell?
[ ] Re-added via script, not mentally?
