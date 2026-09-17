from pathlib import Path
import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st

DATA_DIR = Path(__file__).parent / "data"
PLANTS_FILE = DATA_DIR / "plants_with_exposure.csv"
COMPANY_FILE = DATA_DIR / "company_aggregates.csv"

CAPACITY_COL = "Nominal crude steel capacity (ttpa)"


# Data loading (real exports if available, otherwise mock data for dev/testing)


def _generate_mock_plants(n: int = 60, seed: int = 42) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    owners = [f"Company {c}" for c in "ABCDEFGH"]
    countries = {
        "China": "East Asia",
        "India": "South Asia",
        "Japan": "East Asia",
        "United States": "North America",
        "Germany": "Europe",
        "Brazil": "South America",
    }
    country_list = list(countries.keys())

    country_choice = rng.choice(country_list, size=n)
    region_choice = [countries[c] for c in country_choice]

    return pd.DataFrame(
        {
            "GEM plant ID": [f"MOCK{i:04d}" for i in range(n)],
            "Plant name (English)": [f"Mock Steel Plant {i}" for i in range(n)],
            "Owner": rng.choice(owners, size=n),
            "Country/area": country_choice,
            "Region": region_choice,
            "Latitude": rng.uniform(-50, 60, size=n),
            "Longitude": rng.uniform(-120, 140, size=n),
            "Plant age": rng.uniform(0, 60, size=n),
            CAPACITY_COL: rng.lognormal(mean=7.5, sigma=1.0, size=n),
            "litpop_population": rng.lognormal(mean=10, sigma=1.5, size=n),
            "litpop_asset_value": rng.lognormal(mean=12, sigma=1.5, size=n),
        }
    )


def _company_aggregates_from_plants(plants: pd.DataFrame) -> pd.DataFrame:
    agg = plants.groupby("Owner").agg(
        num_plants=("GEM plant ID", "count"),
        total_capacity_ttpa=(CAPACITY_COL, "sum"),
        num_countries=("Country/area", "nunique"),
        avg_litpop_population=("litpop_population", "mean"),
        avg_litpop_asset_value=("litpop_asset_value", "mean"),
        centroid_lat=("Latitude", "mean"),
        centroid_lon=("Longitude", "mean"),
    )
    return agg.reset_index()


@st.cache_data
def load_data():
    if PLANTS_FILE.exists():
        plants = pd.read_csv(PLANTS_FILE)
        using_mock = False
    else:
        plants = _generate_mock_plants()
        using_mock = True

    if COMPANY_FILE.exists():
        companies = pd.read_csv(COMPANY_FILE)
    else:
        companies = _company_aggregates_from_plants(plants)

    return plants, companies, using_mock


# Page setup

st.set_page_config(page_title="Steel Plants Dashboard", page_icon="\U0001F3ED", layout="wide")

st.title("Global Steel Plants & Exposure Dashboard")
st.markdown(
    "Explore steel plant locations, capacity, and nearby population / asset "
    "exposure (LitPop), aggregated at the plant and company level. "
    "Data: [Global Iron and Steel Tracker](https://globalenergymonitor.org/projects/global-iron-steel-tracker) "
    "and [LitPop](https://www.research-collection.ethz.ch/entities/researchdata/12dcfc4f-9d03-463a-8d6b-76c0dc73cdc8)."
)

plants, companies, using_mock = load_data()

if using_mock:
    st.info(
        "Real data exports not found in `data/`. Showing generated mock data "
        "so the dashboard can be tested standalone. Drop `plants_with_exposure.csv` "
        "and `company_aggregates.csv` into `data/` (see `data/README.md`) to use "
        "the real dataset.",
    )


# Sidebar filters


st.sidebar.header("Filters")

owner_options = sorted(plants["Owner"].dropna().unique())
selected_owners = st.sidebar.multiselect("Company", owner_options, default=[])

region_options = sorted(plants["Region"].dropna().unique())
selected_regions = st.sidebar.multiselect("Region", region_options, default=[])

country_options = sorted(plants["Country/area"].dropna().unique())
selected_countries = st.sidebar.multiselect("Country/area", country_options, default=[])

cap_min = float(np.nanmin(plants[CAPACITY_COL]))
cap_max = float(np.nanmax(plants[CAPACITY_COL]))
capacity_range = st.sidebar.slider(
    "Capacity range (ttpa)",
    min_value=cap_min,
    max_value=cap_max,
    value=(cap_min, cap_max),
)

filtered = plants.copy()
if selected_owners:
    filtered = filtered[filtered["Owner"].isin(selected_owners)]
if selected_regions:
    filtered = filtered[filtered["Region"].isin(selected_regions)]
if selected_countries:
    filtered = filtered[filtered["Country/area"].isin(selected_countries)]
filtered = filtered[
    filtered[CAPACITY_COL].between(capacity_range[0], capacity_range[1])
]


# KPI metrics


col1, col2, col3, col4 = st.columns(4)
col1.metric("Plants shown", f"{len(filtered):,}")
col2.metric("Total capacity (ttpa)", f"{filtered[CAPACITY_COL].sum():,.0f}")
col3.metric("Companies", f"{filtered['Owner'].nunique():,}")
col4.metric("Countries", f"{filtered['Country/area'].nunique():,}")


# Main content: tabs for plant-level vs company-level views


insights_tab, plant_tab, company_tab, table_tab = st.tabs(
    ["EDA insights", "Plant map", "Company map", "Data table"]
)

with insights_tab:
    st.caption(
        "Summary of the exploratory analysis (Part 2), computed live from the "
        "currently filtered plants so it updates as you change the sidebar filters."
    )

    if filtered.empty:
        st.warning("No plants match the current filters.")
    else:
        left, right = st.columns(2)

        with left:
            top_countries = (
                filtered.groupby("Country/area")["GEM plant ID"]
                .count()
                .sort_values(ascending=False)
                .head(10)
                .rename("Plants")
                .reset_index()
            )
            fig = px.bar(
                top_countries,
                x="Plants",
                y="Country/area",
                orientation="h",
                title="Top countries by number of plants",
            )
            fig.update_layout(yaxis=dict(autorange="reversed"), height=350)
            st.plotly_chart(fig, use_container_width=True)

            top_owners_capacity = (
                filtered.groupby("Owner")[CAPACITY_COL]
                .sum()
                .sort_values(ascending=False)
                .head(10)
                .rename("Total capacity (ttpa)")
                .reset_index()
            )
            fig = px.bar(
                top_owners_capacity,
                x="Total capacity (ttpa)",
                y="Owner",
                orientation="h",
                title="Top companies by total capacity",
            )
            fig.update_layout(yaxis=dict(autorange="reversed"), height=350)
            st.plotly_chart(fig, use_container_width=True)

        with right:
            fig = px.histogram(
                filtered,
                x=CAPACITY_COL,
                nbins=30,
                title="Capacity distribution",
            )
            fig.update_layout(height=350)
            st.plotly_chart(fig, use_container_width=True)

            fig = px.histogram(
                filtered,
                x="Plant age",
                nbins=30,
                title="Plant age distribution",
            )
            fig.update_layout(height=350)
            st.plotly_chart(fig, use_container_width=True)

with plant_tab:
    color_metric = st.radio(
        "Color plants by",
        options=["Owner", "litpop_population", "litpop_asset_value"],
        horizontal=True,
    )
    if filtered.empty:
        st.warning("No plants match the current filters.")
    else:
        fig = px.scatter_mapbox(
            filtered,
            lat="Latitude",
            lon="Longitude",
            size=CAPACITY_COL,
            color=color_metric,
            hover_name="Plant name (English)",
            hover_data={
                "Owner": True,
                "Country/area": True,
                CAPACITY_COL: ":,.0f",
                "litpop_population": ":,.0f",
                "litpop_asset_value": ":,.0f",
                "Latitude": False,
                "Longitude": False,
            },
            mapbox_style="open-street-map",
            zoom=1,
            height=600,
        )
        fig.update_layout(margin=dict(l=0, r=0, t=0, b=0))
        st.plotly_chart(fig, use_container_width=True)

with company_tab:
    if companies.empty:
        st.warning("No company aggregates available.")
    else:
        fig = px.scatter_mapbox(
            companies,
            lat="centroid_lat",
            lon="centroid_lon",
            size="total_capacity_ttpa",
            color="avg_litpop_asset_value",
            hover_name="Owner",
            hover_data={
                "num_plants": True,
                "total_capacity_ttpa": ":,.0f",
                "num_countries": True,
                "avg_litpop_population": ":,.0f",
                "avg_litpop_asset_value": ":,.0f",
                "centroid_lat": False,
                "centroid_lon": False,
            },
            mapbox_style="open-street-map",
            zoom=1,
            height=600,
        )
        fig.update_layout(margin=dict(l=0, r=0, t=0, b=0))
        st.plotly_chart(fig, use_container_width=True)

with table_tab:
    st.dataframe(filtered, use_container_width=True)

st.divider()
st.caption(
    "Data sources: Global Energy Monitor Global Iron and Steel Tracker (plant data), "
    "ETH Zurich LitPop (population / asset exposure). "
    "Built for AIDAMS Lab 1."
)
