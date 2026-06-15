# "In which year did X peak/bottom?" over a multi-decade span

## The task
Q asks for the YEAR a long time series (personal saving rate, unemployment,
inflation, deficit/GDP, etc.) reaches its max/min across a span like 1950-1990.
Answer is a single YEAR. These series usually live in a "Profile of the Economy"
chart or a historical statistical-appendix table in the Bulletin front matter.

## #1 FAIL MODE: off-by-one-year (picked an adjacent bar)
Worked fail: "Between 1950 and [redacted], which year did U.S. personal saving rate
peak?" I answered 1974; gold = 1973. [redacted] and 1974 were BOTH ~10% personal-saving
years (mid-70s plateau), so the chart's two tallest bars are nearly the same
height. Eyeballing bar height picks the wrong neighbor.

## Procedure (do NOT eyeball the tallest bar)
1. Find the series. Search text layer for the metric name; if it's a chart with
   no text labels, render at high dpi (pdftoppm -png -r 300) and vision_analyze.
2. Get NUMERIC values, not bar heights. Prefer an embedded data table / data
   labels / axis-gridline readout over visual height. If only bars exist, read
   each candidate's value against the gridlines explicitly.
3. When the top 2-3 years are within visual noise (a plateau), list their numeric
   values side by side and pick the true argmax. Do NOT default to the later year.
4. Tie/near-tie convention: the EARLIER year of a plateau is often the official
   peak (the metric crests then stays high). When two years read equal, lean to
   the earlier one unless a label clearly says otherwise.
5. Sanity-check against well-known history: US personal saving rate peaked in the
   early-mid 1970s ([redacted] crest, ~10-13% by Commerce/BEA framing), high again
   ~1981-82; unemployment peaked 1982-83; CPI inflation peaked 1980. If your read
   contradicts a famous peak year by 1, re-read the two candidate bars/cells.

## Takeaway
Argmax/argmin-YEAR questions are decided at the plateau. The extraction risk is
not "wrong decade" but "wrong neighbor by 1 year." Always compare the top
candidates numerically and prefer the earlier year on a tie.
