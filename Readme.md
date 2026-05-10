# Spotify Music Trends & Audio Features Analysis

## Project Objective

This project is a fully interactive Plotly Dash dashboard for the Spotify Tracks Dataset. It analyzes popularity, genre behavior, audio features, distributions, and release-year trends across a cleaned dataset of 113,382 tracks.

The dashboard is designed for the course requirement that every Week 1 to Week 9 chart type appears meaningfully in one real-world dataset.

## Dataset

- Name: Spotify Tracks Dataset
- Source: https://www.kaggle.com/datasets/maharshipandya/-spotify-tracksdataset
- Raw file: `dataset.csv`
- Cleaned file used by the dashboard: `spotify_trends_dashboard/dataset_5a/spotify_cleaned.csv`
- Cleaned size: 113,382 rows, 18 columns
- Year range in cleaned data: 1987-2026
- Genres: 114 unique genres

## Main Deliverables

| Deliverable | File |
| --- | --- |
| Dash source code | `spotify_trends_dashboard/app.py` |
| Data preprocessing notebook | `spotify_trends_dashboard/five_a_data_prep.ipynb` |
| Final cleaned dataset | `spotify_trends_dashboard/dataset_5a/spotify_cleaned.csv` |
| Documentation | `Readme.md`, `COVERAGE_CHECKLIST.md`, `INDIVIDUAL_DISCUSSION.md` |
| Citations | `CITATIONS.md` |

## How to Run

From the project root:

```bash
./run.sh
```

Then open:

```text
Dashboard:   http://127.0.0.1:8050
5*A Search:  http://127.0.0.1:5173
```

`run.sh` creates the Python virtual environment if needed, installs missing Python packages, installs 5A Search npm packages if needed, and starts both apps in one terminal.

## Dashboard Interactivity

The dashboard includes four interactive controls plus a filtered-data export:

| Control | Purpose |
| --- | --- |
| Genre dropdown | Filters the full dashboard to one genre or all genres |
| Year range slider | Filters tracks by release year |
| Popularity radio buttons | Filters by All, High, Medium, or Low popularity category |
| Track/artist search input | Searches track names and artist names |
| Download button | Exports the current filtered view as CSV |
| Open 5*A Search button | Opens the companion search app |
| 5*A Assistant panel | Sends the current dashboard context into the assistant app |

All KPIs, charts, and the top-tracks table update through a synchronized Dash callback.

## Required Chart Coverage

| Course Week | Required Chart Type | Dashboard Implementation |
| --- | --- | --- |
| Week 1 | Column chart | Chart 1: Average popularity for top 5 genres |
| Week 1 | Bar chart | Chart 2: Average popularity for bottom 5 genres |
| Week 2 | Clustered column chart | Chart 3: High vs low popularity counts in top genres |
| Week 2 | Clustered bar chart | Chart 4: Danceability vs energy for top artists |
| Week 2 | Stacked column chart | Chart 5: Popularity mix in top genres |
| Week 2 | Stacked bar chart | Chart 6: Popularity mix across latest years |
| Week 3 | Scatter chart | Chart 7: Energy vs valence by popularity category |
| Week 4 | Bubble chart | Chart 8: Danceability vs popularity, sized by duration |
| Week 5 | Histogram chart | Chart 9: Tempo distribution by popularity category |
| Week 6 | Box chart | Chart 10: Loudness by popularity category |
| Week 7 | Violin chart | Chart 11: Acousticness density by popularity category |
| Week 8 | Line chart | Chart 12: Average popularity by year with rolling average |
| Week 9 | Area chart | Chart 13: Track volume by popularity category over time |
| Bonus | Heatmap | Chart 14: Audio feature correlation |

## Data Preprocessing Summary

The preprocessing notebook performs a reproducible ETL workflow:

1. Loads the raw Spotify CSV from the project directory.
2. Standardizes column names into a dashboard-ready schema.
3. Coerces numeric fields such as popularity, tempo, loudness, and audio feature scores.
4. Extracts or enriches release year through a staged fallback process:
   dataset year/release date, local cache, Spotify API when credentials exist, MusicBrainz fallback, artist/genre median imputation, then global fallback.
5. Drops rows missing critical analytical fields.
6. Removes fake or invalid genre labels.
7. Clips values to valid Spotify-style ranges.
8. Converts suspicious duration values and keeps durations between 30 seconds and 15 minutes.
9. Creates `Popularity_Category` with ordered labels:
   Low = 0-29, Medium = 30-69, High = 70-100.
10. Removes duplicates and exports the final cleaned CSV.

## Design Direction

The visual design keeps a black-and-white editorial structure inspired by Zara: large serif title, quiet grid structure, square panels, minimal borders, and high contrast text. The chart marks use a controlled color palette so categories, features, and heatmap values are easier to distinguish during discussion.

## 5*A Assistant Integration

The dashboard includes an assistant panel. It builds a prompt from the current filters, including track count, average popularity, top genre, top artist, and median tempo. Clicking **Open Assistant** launches the companion 5A Search app at:

```text
http://127.0.0.1:5173/?assistant=1&q=...
```

The 5A Search app now has a mounted assistant page using its existing `AIChat` component.

## Team Roles

Replace the placeholder names before final submission if required by your instructor:

| Role | Responsibility |
| --- | --- |
| Data preprocessing lead | Owns `five_a_data_prep.ipynb`, cleaning decisions, final dataset validation |
| Visualization lead | Owns chart selection, chart correctness, Plotly figure functions |
| Dashboard interactivity lead | Owns Dash layout, callbacks, controls, export behavior |
| Documentation and Q&A lead | Owns README, citations, discussion guide, final checklist |

## Academic Integrity

External dataset and library sources are cited in `CITATIONS.md`. AI assistance is allowed by the assignment, but every team member should be able to explain the code, preprocessing choices, and chart purposes during the Q&A discussion.
