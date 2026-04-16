import requests
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("GOOGLE_PLACES_KEY")

# Museums with free admission (based on official information)
FREE_MUSEUMS = {
    "Nationalmuseum", "Moderna Museet", "Historiska museet",
    "Medelhavsmuseet", "Hallwylska museet", "Stadsmuseet i Stockholm",
    "Spårvägsmuseet"
}


def search_museums():
    """Search for museums in Stockholm using Google Places API (New) — Text Search."""
    url = "https://places.googleapis.com/v1/places:searchText"
    headers = {
        "Content-Type": "application/json",
        "X-Goog-Api-Key": API_KEY,
        "X-Goog-FieldMask": (
            "places.displayName,places.formattedAddress,places.location,"
            "places.websiteUri,places.regularOpeningHours,places.priceLevel,"
            "places.rating,places.userRatingCount,places.id"
        )
    }
    body = {
        "textQuery": "museum Stockholm Sverige",
        "languageCode": "sv",
        "maxResultCount": 20
    }

    r = requests.post(url, headers=headers, json=body)
    data = r.json()

    print("Status code:", r.status_code)
    if "error" in data:
        print("Error:", data["error"])
        return []

    places = data.get("places", [])
    print(f"Found {len(places)} museums")
    return places


def fetch_all_museums():
    """Fetch museum data, enrich with category tags and popularity score, save to CSV."""
    print("Searching for museums in Stockholm...")
    places = search_museums()

    if not places:
        print("No places found.")
        return

    rows = []
    for p in places:
        # Extract opening hours as a readable string
        opening = p.get("regularOpeningHours", {})
        weekday_text = opening.get("weekdayDescriptions", [])

        # We map columns to match the event-file structure for Power BI harmony
        rows.append({
            "event_id": p.get("id"),
            "name": p.get("displayName", {}).get("text"),
            "url": p.get("websiteUri"),
            "venue_name": p.get("displayName", {}).get("text"),
            "venue_address": p.get("formattedAddress"),
            "venue_city": "Stockholm",
            "venue_lat": p.get("location", {}).get("latitude"),
            "venue_lon": p.get("location", {}).get("longitude"),
            "rating": p.get("rating"),
            "num_reviews": p.get("userRatingCount"),
            "price_level": p.get("priceLevel"),
            "opening_hours": " | ".join(weekday_text),
            "status": "permanent"
        })

    df = pd.DataFrame(rows)

    # --- New Columns for Power BI Integration ---
    df['segment'] = 'Cultural'  # Matches "Arts & Theatre" logic
    df['genre'] = 'Museum'  # Allows filtering specifically for museums
    df['subgenre'] = 'Exhibition'

    # Static temporal data to match event-file format
    df['year'] = 2026
    df['month_name'] = 'All Year'
    # --------------------------------------------

    # Free admission based on official museum information
    df["is_free"] = df["name"].isin(FREE_MUSEUMS)

    # Popularity score: combines rating and review count
    df["popularity_score"] = (df["rating"] * df["num_reviews"].pow(0.5)).round(1)

    # Normalize popularity to 0–100
    min_s = df["popularity_score"].min()
    max_s = df["popularity_score"].max()
    df["popularity_index"] = ((df["popularity_score"] - min_s) / (max_s - min_s) * 100).round(1)

    df = df.sort_values("popularity_index", ascending=False).reset_index(drop=True)

    print(f"\n{len(df)} museums processed and formatted:")
    print(df[["name", "segment", "genre", "popularity_index"]].head().to_string())

    # Save to CSV
    df.to_csv("stockholm_museums.csv", index=False, encoding="utf-8-sig")
    print("\nSuccess! Saved to stockholm_museums.csv")


if __name__ == "__main__":
    fetch_all_museums()