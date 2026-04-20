import pandas as pd
import numpy as np
import re


def get_opening_hours(hours_string):
    """
    Extracts opening and closing hours from the string.
    Returns None, None if no valid data found (= treat as closed all day).
    """
    try:
        times = re.findall(r'(\d{2}:\d{2})', str(hours_string))
        if len(times) >= 2:
            start_hour = int(times[0].split(':')[0])
            end_hour = int(times[1].split(':')[0])
            return start_hour, end_hour
    except:
        pass
    return None, None


def get_day_profile(day_id):
    """
    Returns (base_load, peak_offset) per day type.
    peak_offset shifts the bell curve earlier (negative) or later (positive).
    """
    if day_id == 6:    # Lördag
        return 90, -1.5
    elif day_id == 7:  # Söndag
        return 85, -1.0
    elif day_id == 5:  # Fredag
        return 72, 0.5
    elif day_id == 1:  # Måndag
        return 58, 0.5
    else:              # Tisdag–torsdag
        return 63, 0.0


def generate_weekly_activity():
    # Load the museum data
    df_museums = pd.read_csv("stockholm_museums.csv")

    # Define days and their sort order
    days = [
        {"name": "Monday",    "id": 1},
        {"name": "Tuesday",   "id": 2},
        {"name": "Wednesday", "id": 3},
        {"name": "Thursday",  "id": 4},
        {"name": "Friday",    "id": 5},
        {"name": "Saturday",  "id": 6},
        {"name": "Sunday",    "id": 7}
    ]

    activity_rows = []

    for _, museum in df_museums.iterrows():
        start, end = get_opening_hours(museum.get('opening_hours', ''))

        for day in days:
            base_load, peak_offset = get_day_profile(day['id'])

            for hour in range(9, 21):
                busy_index = 0

                # Om inga öppettider finns, eller utanför öppettid → 0
                if start is not None and start <= hour < end:
                    mid_point = (start + end) / 2 + peak_offset
                    dist_from_peak = abs(hour - mid_point)
                    busy_index = base_load - (dist_from_peak * 11)

                    # Brus proportionellt mot aktivitetsnivån
                    noise_range = max(5, int(busy_index * 0.18))
                    busy_index += np.random.randint(-noise_range, noise_range)

                    # Öppet = minst 1, max 100
                    busy_index = max(1, min(100, int(busy_index)))

                activity_rows.append({
                    "museum_name":  museum['name'],
                    "day_of_week":  day['name'],
                    "day_num":      day['id'],
                    "hour":         hour,
                    "hour_display": f"{hour:02d}:00",
                    "busy_index":   busy_index
                })

    df_activity = pd.DataFrame(activity_rows)
    df_activity.to_csv("museum_activity.csv", index=False)
    print(f"Success! Generated {len(df_activity)} rows of weekly activity data.")


# Run the simulation
generate_weekly_activity()