# Lab 1 : Steel Plants

## Part 1 — Loading the data

Pretty straightforward: we read in the plant data and the capacity sheet
from the Excel file, cleaned u
p the capacity column (some values weren't
numeric), and merged the two on plant ID. Ended up with **1,293 plants** and
45 columns to work with.

## Part 2 — Exploring the data

Some things that stood out:

- 13 out of the 45 columns have missing values, about 7,200 missing cells
  total. Mostly stuff like alternate names, other-language fields, and a
  few of the secondary capacity columns (coking, sinter, etc.) — nothing
  that affects the main analysis.
- Average plant capacity is around 2,840 ttpa, ranging all the way from 0 up
  to 25,499.
- Plant age averages about 39 years, but the max is 287, which is almost
  certainly a data issue rather than an actual 287-year-old plant. Worth
  keeping in mind if we use this column later.
- There are 1,069 different owners in the dataset. Nucor Corp has the most
  plants (13), followed by Cleveland-Cliffs (12) and Nippon Steel (10).
- Total global capacity comes out to about 3.67 million ttpa. By capacity
  (not plant count), ArcelorMittal Nippon Steel India leads the pack at
  86,500 ttpa.

## Part 3 — Putting it on a map

We split the `Coordinates` column into separate latitude/longitude columns
and made three maps with Plotly:

1. A basic world map with one dot per plant, colored by country
2. The same map but with dots sized by capacity and colored by owner, so
   you can spot the big players at a glance
3. A density map weighted by capacity — this one makes it really obvious
   that East Asia (China especially) has way more steel production packed
   in than anywhere else, with Europe and the rest of South/East Asia
   trailing behind

