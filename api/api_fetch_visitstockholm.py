import requests
import pandas as pd
import os

BASE_URL = "https://api.visitstockholm.com/api/public-v1/events/"
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def fetch_all_events():
    events = []
    page = 1

    while True:
        response = requests.get(BASE_URL, params={"page": page})
        data = response.json()
        events.extend(data["results"])
        print(f"Hämtade {len(events)} event...")

        if not data.get("next"):
            break
        page += 1

    return events


def save_events(events):
    df = pd.DataFrame(events)
    output_path = os.path.join(BASE_DIR, "data", "visitstockholm_events.csv")
    df.to_csv(output_path, index=False)
    print(f"Sparade {len(df)} event till {output_path}")


if __name__ == "__main__":
    events = fetch_all_events()
    save_events(events)