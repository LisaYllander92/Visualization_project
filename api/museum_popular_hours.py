import pandas as pd
import numpy as np
import re


def get_open_hours(hours_string):
    """ Extract opening hours. Set 10-18 to default if data is missing. """
    try:
        # Searching for time in format HH:MM – HH:MM
        times = re.findall(r'(\d{2}:\d{2})', hours_string)
        if len(times) >= 2:
            start_hour = int(times[0].split(':')[0])
            end_hour = int(times[1].split(':')[0])
            return start_hour, end_hour
    except:
        pass
    return 10, 18


def generate_smart_activity():
    df_museums = pd.read_csv("stockholm_museums.csv")
    activity_rows = []

    for _, museum in df_museums.iterrows():
        start, end = get_open_hours(str(museum.get('opening_hours', '')))

        for hour in range(8, 21):
            # Base-activity (0 if it's closed, else simulating a random time)
            if start <= hour < end:
                # Creates a curve: more activity during mid day
                mid_point = (start + end) / 2
                dist_from_mid = abs(hour - mid_point)
                busy_index = max(10, 100 - (dist_from_mid * 15))
                # Add randomness
                busy_index += np.random.randint(-10, 10)
                busy_index = min(100, max(0, busy_index))
            else:
                busy_index = 0  # Closed!

            activity_rows.append({
                "name": museum['name'],
                "hour": hour,
                "hour_display": f"{hour:02d}:00",
                "busy_index": int(busy_index)
            })

    df_activity = pd.DataFrame(activity_rows)
    df_activity.to_csv("museum_activity.csv", index=False)
    print("Activity generated based on opening hours!")


generate_smart_activity()