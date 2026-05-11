# Individual Discussion Guide

Use this guide to prepare for the project Q&A. Every team member should be able to explain the parts they worked on and the overall dashboard flow.

## Project Objective

The dashboard analyzes Spotify track popularity, genre differences, audio-feature relationships, feature distributions, and year-based trend movement using one cleaned real-world dataset.

## Data Preprocessing Talking Points

- The raw file is `dataset.csv` from Kaggle.
- The notebook maps raw columns into a consistent schema used by the dashboard.
- Numeric features such as popularity, duration, danceability, energy, valence, tempo, loudness, and acousticness are converted to numeric values.
- Invalid or missing analytical fields are removed so the charts do not use incomplete records.
- Year values come from available release information or the Spotify API year file generated from track IDs.
- Popularity is grouped into ordered categories:
  Low = 0-29, Medium = 30-69, High = 70-100.

## Dashboard Interactivity Talking Points

- The genre dropdown, year range slider, popularity radio buttons, and search input are Dash controls.
- A shared callback filters the dataset once, then updates KPIs, charts, assistant prompt, and the table.
- The download button exports only the currently filtered data.

## Chart Explanation Prompts

- Comparison charts answer which genres, artists, and popularity categories differ most.
- Relationship charts show whether audio features move together or relate to popularity.
- Distribution charts show spread, skew, medians, outliers, and density.
- Time-series charts show how popularity and track volume change by year.

## Likely Q&A Questions

| Question | Short Answer |
| --- | --- |
| Why use a column chart for top genres? | It compares average popularity across a small ranked set of categories. |
| Why use a horizontal bar chart for bottom genres? | Long genre labels are easier to read horizontally. |
| Why use stacked charts? | They show category composition, not just totals. |
| Why use a bubble chart? | It adds duration as a third quantitative variable through marker size. |
| Why use box and violin charts? | Box charts summarize quartiles and outliers; violin charts show the full density shape. |
| Why add a rolling average to the line chart? | It smooths year-to-year noise while keeping the yearly trend visible. |
| Why sample scatter/bubble data? | Large point clouds can be slow and overplotted; sampling keeps the view responsive while preserving the pattern. |
