import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# --- page setup ---
st.set_page_config(page_title="Global Steel Plants", layout="wide")

# --- load the csvs we exported from the notebook ---
@st.cache_data
def load_data():
    df       = pd.read_csv("steel_plants.csv")
    merged   = pd.read_csv("merged_steel_litpop.csv")
    companies = pd.read_csv("company_steel_litpop.csv")
    return df, merged, companies

df, merged_df, company_df = load_data()

# --- title ---
st.title("Global Iron and Steel Plants")
st.caption("Data: Global Energy Monitor – Global Iron and Steel Tracker (June 2026)")

# --- sidebar filters ---
st.sidebar.header("Filters")

# region filter — only 7 options so multiselect works well
all_regions = sorted(df["Region"].dropna().unique())
selected_regions = st.sidebar.multiselect("Region", all_regions, default=all_regions)

# capacity range slider
cap_col = "Nominal crude steel capacity (ttpa)"
cap_min = float(df[cap_col].fillna(0).min())
cap_max = float(df[cap_col].fillna(0).max())
cap_range = st.sidebar.slider("Capacity (ttpa)", cap_min, cap_max, (cap_min, cap_max))

# apply filters to the full plant dataset
filtered = df[
    df["Region"].isin(selected_regions) &
    df[cap_col].fillna(0).between(cap_range[0], cap_range[1])
].copy()

# --- KPI metrics ---
k1, k2, k3, k4 = st.columns(4)
k1.metric("Plants shown",        len(filtered))
k2.metric("Total capacity (ttpa)", f"{filtered[cap_col].sum():,.0f}")
k3.metric("Countries",           filtered["Country/area"].nunique())
k4.metric("Regions",             filtered["Region"].nunique())

st.divider()

# --- map 1: all plants colored by region ---
st.subheader("Plant locations")

plot_df = filtered.dropna(subset=["latitude", "longitude"]).copy()
plot_df["cap_size"] = plot_df[cap_col].fillna(0).clip(lower=1)

fig_map = px.scatter_geo(
    plot_df,
    lat="latitude",
    lon="longitude",
    color="Region",
    size="cap_size",
    size_max=30,
    hover_name="Plant name (English)",
    hover_data={
        "Owner": True,
        "Country/area": True,
        cap_col: ":,.0f",
        "latitude": False,
        "longitude": False,
        "cap_size": False,
    },
    projection="natural earth",
    title="Steel plants by region",
)
fig_map.update_layout(margin={"r": 0, "t": 30, "l": 0, "b": 0})
st.plotly_chart(fig_map, use_container_width=True)

st.divider()

# --- map 2: LitPop exposure (China, India, Japan only) ---
st.subheader("Socio-economic exposure – LitPop (China, India, Japan)")
st.caption("Marker size = plant capacity  ·  Colour = local LitPop exposure value (log scale)")

litpop_plot = merged_df.dropna(subset=["Latitude", "Longitude", "litpop_value"]).copy()
litpop_plot["cap_size"]   = litpop_plot[cap_col].fillna(0).clip(lower=1)
litpop_plot["litpop_log"] = np.log1p(litpop_plot["litpop_value"])

fig_litpop = px.scatter_geo(
    litpop_plot,
    lat="Latitude",
    lon="Longitude",
    size="cap_size",
    size_max=30,
    color="litpop_log",
    hover_name="Plant name (English)",
    hover_data={
        "Owner": True,
        cap_col: ":,.0f",
        "litpop_value": ":,.0f",
        "litpop_log": False,
        "cap_size": False,
    },
    color_continuous_scale="viridis",
    labels={"litpop_log": "LitPop exposure (log)"},
    projection="natural earth",
    title="Plants sized by capacity, coloured by LitPop exposure",
)
fig_litpop.update_layout(margin={"r": 0, "t": 30, "l": 0, "b": 0})
st.plotly_chart(fig_litpop, use_container_width=True)

st.divider()

# --- map 3: one dot per company ---
st.subheader("Company overview (China, India, Japan)")
st.caption("Each dot is one company. Size = total capacity, colour = average LitPop exposure.")

co_plot = company_df.dropna(subset=["Latitude", "Longitude"]).copy()
co_plot["cap_size"]   = co_plot[cap_col].fillna(0).clip(lower=1)
co_plot["litpop_log"] = np.log1p(co_plot["litpop_value"])

fig_company = px.scatter_geo(
    co_plot,
    lat="Latitude",
    lon="Longitude",
    size="cap_size",
    size_max=40,
    color="litpop_log",
    hover_name="Owner",
    hover_data={
        cap_col: ":,.0f",
        "plant_count": True,
        "country_count": True,
        "litpop_value": ":,.0f",
        "litpop_log": False,
        "cap_size": False,
    },
    color_continuous_scale="viridis",
    labels={"litpop_log": "Avg LitPop (log)"},
    projection="natural earth",
    title="Companies sized by capacity, coloured by avg LitPop exposure",
)
fig_company.update_layout(margin={"r": 0, "t": 30, "l": 0, "b": 0})
st.plotly_chart(fig_company, use_container_width=True)

st.divider()

# --- data table ---
st.subheader("Plant data table")

table_cols = [
    "Plant name (English)", "Owner", "Country/area", "Region",
    cap_col, "Main production equipment",
]
st.dataframe(
    filtered[table_cols].reset_index(drop=True),
    use_container_width=True,
)

# --- footer ---
st.caption(
    "Sources: Global Energy Monitor – Global Iron and Steel Tracker (June 2026) · "
    "LitPop: ETH Zurich Research Collection"
)
