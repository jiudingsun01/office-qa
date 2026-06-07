# Digit-frequency / "leading digit" counting questions (Benford-style)

A NON-numeric-extraction category. The question does NOT ask for a value from a
cell; it asks you to COUNT digit occurrences across an entire table region.

Examples seen:
- "Excluding the row and column headers, in the tables on pdf page 41 (report page
  23) of the May 1980 edition ... how many times does the numeral '1' appear as the
  LEADING digit within the table datapoints?"  (gold 104)
- Variants ask: leading digit = D; or total occurrences of digit D anywhere; or
  count of datapoints whose first significant digit is D.

The answer is a bare integer COUNT, no brackets/units.

## What counts as a "datapoint" and a "leading digit"
- DATAPOINT = each numeric cell value in the table body, EXCLUDING the row labels
  (stub) and column headers (the "Excluding the row and column headers" clause is
  always there to tell you to skip those). Excludes page numbers, footnote markers.
- LEADING DIGIT = the first NON-ZERO significant digit of the value as PRINTED.
  - Thousands separators (commas) and the decimal point are NOT digits; ignore them
    when finding the first digit. "1,234" -> leading digit 1. "12.5" -> 1.
  - A leading zero / "0.xxx" -> the leading SIGNIFICANT digit is the first non-zero
    one. "0.45" -> leading 4. ".07" -> 7. (Benford convention: first significant.)
  - A bare "0" or "-" / "..." / blank dash cell has NO significant digit -> skip it.
  - Negative sign is not a digit: "-1.2" -> leading 1.
  - Treat each PRINTED number as one datapoint, including ones that repeat.

## METHOD — do NOT eyeball-count; extract text then count in code
Hand-counting 100+ cells across multiple sub-tables is the #1 error source. The
gold (e.g. 104) is large; a manual tally will drift by several.

1. Identify the exact PDF page. These Qs give BOTH "pdf page N" and "report page M".
   Use the PDF page number directly: pdftotext -f N -l N. (May 1980: pdf 41 = report
   page 23, an offset of 18 — typical for that era's Bulletin, but ALWAYS trust the
   explicit "pdf page" number the question gives.)

2. Extract the page text preserving layout:
       pdftotext -layout -f 41 -l 41 may1980.pdf /tmp/pg41.txt
   Inspect it. Identify the table body rows vs the header rows / stub labels so you
   can exclude headers per the question. If -layout merges columns badly, also try
   plain mode, or pdftoppm -r 300 + vision to confirm structure.

3. Count in Python with an explicit tokenizer. Pull every numeric token from the
   BODY lines only (drop header lines and the leftmost stub-label column), then for
   each token compute its first significant digit and tally:

       import re
       def lead_digit(tok):
           # strip commas, sign, leading zeros/decimal point
           s = tok.replace(',', '').lstrip('-+')
           for ch in s:
               if ch in '123456789':
                   return ch
               # ch in '0' or '.' -> keep scanning for first significant digit
           return None
       # tokens: match numbers incl thousands commas and decimals
       toks = re.findall(r'-?\d[\d,]*\.?\d*', body_text)
       from collections import Counter
       c = Counter(d for t in toks if (d:=lead_digit(t)))
       print(c)              # answer = c['1'] for leading-'1' questions

4. SANITY-CHECK the token set. Print len(toks) — does it match the visible cell
   count? Make sure you did not (a) include header/stub numbers, (b) split "1,234"
   into "1" and "234" (the regex above keeps it whole), (c) miss a sub-table. A
   Bulletin "page" often holds 2+ stacked exhibits — count ALL of them on that page.

## Pitfalls
- "Leading digit" != "contains the digit". Leading = first significant only.
- Commas/decimals are not digits and "1,234" is ONE datapoint with leading 1
  (do not let the regex break it into two numbers — this inflates the '1' count).
- Header/stub exclusion: years (1980), page numbers, column-unit notes ("In
  millions") are NOT datapoints. Read the table structure before tokenizing.
- If the question says "anywhere" / "total occurrences of '1'" instead of leading,
  count every '1' character across all body digits (different tally — re-read the
  phrasing). The May 1980 example was LEADING specifically.
- Answer is a plain integer (e.g. 104). No square brackets, no unit.
