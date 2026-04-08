-- table to store raw data
CREATE TABLE IF NOT EXISTS staging_events (
    id SERIAL PRIMARY KEY,
    raw_data TEXT NOT NULL,
    ingested_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- table to store cleaned data
CREATE TABLE IF NOT EXISTS curated_events (
    id SERIAL PRIMARY KEY,
    name VARCHAR(250) NOT NULL,
    url TEXT NOT NULL,
    image TEXT,
    date DATE,
    time TIMESTAMP,
    status TEXT,
    segment TEXT,
    genre TEXT,
    subgenre TEXT,
    venue_name TEXT,
    adress TEXT,
    venue_lat FLOAT,
    venue_lon FLOAT
);

-- table to store search events (for statistics)
CREATE TABLE IF NOT EXISTS events_search (
    id SERIAL PRIMARY KEY,
    query VARCHAR(255) NOT NULL,
    searched_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
