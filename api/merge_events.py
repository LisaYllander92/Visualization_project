import pandas as pd
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_DIR = os.path.join(BASE_DIR, "data", "output")

VENUE_META = {
    "fasching": {
        "venue_name":    "Fasching",
        "venue_city":    "Stockholm",
        "venue_address": "Kungsgatan 63",
        "venue_lat":     59.3334,
        "venue_lon":     18.0557,
        "segment":       "Nightlife",
        "status":        "onsale",
    },
    "berns": {
        "venue_name":    "Berns",
        "venue_city":    "Stockholm",
        "venue_address": "Berzelii Park",
        "venue_lat":     59.3323,
        "venue_lon":     18.0734,
        "segment":       "Nightlife",
        "status":        "onsale",
    },
}

RENAME_MAP = {
    "venue": "venue_name",
    "address": "venue_address",
    "lat": "venue_lat",
    "lng": "venue_lon",
}

FINAL_COLUMNS = [
    "event_id", "name", "url", "image_url", "date", "time", "status",
    "segment", "genre", "subgenre", "venue_name", "venue_city",
    "venue_address", "venue_lat", "venue_lon", "day_of_week",
    "month_name", "month_num", "year", "hour", "source"
]

def enrich_dates(df):
    """Extrahera dag, månad, år, timme från date/time-kolumner."""
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df["day_of_week"] = df["date"].dt.day_name()
    df["month_name"]  = df["date"].dt.month_name()
    df["month_num"]   = df["date"].dt.month
    df["year"]        = df["date"].dt.year
    df["date"]        = df["date"].dt.strftime("%Y-%m-%d")

    if "time" in df.columns:
        df["hour"] = pd.to_datetime(
            df["time"], format="%H:%M", errors="coerce"
        ).dt.hour

    return df

def merge_events():
    files = {
        "ticketmaster": os.path.join(BASE_DIR, "data", "raw", "events_full_year.csv"),
        "visitstockholm": os.path.join(BASE_DIR, "data", "output", "visitstockholm_clean.csv"),
        "fasching": os.path.join(BASE_DIR, "api", "../data/raw/fasching_events.csv"),
        "berns": os.path.join(BASE_DIR, "data", "raw", "berns_events.csv"),
    }

    dfs = []
    for source, path in files.items():
        if not os.path.exists(path):
            print(f"Varning: {path} finns inte, hoppar över")
            continue

        df = pd.read_csv(path)
        df["source"] = source
        print(f"Laddade {len(df)} event från {source}")

        if source in ("fasching", "berns"):
            df = df.rename(columns=RENAME_MAP)


        if source in VENUE_META:
            for col, val in VENUE_META[source].items():
                if col not in df.columns:
                    df[col] = val
                else:
                    df[col] = df[col].fillna(val)


        df = enrich_dates(df)

        for col in FINAL_COLUMNS:
            if col not in df.columns:
                df[col] = None

        df = df[FINAL_COLUMNS]

        dfs.append(df)

    combined = pd.concat(dfs, ignore_index=True)
    combined = combined.drop_duplicates(subset=["name", "date"], keep="first")

    output_path = os.path.join(OUTPUT_DIR, "events_combined.csv")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    combined.to_csv(output_path, index=False)
    print(f"\nTotalt {len(combined)} event sparade till {output_path}")

if __name__ == "__main__":
    merge_events()