import pandas as pd
import numpy as np
import re


def get_opening_hours(hours_string):
    """
    Extracts opening and closing hours from the string.
    Default is set to 10:00 - 18:00 if no data is found.
    """
    try:
        # Look for time patterns like HH:MM – HH:MM
        times = re.findall(r'(\d{2}:\d{2})', str(hours_string))
        if len(times) >= 2:
            start_hour = int(times[0].split(':')[0])
            end_hour = int(times[1].split(':')[0])
            return start_hour, end_hour
    except:
        pass
    return 10, 18


def generate_weekly_activity():
    # Load the museum data
    df_museums = pd.read_csv("stockholm_museums.csv")

    # Define days and their sort order
    days = [
        {"name": "Monday", "id": 1},
        {"name": "Tuesday", "id": 2},
        {"name": "Wednesday", "id": 3},
        {"name": "Thursday", "id": 4},
        {"name": "Friday", "id": 5},
        {"name": "Saturday", "id": 6},
        {"name": "Sunday", "id": 7}
    ]

    activity_rows = []

    for _, museum in df_museums.iterrows():
        # Get individual opening hours for the museum
        start, end = get_opening_hours(museum.get('opening_hours', ''))

        for day in days:
            is_weekend = day['id'] >= 6

            for hour in range(9, 21):
                busy_index = 0

                # Check if the museum is open during this hour
                if start <= hour < end:
                    # Logic: Create a "peak" in the middle of the opening period
                    mid_point = (start + end) / 2
                    dist_from_peak = abs(hour - mid_point)

                    # Weekend logic: Higher base load (more tourists/families)
                    base_load = 85 if is_weekend else 65

                    # Calculate busy level based on distance from peak time
                    busy_index = base_load - (dist_from_peak * 12)

                    # Add random noise to make data look authentic
                    busy_index += np.random.randint(-15, 15)

                # Ensure values stay within 0-100 range
                busy_index = max(0, min(100, int(busy_index)))

                activity_rows.append({
                    "museum_name": museum['name'],
                    "day_of_week": day['name'],
                    "day_num": day['id'],  # Used for sorting in Power BI
                    "hour": hour,
                    "hour_display": f"{hour:02d}:00",
                    "busy_index": busy_index
                })

    # Save to CSV
    df_activity = pd.DataFrame(activity_rows)
    df_activity.to_csv("museum_activity.csv", index=False)
    print(f"Success! Generated {len(df_activity)} rows of weekly activity data.")


# Run the simulation
generate_weekly_activity()