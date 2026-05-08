import os
import logging
import pandas as pd
import numpy as np
import plotly.express as px
import dash
from dash import dcc, html, Input, Output, State, ctx
import dash_bootstrap_components as dbc
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Data Generation Function (Synthetic Spotify Data)
def generate_synthetic_data():
    np.random.seed(42)
    n = 5000
    genres = ['Pop', 'Rock', 'Hip-Hop', 'Jazz', 'Classical', 'Electronic', 'Country', 'R&B', 'Metal', 'Soul']
    
    data = {
        'track_name': [f'Track {i}' for i in range(n)],
        'artist_name': [f'Artist {np.random.randint(1, 500)}' for i in range(n)],
        'genre': np.random.choice(genres, n),
        'track_popularity': np.random.randint(0, 100, n),
        'track_energy': np.random.uniform(0, 1, n),
        'track_danceability': np.random.uniform(0, 1, n),
        'track_valence': np.random.uniform(0, 1, n),
        'track_tempo': np.random.uniform(60, 180, n),
        'track_duration_ms': np.random.randint(120000, 360000, n),
        'track_loudness': np.random.uniform(-15, -5, n),
        'explicit': np.random.choice([True, False], n),
        'release_date': pd.date_range(start='2000-01-01', end='2023-12-31', periods=n)
    }
    
    df = pd.DataFrame(data)
    df['release_decade'] = (df['release_date'].dt.year // 10) * 10
    df['duration_minutes'] = df['track_duration_ms'] / 60000
    
    # Create mood categories
    df['mood'] = pd.cut(df['track_valence'], bins=3, labels=['Sad', 'Neutral', 'Happy'])
    
    return df

# Load or Generate Data
logger.info("Generating synthetic Spotify dataset...")
df_raw = generate_synthetic_data()
logger.info(f"Dataset generated with {len(df_raw)} tracks.")

# Initialize Dash App
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.FLATLY])
app.title = "Spotify Trends Analytics Capstone"
server = app.server  # For Gunicorn deployment

# Define Layout
app.layout = html.Div([
    # Header
    dbc.Container([
        dbc.Row([
            dbc.Col(html.H1("🎵 Spotify Tracks Analytics Capstone", 
                           className="text-center my-4 text-primary"), width=12),
            dbc.Col(html.P("Interactive analysis of audio features, popularity trends, and genre distributions across 5,000 tracks.", 
                           className="text-center text-muted mb-4"), width=12)
        ])
    ], fluid=True),
    
    # Controls Card
    dbc.Container([
        dbc.Card([
            dbc.CardBody([
                dbc.Row([
                    # Genre Dropdown
                    dbc.Col([
                        html.Label("🎼 Select Genres", className="fw-bold"),
                        dcc.Dropdown(
                            id='dropdown-genre',
                            options=[{'label': g, 'value': g} for g in sorted(df_raw['genre'].unique())],
                            value=df_raw['genre'].unique()[:5].tolist(),
                            multi=True,
                            clearable=False,
                            className="mb-2"
                        )
                    ], md=3),
                    
                    # Year Range Slider
                    dbc.Col([
                        html.Label("📅 Release Year Range", className="fw-bold"),
                        dcc.RangeSlider(
                            id='slider-year',
                            min=int(df_raw['release_date'].dt.year.min()),
                            max=int(df_raw['release_date'].dt.year.max()),
                            value=[2000, 2023],
                            marks={str(y): str(y) for y in range(2000, 2024, 5)},
                            className="mb-2"
                        )
                    ], md=4),
                    
                    # Aggregation Radio
                    dbc.Col([
                        html.Label("📊 Aggregation Method", className="fw-bold"),
                        dcc.RadioItems(
                            id='radio-aggregation',
                            options=['Mean', 'Median', 'Sum'],
                            value='Mean',
                            inline=True,
                            className="mb-2"
                        )
                    ], md=3),
                    
                    # Features Checklist
                    dbc.Col([
                        html.Label("🎚️ Audio Features", className="fw-bold"),
                        dcc.Checklist(
                            id='checklist-features',
                            options=[
                                {'label': ' Energy', 'value': 'track_energy'},
                                {'label': ' Danceability', 'value': 'track_danceability'}
                            ],
                            value=['track_energy', 'track_danceability'],
                            inline=True,
                            className="mb-2"
                        )
                    ], md=2)
                ])
            ])
        ], className="mb-4 shadow-sm")
    ], fluid=True),
    
    # Charts Grid
    dbc.Container([
        # Row 1: Basic Comparison
        dbc.Row([
            dbc.Col(dcc.Loading(dcc.Graph(id='graph-col-popularity'), type="cube"), md=6, className="mb-4"),
            dbc.Col(dcc.Loading(dcc.Graph(id='graph-bar-energy'), type="cube"), md=6, className="mb-4"),
        ]),
        
        # Row 2: Advanced Comparison
        dbc.Row([
            dbc.Col(dcc.Loading(dcc.Graph(id='graph-stacked-explicit'), type="cube"), md=6, className="mb-4"),
            dbc.Col(dcc.Loading(dcc.Graph(id='graph-clustered-mood'), type="cube"), md=6, className="mb-4"),
        ]),
        
        # Row 3: Relationship
        dbc.Row([
            dbc.Col(dcc.Loading(dcc.Graph(id='graph-scatter-trend'), type="cube"), md=6, className="mb-4"),
            dbc.Col(dcc.Loading(dcc.Graph(id='graph-bubble-multivariate'), type="cube"), md=6, className="mb-4"),
        ]),
        
        # Row 4: Distribution
        dbc.Row([
            dbc.Col(dcc.Loading(dcc.Graph(id='graph-histogram-duration'), type="cube"), md=4, className="mb-4"),
            dbc.Col(dcc.Loading(dcc.Graph(id='graph-box-popularity'), type="cube"), md=4, className="mb-4"),
            dbc.Col(dcc.Loading(dcc.Graph(id='graph-violin-energy'), type="cube"), md=4, className="mb-4"),
        ]),
        
        # Row 5: Time Series
        dbc.Row([
            dbc.Col(dcc.Loading(dcc.Graph(id='graph-line-trend'), type="cube"), md=6, className="mb-4"),
            dbc.Col(dcc.Loading(dcc.Graph(id='graph-area-cumulative'), type="cube"), md=6, className="mb-4"),
        ]),
    ], fluid=True),
    
    # Footer
    html.Footer([
        dbc.Container([
            html.Hr(),
            html.P("© 2024 Spotify Analytics Capstone | Built with Plotly Dash & Bootstrap", 
                   className="text-center text-muted")
        ], fluid=True)
    ])
])

# Callback Function
@app.callback(
    [Output(col_id, 'figure') for col_id in [
        'graph-col-popularity', 'graph-bar-energy', 'graph-stacked-explicit', 
        'graph-clustered-mood', 'graph-scatter-trend', 'graph-bubble-multivariate',
        'graph-histogram-duration', 'graph-box-popularity', 'graph-violin-energy',
        'graph-line-trend', 'graph-area-cumulative'
    ]],
    [Input('dropdown-genre', 'value'),
     Input('slider-year', 'value'),
     Input('radio-aggregation', 'value'),
     Input('checklist-features', 'value')]
)
def update_dashboard(selected_genres, year_range, agg_method, selected_features):
    logger.info(f"Updating dashboard: Genres={selected_genres}, Years={year_range}")
    
    try:
        # Filter Data
        mask = (
            df_raw['genre'].isin(selected_genres) &
            (df_raw['release_date'].dt.year >= year_range[0]) &
            (df_raw['release_date'].dt.year <= year_range[1])
        )
        df = df_raw[mask].copy()
        
        if df.empty:
            empty_fig = px.scatter(title="⚠️ No data matches selected filters. Try adjusting your selection.")
            empty_fig.update_layout(height=400, showlegend=False)
            return [empty_fig] * 11

        # Aggregation Function
        def get_agg_func(method):
            return {'Mean': 'mean', 'Median': 'median', 'Sum': 'sum'}.get(method, 'mean')
        agg_func = get_agg_func(agg_method)

        # 1. Column Chart: Top Genres by Popularity
        genre_pop = df.groupby('genre', observed=True)['track_popularity'].agg(agg_func).reset_index()
        genre_pop = genre_pop.sort_values('track_popularity', ascending=False).head(10)
        fig1 = px.bar(genre_pop, x='genre', y='track_popularity', 
                      title=f"Top 10 Genres by {agg_method} Popularity",
                      labels={'genre': 'Genre', 'track_popularity': f'{agg_method} Score'},
                      color='track_popularity', color_continuous_scale='Blues')
        fig1.update_layout(xaxis_tickangle=-45, height=400)

        # 2. Bar Chart: Top Artists by Energy
        artist_energy = df.groupby('artist_name', observed=True)['track_energy'].agg(agg_func).reset_index()
        artist_energy = artist_energy.sort_values('track_energy', ascending=False).head(15)
        fig2 = px.bar(artist_energy, y='artist_name', x='track_energy', orientation='h',
                      title=f"Top 15 Artists by {agg_method} Energy",
                      labels={'artist_name': 'Artist', 'track_energy': f'{agg_method} Energy'},
                      color='track_energy', color_continuous_scale='Viridis')
        fig2.update_layout(margin={'l': 200}, height=400)

        # 3. Stacked Column: Explicit vs Clean
        explicit_counts = df.groupby(['genre', 'explicit'], observed=True).size().reset_index(name='count')
        total_per_genre = explicit_counts.groupby('genre')['count'].transform('sum')
        explicit_counts['percent'] = (explicit_counts['count'] / total_per_genre * 100).round(1)
        fig3 = px.bar(explicit_counts, x='genre', y='percent', color='explicit',
                      title="Proportion of Explicit vs Clean Tracks by Genre (%)",
                      labels={'percent': 'Percentage (%)', 'explicit': 'Explicit'},
                      barmode='stack', color_discrete_map={True: 'red', False: 'green'})
        fig3.update_layout(xaxis_tickangle=-45, height=400)

        # 4. Clustered Column: Features by Mood
        if selected_features:
            mood_df = df.melt(id_vars=['mood'], value_vars=selected_features, 
                              var_name='Feature', value_name='Score')
            agg_mood = mood_df.groupby(['mood', 'Feature'], observed=True)['Score'].agg(agg_func).reset_index()
            fig4 = px.bar(agg_mood, x='mood', y='Score', color='Feature', barmode='group',
                          title=f"{agg_method} Audio Features by Mood Category",
                          labels={'mood': 'Mood', 'Score': 'Average Score'},
                          color_discrete_sequence=px.colors.qualitative.Set2)
        else:
            fig4 = px.scatter(title="Select at least one audio feature")
        fig4.update_layout(height=400)

        # 5. Scatter: Popularity vs Danceability
        sample_df = df.sample(min(1000, len(df)))
        fig5 = px.scatter(sample_df, x='track_danceability', y='track_popularity', 
                          trendline='ols', marginal_x='histogram',
                          title="Relationship: Popularity vs. Danceability",
                          labels={'track_danceability': 'Danceability', 'track_popularity': 'Popularity'},
                          hover_data=['track_name', 'artist_name'],
                          color_discrete_sequence=['#1DB954'])
        fig5.update_traces(opacity=0.6, marker=dict(size=8))
        fig5.update_layout(height=400)

        # 6. Bubble: Energy vs Valence
        bubble_sample = df.sample(min(500, len(df)))
        fig6 = px.scatter(bubble_sample, x='track_energy', y='track_valence', 
                          size='track_tempo', color='genre',
                          title="Multivariate: Energy vs Valence (Bubble Size = Tempo)",
                          labels={'track_energy': 'Energy', 'track_valence': 'Valence'},
                          size_max=40, hover_data=['track_name', 'release_date'])
        fig6.update_traces(marker=dict(line=dict(width=1, color='DarkSlateGrey')))
        fig6.update_layout(height=400, legend=dict(orientation="h", yanchor="bottom", y=1.02))

        # 7. Histogram: Duration
        fig7 = px.histogram(df, x='duration_minutes', nbins=30, marginal='rug',
                            title="Distribution of Track Durations",
                            labels={'duration_minutes': 'Duration (Minutes)', 'count': 'Track Count'},
                            color_discrete_sequence=['#FF6B6B'])
        fig7.add_vline(x=df['duration_minutes'].mean(), line_dash="dash", 
                       annotation_text=f"Mean: {df['duration_minutes'].mean():.1f} min")
        fig7.update_layout(height=400)

        # 8. Box: Popularity by Genre
        top_genres = df['genre'].value_counts().head(8).index
        df_box = df[df['genre'].isin(top_genres)]
        fig8 = px.box(df_box, x='genre', y='track_popularity', color='genre',
                      title="Popularity Distribution by Genre (Outliers Shown)",
                      labels={'genre': 'Genre', 'track_popularity': 'Popularity Score'},
                      points='outliers')
        fig8.update_layout(showlegend=False, xaxis_tickangle=-45, height=400)

        # 9. Violin: Energy by Decade
        fig9 = px.violin(df, x='release_decade', y='track_energy', color='release_decade',
                         title="Energy Density Distribution Across Decades",
                         labels={'release_decade': 'Decade', 'track_energy': 'Energy'},
                         box=True, points=False)
        fig9.update_layout(showlegend=False, height=400)

        # 10. Line: Time Series Trend
        df_sorted = df.sort_values('release_date')
        time_series = df_sorted.groupby(pd.Grouper(key='release_date', freq='ME'))['track_popularity'].mean().reset_index()
        time_series = time_series.dropna()
        fig10 = px.line(time_series, x='release_date', y='track_popularity', markers=True,
                        title="Temporal Trend: Average Track Popularity Over Time",
                        labels={'release_date': 'Date', 'track_popularity': 'Mean Popularity'},
                        color_discrete_sequence=['#4ECDC4'])
        fig10.update_layout(xaxis_dtick='M12', height=400)

        # 11. Area: Cumulative Market Share
        area_data = df.groupby([pd.Grouper(key='release_date', freq='YE'), 'genre'], observed=True).size().reset_index(name='count')
        pivot_area = area_data.pivot(index='release_date', columns='genre', values='count').fillna(0)
        pivot_area_norm = pivot_area.div(pivot_area.sum(axis=1), axis=0)
        pivot_area_norm = pivot_area_norm.reset_index()
        pivot_area_melt = pivot_area_norm.melt(id_vars='release_date', var_name='genre', value_name='proportion')
        
        fig11 = px.area(pivot_area_melt, x='release_date', y='proportion', color='genre',
                        title="Cumulative Market Share of Genres Over Time (Normalized %)",
                        labels={'release_date': 'Year', 'proportion': 'Market Share'},
                        groupnorm='fraction')
        fig11.update_layout(height=400)

        return [fig1, fig2, fig3, fig4, fig5, fig6, fig7, fig8, fig9, fig10, fig11]

    except Exception as e:
        logger.error(f"Error in callback: {str(e)}")
        error_fig = px.scatter(title=f"⚠️ Error: {str(e)}")
        error_fig.update_layout(height=400)
        return [error_fig] * 11

if __name__ == '__main__':
    print("🚀 Starting Spotify Analytics Dashboard...")
    print("🌐 Access the dashboard at: http://127.0.0.1:8050/")
    app.run(debug=True, host='0.0.0.0', port=8050)
