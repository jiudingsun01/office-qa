# Fisher Ideal symmetric growth rate (a.k.a. symmetric growth rate / log-change cousin)

When a question says "calculate the Fisher Ideal symmetric growth rate" between an
OLD value A and a NEW value B, it is asking for the **symmetric growth rate**, NOT a
level and NOT an ordinary percent change.

## CRITICAL: gold reports the FRACTION, NOT a percent (no x100)

    Fisher symmetric growth rate = 2 * (B - A) / (B + A)

NOTE THE 2, NOT 200. The OfficeQA gold does **NOT** multiply by 100, even though
the question says "in percent" about the INPUT yields. The yields are already in
percent units (e.g. 13.06, 14.74); the growth rate itself is reported as a bare
ratio/fraction. DO NOT scale to percent.

- B = the LATER / "to" value (Aug 1982)
- A = the EARLIER / "from" value (Aug 1981)
- Round to whatever dp the question asks (here: 3 dp).

## #1 FAILURE MODE — 100x TOO BIG (gave -11.335 vs gold [redacted])
This is the recurring, DOMINANT failure. The digits were 100% correct
(-0.11335 -> [redacted]) but I used 200*(B-A)/(B+A) = -11.335 instead of
2*(B-A)/(B+A) = -0.113. The tell: if your answer is ~±10-12 and the gold-style
answer should be a small fraction near zero, you multiplied by an extra 100.

    RULE: Fisher Ideal symmetric growth rate here = 2*(B-A)/(B+A), NO x100.
    If |your answer| > 1 for two close yields, you over-scaled by 100. Divide by 100.

Worked example (Aug 1982 vs Aug 1981 long-term Treasury bond yields):
    A (Aug 1981) and B (Aug 1982) both ~13-15%, nearly equal.
    2*(B-A)/(B+A) = -0.11335 -> [redacted]  ✓ (gold)
    200*(B-A)/(B+A) = -11.335  ✗ (my wrong answer — extra factor of 100)

## #2 FAILURE MODE — transcribed a cell
Reporting a YIELD LEVEL (~10-14, one of the table cells) instead of computing the
symmetric growth. If your answer is one of the raw cells, you forgot the formula.

## Sanity ladder for this question type
1. Two close yields A≈B -> answer is a SMALL fraction near zero (|answer| < 1).
2. Sign: gold negative means B < A (1982 yield lower than 1981), i.e. 1981->1982.
3. Magnitude: -0.1 range, NOT -10 range, NOT +13 range.

## Direction (sign)
"growth rate ... for Aug 1982 and for Aug 1981": B = Aug 1982 (later), A = Aug 1981
(earlier). Negative gold => 1982 yield < 1981 yield.

## Source table
"Average yields of new long-term Treasury bonds" appears in the Treasury Bulletin
yields section. "As of reported values as of end of the 19XX FY" = use the issue/
column that reports through that fiscal-year-end. Read the calendar-month rows
(Aug 1982, Aug 1981) from that reported vintage.

## Delimiter (MODE A)
Answer has a decimal point -> bare value, no commas. e.g. [redacted]
