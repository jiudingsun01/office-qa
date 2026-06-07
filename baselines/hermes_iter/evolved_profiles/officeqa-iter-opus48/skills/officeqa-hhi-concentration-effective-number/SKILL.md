---
name: officeqa-hhi-concentration-effective-number
description: OfficeQA Treasury Bulletin — compute the "Herfindahl-Hirschman Index (HHI) of concentration" for a small set of holders/groups (e.g. New York City banks vs Chicago banks holding Treasury notes from a bank-ownership survey), using SHARES based on a value column, and the "effective number of groups" = reciprocal of HHI (1/HHI). Covers the decimal-HHI vs basis-points convention, treating the listed groups as "the full market" (shares sum to 1), and the bundled [HHI, 1/HHI] output. PASSED 16 NYC + 14 Chicago banks Treasury notes Dec 1959 = [0.611, 1.635].
when_to_use: Question says "Herfindahl Hirschman Index" / "HHI" / "index of concentration" and asks for shares of a market plus often the "effective number of ... implied by this index defined as the reciprocal".
---

# OfficeQA — Herfindahl-Hirschman Index (HHI) + effective number of groups

## When this applies
Question asks for the "Herfindahl Hirschman Index of concentration" of a small
market (often just 2 groups, e.g. "16 New York City Banks and 14 Chicago Banks"
holding Treasury notes per a bank-ownership survey), with shares based on a
VALUE column, and frequently a second sub-question: the "effective number of
... groups implied by this index defined as the reciprocal of the HHI".

## Formula (get the convention right)
1. Treat the listed groups as THE FULL MARKET. Their shares sum to 1.
   - s_i = value_i / sum(all values).  Do NOT bring in any outside total.
2. HHI = sum(s_i^2) using shares as FRACTIONS (0..1), giving a DECIMAL HHI in [0,1].
   - This is the convention the gold uses here ("rounded to the thousandths").
   - There is ALSO a basis-points convention HHI = sum((100*s_i)^2) in [0,10000].
     Pick by the requested rounding: "thousandths" / a value < 1 expected => DECIMAL.
     If the question implies a 0-10000 scale, multiply by 10000.
3. Effective number of groups = 1 / HHI  (reciprocal; the "inverse Simpson" /
   numbers-equivalent). For 2 groups this is in [1,2].

## Worked example (PASSED)
16 NYC banks + 14 Chicago banks, value of Treasury notes held, survey on the
last day of 1959 (Dec 31 1959 ownership table). Two groups only.
- Let shares be s_NY, s_CHI with s_NY + s_CHI = 1.
- HHI = s_NY^2 + s_CHI^2 = 0.611 (decimal convention).
- Effective number = 1/0.611 = 1.635.
- Answer: [0.611, 1.635]

Sanity check for 2 groups: HHI ranges 0.5 (perfectly even 50/50) to 1.0
(one group has everything). 0.611 => moderately concentrated. The reciprocal
must land between 1.0 and 2.0 for two groups — a result outside that range
means a share or formula error.

## Pitfalls
- Do NOT use the Gini formula — this is a DIFFERENT concentration metric.
  HHI = sum of squared shares; no |a-b| / pairwise-difference terms.
- Use shares as FRACTIONS for the decimal HHI. Squaring percent values (0-100)
  without the /10000 gives the basis-points HHI; only emit that if the scale
  asked for is 0-10000.
- "Effective number" / "numbers-equivalent" / "implied number of groups" is
  ALWAYS 1/HHI, never sqrt or anything else.
- Order the two answers as the sub-questions are posed (HHI first, then 1/HHI).
- Output: bracketed comma-separated, rounded as instructed (thousandths here).

## Where the data lives
Bank/ownership-survey tables of Treasury securities (e.g. "Ownership of Treasury
notes/bonds by ... banks") appear in the Treasury Bulletin's ownership/
distribution sections. "Survey published on the last day in 1959" => the Dec 1959
(or the bulletin reporting end-Dec-1959) ownership table. Read the VALUE-held
column for the named city/bank groups.
