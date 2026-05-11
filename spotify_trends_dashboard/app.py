from __future__ import annotations
import argparse
import os
from pathlib import Path
from urllib.parse import quote_plus
import pandas as pd
import plotly.express as px
from dash import Dash, Input, Output, State, dash_table, dcc, html, no_update

ROOT_DIR = Path(__file__).resolve().parent
DATA_CANDIDATES = [
    ROOT_DIR / "spotify_cleaned.csv",
    ROOT_DIR / "dataset_5a" / "spotify_cleaned.csv",
]

BG_COLOR = "#F7F6F2"
CARD_COLOR = "#FFFFFF"
INPUT_BG = "#FFFFFF"
TEXT_COLOR = "#111111"
MUTED_TEXT = "#6F6F6F"
GRID_COLOR = "#E5E2DC"
BORDER_COLOR = "#D8D4CC"
ROW_ALT = "#F2F0EB"

CATEGORY_COLORS = {"Low": "#64748B", "Medium": "#F59E0B", "High": "#10B981"}
FEATURE_COLORS = {"danceability": "#2563EB", "energy": "#EF4444"}
GENRE_SEQUENCE = ["#111111", "#2563EB", "#EF4444", "#10B981", "#F59E0B", "#7C3AED", "#0891B2", "#DB2777"]
HEATMAP_SCALE = ["#7C2D12", "#F7F6F2", "#064E3B"]
BUTTON_STYLE = {
    "background": "#111111",
    "color": "#FFFFFF",
    "border": "1px solid #111111",
    "fontWeight": "700",
    "padding": "11px 16px",
    "borderRadius": "0",
    "cursor": "pointer",
    "letterSpacing": "0",
}
SECONDARY_BUTTON_STYLE = {
    "background": "#FFFFFF",
    "color": "#111111",
    "border": "1px solid #111111",
    "fontWeight": "700",
    "padding": "11px 16px",
    "borderRadius": "0",
    "cursor": "pointer",
    "letterSpacing": "0",
    "textDecoration": "none",
    "display": "inline-block",
}
PANEL_STYLE = {
    "background": CARD_COLOR,
    "border": f"1px solid {BORDER_COLOR}",
    "borderRadius": "0",
    "padding": "16px",
}
SECTION_TITLE_STYLE = {
    "color": TEXT_COLOR,
    "fontWeight": "700",
    "fontSize": "18px",
    "letterSpacing": "0",
    "margin": "20px 0 10px",
    "textTransform": "uppercase",
}
COMPARISON_GRID_STYLE = {
    "display": "grid",
    "gridTemplateColumns": "repeat(auto-fit, minmax(min(100%, 330px), 1fr))",
    "gap": "14px",
    "marginBottom": "16px",
}
WIDE_CHART_GRID_STYLE = {
    "display": "grid",
    "gridTemplateColumns": "repeat(auto-fit, minmax(min(100%, 380px), 1fr))",
    "gap": "14px",
    "marginBottom": "16px",
}
SINGLE_CHART_GRID_STYLE = {
    "display": "grid",
    "gridTemplateColumns": "minmax(0, 1fr)",
    "gap": "14px",
    "marginBottom": "16px",
}

CATEGORY_ORDER = ["Low", "Medium", "High"]
LABELS = {
    "track_genre": "Genre",
    "artists": "Artist",
    "popularity": "Popularity",
    "Popularity_Category": "Popularity Category",
    "danceability": "Danceability",
    "energy": "Energy",
    "valence": "Valence",
    "tempo": "Tempo (BPM)",
    "loudness": "Loudness (dB)",
    "acousticness": "Acousticness",
    "duration_min": "Duration (minutes)",
    "Year": "Year",
    "count": "Tracks Count",
    "percent": "Share of Tracks (%)",
    "metric": "Audio Feature",
    "value": "Average Score",
}


def _load_data() -> pd.DataFrame:
    # Load cleaned dataset from expected locations and normalize schema aliases.
    csv_path = next((p for p in DATA_CANDIDATES if p.exists()), None)
    if csv_path is None:
        raise FileNotFoundError("spotify_cleaned.csv not found. Run the notebook first.")

    df = pd.read_csv(csv_path, low_memory=False)

    rename_map = {
        "Popularity": "popularity",
        "Genre": "track_genre",
        "genre": "track_genre",
        "Artist": "artists",
        "artist": "artists",
        "Track": "track_name",
        "track": "track_name",
        "Duration": "duration_ms",
        "duration": "duration_ms",
        "Year": "Year",
    }
    for src, dst in rename_map.items():
        if src in df.columns and dst not in df.columns:
            df[dst] = df[src]

    if "Year" not in df.columns and "year" in df.columns:
        df["Year"] = pd.to_numeric(df["year"], errors="coerce")

    if "Year" not in df.columns and "release_date" in df.columns:
        df["Year"] = pd.to_datetime(df["release_date"], errors="coerce").dt.year

    if "Year" not in df.columns:
        raise ValueError("Cleaned Spotify data must include a real Year column. Run the preprocessing notebook first.")

    if "Popularity_Category" not in df.columns and "popularity" in df.columns:
        df["Popularity_Category"] = pd.cut(
            pd.to_numeric(df["popularity"], errors="coerce"),
            bins=[-1, 29, 69, 100],
            labels=["Low", "Medium", "High"],
        )

    required = [
        "track_name",
        "artists",
        "track_genre",
        "popularity",
        "danceability",
        "energy",
        "valence",
        "tempo",
        "loudness",
        "acousticness",
        "duration_ms",
        "Year",
        "Popularity_Category",
    ]

    for col in [
        "popularity",
        "danceability",
        "energy",
        "valence",
        "tempo",
        "loudness",
        "acousticness",
        "duration_ms",
        "Year",
    ]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    df = df.dropna(subset=[c for c in required if c in df.columns]).copy()
    df["track_genre"] = df["track_genre"].astype(str).str.strip()
    df["artists"] = df["artists"].astype(str).str.strip()
    df["track_name"] = df["track_name"].astype(str).str.strip()

    banned = {"music", "unknown", "other", "n/a", "na", "nan", "none", ""}
    df = df[~df["track_genre"].str.lower().isin(banned)]

    df["popularity"] = df["popularity"].clip(0, 100)
    df["danceability"] = df["danceability"].clip(0, 1)
    df["energy"] = df["energy"].clip(0, 1)
    df["valence"] = df["valence"].clip(0, 1)
    df["acousticness"] = df["acousticness"].clip(0, 1)
    df["duration_ms"] = df["duration_ms"].clip(30000, 900000)
    df["duration_min"] = (df["duration_ms"] / 60000).round(2)
    df["Year"] = df["Year"].round().astype(int)
    df = df[df["Year"].between(1900, 2035)]

    df["Popularity_Category"] = pd.Categorical(
        df["Popularity_Category"].astype(str),
        categories=["Low", "Medium", "High"],
        ordered=True,
    )

    return df


def _style(fig, title: str):
    fig.update_layout(
        title={"text": title, "x": 0.01, "font": {"size": 18, "color": TEXT_COLOR, "family": "Cormorant Garamond, Georgia, serif"}},
        paper_bgcolor=CARD_COLOR,
        plot_bgcolor=CARD_COLOR,
        colorway=GENRE_SEQUENCE,
        font={"color": TEXT_COLOR, "family": "Inter, Manrope, Segoe UI, sans-serif"},
        margin={"l": 45, "r": 18, "t": 68, "b": 40},
        legend={
            "orientation": "h",
            "y": 1.05,
            "x": 0.0,
            "font": {"size": 11, "color": MUTED_TEXT},
            "bgcolor": "rgba(255,255,255,0)",
        },
        hoverlabel={"bgcolor": "#111111", "bordercolor": "#111111", "font": {"color": "#FFFFFF"}},
        hovermode="closest",
    )
    fig.update_xaxes(
        gridcolor=GRID_COLOR,
        zeroline=False,
        linecolor=TEXT_COLOR,
        tickcolor=TEXT_COLOR,
        ticks="outside",
        title_font={"color": TEXT_COLOR},
    )
    fig.update_yaxes(
        gridcolor=GRID_COLOR,
        zeroline=False,
        linecolor=TEXT_COLOR,
        tickcolor=TEXT_COLOR,
        ticks="outside",
        title_font={"color": TEXT_COLOR},
    )
    return fig


def _empty_figure(title: str, message: str):
    fig = px.scatter()
    fig.update_layout(
        title={"text": title, "x": 0.01, "font": {"size": 18, "color": TEXT_COLOR, "family": "Cormorant Garamond, Georgia, serif"}},
        paper_bgcolor=CARD_COLOR,
        plot_bgcolor=CARD_COLOR,
        font={"color": TEXT_COLOR, "family": "Inter, Manrope, Segoe UI, sans-serif"},
        margin={"l": 45, "r": 18, "t": 68, "b": 40},
    )
    fig.add_annotation(text=message, x=0.5, y=0.5, xref="paper", yref="paper", showarrow=False, font={"size": 15, "color": MUTED_TEXT})
    fig.update_xaxes(visible=False)
    fig.update_yaxes(visible=False)
    return fig


def _filtered_view(df: pd.DataFrame, genre: str, year_range: list[int], scope: str, query: str | None) -> pd.DataFrame:
    # Apply all global filters used by the interactive controls.
    y1, y2 = int(year_range[0]), int(year_range[1])
    view = df[df["Year"].between(y1, y2)]
    if genre != "All":
        view = view[view["track_genre"] == genre]
    if scope != "All":
        view = view[view["Popularity_Category"].astype(str) == scope]
    if query and query.strip():
        q = query.strip().lower()
        match_track = view["track_name"].str.lower().str.contains(q, na=False)
        match_artist = view["artists"].str.lower().str.contains(q, na=False)
        view = view[match_track | match_artist]
    return view


def _kpis(df: pd.DataFrame) -> tuple[str, str, str, str, str, str]:
    # Summarize current filtered state for top-level KPI cards and insight text.
    if df.empty:
        return "0", "0.0", "N/A", "N/A", "N/A", "No records match current filters."
    tracks = f"{len(df):,}"
    avg_pop = f"{df['popularity'].mean():.1f}"
    top_genre = df.groupby("track_genre")["popularity"].mean().sort_values(ascending=False).index[0]
    top_artist = df["artists"].value_counts().index[0]
    years = f"{int(df['Year'].min())} - {int(df['Year'].max())}"
    insight = (
        f"Filtered view has {len(df):,} tracks. "
        f"Top genre by average popularity is {top_genre}, top artist presence is {top_artist}, "
        f"with mean popularity {df['popularity'].mean():.1f} and median tempo {df['tempo'].median():.1f} BPM."
    )
    return tracks, avg_pop, top_genre, top_artist, years, insight


def _assistant_prompt(df: pd.DataFrame, genre: str, year_range: list[int], scope: str, query: str | None) -> tuple[str, str]:
    if df.empty:
        prompt = "Spotify tracks analysis: explain why the current dashboard filters return no matching tracks."
        return prompt, f"http://127.0.0.1:5173/?assistant=1&q={quote_plus(prompt)}"

    top_genre = df.groupby("track_genre")["popularity"].mean().sort_values(ascending=False).index[0]
    top_artist = df["artists"].value_counts().index[0]
    filters = [
        f"years {int(year_range[0])}-{int(year_range[1])}",
        f"genre {genre}" if genre != "All" else "all genres",
        f"{scope} popularity" if scope != "All" else "all popularity tiers",
    ]
    if query and query.strip():
        filters.append(f"search text {query.strip()}")

    prompt = (
        "Spotify dashboard assistant: explain the current filtered view "
        f"({', '.join(filters)}). "
        f"The view has {len(df):,} tracks, average popularity {df['popularity'].mean():.1f}, "
        f"top genre {top_genre}, top artist {top_artist}, median tempo {df['tempo'].median():.1f} BPM. "
        "Give 5 short insights and 3 presentation talking points."
    )
    return prompt, f"http://127.0.0.1:5173/?assistant=1&q={quote_plus(prompt)}"


def chart_1_top5_genres(df: pd.DataFrame):
    if df.empty:
        return _empty_figure("1) Column: Avg Popularity for Top 5 Genres", "No data")
    agg = df.groupby("track_genre", as_index=False)["popularity"].mean().sort_values("popularity", ascending=False).head(5)
    fig = px.bar(
        agg,
        x="track_genre",
        y="popularity",
        color="track_genre",
        text="popularity",
        color_discrete_sequence=GENRE_SEQUENCE,
        labels=LABELS,
    )
    fig.update_traces(showlegend=False, texttemplate="%{text:.1f}", textposition="outside", marker_line_color="#111111", marker_line_width=0.8)
    fig.update_yaxes(range=[0, min(100, max(20, agg["popularity"].max() * 1.18))])
    return _style(fig, "1) Column: Avg Popularity for Top 5 Genres")


def chart_2_bottom5_genres(df: pd.DataFrame):
    if df.empty:
        return _empty_figure("2) Bar: Avg Popularity for Bottom 5 Genres", "No data")
    agg = df.groupby("track_genre", as_index=False)["popularity"].mean().sort_values("popularity", ascending=True).head(5)
    fig = px.bar(
        agg,
        x="popularity",
        y="track_genre",
        orientation="h",
        color="track_genre",
        text="popularity",
        color_discrete_sequence=list(reversed(GENRE_SEQUENCE)),
        labels=LABELS,
    )
    fig.update_traces(showlegend=False, texttemplate="%{text:.1f}", textposition="outside", marker_line_color="#111111", marker_line_width=0.8)
    fig.update_yaxes(categoryorder="total ascending")
    return _style(fig, "2) Bar: Avg Popularity for Bottom 5 Genres")


def chart_3_clustered_column(df: pd.DataFrame):
    if df.empty:
        return _empty_figure("3) Clustered Column: High vs Low Counts in Top 4 Genres", "No data")
    top4 = df["track_genre"].value_counts().head(4).index
    subset = df[df["track_genre"].isin(top4) & df["Popularity_Category"].isin(["High", "Low"])]
    grouped = subset.groupby(["track_genre", "Popularity_Category"], as_index=False, observed=True).size().rename(columns={"size": "count"})
    fig = px.bar(
        grouped,
        x="track_genre",
        y="count",
        color="Popularity_Category",
        barmode="group",
        color_discrete_map=CATEGORY_COLORS,
        labels=LABELS,
    )
    fig.update_traces(marker_line_color="#111111", marker_line_width=0.7)
    return _style(fig, "3) Clustered Column: High vs Low Counts in Top 4 Genres")


def chart_4_clustered_bar(df: pd.DataFrame):
    if df.empty:
        return _empty_figure("4) Clustered Bar: Avg Danceability vs Energy for Top 5 Artists", "No data")
    top5_artists = df["artists"].value_counts().head(5).index
    subset = df[df["artists"].isin(top5_artists)]
    grouped = (
        subset.groupby("artists", as_index=False)[["danceability", "energy"]]
        .mean()
        .melt(id_vars="artists", var_name="metric", value_name="value")
    )
    fig = px.bar(
        grouped,
        x="value",
        y="artists",
        color="metric",
        orientation="h",
        barmode="group",
        color_discrete_map=FEATURE_COLORS,
        labels=LABELS,
    )
    fig.update_traces(marker_line_color="#111111", marker_line_width=0.7)
    return _style(fig, "4) Clustered Bar: Avg Danceability vs Energy for Top 5 Artists")


def chart_5_stacked_column(df: pd.DataFrame):
    if df.empty:
        return _empty_figure("5) Stacked Column: Popularity Mix in Top 5 Genres", "No data")
    top5 = df["track_genre"].value_counts().head(5).index
    subset = df[df["track_genre"].isin(top5)]
    grouped = subset.groupby(["track_genre", "Popularity_Category"], as_index=False, observed=True).size().rename(columns={"size": "count"})
    grouped["percent"] = grouped["count"] / grouped.groupby("track_genre")["count"].transform("sum") * 100
    fig = px.bar(
        grouped,
        x="track_genre",
        y="percent",
        color="Popularity_Category",
        barmode="stack",
        category_orders={"Popularity_Category": CATEGORY_ORDER},
        color_discrete_map=CATEGORY_COLORS,
        custom_data=["count"],
        labels=LABELS,
    )
    fig.update_traces(marker_line_color="#FFFFFF", marker_line_width=0.8, hovertemplate="%{x}<br>%{legendgroup}: %{y:.1f}%<br>Tracks: %{customdata[0]:,}<extra></extra>")
    return _style(fig, "5) Stacked Column: Popularity Mix in Top 5 Genres (%)")


def chart_6_stacked_bar(df: pd.DataFrame):
    if df.empty:
        return _empty_figure("6) Stacked Bar: Popularity Mix Across Years", "No data")
    available = sorted(df["Year"].dropna().astype(int).unique())[-5:]
    subset = df[df["Year"].isin(available)]
    grouped = subset.groupby(["Year", "Popularity_Category"], as_index=False, observed=True).size().rename(columns={"size": "count"})
    grouped["Year"] = grouped["Year"].astype(str)
    grouped["percent"] = grouped["count"] / grouped.groupby("Year")["count"].transform("sum") * 100
    fig = px.bar(
        grouped,
        x="percent",
        y="Year",
        color="Popularity_Category",
        orientation="h",
        barmode="stack",
        category_orders={"Popularity_Category": CATEGORY_ORDER, "Year": [str(y) for y in available]},
        color_discrete_map=CATEGORY_COLORS,
        custom_data=["count"],
        labels=LABELS,
    )
    fig.update_traces(marker_line_color="#FFFFFF", marker_line_width=0.8, hovertemplate="%{y}<br>%{legendgroup}: %{x:.1f}%<br>Tracks: %{customdata[0]:,}<extra></extra>")
    return _style(fig, "6) Stacked Bar: Popularity Mix Across Latest Years (%)")


def chart_7_scatter(df: pd.DataFrame):
    if df.empty:
        return _empty_figure("7) Scatter: Energy vs Valence by Popularity Category", "No data")
    plot_df = df.sample(n=min(len(df), 7000), random_state=42) if len(df) > 7000 else df
    corr = plot_df[["energy", "valence"]].corr(numeric_only=True).iloc[0, 1]
    fig = px.scatter(
        plot_df,
        x="energy",
        y="valence",
        color="Popularity_Category",
        opacity=0.58,
        color_discrete_map=CATEGORY_COLORS,
        hover_data=["track_name", "artists", "track_genre", "popularity"],
        render_mode="webgl",
        labels=LABELS,
    )
    fig.update_traces(marker={"line": {"width": 0.25, "color": "#FFFFFF"}})
    fig.add_annotation(
        text=f"r = {corr:.2f}",
        x=0.02,
        y=0.98,
        xref="paper",
        yref="paper",
        showarrow=False,
        bgcolor="#FFFFFF",
        bordercolor=BORDER_COLOR,
        font={"color": TEXT_COLOR, "size": 12},
    )
    return _style(fig, "7) Scatter: Energy vs Valence by Popularity Category")


def chart_8_bubble(df: pd.DataFrame):
    if df.empty:
        return _empty_figure("8) Bubble: Danceability vs Popularity (Size = Duration, Color = Genre)", "No data")
    preferred = ["pop", "rock", "hip-hop", "hip hop"]
    available = {g.lower(): g for g in df["track_genre"].dropna().unique()}
    selected = [available[p] for p in preferred if p in available][:3]
    if len(selected) < 3:
        selected = df["track_genre"].value_counts().head(3).index.tolist()

    subset = df[df["track_genre"].isin(selected)].copy()
    subset = subset.sample(n=min(len(subset), 5000), random_state=42) if len(subset) > 5000 else subset
    subset["duration_min"] = subset["duration_min"].clip(0.8, 10)
    fig = px.scatter(
        subset,
        x="danceability",
        y="popularity",
        size="duration_min",
        size_max=45,
        color="track_genre",
        opacity=0.58,
        hover_data=["track_name", "artists", "duration_min"],
        color_discrete_sequence=GENRE_SEQUENCE,
        labels=LABELS,
    )
    fig.update_traces(marker={"line": {"width": 0.5, "color": "#FFFFFF"}})
    return _style(fig, "8) Bubble: Danceability vs Popularity (Size = Duration, Color = Genre)")


def chart_9_histogram(df: pd.DataFrame):
    if df.empty:
        return _empty_figure("9) Histogram: Tempo Distribution", "No data")
    fig = px.histogram(
        df,
        x="tempo",
        nbins=40,
        color="Popularity_Category",
        barmode="overlay",
        opacity=0.62,
        category_orders={"Popularity_Category": CATEGORY_ORDER},
        color_discrete_map=CATEGORY_COLORS,
        labels=LABELS,
    )
    median_tempo = df["tempo"].median()
    fig.add_vline(
        x=median_tempo,
        line_color="#111111",
        line_width=2,
        annotation_text=f"Median {median_tempo:.1f}",
        annotation_position="top right",
    )
    fig.update_yaxes(title_text="Tracks Count")
    return _style(fig, "9) Histogram: Tempo Distribution")


def chart_10_box(df: pd.DataFrame):
    if df.empty:
        return _empty_figure("10) Box: Loudness by Popularity Category", "No data")
    fig = px.box(
        df,
        x="Popularity_Category",
        y="loudness",
        color="Popularity_Category",
        points="outliers",
        category_orders={"Popularity_Category": CATEGORY_ORDER},
        color_discrete_map=CATEGORY_COLORS,
        labels=LABELS,
    )
    fig.update_traces(boxmean=True, marker_line_color="#111111")
    return _style(fig, "10) Box: Loudness by Popularity Category")


def chart_11_violin(df: pd.DataFrame):
    if df.empty:
        return _empty_figure("11) Violin: Acousticness by Popularity Category", "No data")
    fig = px.violin(
        df,
        x="Popularity_Category",
        y="acousticness",
        color="Popularity_Category",
        box=True,
        points=False,
        category_orders={"Popularity_Category": CATEGORY_ORDER},
        color_discrete_map=CATEGORY_COLORS,
        labels=LABELS,
    )
    fig.update_traces(meanline_visible=True, line_color="#111111")
    return _style(fig, "11) Violin: Acousticness by Popularity Category")


def chart_12_line(df: pd.DataFrame):
    if df.empty:
        return _empty_figure("12) Line: Average Popularity by Year", "No data")
    grouped = df.groupby("Year", as_index=False)["popularity"].mean().sort_values("Year")
    grouped["Rolling 3-Year Avg"] = grouped["popularity"].rolling(3, min_periods=1).mean()
    line_df = grouped.melt(id_vars="Year", value_vars=["popularity", "Rolling 3-Year Avg"], var_name="metric", value_name="value")
    line_df["metric"] = line_df["metric"].replace({"popularity": "Average Popularity"})
    fig = px.line(
        line_df,
        x="Year",
        y="value",
        color="metric",
        markers=True,
        color_discrete_map={"Average Popularity": "#111111", "Rolling 3-Year Avg": "#8A8A8A"},
        labels={**LABELS, "value": "Average Popularity", "metric": "Measure"},
    )
    fig.update_traces(line={"width": 3}, marker={"size": 7})
    return _style(fig, "12) Line: Average Popularity by Year")


def chart_13_area(df: pd.DataFrame):
    if df.empty:
        return _empty_figure("13) Area: Stacked Track Volume by Popularity Category", "No data")
    grouped = df.groupby(["Year", "Popularity_Category"], as_index=False, observed=True).size().rename(columns={"size": "count"})
    fig = px.area(
        grouped,
        x="Year",
        y="count",
        color="Popularity_Category",
        category_orders={"Popularity_Category": CATEGORY_ORDER},
        color_discrete_map=CATEGORY_COLORS,
        labels=LABELS,
    )
    return _style(fig, "13) Area: Stacked Track Volume by Popularity Category")


def chart_14_heatmap(df: pd.DataFrame):
    if df.empty:
        return _empty_figure("14) Heatmap: Audio Feature Correlation", "No data")
    cols = ["popularity", "danceability", "energy", "valence", "tempo", "loudness", "acousticness"]
    corr = df[cols].corr(numeric_only=True).round(2)
    fig = px.imshow(
        corr,
        text_auto=True,
        zmin=-1,
        zmax=1,
        color_continuous_scale=HEATMAP_SCALE,
        labels={"color": "Correlation"},
    )
    fig.update_layout(coloraxis_colorbar={"title": "Corr"})
    fig.update_xaxes(title_text="Audio Feature")
    fig.update_yaxes(title_text="Audio Feature")
    return _style(fig, "14) Heatmap: Audio Feature Correlation")


def _card(graph_id: str, fig):
    return html.Div(
        dcc.Loading(
            dcc.Graph(id=graph_id, figure=fig, config={"displaylogo": False, "toImageButtonOptions": {"format": "png", "scale": 2}}),
            type="default",
            color=TEXT_COLOR,
        ),
        style={
            "background": CARD_COLOR,
            "border": f"1px solid {BORDER_COLOR}",
            "borderRadius": "0",
            "padding": "6px",
        },
    )


def _top_tracks(df: pd.DataFrame) -> list[dict[str, str | int | float]]:
    # Build compact top-tracks table sorted by popularity and engagement features.
    if df.empty:
        return []
    top = (
        df[["track_name", "artists", "track_genre", "Year", "popularity", "danceability", "energy"]]
        .sort_values(["popularity", "energy", "danceability"], ascending=False)
        .head(12)
        .copy()
    )
    top["danceability"] = top["danceability"].round(3)
    top["energy"] = top["energy"].round(3)
    return top.to_dict("records")


def _kpi_card(label: str, value_id: str):
    return html.Div(
        [
            html.Div(label, style={"color": MUTED_TEXT, "fontSize": "12px", "fontWeight": "700", "textTransform": "uppercase"}),
            html.Div(id=value_id, style={"fontSize": "28px", "fontWeight": "700", "color": TEXT_COLOR, "marginTop": "8px"}),
        ],
        style=PANEL_STYLE,
    )


def _assistant_card():
    return html.Div(
        style={
            **PANEL_STYLE,
            "display": "grid",
            "gridTemplateColumns": "minmax(0, 1fr) auto",
            "gap": "14px",
            "alignItems": "center",
            "marginBottom": "18px",
            "borderLeft": "6px solid #2563EB",
        },
        children=[
            html.Div(
                [
                    html.Div(
                        "5*A Assistant",
                        style={
                            "fontFamily": "Cormorant Garamond, Georgia, serif",
                            "fontSize": "28px",
                            "fontWeight": "700",
                            "lineHeight": "1",
                        },
                    ),
                    html.Div(
                        id="assistant-prompt",
                        style={"color": MUTED_TEXT, "fontSize": "14px", "lineHeight": "1.55", "marginTop": "8px"},
                    ),
                ]
            ),
            html.A(
                "Open Assistant",
                id="assistant-open-link",
                href="http://127.0.0.1:5173",
                target="_blank",
                style=SECONDARY_BUTTON_STYLE,
            ),
        ],
    )


DATA = _load_data()
ALL_GENRES = sorted(DATA["track_genre"].dropna().unique().tolist())
YEAR_MIN = int(DATA["Year"].min())
YEAR_MAX = int(DATA["Year"].max())

slider_min = YEAR_MIN
slider_max = YEAR_MAX
if slider_min == slider_max:
    slider_min = YEAR_MIN - 1
    slider_max = YEAR_MAX + 1


def _year_marks(start: int, end: int):
    span = max(1, end - start)
    if span <= 8:
        years = list(range(start, end + 1))
    else:
        ticks = 6
        years = sorted({start + round(i * span / (ticks - 1)) for i in range(ticks)} | {start, end})
    return {y: {"label": str(y), "style": {"color": MUTED_TEXT, "fontSize": "11px"}} for y in years}


app = Dash(__name__)
server = app.server
app.title = "Spotify Music Trends"
app.index_string = """
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
        <link rel=\"preconnect\" href=\"https://fonts.googleapis.com\">
        <link rel=\"preconnect\" href=\"https://fonts.gstatic.com\" crossorigin>
        <link href=\"https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@500;600;700&family=Inter:wght@400;500;600;700&display=swap\" rel=\"stylesheet\">
        <style>
            :root {
                color-scheme: light;
            }
            body {
                margin: 0;
                background: #F7F6F2;
                color: #111111;
            }
            * {
                box-sizing: border-box;
                font-family: 'Inter', 'Segoe UI', sans-serif;
                letter-spacing: 0;
            }
            button,
            input,
            .Select-control {
                border-radius: 0 !important;
            }
            .rc-slider-mark-text {
                color: #6F6F6F !important;
                font-size: 12px;
            }
            .rc-slider-mark-text-active {
                color: #111111 !important;
            }
            .rc-slider-mark {
                margin-top: 2px;
            }
            .rc-slider-track {
                background-color: #111111;
            }
            .rc-slider-rail {
                background-color: #D8D4CC;
            }
            .rc-slider-handle {
                border: 2px solid #111111;
                background-color: #FFFFFF;
                box-shadow: none;
            }
            .Select-control,
            .Select-menu-outer,
            .Select-menu,
            .Select-value-label,
            .Select-placeholder,
            .Select input {
                background-color: #FFFFFF !important;
                color: #111111 !important;
                border-color: #D8D4CC !important;
            }
            .control-dropdown .Select-control {
                background-color: #FFFFFF !important;
                border: 1px solid #111111 !important;
                min-height: 48px !important;
                padding: 4px 8px !important;
            }
            .control-dropdown .Select-input > input::placeholder {
                color: #6F6F6F !important;
                font-size: 14px !important;
            }
            .control-dropdown .Select-input > input {
                padding: 6px 8px !important;
                font-size: 14px !important;
                color: #111111 !important;
            }
            .control-dropdown .Select-menu-outer,
            .control-dropdown .Select-menu {
                background-color: #FFFFFF !important;
                border: 1px solid #111111 !important;
                z-index: 2200 !important;
                max-height: 250px !important;
            }
            .control-dropdown .VirtualizedSelectOption,
            .control-dropdown .Select-option {
                background-color: #FFFFFF !important;
                color: #111111 !important;
                padding: 10px 12px !important;
                font-size: 14px !important;
            }
            .control-dropdown .VirtualizedSelectFocusedOption,
            .control-dropdown .Select-option.is-focused {
                background-color: #111111 !important;
                color: #FFFFFF !important;
            }
            .control-dropdown .Select-value-label,
            .control-dropdown .Select-placeholder,
            .control-dropdown .Select-input > input {
                color: #111111 !important;
                font-size: 14px !important;
            }
            .control-dropdown .Select-value,
            .control-dropdown .Select-value span,
            .control-dropdown .Select-arrow-zone,
            .control-dropdown .Select-clear-zone {
                background-color: #FFFFFF !important;
                color: #111111 !important;
            }
            .control-radio label {
                color: #111111 !important;
                font-weight: 600 !important;
                display: inline-flex !important;
                align-items: center !important;
                gap: 6px !important;
                margin-right: 14px !important;
            }
            .control-radio input[type="radio"] {
                accent-color: #111111;
            }
            input[type="text"]::placeholder {
                color: #6F6F6F !important;
                opacity: 1;
            }
            input[type="text"]:focus,
            button:focus,
            .Select-control:focus-within {
                outline: 2px solid #111111;
                outline-offset: 2px;
            }
            @media (max-width: 1200px) {
                #control-grid {
                    grid-template-columns: repeat(2, 1fr) !important;
                }
            }
            @media (max-width: 768px) {
                #control-grid {
                    grid-template-columns: 1fr !important;
                    gap: 12px !important;
                }
            }
        </style>
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
"""

app.layout = html.Div(
    style={"backgroundColor": BG_COLOR, "minHeight": "100vh", "padding": "26px", "color": TEXT_COLOR},
    children=[
        html.Div(
            style={"maxWidth": "1720px", "margin": "0 auto"},
            children=[
                html.Header(
                    style={"borderBottom": f"1px solid {TEXT_COLOR}", "paddingBottom": "20px", "marginBottom": "18px"},
                    children=[
                        html.Div(
                            "Spotify Music Trends",
                            style={
                                "fontFamily": "Cormorant Garamond, Georgia, serif",
                                "fontSize": "clamp(42px, 7vw, 94px)",
                                "lineHeight": "0.92",
                                "fontWeight": "700",
                                "textTransform": "uppercase",
                            },
                        ),
                        html.Div(
                            f"Popularity, audio features, genre behavior, and release-year movement across {len(DATA):,} cleaned Spotify tracks.",
                            style={"color": MUTED_TEXT, "fontSize": "15px", "marginTop": "12px", "maxWidth": "760px"},
                        ),
                    ],
                ),
                html.Div(
                    id="control-grid",
                    style={
                        **PANEL_STYLE,
                        "display": "grid",
                        "gridTemplateColumns": "repeat(auto-fit, minmax(260px, 1fr))",
                        "gap": "16px",
                        "marginBottom": "16px",
                    },
                    children=[
                        html.Div(
                            children=[
                                html.Label("Genre", style={"color": TEXT_COLOR, "fontWeight": "700", "marginBottom": "6px", "display": "block"}),
                                dcc.Dropdown(
                                    id="genre-dropdown",
                                    className="control-dropdown",
                                    options=[{"label": "All", "value": "All"}] + [{"label": g, "value": g} for g in ALL_GENRES],
                                    value="All",
                                    clearable=False,
                                    maxHeight=180,
                                    style={"color": TEXT_COLOR, "fontWeight": "600", "backgroundColor": INPUT_BG},
                                ),
                            ]
                        ),
                        html.Div(
                            children=[
                                html.Label("Year Range", style={"color": TEXT_COLOR, "fontWeight": "700", "marginBottom": "6px", "display": "block"}),
                                dcc.RangeSlider(
                                    id="year-slider",
                                    min=slider_min,
                                    max=slider_max,
                                    value=[YEAR_MIN, YEAR_MAX],
                                    allowCross=False,
                                    marks=_year_marks(slider_min, slider_max),
                                    tooltip={"placement": "bottom", "always_visible": False},
                                ),
                            ]
                        ),
                        html.Div(
                            children=[
                                html.Label("Popularity Scope", style={"color": TEXT_COLOR, "fontWeight": "700", "marginBottom": "6px", "display": "block"}),
                                dcc.RadioItems(
                                    id="popularity-radio",
                                    className="control-radio",
                                    options=[
                                        {"label": "All", "value": "All"},
                                        {"label": "High", "value": "High"},
                                        {"label": "Medium", "value": "Medium"},
                                        {"label": "Low", "value": "Low"},
                                    ],
                                    value="All",
                                    inline=True,
                                ),
                            ]
                        ),
                        html.Div(
                            children=[
                                html.Label("Track or Artist", style={"color": TEXT_COLOR, "fontWeight": "700", "marginBottom": "6px", "display": "block"}),
                                dcc.Input(
                                    id="track-search",
                                    type="text",
                                    placeholder="Search",
                                    debounce=True,
                                    style={
                                        "width": "100%",
                                        "background": INPUT_BG,
                                        "border": f"1px solid {TEXT_COLOR}",
                                        "padding": "13px 12px",
                                        "color": TEXT_COLOR,
                                        "fontWeight": "600",
                                    },
                                ),
                            ]
                        ),
                    ],
                ),
                html.Div(
                    style={"display": "flex", "justifyContent": "space-between", "alignItems": "center", "gap": "12px", "marginBottom": "16px", "flexWrap": "wrap"},
                    children=[
                        html.Div(
                            f"{len(DATA):,} cleaned tracks | {len(ALL_GENRES)} genres | {YEAR_MIN}-{YEAR_MAX}",
                            style={"color": MUTED_TEXT, "fontSize": "13px"},
                        ),
                        html.Div(
                            style={"display": "flex", "gap": "10px", "flexWrap": "wrap"},
                            children=[
                                html.A("Open 5*A Search", href="http://127.0.0.1:5173", target="_blank", style=SECONDARY_BUTTON_STYLE),
                                html.Button("Download Filtered CSV", id="download-btn", n_clicks=0, style=BUTTON_STYLE),
                            ],
                        ),
                        dcc.Download(id="download-data"),
                    ],
                ),
                html.Div(
                    style={"display": "grid", "gridTemplateColumns": "repeat(auto-fit, minmax(180px, 1fr))", "gap": "12px", "marginBottom": "14px"},
                    children=[
                        _kpi_card("Tracks in View", "kpi-tracks"),
                        _kpi_card("Average Popularity", "kpi-pop"),
                        _kpi_card("Top Genre", "kpi-genre"),
                        _kpi_card("Top Artist", "kpi-artist"),
                        _kpi_card("Year Span", "kpi-years"),
                    ],
                ),
                html.Div(
                    id="insight-line",
                    style={
                        **PANEL_STYLE,
                        "marginBottom": "18px",
                        "lineHeight": "1.6",
                        "color": TEXT_COLOR,
                        "whiteSpace": "normal",
                        "wordWrap": "break-word",
                        "minHeight": "56px",
                        "fontSize": "15px",
                    },
                ),
                _assistant_card(),
                html.H3("Comparison", style=SECTION_TITLE_STYLE),
                html.Div(
                    style=COMPARISON_GRID_STYLE,
                    children=[
                        _card("chart-1", chart_1_top5_genres(DATA)),
                        _card("chart-2", chart_2_bottom5_genres(DATA)),
                        _card("chart-3", chart_3_clustered_column(DATA)),
                        _card("chart-4", chart_4_clustered_bar(DATA)),
                        _card("chart-5", chart_5_stacked_column(DATA)),
                        _card("chart-6", chart_6_stacked_bar(DATA)),
                    ],
                ),
                html.H3("Relationship", style=SECTION_TITLE_STYLE),
                html.Div(
                    style=WIDE_CHART_GRID_STYLE,
                    children=[
                        _card("chart-7", chart_7_scatter(DATA)),
                        _card("chart-8", chart_8_bubble(DATA)),
                    ],
                ),
                html.H3("Distribution", style=SECTION_TITLE_STYLE),
                html.Div(
                    style=COMPARISON_GRID_STYLE,
                    children=[
                        _card("chart-9", chart_9_histogram(DATA)),
                        _card("chart-10", chart_10_box(DATA)),
                        _card("chart-11", chart_11_violin(DATA)),
                    ],
                ),
                html.H3("Time Series", style=SECTION_TITLE_STYLE),
                html.Div(
                    style=WIDE_CHART_GRID_STYLE,
                    children=[
                        _card("chart-12", chart_12_line(DATA)),
                        _card("chart-13", chart_13_area(DATA)),
                    ],
                ),
                html.H3("Feature Correlation", style=SECTION_TITLE_STYLE),
                html.Div(
                    style=SINGLE_CHART_GRID_STYLE,
                    children=[_card("chart-14", chart_14_heatmap(DATA))],
                ),
                html.H3("Top Tracks Snapshot", style=SECTION_TITLE_STYLE),
                html.Div(
                    style={**PANEL_STYLE, "padding": "10px"},
                    children=[
                        dash_table.DataTable(
                            id="top-tracks-table",
                            columns=[
                                {"name": "Track", "id": "track_name"},
                                {"name": "Artist", "id": "artists"},
                                {"name": "Genre", "id": "track_genre"},
                                {"name": "Year", "id": "Year"},
                                {"name": "Popularity", "id": "popularity"},
                                {"name": "Danceability", "id": "danceability"},
                                {"name": "Energy", "id": "energy"},
                            ],
                            data=_top_tracks(DATA),
                            page_size=12,
                            sort_action="native",
                            style_as_list_view=True,
                            style_table={"overflowX": "auto"},
                            style_header={"backgroundColor": "#111111", "color": "#FFFFFF", "fontWeight": "700", "border": "none"},
                            style_cell={
                                "backgroundColor": CARD_COLOR,
                                "color": TEXT_COLOR,
                                "border": f"1px solid {BORDER_COLOR}",
                                "fontSize": "13px",
                                "padding": "10px",
                                "maxWidth": "220px",
                                "whiteSpace": "normal",
                                "fontFamily": "Inter, Segoe UI, sans-serif",
                            },
                            style_data_conditional=[{"if": {"row_index": "odd"}, "backgroundColor": ROW_ALT}],
                        )
                    ],
                ),
            ],
        )
    ],
)


@app.callback(
    Output("kpi-tracks", "children"),
    Output("kpi-pop", "children"),
    Output("kpi-genre", "children"),
    Output("kpi-artist", "children"),
    Output("kpi-years", "children"),
    Output("insight-line", "children"),
    Output("assistant-prompt", "children"),
    Output("assistant-open-link", "href"),
    Output("chart-1", "figure"),
    Output("chart-2", "figure"),
    Output("chart-3", "figure"),
    Output("chart-4", "figure"),
    Output("chart-5", "figure"),
    Output("chart-6", "figure"),
    Output("chart-7", "figure"),
    Output("chart-8", "figure"),
    Output("chart-9", "figure"),
    Output("chart-10", "figure"),
    Output("chart-11", "figure"),
    Output("chart-12", "figure"),
    Output("chart-13", "figure"),
    Output("chart-14", "figure"),
    Output("top-tracks-table", "data"),
    Input("genre-dropdown", "value"),
    Input("year-slider", "value"),
    Input("popularity-radio", "value"),
    Input("track-search", "value"),
)
def update_dashboard(genre: str, year_range: list[int], scope: str, search_text: str | None):
    # Single callback keeps all major visuals synchronized with shared filters.
    view = _filtered_view(DATA, genre, year_range, scope, search_text)
    tracks, avg_pop, top_genre, top_artist, years, insight = _kpis(view)
    assistant_prompt, assistant_href = _assistant_prompt(view, genre, year_range, scope, search_text)
    return (
        tracks,
        avg_pop,
        top_genre,
        top_artist,
        years,
        insight,
        assistant_prompt,
        assistant_href,
        chart_1_top5_genres(view),
        chart_2_bottom5_genres(view),
        chart_3_clustered_column(view),
        chart_4_clustered_bar(view),
        chart_5_stacked_column(view),
        chart_6_stacked_bar(view),
        chart_7_scatter(view),
        chart_8_bubble(view),
        chart_9_histogram(view),
        chart_10_box(view),
        chart_11_violin(view),
        chart_12_line(view),
        chart_13_area(view),
        chart_14_heatmap(view),
        _top_tracks(view),
    )


@app.callback(
    Output("download-data", "data"),
    Input("download-btn", "n_clicks"),
    State("genre-dropdown", "value"),
    State("year-slider", "value"),
    State("popularity-radio", "value"),
    State("track-search", "value"),
    prevent_initial_call=True,
)
def download_filtered_data(n_clicks: int, genre: str, year_range: list[int], scope: str, search_text: str | None):
    # Export only the currently filtered view to keep analysis reproducible.
    if not n_clicks:
        return no_update
    view = _filtered_view(DATA, genre, year_range, scope, search_text)
    cols = [
        "track_name",
        "artists",
        "track_genre",
        "Year",
        "popularity",
        "danceability",
        "energy",
        "valence",
        "tempo",
        "loudness",
        "acousticness",
        "duration_ms",
        "Popularity_Category",
    ]
    export_cols = [c for c in cols if c in view.columns]
    return dcc.send_data_frame(view[export_cols].to_csv, "spotify_filtered_view.csv", index=False)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--host", type=str, default=None)
    parser.add_argument("--port", type=int, default=None)
    args, _ = parser.parse_known_args()

    host = args.host or os.getenv("HOST", "127.0.0.1")
    port = args.port or int(os.getenv("PORT", "8050"))
    app.run(debug=True, host=host, port=port)
