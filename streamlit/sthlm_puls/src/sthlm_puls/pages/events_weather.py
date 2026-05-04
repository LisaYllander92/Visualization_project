import streamlit as st
import pandas as pd
from components.weather import fetch_weather_forecast
from components.charts import plot_events_weather


st.title("📅 This Week in Stockholm")
st.markdown("Find the best day to experience Stockholm's cultural scene.")

# Load data
weather = fetch_weather_forecast(days=7)
events  = pd.read_csv("assets/data/events_combined.csv")
events["date"] = pd.to_datetime(events["date"])

# Count events per day
events_per_day = (
    events[events["date"].dt.date.between(
        weather["date"].dt.date.min(),
        weather["date"].dt.date.max()
    )]
    .groupby(events["date"].dt.date)
    .size()
    .reset_index(name="num_events")
)
events_per_day["date"] = pd.to_datetime(events_per_day["date"])

# Merge
df_merged = weather.merge(events_per_day, on="date", how="left")
df_merged["num_events"] = df_merged["num_events"].fillna(0).astype(int)

# Plot
fig = plot_events_weather(df_merged)
st.pyplot(fig)