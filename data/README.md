# Expected data exports (contract for `app.py`)

`app.py` (Part 6) reads its data from this folder. Until these files exist, the
dashboard falls back to generated mock data so it can be built and tested
independently of Parts 1-5. Drop in real exports from the notebook using these
exact filenames and columns and the dashboard will pick them up automatically
(no code changes needed).

## `plants_processed.csv` (Part 1 output)

Cleaned plant-level data, one row per plant, coordinates already split.

| column | type | notes |
|---|---|---|
| `GEM plant ID` | str | unique plant identifier |
| `Plant name (English)` | str | |
| `Owner` | str | company name |
| `Country/area` | str | |
| `Region` | str | |
| `Latitude` | float | parsed from `Coordinates` |
| `Longitude` | float | parsed from `Coordinates` |
| `Plant age` | float | years |
| `Nominal crude steel capacity (ttpa)` | float | |

## `plants_with_exposure.csv` (Part 4 output)

Same as `plants_processed.csv`, plus the LitPop fields matched by nearest
neighbor / spatial join. Column names below are what `app.py` looks for —
rename on your side if your LitPop extract uses different names.

| column | type | notes |
|---|---|---|
| *(all columns from `plants_processed.csv`)* | | |
| `litpop_population` | float | population value at nearest LitPop cell |
| `litpop_asset_value` | float | asset/exposure value at nearest LitPop cell |

## `company_aggregates.csv` (Part 5 output)

One row per `Owner`.

| column | type | notes |
|---|---|---|
| `Owner` | str | |
| `num_plants` | int | |
| `total_capacity_ttpa` | float | |
| `num_countries` | int | distinct `Country/area` values |
| `avg_litpop_population` | float | mean over the company's plants |
| `avg_litpop_asset_value` | float | mean over the company's plants |
| `centroid_lat` | float | mean latitude of the company's plants |
| `centroid_lon` | float | mean longitude of the company's plants |

If you use different names, either rename your export columns to match this
table before saving (simplest), or update the `COLUMN_*` constants near the
top of `app.py`.
