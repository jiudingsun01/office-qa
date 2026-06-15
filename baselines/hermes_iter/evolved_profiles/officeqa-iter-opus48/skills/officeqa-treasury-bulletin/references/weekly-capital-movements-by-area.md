# Weekly "Capital Movements between U.S. and Foreign Countries/Areas" — date-anchored net flow

## When this applies
Question names a FOREIGN AREA or country (Latin America, Continental Europe,
United Kingdom, Far East, Canada, etc.), asks for a NET capital inflow/outflow
"in thousands of dollars," and bounds it by WEEKDAY-ANCHORED calendar dates
("between the third Thursday and fourth Wednesday in Jan 1939"). These come from
the 1938-1940s Treasury Bulletin "Capital Movements" exhibits, which report by
WEEK, with each week labeled by its ending date (often Wednesday-ending).

## The table layout
- Section: "Capital Movements between the United States and Foreign Countries"
  (a multi-page exhibit, early in late-1930s/1940s Bulletins).
- Rows = foreign AREAS and individual COUNTRIES (Latin America is an AREA
  aggregate row; individual Latin republics sum into it).
- Columns = successive WEEKS, each headed by a date (week-ending date).
- Sign convention: the table reports net capital movement. A net INFLOW to the
  US vs net OUTFLOW is given by the sign of the cumulative/period figure. Report
  the MAGNITUDE the table gives for the requested span; the word "inflow OR
  outflow" means just report the signed/absolute net the cells yield — gold is a
  bare positive integer in thousands (e.g. [redacted]).

## Resolving the weekday-anchored dates (the main gotcha)
"Third Thursday" and "fourth Wednesday" are CALENDAR computations, not table
ordinals. Compute them explicitly:
- Jan 1939: Jan 1 = Sunday. Thursdays = 5,12,19,26 -> 3rd Thursday = Jan 19.
  Wednesdays = 4,11,18,25 -> 4th Wednesday = Jan 25.
- So the span is Jan 19 -> Jan 25, 1939 (one week's worth).
Use Python to avoid off-by-one:
```python
import datetime, calendar
def nth_weekday(year, month, weekday, n):  # weekday: Mon=0..Sun=6
    d = [datetime.date(year,month,day)
         for day in range(1, calendar.monthrange(year,month)[1]+1)
         if datetime.date(year,month,day).weekday()==weekday]
    return d[n-1]
start = nth_weekday(1939,1,3,3)   # Thursday=3, 3rd  -> 1939-01-19
end   = nth_weekday(1939,1,2,4)   # Wednesday=2, 4th -> 1939-01-25
```

## How to read the net for the span
The weekly columns are headed by their week-ending date. The span Jan 19->Jan 25
lands inside the week ending ON or just after Jan 25 (the Wednesday-ending
week). Net flow "between" the two dates = the value in the week-ending column(s)
that cover that interval, OR the difference of two cumulative columns if the
table is cumulative. Verify whether the table is PER-WEEK (read the single
matching column) or CUMULATIVE-to-date (subtract the start-date column from the
end-date column). For Jan 1939 Latin America the matching weekly net = [redacted]
(thousands), reported as a bare integer.

## Unit / format
- Table is already in THOUSANDS of dollars; the Q asks for thousands, so NO
  rescaling — read the cell verbatim.
- Answer = single bare integer, Mode A style (no thousands grouping needed for a
  4-digit value): 1461.

## Worked example (CORRECT)
Q: "Between the third Thursday and fourth Wednesday in Jan 1939, net total
capital inflow/outflow (thousands) between US and Latin America?"
- 3rd Thu Jan 1939 = Jan 19; 4th Wed = Jan 25.
- Read Latin America row, week covering Jan 19-25, value = 1461.
- Answer: 1461. Gold: 1461.

## Pitfalls
- Do NOT treat "third Thursday" as "third weekly column" — resolve real dates.
- Latin America is an AREA aggregate, not a single country; read the aggregate
  row, not a constituent (Brazil, Argentina...).
- Confirm per-week vs cumulative before reporting; a cumulative table needs a
  difference of two columns.
