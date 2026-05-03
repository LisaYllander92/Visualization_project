import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime

def scrape_fasching():
    """Fetch events from Fasching via WordPress AJAX endpoint."""
    url = "https://www.fasching.se/wp-admin/admin-ajax.php"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Referer": "https://www.fasching.se/kalendarium/",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {
        "action":  "fm_ajax_query",
        "orderby": "calendar",
        "curdate": "0",
        "limit":   "100",  # Hämta fler på en gång
        "offset":  "0",
        "year":    "0",
        "month":   "0",
        "day":     "0",
        "search":  "",
        "view":    "default",
        "terms[]": "96"
    }

    print("Fetching events from Fasching AJAX...")
    r = requests.post(url, headers=headers, data=data, timeout=15)
    r.raise_for_status()

    soup = BeautifulSoup(r.text, "html.parser")

    events = []
    for li in soup.select("li.card, li.js-grid-item"):
        try:
            date  = li.get("data-date")
            time  = li.get("data-time")
            name  = li.select_one("h2, h3, .card__title")
            link  = li.select_one("a")
            img   = li.select_one("img")

            events.append({
                "name":       name.text.strip() if name else None,
                "date":       date,
                "time":       time,
                "venue":      "Fasching",
                "address":    "Kungsgatan 63, Stockholm",
                "genre":      "Jazz/Klubb",
                "is_free":    False,
                "image_url":  img["src"] if img else None,
                "url":        link["href"] if link else None,
                "source":     "fasching.se",
                "fetched_at": datetime.today().strftime("%Y-%m-%d")
            })
        except Exception as e:
            print(f"  Skipped one event: {e}")
            continue

    print(f"Found {len(events)} events")
    return pd.DataFrame(events)


if __name__ == "__main__":
    df = scrape_fasching()

    if df.empty:
        print("No events found.")
        print("DEBUG - first 500 chars of response:")
    else:
        print(df[["name", "date", "time"]].to_string())
        df.to_csv("../data/raw/fasching_events.csv", index=False, encoding="utf-8-sig")
        print("\nSaved to fasching_events.csv")