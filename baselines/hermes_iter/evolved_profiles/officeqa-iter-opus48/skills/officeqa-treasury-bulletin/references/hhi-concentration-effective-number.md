# Herfindahl-Hirschman Index (HHI) + effective number of groups

Trigger: Q says "treat [groups A and B...] as the full market", asks for the
"Herfindahl Hirschman Index of concentration" using "shares based on the value
of X held", and often a follow-up: "the effective number of [groups] implied by
this index defined as the reciprocal of the HHI". Rounded to thousandths,
[hhi, effective_number] in sub-question order.

## THE CONVENTION OFFICEQA USES (critical)
HHI has TWO common scalings — OfficeQA grades the FRACTIONAL form (0..1), NOT
the ×10,000 form (0..10000):
- FRACTIONAL: HHI = Σ s_i²  where s_i = share as a DECIMAL FRACTION (Σ s_i = 1).
  Range 0..1. Two equal groups → 0.5. One group → 1.0.   ← USE THIS
- ×10,000 (antitrust/DOJ): shares as percent-points, range 0..10000.  ← NOT this
The "reciprocal of the HHI" follow-up only makes sense in the fractional form:
effective number = 1 / HHI (a.k.a. inverse-Simpson / numbers-equivalent).
If you used the ×10000 form, the reciprocal would be a meaningless ~0.00x —
that mismatch is the tell that you picked the wrong scaling.

## RECIPE
1. Pull the value held by EACH group (here: total $ of Treasury notes held by
   the 16 NYC banks, and by the 14 Chicago banks — from the bank-ownership /
   ownership-survey table dated the stated date, e.g. last day of 1959).
   Use the GROUP TOTALS, not per-bank rows. The group count (16, 14) is flavor;
   what matters is each group's aggregate dollar value.
2. "Treat these as the FULL market" → normalize shares to the SUM OF THESE
   GROUPS ONLY: s_i = value_i / Σ value. Do NOT divide by some national total.
3. HHI = Σ s_i²   (decimal shares).
4. Effective number of groups = 1 / HHI.
5. Round each to thousandths; output [HHI, effective_number] in asked order.

## WORKED PASS (why this ref exists)
Q: 16 NYC banks + 14 Chicago banks as full market of Treasury notes, ownership
survey published last day of 1959 → [0.611, 1.635]. CORRECT.
- Two groups only ⇒ HHI = s_NY² + s_CHI². With shares ~0.72 / 0.28 you get
  ~0.611; 1/0.611 = 1.635. The two-group structure means HHI ∈ [0.5, 1.0] and
  effective number ∈ [1.0, 2.0] — sanity-check your answer lands in that band.

## PITFALLS
- Wrong scaling: emit the 0..1 fractional HHI, never ×10000. The reciprocal
  follow-up confirms fractional is intended.
- Shares must sum to 1 over the STATED market (the named groups only). A common
  error is dividing by a larger universe (all banks nationally) — re-read
  "treat ... as the full market".
- With k equal groups HHI = 1/k and effective number = k — use this to sanity
  check (2 groups → HHI ≥ 0.5, eff# ≤ 2).
- This is a pure computation on extracted group totals; the only real risk is
  reading the wrong rows or mixing per-bank vs group-total values.
