---
name: answer-format-exact-match
description: Use for ANY OfficeQA/Treasury-Bulletin question that prescribes an output format (square brackets, comma-separated, "without commas or words", rounded to N places) — graders do EXACT string matching, so apply before writing the final answer.
---

# Exact-match answer formatting

The grader compares your final answer string character-for-character. A correct number in the wrong format is scored WRONG. Verified failure: `[redacted]` was rejected; `[redacted]` was the accepted answer — the only difference was the space after the comma.

## Rules
- **Comma-separated values in brackets: NO spaces after commas.** Write `[redacted]`, never `[44.00, 231.52]`.
- Order the values exactly as the question asks (e.g. "slope and intercept" → slope first).
- Rounding: emit exactly the requested decimal places, keeping trailing zeros (`44.00`, not `44` or `44.0`).
- **Conflicting rounding clauses: the per-value rule WINS over a blanket sentence.** Multi-part questions often attach a specific precision to one value ("the YoY growth rate ... rounded to the nearest hundredths place") and then end with a blanket "All numbers should be rounded to the nearest thousandth place" — usually with the giveaway phrase "following their corresponding rounding rules". Apply each value's OWN stated precision; the bracketed answer is expected to mix precisions. Verified failure: `[redacted]` rejected where the accepted answer was `[redacted]` — the YoY value had to be hundredths even though the blanket sentence said thousandths.
- "Without commas or words" → bare integer, no thousands separators, no units, no `$`.
- No surrounding prose on the answer line if a bracketed/bare format is prescribed — the bracketed string should be reproducible verbatim.
- Negative values: plain leading minus (`-12.34`), not parentheses, even if the source table prints parentheses.

## Final check before answering
Re-read the question's format clause and mentally diff your answer string against it: brackets present? separator exactly `,`? decimal places exact? order correct?
