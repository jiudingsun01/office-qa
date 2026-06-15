---
name: tb-weekly-capital-movements
description: Use for any question about capital inflow/outflow between the US and a foreign country or region (Latin America, Canada, Far East, Total Europe) over a WEEKLY span — especially spans phrased as "between the Nth Thursday and Mth Wednesday" of a month, which map to "week ended [Wednesday]" rows.
---

# Weekly "Net Capital Movement between the US and Foreign Countries" tables

Verified on: "Between the third Thursday and fourth Wednesday in Jan [redacted]
net capital inflow/outflow with Latin America?" → week ended Jan. 25, 1939,
Latin America net = [redacted] (thousands of dollars, inflow). CORRECT.

## 1. Locate the table
- Table title: **"Net Capital Movement between the United States and Foreign
  Countries"** (early bulletins, 1939+). Grep the parsed files for
  `Net Capital Movement between` or `Latin America`.
- Publication lag ≈ 2-3 months: weekly data for month M appears in the issue
  titled "...through [M] YYYY", typically `treasury_bulletin_YYYY_{M+2 or M+3}.txt`
  (e.g. January 1939 weeks → the 1939_04 issue; "through December 1938" → 1939_03).
- Units: **thousands of dollars**. Sign convention printed in the header:
  **"Capital inflow or capital outflow (-)"** — positive = net inflow into the US.
- Columns: United Kingdom, France, Germany, Italy, Netherlands, Switzerland,
  Other Europe, Total Europe, Canada, **Latin America**, Far East, All other,
  Grand total.

## 2. Map the phrased date span to a "week ended" row
Reporting weeks run **Thursday through Wednesday** and are labeled
**"Week ended [Wednesday date]"**. So:
- "between the Nth Thursday and the Wednesday that follows" = ONE reporting
  week = the row "week ended" on that Wednesday.
- Compute the actual calendar dates (e.g. Jan 1939: Thursdays 5/12/19/26,
  Wednesdays 4/11/18/25 → 3rd Thursday = Jan 19, 4th Wednesday = Jan 25
  → row "Jan. 25"). Don't assume; enumerate the weekdays for that month.
- A span covering multiple Thursday→Wednesday weeks = sum of the
  corresponding consecutive "week ended" rows.

## 3. Table structure: five stacked blocks, NET may be truncated in OCR
The table stacks five classification blocks, each with annual rows then
weekly "Week ended" rows:
1. MOVEMENT IN SHORT-TERM BANKING FUNDS
2. MOVEMENT IN BROKERAGE BALANCES
3. MOVEMENT IN TRANSACTIONS IN DOMESTIC SECURITIES
4. MOVEMENT IN TRANSACTIONS IN FOREIGN SECURITIES
5. NET CAPITAL MOVEMENT(S) ← the answer block

**OCR pitfall:** in the parsed text the final NET block's weekly rows are
sometimes cut off (e.g. 1939_04 shows only NET annual rows). Fallback:
**NET = sum of the four component blocks' rows for the same week and
column.** Verified: Jan. 25 Latin America = [redacted] + [redacted] + ([redacted]) + [redacted] = [redacted].
Use this also as a cross-check when the NET row IS present.

## 4. Cross-check
The same weekly row is reprinted in the next 1-2 monthly issues (each issue
carries ~the latest 4-5 weeks plus monthly totals) — confirm the value there
if OCR looks dubious (see tb-cross-issue-ocr-check).

## 5. Answer format
Bare number in thousands, no commas, no "(net inflow)" label — see
answer-format skill. Keep the minus sign if the net is an outflow.
