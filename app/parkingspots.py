import requests
import pandas as pd
from geopy.distance import geodesic

def fetch_parking_data(api_key):
    url = f"https://openparking.stockholm.se/LTF-Tolken/v1/ptillstand/all?outputFormat=json&apiKey={api_key}"
    response = requests.get(url)
    return pd.DataFrame(response.json()["features"])

def nearest_parking(event_lat, event_lon, parking_df):
    parking_df["distance_meter"] = parking_df.apply(
        lambda row: geodesic(
            (event_lat, event_lon),
            (row["lat"], row["lon"])
        ).meters,
        axis=1
    )
    nearest = parking_df.loc[parking_df["distance_meter"].idxmin()]
    return nearest["name"], nearest["distance_meter"]

def enrich_with_parking(events_df, parking_df):
    events_df[["nearest_parking", "parking_distance"]] = events_df.apply(
        lambda row: pd.Series(
            nearest_parking(row["venue_lat"], row['venue_lon'], parking_df)
        ),
        axis=1
    )
    return events_df