""" ETL = Extract, Transform, Load
   Extract : read events_full.csv
   Transform : validate, flag, clean
   Load   :write to PostgreSQL + export cleaned.csv and rejected.csv"""



import os

import pandas as pd
from sqlalchemy import text
from app.db import get_engine

""" __file__ is the path to this script. We go one level up (..) to reach the
project root, then point to folder data(CSV) and the output folder."""

#BASE_DIR = os.path.join(os.path.dirname(__file__), "..")

"""CSV_PATH = os.path.join(BASE_DIR, "data", "events_full.csv")
OUTPUT_DIR = os.path.join(BASE_DIR, "output")
os.makedirs(OUTPUT_DIR, exist_ok=True)"""

csv_file = "data/events_full.csv"

OUTPUT_DIR = os.path.abspath("data/output")
os.makedirs(OUTPUT_DIR, exist_ok=True)


# EXTRACT
def extract() -> pd.DataFrame:
    print("\n[EXTRACT] Loading CSV...")
    df = pd.read_csv(csv_file)

    # Drop empty price and fetched_at columns
    df = df.drop(columns=[c for c in ["price_min", "price_max", "price_currency","fetched_at" ] if c in df.columns])

    print(f"[EXTRACT] Rows: {len(df)}")
    return df

# TRANSFORM (Validate + Clean)

def transform(df: pd.DataFrame):
    rejected = []

    df = df.copy()

    #  Reject: missing ID 
    mask = df["event_id"].isna() | (df["event_id"].str.strip() == "")
    rejected.append(df[mask].assign(rejected_reason="Missing event_id"))
    df = df[~mask] 

    # Reject: missing name 
    mask = df["name"].isna() | (df["name"].str.strip() == "")
    rejected.append(df[mask].assign(rejected_reason="Missing name"))
    df = df[~mask]

    #  Reject: invalid date
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    mask = df["date"].isna()
    rejected.append(df[mask].assign(rejected_reason="Invalid date"))
    df = df[~mask]

    #  Reject: duplicates
    mask = df.duplicated("event_id")
    rejected.append(df[mask].assign(rejected_reason="Duplicate event_id"))
    df = df[~mask]

    #  Clean time
    df["time"] = pd.to_datetime(df["time"], format= "mixed", errors="coerce").dt.strftime("%H:%M")

    """ Derive extra time columns for analysis
    These are useful for the charts (e.g. "how many events per month?")"""
    #  Derived columns
    df["day_of_week"] = df["date"].dt.day_name()
    df["month_name"] = df["date"].dt.strftime("%B")
    df["month_num"] = df["date"].dt.month
    df["year"] = df["date"].dt.year
    df["hour"] = pd.to_datetime(df["time"], format= "mixed", errors="coerce").dt.hour

    #month ordering 

    df["month_name"] = pd.Categorical(
    df["month_name"],
    categories=[
        "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"
    ],
    ordered=True
)
    

    #Fill missing values 
    df["venue_name"] = df["venue_name"].replace("", None).fillna("Unknown Venue")

    for col in ["segment", "genre", "subgenre"]:
        df[col] = df[col].replace("", None).fillna("Unknown")

    df["venue_city"] = df["venue_city"].replace("", None).fillna("Stockholm")

    #Strip whitespace 
    text_cols = ["name", "segment", "genre", "subgenre", "venue_name", "venue_city"]
    for col in text_cols:
        if col in df.columns:
            df[col] = df[col].str.strip()


    # Combine rejected
    rejected_df = pd.concat(rejected, ignore_index=True) if rejected else pd.DataFrame()

    print(f"[TRANSFORM] Clean: {len(df)} | Rejected: {len(rejected_df)}")

    return df, rejected_df


def ensure_tables(engine):
    
        ddl = """
        CREATE TABLE IF NOT EXISTS events_raw (
            event_id        VARCHAR PRIMARY KEY,
            name            VARCHAR,
            url             VARCHAR,
            image_url       VARCHAR,
            date            DATE,
            time            VARCHAR,
            status          VARCHAR,
            venue_id        VARCHAR,
            category_id     INTEGER,
            segment         VARCHAR,
            genre           VARCHAR,
            subgenre        VARCHAR,
            venue_name      VARCHAR,
            venue_city      VARCHAR,
            venue_address   VARCHAR,
            venue_lat       DOUBLE PRECISION,
            venue_lon       DOUBLE PRECISION
        );

        CREATE TABLE IF NOT EXISTS events_clean (
            event_id        VARCHAR PRIMARY KEY,
            name            VARCHAR NOT NULL,
            url             VARCHAR,
            image_url       VARCHAR,
            date                DATE,
            time      VARCHAR,
            status          VARCHAR,
            segment         VARCHAR,
            genre           VARCHAR,
            subgenre        VARCHAR,
            venue_name      VARCHAR,
            venue_city      VARCHAR,
            venue_address   VARCHAR,
            venue_lat       DOUBLE PRECISION,
            venue_lon       DOUBLE PRECISION,
            day_of_week     VARCHAR,
            month_name      VARCHAR,
            month_num       INTEGER,
            year            INTEGER,
            hour            INTEGER
        );
        """
        with engine.connect() as conn:
            conn.execute(text(ddl))
            conn.commit()


def load(clean_df: pd.DataFrame, raw_df: pd.DataFrame, engine):
    

    print("\n[LOAD] Writing to PostgreSQL...")

    with engine.connect() as conn:
        conn.execute(text("TRUNCATE TABLE events_clean"))
        conn.execute(text("TRUNCATE TABLE events_raw"))
        conn.commit()

    raw_df.to_sql("events_raw", con=engine, if_exists="append", index=False, method="multi")


    
        # Write cleaned data to events_clean
       # Only keep columns that exist in the events_clean table schema
        # Only write columns that exist in the events_clean schema
    clean_cols = [
            "event_id", "name", "url", "image_url", "date", "time",
             "status", "segment", "genre", "subgenre", "venue_name", "venue_city",
             "venue_address", "venue_lat", "venue_lon",
              "day_of_week", "month_name", "month_num", "year", "hour",
        ]
     
    clean_df[[c for c in clean_cols if c in clean_df.columns]].to_sql(
           "events_clean", con=engine, if_exists="append", index=False, method="multi"
     )

    print(f"[LOAD] Raw: {len(raw_df)} | Clean: {len(clean_df)}")


# EXPORT

def export(clean_df, rejected_df):
    clean_path = os.path.join(OUTPUT_DIR, "clean.csv")
    rejected_path = os.path.join(OUTPUT_DIR, "rejected.csv")

    clean_df.to_csv(clean_path, index=False)
    rejected_df.to_csv(rejected_path, index=False)

    print(f"[EXPORT] CSV files saved:\n  - {clean_path}\n  - {rejected_path}")

    #print("[EXPORT] CSV files saved")


# RUN PIPELINE

def run():
    print("\n=== Events Pipeline ===")

    # Step 1: Extract
    raw = extract()

    # Step 2: Transform
    clean, rejected = transform(raw)

   
    try:
        engine = get_engine()
        ensure_tables(engine)
        load(clean, raw, engine)
    except Exception as e:
        print(f"[LOAD ERROR] {e}")
        print("Skipping DB load...")


    # Step 4: Export
    export(clean, rejected)

    

    print("\nPipeline complete ")


if __name__ == "__main__":
    run()