import streamlit as st
import pandas as pd
import plotly.express as px

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(
    page_title="Stockholm Cultural Events",
    page_icon="🎭",
    layout="wide"
)

# -----------------------------
# LOAD DATA
# -----------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("data/output/events_full_year.csv")

    # Convert date/time
    df["date"] = pd.to_datetime(df["date"])
    df["month"] = df["date"].dt.month_name()
    df["weekday"] = df["date"].dt.day_name()

    # Clean price if exists
    if "price" in df.columns:
        df["price"] = pd.to_numeric(df["price"], errors="coerce").fillna(0)

    return df


df = load_data()

# -----------------------------
# HEADER
# -----------------------------
st.title("🎭 Stockholm Cultural Events")
st.caption("Discover music, theatre, arts and more happening in Stockholm.")

# -----------------------------
# KPI CARDS
# -----------------------------
col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Events", len(df))
col2.metric("Upcoming Events", (df["date"] >= pd.Timestamp.today()).sum())
col3.metric("Venues", df["venue_name"].nunique())
col4.metric("Categories", df["genre"].nunique())

st.divider()

# -----------------------------
# TABS
# -----------------------------
tab1, tab2, tab3, tab4 = st.tabs(["🔎 Discover", "🗺 Map", "📊 Trends", "🔥 Popular"])

# -----------------------------
# FILTERS (DISCOVER)
# -----------------------------
with tab1:
    st.subheader("Discover Events")

    colf1, colf2, colf3, colf4 = st.columns([3, 1, 1, 1])

    search = colf1.text_input("Search by name", "")
    category = colf2.selectbox("Category", ["All"] + sorted(df["genre"].dropna().unique()))
    date_filter = colf3.date_input("From date", value=None)
    max_price = colf4.number_input("Max price (SEK)", value=0)

    filtered = df.copy()

    if search:
        filtered = filtered[filtered["name"].str.contains(search, case=False, na=False)]

    if category != "All":
        filtered = filtered[filtered["genre"] == category]

    if date_filter:
        filtered = filtered[filtered["date"] >= pd.to_datetime(date_filter)]

    if "price" in filtered.columns and max_price > 0:
        filtered = filtered[filtered["price"] <= max_price]

    st.write(f"### {len(filtered)} events found")

    # -----------------------------
    # EVENT CARDS
    # -----------------------------
    for _, row in filtered.iterrows():
        with st.container():
            colA, colB = st.columns([1, 3])

            with colA:
                if "image_url" in row and pd.notna(row["image_url"]):
                    st.image(row["image_url"], use_container_width=True)

            with colB:
                st.markdown(f"### {row['name']}")
                st.write(f"📅 {row['date'].date()}  |  🕒 {row.get('time','')}")
                st.write(f"📍 {row['venue_name']} - {row['venue_city']}")
                st.write(f"🎭 {row.get('genre','')} | {row.get('subgenre','')}")

                if "url" in row and pd.notna(row["url"]):
                    st.link_button("Buy tickets →", row["url"])

        st.divider()

# -----------------------------
# MAP TAB
# -----------------------------
with tab2:
    st.subheader("Event Map")

    if "venue_lat" in df.columns and "venue_lon" in df.columns:
        map_df = df.dropna(subset=["venue_lat", "venue_lon"])
        map_df = map_df.rename(columns={
    "venue_lat": "lat",
    "venue_lon": "lon"
})

        st.map(map_df[["lat", "lon"]])

        #st.map(map_df[["venue_lat", "venue_lon"]])

    else:
        st.warning("No coordinates available")

# -----------------------------
# TRENDS TAB
# -----------------------------
with tab3:
    st.subheader("Event Trends")

    col1, col2 = st.columns(2)

    with col1:
        genre_counts = df["genre"].value_counts().reset_index()
        genre_counts.columns = ["genre", "count"]

        fig = px.bar(genre_counts, x="genre", y="count", title="Events by Genre")
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        monthly = df["month"].value_counts().reset_index()
        monthly.columns = ["month", "count"]

        fig2 = px.line(monthly, x="month", y="count", title="Events by Month")
        st.plotly_chart(fig2, use_container_width=True)

# -----------------------------
# POPULAR TAB
# -----------------------------
with tab4:
    st.subheader("Popular Events")

    popular = df.copy()

    # simple popularity rule (you can replace with real metric)
    popular = popular.sort_values("date")

    st.dataframe(
        popular[["name", "date", "venue_name", "genre", "url"]],
        use_container_width=True
    )