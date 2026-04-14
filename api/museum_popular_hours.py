import numpy as np
import pandas as pd
import os


def generate_hourly_activity(museum_df):
    """
    Creates simulated hourly activity data (foot traffic) for museums
    to visualize busy periods throughout the day.
    """
    hourly_rows = []

    # Define the time range (from 09:00 to 21:00)
    hours = list(range(9, 22))

    for _, museum in museum_df.iterrows():
        # Using 'name' as the primary key to link with the main museum file
        museum_name = museum['name']

        for hour in hours:
            # Simulate foot traffic using a normal distribution (Bell Curve)
            # Peak activity is set around 14:00 (2 PM)
            # Formula: 100 * exp(-((x - mu)**2) / (2 * sigma**2))
            mu = 14  # Peak hour
            sigma = 3  # Spread of the curve

            base_pop = 100 * np.exp(-((hour - mu) ** 2) / (2 * sigma ** 2))

            # Add random noise to make the data look more organic/realistic
            random_noise = np.random.randint(-5, 5)
            busy_score = max(0, min(100, int(base_pop + random_noise)))

            # Reduce activity score if it's outside typical peak operating hours
            if hour > 20 or hour < 10:
                busy_score = int(busy_score * 0.2)

            hourly_rows.append({
                "museum_name": museum_name,
                "hour": hour,
                "hour_display": f"{hour:02d}:00",
                "busy_index": busy_score
            })

    # Create DataFrame and save to CSV
    hourly_df = pd.DataFrame(hourly_rows)
    output_file = "museum_activity.csv"
    hourly_df.to_csv(output_file, index=False, encoding="utf-8-sig")

    print(f"Success! Simulated activity data saved to: {output_file}")
    print(f"Total rows generated: {len(hourly_df)}")


# --- Execution Block ---
if __name__ == "__main__":
    input_file = "stockholm_museums.csv"

    if os.path.exists(input_file):
        # Load the existing museum data
        df_museums = pd.read_csv(input_file)
        # Run the generator
        generate_hourly_activity(df_museums)
    else:
        print(f"Error: Could not find '{input_file}'.")
        print("Please make sure your museum scraper has run successfully first.")