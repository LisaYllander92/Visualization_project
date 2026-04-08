import requests
import pandas as pd

API_KEY = "mge7jublv8ldXpcWwPPmfAdDtelWwHuA"

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

events = data["_embedded"]["events"]

df = pd.DataFrame(events)
df.to_csv("events.csv", index=False)
print(df.head())