---
name: officeqa-ownership-survey-2source-stepfunction-monthcount
description: >-
  OfficeQA Treasury Bulletin — questions that say "using ONLY exactly 2 (or N) sources of
  recorded Treasury ownership surveys, 1 recorded end of month MMM YYYY and 1 recorded end of
  month MMM YYYY+1, how many calendar months from [month after first] to [a later month]
  inclusive had [a series value] exceeding $X". The survey is sampled at only N dates but the
  answer counts MONTHS over a long range, so each survey value is HELD CONSTANT (forward-filled
  step function) over its 12-month block. Answer equals the months in each block times whether
  that block clears the threshold, summed. So with N surveys the answer is a multiple of 12.
  PASSED interpretation 12 means exactly one of two 12-month blocks above 20000 million.
---

# OfficeQA — 2-Source Ownership Survey, Step-Function Month Count

## When this applies
The question has ALL of these features:
- "Using only exactly 2 sources of recorded treasury ownership surveys ..." (or N sources).
- It pins specific survey dates: "1 recorded on the end of month January 1977 and 1 recorded on the end of month January 1978" → these are the ONLY observed data points.
- It then asks a MONTH-COUNT over a span longer than the number of sources:
  "how many calendar months from February 1977 to January 1979 inclusive had a total nominal outstanding of interest-bearing marketable U.S. Treasury bills exceeding $20000 million in par values?"

The mismatch is the whole point: 2 data points, but a 24-month answer window.

## The core trick: forward-fill each survey over its block (step function)
Do NOT interpolate. Do NOT count only the 2 survey months. Each survey value is treated
as the constant value for the 12 months it "owns":
- Survey at end of Jan 1977 governs the block **Feb 1977 → Jan 1978** (12 months).
- Survey at end of Jan 1978 governs the block **Feb 1978 → Jan 1979** (12 months).
(General: a survey dated end-of-MMM governs the 12 months from MMM+1 of that year through MMM
of the next year. The window in the question is exactly N×12 months = N blocks.)

Then:
1. For each block, read the single survey value of the named series (here: total of the
   "Treasury bills" column under interest-bearing MARKETABLE in the Survey of Ownership /
   Ownership of Treasury Securities table, in $ millions, par value).
2. Test value > threshold (strict "exceeding").
3. If a block clears the threshold, it contributes ALL 12 of its months to the count; if not,
   it contributes 0.
4. Sum across blocks.

So with 2 surveys the answer is almost always one of {0, 12, 24}. Gold = 12 ⇒ exactly one of the
two survey values exceeded $20,000M.

## Why a naive answer (e.g. 7) is wrong
Counting individual issue lines, interpolating between the two dates, or mixing in other
security types (notes/bonds/certificates) produces a non-multiple-of-12 number. If the question
gives N survey sources and an N×12-month inclusive window, the answer MUST be a multiple of 12
(a whole number of full blocks). Any answer that is not k×12 means you mis-modeled it.

## Pitfalls
- Isolate the series: "interest-bearing marketable U.S. Treasury bills" = the BILLS column only,
  marketable + interest-bearing, NOT total marketable, NOT bills+notes.
- "Inclusive" + "from the month AFTER the first survey": Feb1977→Jan1979 is exactly 24 months =
  2 full blocks. Verify the window length equals N×12 before assuming clean blocks.
- Strict "exceeding"/"more than" — a value exactly == threshold does not count.
- Units are $ millions, par value. "$20000 million" is the literal cell value 20000.
- The survey-date preamble looks like a distractor but here it is load-bearing: it tells you the
  SAMPLING dates that define the blocks. Use them to build the step function, not to restrict the
  count to 2 months.

## Output
Plain integer (a multiple of 12 for N full blocks). PASSED gold: 12.
