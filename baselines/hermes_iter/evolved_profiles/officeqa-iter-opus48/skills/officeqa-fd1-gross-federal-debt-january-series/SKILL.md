---
name: officeqa-fd1-gross-federal-debt-january-series
description: OfficeQA Treasury Bulletin — extract a multi-year series of TOTAL GROSS U.S. federal debt (incl. agency securities like FHA) from Table FD-1 "Summary of Federal Debt", e.g. "list gross federal debt at end of fiscal month January from YYYY to YYYY".
category: research
---

# OfficeQA: FD-1 Gross Federal Debt — multi-year January (or any-month) series

## Trigger
Question asks for "total gross U.S. federal debt at end of fiscal month <MONTH> from YEAR1 to YEAR2", "should include securities issued by federal agencies (FHA, etc.)", "as a comma-separated list". Only ONE source doc may be provided but the answer spans many years.

## The right table & column
- Table **FD-1 "Summary of Federal Debt"** (In millions of dollars), in the FEDERAL DEBT section (~page 20-37 depending on bulletin size; large bulletins push it deeper).
- Answer column = the FIRST data column: **"Total outstanding > Total"** (older) / **"Amount outstanding > Total 1/"** (1975+). This = Public debt securities + Agency securities = GROSS debt including agency (FHA etc.) issues. Verify: Total = PublicDebt + Agency in the same row.
- FD-1 has a monthly section (recent ~13 months) and an annual fiscal-year-end section. For "end of fiscal month January YYYY" use the **monthly row "YYYY-Jan"**, NOT the annual (June FY-end) row.

## Reporting lag (critical)
A bulletin dated month M reports data ~2 months in arrears. So:
- The "January YYYY" monthly row first appears in the ~**April YYYY** bulletin and stays for ~a year.
- A literal "January YYYY bulletin" reports only thru ~**November YYYY-1** (no same-year January row).
If the corpus lacks the exact January bulletins, take each year's FD-1 "YYYY-Jan" row from whatever available bulletin contains it — the revised value is stable. The benchmark gold = the FD-1 January-row series.

## Pitfalls
- **FD-2 confusion:** Table FD-2 (Computed Interest Charge) sits directly below FD-1 on the SAME page and ALSO has a "YYYY-Jan" row with a similar-magnitude number (interest-bearing debt base). DO NOT grep blindly — e.g. 1980 FD-1 Jan = 854,741 but FD-2 Jan = 846,517. Confirm you're in FD-1 (columns: Total / Public debt securities / Agency securities / Government accounts / The public).
- **OCR row-label offset:** pdftotext -layout frequently prints the month label on the line BELOW (or above) its number row, causing 1-row misreads. When a digit is decision-critical, render with `pdftoppm -r 200 -png -f P -l P file.pdf /tmp/x` then VISION-read the exact January row plus its neighbors (Dec, Feb) to lock alignment. (Caught a 401,845 vs 403,167 error this way.)
- **IMF definition shift:** Bulletins through ~[redacted] INCLUDE the IMF/international non-interest notes (~$825M) inside the public-debt-securities Total; 1974+ EXCLUDE them (footnote 1/ "adjusted to exclude issues to IMF"). So the early-year Totals are ~825 higher than they'd be on the later definition. Report each year AS THAT ERA's bulletin states it (the per-bulletin authentic figure) unless the question demands one consistent definition.
- Wrong-table trap: some pages at the expected number are FO-4 "Gross Obligations Incurred" — not FD-1. Check the title.

## Locating FD-1 fast
```
for a in $(seq 20 44); do
  pdftotext -layout -f $a -l $a BULLETIN.pdf - 2>/dev/null \
   | grep -q "Summary of Federal Debt" && echo "FD-1 page $a"; done
```
Then `pdftotext -layout -f P -l P BULLETIN.pdf - | grep -iE "YYYY[- ]*Jan"` and verify column = Total (= PublicDebt+Agency).

## Worked result (Jan gross debt, FD-1 Total, millions) — GOLD-VERIFIED
1969→1980: 374443, 381327, 401845, 433432, 461855, 478957, 505483, **595307**, 664852, 731821, 798733, 854741.
WARNING: an earlier run of THIS skill emitted Jan-1977 = 595329 and FAILED (gold = 595307, a 22-unit trailing-digit OCR slip; rest of the 12-value series was correct). When a value ends in the hundreds/tens, the last 2–3 digits are the high-risk OCR zone — VISION-read (pdftoppm -r 200) the FD-1 Jan-1977 Total cell, do NOT trust the pdftotext digits. Confirm Total = PublicDebt + Agency in that same row to catch the slip.
Sources used (FD-1 January rows): 1969 from 1969_10/1970_01; 1970 from 1970_04; 1971 from 1972_03 (vision-confirmed); 1972/[redacted] from 1973_03; 1974/1975 from 1975_03; 1976/1977 from 1977_03; 1978 from 1978_03; 1979 from 1980_02/1980_03; 1980 from 1980_03/1980_04.

## Output
Comma-separated list in chronological order, plain numbers (no $, no thousands-commas inside numbers to avoid CSV ambiguity), in millions, wrapped in <FINAL_ANSWER>...</FINAL_ANSWER>.
