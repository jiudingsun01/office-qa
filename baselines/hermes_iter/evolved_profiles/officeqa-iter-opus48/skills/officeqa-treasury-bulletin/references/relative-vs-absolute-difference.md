# "RELATIVE difference" vs "ABSOLUTE difference" — DO NOT confuse them

## PRE-SUBMIT GATE (knowledge existed but was NOT applied — failed AGAIN)
Before emitting ANY answer, grep the question text for the word "relative"
(also "percent difference", "percentage difference", "percent change", "how
much larger/smaller"). If present and you are about to submit a plain
subtraction A-B, STOP: you owe (A-B)/base*100, which is ~1/base times larger.
Sanity flag: if your absolute pp gap is single-digit (e.g. 3.85) and the
quantities involved are ~20-30%, the relative answer will be ~10-20 — they are
NOT close, so a single-digit answer to a "relative" question is almost always
the un-normalized absolute gap. This exact question (1980/81 savings-note
redemption rate) was failed once with the reference already written; the miss
was forgetting to LOAD/APPLY this rule, not a math gap.

## The trap (recurring fail)
OfficeQA freely mixes two near-identical phrasings that mean DIFFERENT math:

- "ABSOLUTE difference [in percentage points]" of two rates A, B
  => answer = |A - B|   (just subtract; if rates, ×100 for pp)

- "RELATIVE difference [in percentage points]" of two rates A, B
  => answer = |A - B| / B * 100   (difference normalized by a BASE, then ×100)
  The "in percentage points" / "rounded to hundredth" wording does NOT
  downgrade it to a plain subtraction — "RELATIVE" is the operative word.

If you report the absolute difference when the question said RELATIVE, your
digits look plausible but you're off by a factor of ~1/base. Concrete fail:
saving-note "redemption rate out of average amount outstanding" for 1980 vs
1981. I reported |r1980 - r1981| = 3.85 (absolute pp gap). Gold = 17.69 =
relative difference = |r1980 - r1981| / r_base * 100. (Here base ≈ 21.8%, so
3.85/21.8 ≈ 0.1769.) Factor ~4.6x off, all digits otherwise fine.

## Decision rule
Scan the question for the literal word:
- "relative difference" / "relative change" / "percent difference between" /
  "percentage difference" / "how much larger/smaller ... than" => NORMALIZE.
  answer = |A - B| / base * 100.
- "absolute difference" / "difference in percentage points" with NO
  "relative"/"percent" qualifier => plain |A - B|.

## Which value is the BASE for relative difference?
BASE = the EARLIER / FIRST-listed period (the chronological starting point).
For "X for the 1980 and 1981 calendar years" => base = 1980 (the earlier year).
CONFIRMED by the gold: 1980/1981 case, |r1980 - r1981| = 3.85, base r1980 ≈ 21.8,
3.85 / 21.8 * 100 = 17.69 = gold. So the SMALLER/earlier-year rate was the
denominator. Rule: divide by the rate of the year you are measuring change FROM
(the earlier year), exactly like a percent-change. Only fall back to "try both
years as denominator" if the earlier-year base does NOT land on a clean value
matching the requested rounding.

## "rate out of the average amount outstanding"
For savings-securities tables (Savings Bonds / Savings Notes section of the
Bulletin): the "redemption rate out of average amount outstanding" for a
calendar year = (year's total redemptions) / (average amount outstanding for
that year) * 100. Average outstanding ≈ (begin-of-year + end-of-year)/2 unless
the table prints an explicit annual-average column. Compute this rate for EACH
year FIRST, then apply the relative-difference formula above.
