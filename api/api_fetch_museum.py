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
    """Fetch museum data, enrich with popularity score and free admission flag, save to CSV."""
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

        rows.append({
            "name":          p.get("displayName", {}).get("text"),
            "address":       p.get("formattedAddress"),
            "lat":           p.get("location", {}).get("latitude"),
            "lon":           p.get("location", {}).get("longitude"),
            "website":       p.get("websiteUri"),
            "rating":        p.get("rating"),
            "num_reviews":   p.get("userRatingCount"),
            "price_level":   p.get("priceLevel"),
            "opening_hours": " | ".join(weekday_text),
            "place_id":      p.get("id"),
        })

    df = pd.DataFrame(rows)

    # Free admission based on official museum information
    df["is_free"] = df["name"].isin(FREE_MUSEUMS)

    # Popularity score: combines rating and review count
    # Formula: rating × sqrt(num_reviews) — rewards both quality and volume
    df["popularity_score"] = (df["rating"] * df["num_reviews"].pow(0.5)).round(1)

    # Normalize popularity to 0–100 for easier comparison and visualization
    min_s = df["popularity_score"].min()
    max_s = df["popularity_score"].max()
    df["popularity_index"] = ((df["popularity_score"] - min_s) / (max_s - min_s) * 100).round(1)

    df = df.sort_values("popularity_index", ascending=False).reset_index(drop=True)

    print(f"\n{len(df)} museums found:")
    print(df[["name", "rating", "num_reviews", "popularity_index", "is_free"]].to_string())

    df.to_csv("stockholm_museums.csv", index=False, encoding="utf-8-sig")
    print("\nSaved to stockholm_museums.csv")


if __name__ == "__main__":
    fetch_all_museums()