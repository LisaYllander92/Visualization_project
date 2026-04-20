import pandas as pd
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_DIR = os.path.join(BASE_DIR, "data", "output")

def merge_events():
    files = {
        "ticketmaster": os.path.join(BASE_DIR, "api", "events_full_year.csv"),
        "visitstockholm": os.path.join(BASE_DIR, "data", "output", "visitstockholm_clean.csv"),
        "fasching": os.path.join(BASE_DIR, "api", "fasching_events.csv"),
        "berns": os.path.join(BASE_DIR, "api", "berns_events.csv"),
    }

    dfs = []
    for source, path in files.items():
        if os.path.exists(path):
            df = pd.read_csv(path)
            df["source"] = source
            dfs.append(df)
            print(f"Laddade {len(df)} event från {source}")
        else:
            print(f"Varning: {path} finns inte, hoppar över")

    combined = pd.concat(dfs, ignore_index=True)
    output_path = os.path.join(OUTPUT_DIR, "events_combined.csv")
    combined.to_csv(output_path, index=False)
    print(f"\nTotalt {len(combined)} event sparade till {output_path}")

if __name__ == "__main__":
    merge_events()