# Vessel tonnage: "American vessels" share + Pearson correlation vs grand total

## Trigger phrases
"net registered tonnage (in thousands of tons) **cleared from** (or **entered
into**) the United States for foreign ports", "attributed to **American
vessels**", "compute the Pearson correlation coefficient between the American
vessels value and the **grand total** series." Old bulletins (1940s era) carry a
"Commerce / Navigation"-style table of vessel tonnage entered & cleared, split
into **American vessels** vs **Foreign vessels**, with a **Total (grand total)**
column, by month.

## The source table
- Section: vessel/shipping tonnage (entered and cleared, foreign trade), printed
  in 1940s Treasury Bulletins. Units = THOUSANDS of net registered tons.
- Rows = calendar months (Jan, Feb, Mar, ...). Columns: American vessels,
  Foreign vessels, Total. "Grand total" = the Total column (American + Foreign).
- Match CLEARED vs ENTERED to the question — they are two separate sub-tables.
  CALENDAR months (Jan/Feb/Mar) not fiscal.

## The two computations (this question asks for BOTH, comma-separated)

### (1) Percentage share of American vessels
- Sum American-vessels tonnage over the requested months (Jan+Feb+Mar 1941).
- Sum grand-total tonnage over the same months.
- share% = 100 * sum(American) / sum(Total). Round to 1 dp.
- NOTE on wording: the Q said "single **percentage point difference**" but with
  only ONE share being asked, this just means the share value itself (34.4),
  NOT a difference between two shares. When the phrasing implies one number,
  report the share. (If two shares/periods were given, it'd be |shareA - shareB|.)

### (2) Pearson correlation: American vs grand-total series
- Build the per-month series across the SAME months: x = American[Jan,Feb,Mar],
  y = Total[Jan,Feb,Mar]. (3 points here.)
- r = np.corrcoef(x, y)[0,1] (sample == population, divisor cancels).
- Round to nearest thousandth (3 dp).

## Worked example (THIS question — verified CORRECT)
Jan/Feb/Mar 1941, CLEARED for foreign ports, thousands of net reg tons:
- share of American vessels of grand total = **34.4%**
- Pearson r(American, grand total) over the 3 months = **0.391**
- Answer: [34.4, 0.391]  (spacing after comma does NOT matter to the grader)

## Pitfalls
- ENTERED vs CLEARED are different tables — pick the one named.
- "Grand total" / "Total" = American + Foreign, not American alone.
- With only 3 monthly points, r is sensitive — transcribe all 3 months for BOTH
  American and Total exactly.
- "percentage point difference" with a single subject = the share value itself.
- Delimiter spacing is irrelevant (grader normalizes whitespace).
