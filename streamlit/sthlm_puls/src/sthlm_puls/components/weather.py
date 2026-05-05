import streamlit as st
import requests
import pandas as pd
from datetime import datetime


@st.cache_data(ttl=3600)
def fetch_weather_forecast(days: int = 7) -> pd.DataFrame:
    """Fetch weather forecast for Stockholm from Open-Meteo API."""
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude":      59.33,
        "longitude":     18.07,
        "daily": ",".join([
            "temperature_2m_max",
            "temperature_2m_min",
            "precipitation_sum",
            "weathercode"
        ]),
        "timezone":      "Europe/Stockholm",
        "forecast_days": days
    }

    r = requests.get(url, params=params, timeout=15)
    r.raise_for_status()

    daily = r.json()["daily"]
    rows = []
    for i in range(len(daily["time"])):
        rows.append({
            "date":          daily["time"][i],
            "temp_max":      daily["temperature_2m_max"][i],
            "temp_min":      daily["temperature_2m_min"][i],
            "precipitation": daily["precipitation_sum"][i],
            "weathercode":   daily["weathercode"][i],
            "fetched_at":    datetime.today().strftime("%Y-%m-%d")
        })

    df = pd.DataFrame(rows)
    df["date"] = pd.to_datetime(df["date"])
    df["icon"] = df["weathercode"].apply(get_weather_icon)
    df["day_label"] = df["date"].dt.strftime("%a %d/%m").replace(
        {"Mon": "Mon", "Tue": "Tue", "Wed": "Wed",
         "Thu": "Thu", "Fri": "Fri", "Sat": "Sat", "Sun": "Sun"}
    )
    return df


def get_weather_icon(code: int) -> str:
    """Map Open-Meteo weathercode to emoji."""
    if code == 0:                return "☀️"
    if code in range(1, 4):      return "🌤️"
    if code in range(45, 49):    return "🌫️"
    if code in range(51, 68):    return "🌧️"
    if code in range(71, 78):    return "🌨️"
    if code in range(80, 83):    return "🌦️"
    if code == 95:               return "⛈️"
    return "❓"