# Stockholm Events & Culture — Visualization Project

A data engineering and visualization project that aggregates events, museums and cultural activities in Stockholm from multiple open APIs. Built as part of a collaborative DE + UX school project.

---

## Project overview

The goal is to collect, clean and visualize data about what's happening in Stockholm — concerts, theatre, exhibitions, museums and more — to support data-driven decisions and present insights through dashboards and storytelling.

---

## Data sources

| Source | Type | Content |
|---|---|---|
| Ticketmaster Discovery API | REST API | Events, concerts, sport, theatre |
| Eventbrite API | REST API | Local events, exhibitions, workshops |
| Riksteatern | RSS feed | Theatre and performing arts |
| Google Places API (New) | REST API | Museums, addresses, opening hours, ratings |

---

## Project structure

```
visualization_project/
├── api/
│   ├── fetch_data_ticketmaster.py   # Fetch events from Ticketmaster
│   ├── fetch_data_kulturbas.py      # Fetch Stockholm museums via Google Places
│   ├── populate_times.py            # Popularity score based on ratings + reviews
│   └── normalizer.py                # Normalize data from all sources to unified format
├── eda/
│   └──                              # EDA notebooks (pandas + duckdb) — to be added
├── dashboards/
│   └──                              # Power BI and Streamlit dashboards — to be added
├── .env                             # API keys (not tracked in Git)
├── .gitignore
└── README.md
```

---

## Setup

### 1. Clone the repo
```bash
git clone https://github.com/<your-username>/visualization_project.git
cd visualization_project
```

### 2. Install dependencies
```bash
uv sync
```

### 3. Add API keys
Create a `.env` file in the project root:
```
TICKETMASTER_KEY=your_key_here
EVENTBRITE_TOKEN=your_token_here
GOOGLE_PLACES_KEY=your_key_here
```

### 4. Run data fetching scripts
```bash
uv run api/fetch_data_ticketmaster.py
uv run api/fetch_data_kulturbas.py
```

---

## API setup

| API | Where to get key |
|---|---|
| Ticketmaster | developer.ticketmaster.com |
| Eventbrite | eventbrite.com/platform/api |
| Google Places (New) | console.cloud.google.com → Enable "Places API (New)" |

---

## Output data

| File | Description |
|---|---|
| `events_full_year.csv` | All Stockholm events from Ticketmaster |
| `stockholm_museums_google.csv` | Museums with address, opening hours, rating |
| `stockholm_museums_full_popularity.csv` | Museums with popularity index (0–100) and free admission flag |

> CSV files are excluded from Git via `.gitignore`.

---

## Deliverables

- [ ] EDA per team member (pandas + duckdb)
- [ ] Power BI dashboard with KPIs, filters, line chart and bar chart
- [ ] Min. 2 data storytelling graphs in matplotlib
- [ ] Streamlit dashboard (VG)
- [ ] Deployed Streamlit app (VG)

---

## Team

<!-- Add names here -->

---

## Status

> Work in progress — data collection complete, EDA and dashboards in progress.