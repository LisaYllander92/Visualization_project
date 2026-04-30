# STHLMs Puls — Stockholm Events Visualization

A data engineering and visualization project that aggregates events, museums 
and cultural activities in Stockholm from multiple sources. Built as part of 
a collaborative DE25 school project.

## Project Overview

The goal is to collect, clean and visualize data about what's happening in 
Stockholm — concerts, theatre, exhibitions, museums and more — presented 
through an interactive Power BI dashboard and data storytelling graphs.

## Data Sources

| Source | Type | Content |
|--------|------|---------|
| Ticketmaster Discovery API | REST API | Events, concerts, sport, theatre |
| VisitStockholm | Web scrape/API | Cultural events, exhibitions, guided tours |
| Fasching | Custom fetch | Jazz & club events |
| Berns | Custom fetch | Music & nightlife events |
| Google Places API | REST API | Museums, addresses, opening hours, ratings |
| Open-Meteo API | REST API | Weather forecast for Stockholm |

## Project Structure
visualization_project/
├── api/
│   ├── api_fetch_full_year.py      # Fetch events from Ticketmaster
│   ├── api_fetch_visitstockholm.py # Fetch events from VisitStockholm
│   ├── api_fetch_museum.py         # Fetch museums via Google Places
│   ├── api_clean_visitstockholm.py # Clean and classify VisitStockholm data
│   ├── fetch_fasching.py           # Fetch Fasching events
│   ├── fetch_berns.py              # Fetch Berns events
│   ├── fetch_weather.py            # Fetch weather data
│   ├── merge_events.py             # Merge all event sources
│   └── museum_activity.py          # Museum popularity scores
├── eda/
│   ├── eda_rickard.ipynb           # EDA - Rickard
│   ├── eda_lisa.ipynb              # EDA - Lisa
│   ├── eda_dennis.ipynb            # EDA - Dennis
│   └── eda_mossad.ipynb            # EDA - Mossad
├── data/
│   ├── raw/                        # Raw fetched data
│   └── output/                     # Cleaned and merged data
├── .env                            # API keys (not tracked in Git)
├── .gitignore
└── README.md

## Setup

### 1. Clone the repo
```bash
git clone https://github.com/rickardgarnau-byte/datavisualization_course.git
cd datavisualization_course
```

### 2. Install dependencies
```bash
uv sync
```

### 3. Add API keys
Create a `.env` file in the project root:
TICKETMASTER_KEY=your_key_here
GOOGLE_PLACES_KEY=your_key_here

### 4. Fetch and process data
```bash
uv run api/api_fetch_full_year.py
uv run api/api_fetch_visitstockholm.py
uv run api/api_fetch_museum.py
uv run api/api_clean_visitstockholm.py
uv run api/merge_events.py
```

## API Setup

| API | Where to get key |
|-----|-----------------|
| Ticketmaster | developer.ticketmaster.com |
| Visit Stockholm | https://api.visitstockholm.com/ |
| Google Places (New) | console.cloud.google.com → Enable "Places API (New)" |
| Open-Meteo | No key needed — free and open |

## Output Data

| File | Description |
|------|-------------|
| events_full_year.csv | All Stockholm events from Ticketmaster |
| visitstockholm_clean.csv | Cleaned VisitStockholm events |
| events_combined.csv | Merged events from all sources (~1200 events) |
| stockholm_museums.csv | Museums with address, opening hours, rating |
| museum_activity.csv | Museums with popularity index and free admission flag |

CSV files are excluded from Git via `.gitignore`.

## Deliverables

- [x] EDA per team member (pandas + duckdb)
- [x] Power BI dashboard with KPIs, filters, bar charts and pie charts
- [x] Published Power BI dashboard
- [x] Min. 2 data storytelling graphs in matplotlib

## Known Data Quality Issues

- VisitStockholm API uses "Jazz & Blues" as default genre for unclassified 
  music events. We handle this with a custom `assign_genre()` function that 
  reclassifies events based on event name.
- VisitStockholm events lack time data (only date available).

## Team

| Name | Role |
|------|------|
| Rickard | Startsida, Scenkonst, Nattliv, data pipeline |
| Lisa | Museum, semantic model, data pipeline |
| Dennis | Musik |
| Mossad | Övrigt |

## Status

Complete — data collection, cleaning, EDA and Power BI dashboard done.
