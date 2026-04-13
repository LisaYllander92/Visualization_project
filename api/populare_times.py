import populartimes
import pandas as pd
import os
import time
from dotenv import load_dotenv
load_dotenv()

API_KEY = os.getenv("GOOGLE_PLACES_KEY")

# Manuell fri-entré-lista (officiell info från respektive museum)
FREE_MUSEUMS = {
    "Nationalmuseum",
    "Moderna Museet",
    "Historiska museet",
    "Medelhavsmuseet",
    "Hallwylska museet",
    "Stadsmuseet i Stockholm",
    "Spårvägsmuseet",
}

def fetch_popular_times():
    df = pd.read_csv("../data/stockholm_museums.csv")

    all_rows = []
    for _, row in df.iterrows():
        name = row["name"]
        place_id = row["place_id"]
        print(f"Hämtar populära tider för: {name}...")

        try:
            data = populartimes.get_id(API_KEY, place_id)
            popular = data.get("populartimes", [])

            # Hitta dag + timme med flest besökare
            peak_day, peak_hour, peak_val = None, None, 0
            for day_data in popular:
                for hour, val in enumerate(day_data["data"]):
                    if val > peak_val:
                        peak_val = val
                        peak_day = day_data["name"]
                        peak_hour = hour

            # Bygg en enkel dict per dag med timmar som kolumner
            hours_by_day = {}
            for day_data in popular:
                hours_by_day[day_data["name"]] = day_data["data"]

            all_rows.append({
                "name":        name,
                "address":     row["address"],
                "lat":         row["lat"],
                "lon":         row["lon"],
                "website":     row["website"],
                "rating":      row["rating"],
                "num_reviews": row["num_reviews"],
                "opening_hours": row["opening_hours"],
                "is_free":     name in FREE_MUSEUMS,
                "peak_day":    peak_day,
                "peak_hour":   f"{peak_hour}:00" if peak_hour else None,
                "peak_value":  peak_val,  # 0-100, relativt besökarantal
                "popular_times_raw": str(hours_by_day),
            })
        except Exception as e:
            print(f"  Kunde inte hämta: {e}")
            all_rows.append({
                "name":     name,
                "address":  row["address"],
                "lat":      row["lat"],
                "lon":      row["lon"],
                "website":  row["website"],
                "rating":   row["rating"],
                "num_reviews": row["num_reviews"],
                "opening_hours": row["opening_hours"],
                "is_free":  name in FREE_MUSEUMS,
                "peak_day": None,
                "peak_hour": None,
                "peak_value": None,
                "popular_times_raw": None,
            })

        time.sleep(1)

    result_df = pd.DataFrame(all_rows)
    result_df.to_csv("stockholm_museums_full.csv", index=False, encoding="utf-8-sig")
    print(f"\nKlar! Sparad till stockholm_museums_full.csv")
    print(result_df[["name", "is_free", "peak_day", "peak_hour", "peak_value"]].to_string())

if __name__ == "__main__":
    fetch_popular_times()