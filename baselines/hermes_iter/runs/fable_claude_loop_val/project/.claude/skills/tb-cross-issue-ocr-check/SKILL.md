---
name: tb-cross-issue-ocr-check
description: Use whenever an answer hinges on a few specific table datapoints pulled from parsed/OCR bulletin text — above all when a small-magnitude value sits in a denominator (ratios, elasticities, percent changes). Cross-validate each load-bearing value against the same row reprinted in 2-4 consecutive issues before computing.
---

# Cross-issue OCR validation of Treasury Bulletin datapoints

The parsed bulletin text files contain occasional single-digit OCR errors
(e.g. one issue printed a March 1960 value as `20174` when the true figure
was `20774`). A single corrupted digit in a denominator turned a correct
arc-elasticity procedure into a WRONG answer (-3.147 instead of -3.524).

## Key fact that makes validation cheap
Each monthly figure is reprinted in **many consecutive bulletin issues**:
the row for month M appears in the issue ~2–3 months after M and keeps
appearing (in the same table) for roughly the next 6–12 monthly issues.
So every monthly datapoint has 4+ independent OCR'd copies available in
`treasury_bulletins_parsed/transformed/treasury_bulletin_YYYY_MM.txt`.

## Procedure
1. Identify which raw values are **load-bearing**: anything in a ratio,
   elasticity, or percent change — above all small (4–6 digit) values in a
   denominator, where one wrong digit shifts the result by 3–10%.
2. For each load-bearing value, grep the SAME table row in **2–4 other
   issues** (the next few monthly bulletins after the one you first used).
   Locate the table by a distinctive header phrase, e.g.
   `grep -n "Total collections reported by Internal Revenue" <file>`,
   then pull the month's row from the lines that follow.
3. **Take the majority value.** One issue disagreeing with three others is
   an OCR error in that issue, even if it is the issue the question seems
   to point at. (Genuine data revisions across issues exist but are rare
   for these tables and usually change more than one digit.)
4. If copies are split or unavailable, sanity-check against neighboring
   months of the same series — a value breaking the local pattern by an
   odd internal digit (not order of magnitude) is suspect.

Verified example: unemployment-insurance collections for Mar [redacted] printed
as `20174` in one issue but `20774` in three later issues — the majority
value 20774 was correct, and using the corrupted copy in a denominator
shifted an arc-elasticity answer from [redacted] (right) to −3.147 (wrong).
(Arc-elasticity and other formulas live in tb-chained-arithmetic-and-fx.)
