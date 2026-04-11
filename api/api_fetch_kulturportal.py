import requests
import pandas as pd
from datetime import datetime
import time

API_KEY = "mge7jublv8ldXpcWwPPmfAdDtelWwHuA"
URL = "https://app.ticketmaster.com/discovery/v2/events"

all_cleaned_events = []

# Vi loopar igenom 5 sidor för att vara säkra på att få med hela året (ca 1000 events totalt)
for page in range(5):
    print(f"Hämtar sida {page}...")

    params = {
        "apikey": API_KEY,
        "city": "Stockholm",
        "size": 200,
        "page": page,
        "sort": "date,asc",
        "locale": "*"
    }

    try:
        response = requests.get(URL, params=params)
        data = response.json()

        if "_embedded" in data:
            events = data["_embedded"]["events"]

            for e in events:
                # Datum och tidhantering
                local_date_str = e.get("dates", {}).get("start", {}).get("localDate")
                local_time_str = e.get("dates", {}).get("start", {}).get("localTime", "00:00:00")

                dt_obj = None
                if local_date_str:
                    try:
                        dt_obj = datetime.strptime(local_date_str, "%Y-%m-%d")
                    except:
                        pass

                # Pris och arena
                price_data = e.get("priceRanges", [{}])[0]
                venue = e.get("_embedded", {}).get("venues", [{}])[0]

                event_info = {
                    "event_id": e.get("id"),
                    "name": e.get("name"),
                    "url": e.get("url"),
                    "image_url": e.get("images", [{}])[0].get("url"),
                    "date": local_date_str,
                    "time": local_time_str,
                    "status": e.get("dates", {}).get("status", {}).get("code"),
                    "segment": e.get("classifications", [{}])[0].get("segment", {}).get("name"),
                    "genre": e.get("classifications", [{}])[0].get("genre", {}).get("name"),
                    "subgenre": e.get("classifications", [{}])[0].get("subGenre", {}).get("name"),
                    "venue_name": venue.get("name"),
                    "venue_city": venue.get("city", {}).get("name"),
                    "venue_address": venue.get("address", {}).get("line1"),
                    "venue_lat": venue.get("location", {}).get("latitude"),
                    "venue_lon": venue.get("location", {}).get("longitude"),
                    "price_min": price_data.get("min"),
                    "price_max": price_data.get("max"),

                    # Tids-extraktion för Power BI
                    "day_of_week": dt_obj.strftime("%A") if dt_obj else None,
                    "month_name": dt_obj.strftime("%B") if dt_obj else None,
                    "month_num": dt_obj.month if dt_obj else None,
                    "year": dt_obj.year if dt_obj else None,
                    "hour": int(local_time_str.split(":")[0]) if local_time_str else None
                }
                all_cleaned_events.append(event_info)
        else:
            # Om det inte finns fler sidor bryter vi loopen
            print("Inga fler events hittades.")
            break

        # Ticketmaster har en gräns på 5 anrop per sekund, så vi pausar lite
        time.sleep(0.3)

    except Exception as e:
        print(f"Ett fel uppstod på sida {page}: {e}")
        break

# Skapa DataFrame och rensa
df = pd.DataFrame(all_cleaned_events)
df = df.drop_duplicates(subset=['event_id'])  # Viktigt! Tar bort dubbletter mellan sidorna
df = df.dropna(subset=['name', 'date'])

# Spara
df.to_csv("events_stockholm_full_year.csv", index=False, encoding='utf-8-sig')

print(f"Klart! Totalt sparades {len(df)} unika events för hela året.")