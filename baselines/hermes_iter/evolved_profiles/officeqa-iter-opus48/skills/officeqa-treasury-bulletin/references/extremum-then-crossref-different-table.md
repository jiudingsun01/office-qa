# Two-stage: find argmin/argmax MONTH-YEAR of a derived series, then read a DIFFERENT table at that date

## The task shape
A single question chains TWO independent lookups across TWO different tables:
1. STAGE 1 (locate the date): "Between 1960-1969, find the month+year where the
   yield SPREAD between corporate Aa bonds and Treasury bonds reached its MINIMUM,
   per the June 1970 bulletin." -> the answer to stage 1 is a (month, year), and it
   is NOT itself reported in the doc; you must COMPUTE the derived series
   (spread = col_A - col_B) month by month and take argmin/argmax.
2. STAGE 2 (read the payload): "In that month+year, what were the railroad
   retirement account trust RECEIPTS?" -> go to a COMPLETELY DIFFERENT table
   (trust-fund receipts/expenditures), find that exact month row, read the cell.

The final answer is the STAGE-2 number, not the date. The date is just an index.

## Procedure
1. Stage 1 series: the interest-rate / bond-yield table (often "Yields of Treasury
   securities" + a "corporate bond" comparison, or in the back statistical section).
   Pull BOTH columns for every month in the window. Compute spread = corporate - tsy
   for each month. Build the full list; argmin/argmax over it. Do NOT eyeball — many
   spreads cluster; carry the actual subtraction per month.
2. "As published in the <Month Year> bulletin" pins WHICH bulletin issue to open —
   that issue's tables contain the historical window, so use that PDF, not a later one.
3. Stage 2 lookup: railroad retirement / trust-fund RECEIPTS live in the
   trust-fund accounts table (receipts and expenditures of trust accounts).
   Match the SAME calendar month+year row found in stage 1.

## Units / format gotchas
- Older bulletins (1960s-70s) report many trust-fund and account figures in WHOLE
  NOMINAL DOLLARS, already exact (e.g. railroad retirement receipts = [redacted] =
  $92 million written out fully). The Q here said "nominal dollars ... full number
  without commas" -> output the raw integer [redacted], NO scaling, NO rounding.
- Do NOT assume "millions" scaling. Check the column header: if the cell literally
  reads a full-dollar figure, copy it verbatim (strip commas only).
- "without commas or words" = bare integer, single value (not bracketed list when
  the question asks for one final number).

## Takeaway
When a question's first clause computes an extremum of a DERIVED quantity to pick a
date, treat it purely as an index step: compute the spread/derived series properly,
take argmin/argmax, then pivot to the SECOND table for the actual answer. The two
tables are unrelated; the only shared key is the calendar month+year.
