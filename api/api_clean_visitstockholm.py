import pandas as pd
import ast
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INPUT_PATH = os.path.join(BASE_DIR, "data", "raw", "visitstockholm_events.csv")
OUTPUT_PATH = os.path.join(BASE_DIR, "data", "output", "visitstockholm_clean.csv")

def parse_dict(val, key="en"):
    try:
        d = ast.literal_eval(val)
        return d.get(key, "")
    except:
        return val

def parse_location(val, key="latitude"):
    try:
        d = ast.literal_eval(val)
        return d.get(key, "")
    except:
        return ""

def parse_category(val, level="segment"):
    try:
        cats = ast.literal_eval(val)
        if not cats:
            return ""
        if level == "segment":
            return cats[0].get("title", "")
        if level == "genre":
            subs = cats[0].get("subcategories", [])
            return subs[0].get("title", "") if subs else ""
        if level == "subgenre":
            subs = cats[0].get("subcategories", [])
            return subs[1].get("title", "") if len(subs) > 1 else ""
    except:
        return ""

def assign_genre(row):
    if pd.notna(row["genre"]):
        return row["genre"]

    name = str(row["name"]).lower()
    segment = str(row["segment"])


    if any(w in name for w in ["food", "mat", "brunch", "dinner", "wine", "beer", "cocktail", "tasting", "chocolate", "oyster", "pasta", "rum", "beermakers", "fermentation"]):
        return "Food & Drink"


    if any(w in name for w in ["tour", "walk", "sightseeing", "guided", "vandring", "visning", "promenad"]):
        return "Guided Tours"

    if any(w in name for w in ["hike", "kayak", "kayaking", "archipelago", "nature", "birdwatch", "camping", "sauna", "bike", "fishing"]):
        return "Nature & Outdoor"


    if any(w in name for w in ["music", "concert", "dance", "festival", "jazz", "blues", "choir", "orchestra", "club", "rave", "party", "disco", "forró"]):
        return "Jazz & Blues" if segment == "Music" else "Culture & Arts"


    if any(w in name for w in ["art", "exhibition", "museum", "gallery", "paint", "craft", "design", "photo"]):
        return "Culture & Arts"


    if any(w in name for w in ["family", "kids", "children", "pippi", "storybook", "easter", "walpurgis", "valborg", "midsummer"]):
        return "Family"


    if any(w in name for w in ["history", "historical", "medieval", "secret", "ghost", "spy", "stockholm", "old town", "gamla stan"]):
        return "Culture & Arts"


    if segment == "Music":
        return "Jazz & Blues"
    if segment == "Arts & Theatre":
        return "Culture & Arts"

    return "Miscellaneous"

def clean():
    df = pd.read_csv(INPUT_PATH)

    df["name"] = df["title"].apply(parse_dict)
    df["venue_lat"] = df["location"].apply(lambda x: parse_location(x, "latitude"))
    df["venue_lon"] = df["location"].apply(lambda x: parse_location(x, "longitude"))
    df["segment"] = df["categories"].apply(lambda x: parse_category(x, "segment"))
    df["genre"] = df["categories"].apply(lambda x: parse_category(x, "genre"))
    df["subgenre"] = df["categories"].apply(lambda x: parse_category(x, "subgenre"))

    df["date"] = pd.to_datetime(df["start_date"], errors="coerce")
    df["day_of_week"] = df["date"].dt.day_name()
    df["month_name"] = df["date"].dt.month_name()
    df["month_num"] = df["date"].dt.month
    df["year"] = df["date"].dt.year
    df["hour"] = pd.to_datetime(df["start_time"], errors="coerce").dt.hour
    df["date"] = df["date"].dt.strftime("%Y-%m-%d")

    df = df.drop(columns=["url"], errors="ignore")

    result = df.rename(columns={
        "id": "event_id",
        "external_website_url": "url",
        "address": "venue_address",
        "city": "venue_city",
    })

    result["image_url"] = ""
    result["status"] = "onsale"
    result["time"] = df["start_time"]

    columns = [
        "event_id", "name", "url", "image_url", "date", "time", "status",
        "segment", "genre", "subgenre", "venue_name", "venue_city",
        "venue_address", "venue_lat", "venue_lon", "day_of_week",
        "month_name", "month_num", "year", "hour"
    ]

    tm = pd.read_csv(os.path.join(BASE_DIR, "data", "output", "events_full_year.csv"))
    result["name_lower"] = result["name"].str.lower().str.strip()
    tm["name_lower"] = tm["name"].str.lower().str.strip()

    overlap_keys = set(zip(tm["name_lower"], tm["date"]))
    result = result[~result.apply(lambda r: (r["name_lower"], r["date"]) in overlap_keys, axis=1)]
    result = result.drop(columns=["name_lower"])
    result = result.replace("", pd.NA)
    result = result.dropna(subset=["venue_lat", "venue_lon"])

    venues_to_remove = [
        "Stockholmsmässan",
        "Kistamässan",
        "Nacka Strandsmässan",
        "Various places in Stockholm",
        "Multiple places across the City of Stockholm",
        "Various locations in Stockholm",
        "Several places in Stockholm",
        "Several different venues in Stockholm. For more information, visit the official website for the event.",
        "Djurönäset",
        "Grinda",
        "Grinda Wärdshus",
        "Vaxholms Gästhamn",
        "Vaxholms Bed & Breakfast",
        "Utö Värdshus",
        "Furusunds Gästhamn",
        "Siggesta Gård",
        "Rotebro, Sollentuna",
        "Kapellet Norrtälje",
        "En del av E4 Förbifart Stockholm",
    ]

    result = result[~result["venue_name"].isin(venues_to_remove)]

    result.loc[
        result["name"].str.contains("Grändernas hemligheter", na=False),
        "venue_name"
    ] = "Slottsbacken"


    result["genre"] = result.apply(assign_genre, axis=1)

    segment_mapping = {
        "Music": "Music",
        "Exhibitions": "Arts & Theatre",
        "Stage & Film": "Arts & Theatre",
        "Guided tours": "Arts & Theatre",
        "Family": "Arts & Theatre",
        "Clubs & Parties": "Music",
        "Festivals": "Music",
        "Fairs": "Miscellaneous",
        "Eat & Drink": "Miscellaneous",
        "Networking & Community": "Miscellaneous",
        "Science & Tech": "Miscellaneous",
        "Careers & Leadership": "Miscellaneous",
        "Sports & Wellbeing": "Sports",
    }

    result["segment"] = result["segment"].map(segment_mapping)


    result.loc[result["name"] == "Empire of the Sun", "url"] = "https://www.livenation.se/event/empire-of-the-sun-stockholm-tickets-edp1648175"


    result = result[result["url"].notna() & (result["url"] != "")]

    default_images = {
        "Music": "https://images.unsplash.com/...",
        "Arts & Theatre": "https://images.unsplash.com/...",
        "Miscellaneous": "https://images.unsplash.com/...",
        "Sports": "https://images.unsplash.com/...",
    }

    result["image_url"] = result.apply(
        lambda r: r["image_url"] if pd.notna(r["image_url"]) and r["image_url"] != ""
        else default_images.get(r["segment"], ""),
        axis=1
    )

    result[columns].to_csv(OUTPUT_PATH, index=False)
    print(f"Sparade {len(result)} event till {OUTPUT_PATH}")

if __name__ == "__main__":
    clean()