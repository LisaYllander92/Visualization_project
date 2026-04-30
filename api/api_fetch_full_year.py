import requests
import pandas as pd
from datetime import datetime
import time
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("TICKETMASTER_KEY")
URL = "https://app.ticketmaster.com/discovery/v2/events"

all_events = []

# Loop through all five pages to make sure we get all the data for this year.
for page in range(5):
    print(f"Retrieve page {page}...")

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
                # 1. Managing date and time
                local_date_str = e.get("dates", {}).get("start", {}).get("localDate")
                local_time_str = e.get("dates", {}).get("start", {}).get("localTime", "00:00:00")

                dt_obj = None
                if local_date_str:
                    try:
                        dt_obj = datetime.strptime(local_date_str, "%Y-%m-%d")
                    except:
                        pass

                # 2. Fetch location information for venue
                venue = e.get("_embedded", {}).get("venues", [{}])[0]

                # 3. Structure data
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

                    # Time units for Power BI-filter and graphs
                    "day_of_week": dt_obj.strftime("%A") if dt_obj else None,
                    "month_name": dt_obj.strftime("%B") if dt_obj else None,
                    "month_num": dt_obj.month if dt_obj else None,
                    "year": dt_obj.year if dt_obj else None,
                    "hour": int(local_time_str.split(":")[0]) if local_time_str else None
                }
                all_events.append(event_info)
        else:
            print("No more events found.")
            break

        # Ticketmaster has a limit for five API-calls per second
        time.sleep(0.3)

    except Exception as e:
        print(f"Error occurred on page {page}: {e}")
        break

df = pd.DataFrame(all_events)

# Only runs if we have the data
if not df.empty:
    print("Cleaning data...")
    df = df.drop_duplicates(subset=['event_id'])
    df = df.dropna(subset=['name', 'date'])

    df["time"] = pd.to_datetime(df["time"], format="mixed", errors="coerce").dt.strftime("%H:%M")

    # Spara till csv-fil
    df.to_csv("../data/events_full_year.csv", index=False, encoding='utf-8-sig')
    print(f"Done! Total saved {len(df)} unique events for the entire year.")
else:
    print("Empty DataFrame because no events was found for this search. No file created.")