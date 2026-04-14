import requests
import pandas as pd

API_KEY = "TICKETMASTER_API_KEY"

# Find events and filter your search by location, date, availability, and much more.
URL = "https://app.ticketmaster.com/discovery/v2/events"


# Parameters to set API limit
params = {
    "apikey": API_KEY,
    "city": "Stockholm",
    "size": 200
}

response = requests.get(URL, params=params)
data = response.json()

# Check if Key exists
if "_embedded" in data:
    events = data["_embedded"]["events"]
    df = pd.DataFrame(events)
    df.to_csv("events.csv", index=False)
    print(f"Success! Fetched {len(df)} events.")
    print(df.head())
else:
    # If API didn't find anything or missing Key.
    print("No events found for this search. No file created.")
    events = []