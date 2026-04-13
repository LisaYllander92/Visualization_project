import streamlit as st
import pandas as pd
import duckdb
import pydeck as pdk

# ---------------------------
# Load Data
# ---------------------------
df = pd.read_csv("data/events_full_year.csv")

# Convert date
df["date"] = pd.to_datetime(df["date"])

# ---------------------------
# Title
# ---------------------------
st.title("🎟️ Stockholm Events Dashboard")

# ---------------------------
# Sidebar Filters
# ---------------------------
st.sidebar.header("Filters")

# Date filter
date_range = st.sidebar.date_input(
    "Select Date Range",
    [df["date"].min(), df["date"].max()]
)

# Genre filter
genres = st.sidebar.multiselect(
    "Select Genre",
    options=df["genre"].unique(),
    default=df["genre"].unique()
)

# Venue filter
venues = st.sidebar.multiselect(
    "Select Venue",
    options=df["venue_name"].unique(),
    default=df["venue_name"].unique()
)

# ---------------------------
# Apply Filters
# ---------------------------
filtered_df = df[
    (df["date"].between(pd.to_datetime(date_range[0]), pd.to_datetime(date_range[1]))) &
    (df["genre"].isin(genres)) &
    (df["venue_name"].isin(venues))
]

# ---------------------------
# KPIs
# ---------------------------
st.subheader("📊 Key Metrics")

col1, col2, col3 = st.columns(3)

col1.metric("Total Events", len(filtered_df))
col2.metric("Unique Venues", filtered_df["venue_name"].nunique())
col3.metric("Unique Genres", filtered_df["genre"].nunique())

# ---------------------------
# Top Events (Table + URL)
# ---------------------------
st.subheader("🎟️ Events List")

# Make clickable links
filtered_df["ticket_link"] = filtered_df["url"].apply(
    lambda x: f"[View Event]({x})"
)

st.write(
    filtered_df[
        ["name", "date", "venue_name", "genre", "ticket_link"]
    ].sort_values(by="date")
)

# ---------------------------
# Top Venues
# ---------------------------
st.subheader("🏟️ Top Venues")

venue_counts = (
    filtered_df["venue_name"]
    .value_counts()
    .head(10)
)

st.bar_chart(venue_counts)

# ---------------------------
# Peak Hours
# ---------------------------
st.subheader("⏰ Event Distribution by Hour")

hour_counts = (
    filtered_df["hour"]
    .value_counts()
    .sort_index()
)

st.line_chart(hour_counts)

# ---------------------------
# Map View
# ---------------------------
st.subheader("🗺️ Event Locations")

map_df = filtered_df.dropna(subset=["venue_lat", "venue_lon"])

st.pydeck_chart(pdk.Deck(
    initial_view_state=pdk.ViewState(
        latitude=59.3293,
        longitude=18.0686,
        zoom=10,
        pitch=50,
    ),
    layers=[
        pdk.Layer(
            "ScatterplotLayer",
            data=map_df,
            get_position='[venue_lon, venue_lat]',
            get_radius=200,
            get_fill_color=[255, 0, 0],
            pickable=True,
        ),
    ],
))