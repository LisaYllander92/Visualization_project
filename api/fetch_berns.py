import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime

def scrape_berns():
    """Scrape upcoming events from Berns website."""
    url = "https://www.berns.se/kalender/"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}

    print("Fetching events from Berns...")
    r = requests.get(url, headers=headers, timeout=15)
    r.raise_for_status()

    soup = BeautifulSoup(r.text, "html.parser")

    events = []
    for item in soup.select("div.calender-item"):
        try:
            name  = item.select_one(".citem-title h5")
            date  = item.select_one(".citem-meta")
            link  = item.select_one("a")
            img   = item.select_one("img")

            if not name:
                continue

            raw_date = date.text.strip() if date else ""
            clean_date = raw_date.split("\n")[0].strip()

            # Convert date to "YYYY-MM-DD"
            try:
                clean_date = datetime.strptime(clean_date, "%d %B %Y").strftime("%Y-%m-%d")
            except:
                pass  # Keep original format if it fails

            events.append({
                "name":       name.text.strip(),
                "date":       clean_date,
                "venue":      "Berns",
                "address":    "Berzelii Park, Stockholm",
                "genre":      "Klubb/Konsert",
                "is_free":    False,
                "image_url":  img["src"] if img else None,
                "url":        link["href"] if link else None,
                "source":     "berns.se",
                "fetched_at": datetime.today().strftime("%Y-%m-%d")
            })
        except Exception as e:
            print(f"  Skipped one event: {e}")
            continue

    df = pd.DataFrame(events).drop_duplicates(subset=["name"])
    print(f"Found {len(df)} events")
    return df


if __name__ == "__main__":
    df = scrape_berns()

    if df.empty:
        print("No events found.")
    else:
        print(df[["name", "date"]].to_string())
        df.to_csv("../data/raw/berns_events.csv", index=False, encoding="utf-8-sig")
        print("\nSaved to berns_events.csv")