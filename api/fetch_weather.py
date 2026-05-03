import requests
import pandas as pd
from datetime import datetime


def fetch_weather_forecast(days: int = 10) -> pd.DataFrame:
    """
    Fetch a weather forecast for Stockholm using Open-Meteo API.
    No API key required. Returns one row per day for the next `days` days.

    Weathercode reference (subset):
        0  = Clear sky
        1-3 = Partly cloudy
        45, 48 = Fog
        51-67 = Drizzle / Rain
        71-77 = Snow
        80-82 = Rain showers
        95  = Thunderstorm
    """
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude":     59.33,
        "longitude":    18.07,
        "daily": ",".join([
            "temperature_2m_max",
            "temperature_2m_min",
            "precipitation_sum",
            "weathercode"
        ]),
        "timezone":      "Europe/Stockholm",
        "forecast_days": days
    }

    print(f"Fetching {days}-day weather forecast for Stockholm...")
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

    print(f"Retrieved {len(df)} days of forecast data")
    return df


if __name__ == "__main__":
    df = fetch_weather_forecast(days=10)

    print(df[["date", "temp_max", "temp_min", "precipitation", "weathercode"]].to_string())

    df.to_csv("../data/raw/stockholm_weather.csv", index=False, encoding="utf-8-sig")
    print("\nSaved to stockholm_weather.csv")