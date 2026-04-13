import requests
import pandas as pd

MY_TOKEN = 'FJFYXZFFKJJHZK3OYI4N'

# Vi testar den mest klassiska sök-endpointen
# Vi lägger till expand=venue för att få med platsen direkt
url = "https://www.eventbriteapi.com/v3/events/search/"

params = {
    "location.address": "Stockholm",
    "location.within": "10km",
    "expand": "venue"
}

headers = {
    "Authorization": f"Bearer {MY_TOKEN}"
}

print("Försöker hämta publika events via search-funktionen...")

response = requests.get(url, headers=headers, params=params)

if response.status_code == 200:
    data = response.json()
    events = data.get('events', [])

    if events:
        df = pd.DataFrame(events)
        # Snyggar till namnet
        df['event_name'] = df['name'].apply(lambda x: x.get('text') if isinstance(x, dict) else x)

        print(f"Hittade {len(df)} events!")
        df.to_csv('eventbrite_data.csv', index=False)
        print("Klar! Filen 'eventbrite_data.csv' skapad.")
    else:
        print("Inga events hittades för Stockholm.")
else:
    print(f"Det gick inte. Status: {response.status_code}")
    print("Svar från Eventbrite:", response.text)