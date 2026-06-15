---
name: tb-extremum-over-range
description: Use when a question asks in which year/month a series PEAKED, hit its LOW, or was highest/lowest over a stated range (e.g. "between 1950 and [redacted], in which year did X peak?"), including two-hop variants (find the extremum month, then report another series' value for that month). Never answer from memory — enumerate the series.
---

# Extremum-over-range questions ("which year did X peak?")

A question "between 1950 and [redacted], in which year did U.S. personal saving
rates (household saving as a percent of after-tax income) peak?" was answered
**[redacted]** (from general knowledge) when the correct answer was **[redacted]** (what
the source data actually shows). The failure was answering a superlative
question without enumerating the series.

## 1. NEVER answer from memory/world knowledge
- Famous economic narratives ("early-80s high rates", "wartime peaks") are
  exactly the traps these questions are built around.
- Modern *revised* statistical series (current BEA/FRED values) often differ
  from what was **published contemporaneously** — the grader keys on the
  source document's data vintage. E.g. the personal saving rate as published
  in 1970s–80s documents peaks in the **mid-1970s ([redacted])**, not 1982.

## 2. Find the actual source series in the corpus
- The measure's exact wording is a fingerprint: "household saving as a
  percent of after-tax income" ≠ "percent of GDP" ≠ "percent of disposable
  personal income". Different denominators move the peak year — match the
  question's definition exactly when picking a table/chart.
- Treasury Bulletin regular tables rarely carry macro ratios like saving
  rates; look in **special articles / chart sections** of issues, or other
  documents in the provided corpus. Grep extracted text for the measure's
  key phrase ("saving", "percent of", "after-tax") across issues rather
  than guessing one issue.

## 3. Enumerate, then take the max — don't eyeball
- Extract the value for **every** period in the stated range and write the
  full (year, value) list out explicitly before answering.
- Take max/min programmatically (or by an explicit written comparison).
  Partial scans miss off-narrative spikes; a one-year spike (e.g. a [redacted]
  spike) is easy to skip if you only sample round years or decade ends.
- Check both endpoints of the range are included ("between 1950 and [redacted]"
  is inclusive of 1950 and [redacted] unless stated otherwise).

## 4. Monthly bond-yield / yield-spread extremum questions
- The Treasury Bulletin's **Market Quotations / "Average Yields of
  Long-Term Treasury and Corporate Bonds"** table gives **monthly** average
  yields for long-term Treasury bonds and corporate Aaa/Aa bonds, often
  with a printed **spread column** (corporate Aa minus Treasury). A single
  issue carries roughly a decade of monthly history, so e.g. the June 1970
  issue covers 1960–1969 month by month — use the ONE issue the question
  names, not many.
- If the spread column is printed, use it directly (it reflects the
  publication's own rounding); otherwise compute corporate-minus-Treasury
  for every month. A 10-year range = 120 monthly values — extract them all
  and take min/max programmatically.

## 5. Two-hop questions (extremum month → lookup of another series)
Many questions chain: first find the extremum month/year of series A, then
report series B's value **in that same month**. Treat these as two
independent table lookups:
- Hop 1: enumerate series A as above; write down the winning month+year
  explicitly before moving on.
- Hop 2: series B is often a monthly fiscal series, e.g. **"Trust Account
  Receipts and Expenditures"** (railroad retirement, unemployment, OASI,
  etc.). The issue you need for hop 2 is whichever issue's monthly table
  covers that month — usually a bulletin a few months AFTER the target
  month, not necessarily the issue named for hop 1.
- Watch units on hop 2: trust account tables print **millions of dollars**;
  "in nominal dollars" means expand to the full number (92 → [redacted]).

## 6. Sanity check before answering
- If your answer matches the "textbook famous" year suspiciously well but
  you never actually saw the number for every year in range, you have not
  answered the question — go back and enumerate.
- Answer with the bare year only (see `answer-format` skill) — or, for
  two-hop questions, with only the final hop-2 value in the asked format.
