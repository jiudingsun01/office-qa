---
name: answer-format
description: Use when writing the final answer line for any OfficeQA / Treasury-Bulletin question, especially when the requested unit (billions, nominal dollars) differs from the table's printed unit. The grader is strict exact-match on the answer string — formatting or unit-scaling errors alone make a correct value WRONG.
---

# Final answer formatting (strict exact-match grader)

A numerically correct answer was graded WRONG because it was written as
`1,461 (net inflow)` when the expected string was `[redacted]`.

Rules for the final answer:

1. **Output the bare number only.** No thousands separators (`[redacted]`, not `1,461`),
   no currency symbols, no units (the question already fixes the unit, e.g.
   "in thousands of dollars" — do not append "thousand" or "$").
2. **No parenthetical qualifiers or direction labels.** Do not add
   "(net inflow)", "(outflow)", "(approx.)", etc. If the question asks
   "inflow or outflow", the sign/magnitude alone is the expected answer
   unless the question explicitly asks you to state the direction in words.
3. **Match the question's implied precision.** If the source table gives the
   value at the precision asked for, report it verbatim from the table —
   do not round, rescale, or reformat.
4. **Negative values:** use a leading minus sign (`-123`), not parentheses
   (`(123)`), even though Treasury Bulletin tables print negatives in
   parentheses or italics.
5. Put explanation/working in the body of the response if useful, but the
   line presented as the answer must be the clean value alone.
6. **Multi-part questions:** if the question says "enclosed in square
   brackets with comma-separated values in the order of the sub-questions",
   output exactly that — e.g. `[redacted]` — values in sub-question
   order, each formatted to the requested unit/precision, nothing else
   on the line.

## Unit rescaling (table unit ≠ answer unit) — recurring pitfall

- Most Treasury Bulletin tables print values **in millions of dollars** —
  check the table header; some tables use thousands.
- Question asks billions, table prints millions: divide by 1,000.
  Table prints thousands: divide by 1,000,000.
- Question asks for the value "in nominal dollars" / "the full number" and
  the table prints millions: **multiply by 1,000,000**
  (e.g. a printed "92" → answer `[redacted]`, no commas).
- Do all arithmetic (differences, sums, ratios) on raw table values first;
  rescale and round ONLY at the final step, to exactly the precision asked
  ("nearest thousandth" = 3 decimals, keep trailing zeros if needed).
  Never subtract two already-rounded numbers — unless the question
  explicitly says to round the inputs first.
