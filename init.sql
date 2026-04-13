-- table to store raw data
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

-- table to store cleaned data
CREATE TABLE IF NOT EXISTS events_clean (
    event_id        VARCHAR PRIMARY KEY,
    name            VARCHAR NOT NULL,
    url             VARCHAR,
    image_url       VARCHAR,
    date            DATE,
    time            VARCHAR,
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

-- table to store search events (for statistics)
-- CREATE TABLE IF NOT EXISTS events_search (
--    id SERIAL PRIMARY KEY,
--    query VARCHAR(255) NOT NULL,
--    searched_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
