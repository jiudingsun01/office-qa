---
name: numeric-answer-format
description: Use whenever the final answer to an OfficeQA / Treasury-Bulletin question is numeric — grading is exact string match, so the answer line must be a bare number (no separators, units, labels, or annotations) unless the question prescribes a wrapper format.
---

# Format numeric final answers for exact-match grading

The grader compares your final answer string against the gold answer literally. A correct value in the wrong format is scored WRONG (observed: answered `[redacted] (net inflow)`, gold was `[redacted]`, verdict WRONG).

## Rules for the final answer line

1. **No thousands separators.** Write `[redacted]`, not `1,461`.
2. **No parenthetical annotations or labels.** Do not append `(net inflow)`, `(thousands of dollars)`, units, or direction words. If the question asks "inflow or outflow", the gold answer is typically just the magnitude — give the bare number.
3. **No currency symbols or sign decoration** unless the value is genuinely negative in the source table (then a plain leading `-` is fine).
4. **Keep the value in the units the question asks for** (e.g. "in thousands of dollars" → report the table figure as-is if the table is already in thousands; do not convert to full dollars).
5. **Bare number only on the answer line.** Put any explanation (direction, table, computation) in surrounding prose, never inside the answer string itself.

## Multi-part answers

Some questions ask several sub-questions and dictate a container format, e.g. "enclosed in square brackets with comma-separated values in the order of the sub-questions presented." Follow that literally: `[5.123, 7.890]` — values in the asked order, each formatted per the rules above, rounded to exactly the requested precision (keep trailing zeros if the rounding demands them, e.g. `7.890` for thousandths).

## Quick self-check before submitting

- Does the answer string contain only digits, an optional leading `-`, and an optional decimal point? If not, strip everything else — unless the question explicitly prescribed a wrapper format (brackets, comma-separated parts), in which case match that wrapper exactly.
