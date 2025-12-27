import pandas as pd
import plotly.express as px

# Load data
df = pd.read_excel('data_housing_unpivoted.xlsx')
df['Quarter_ts'] = pd.to_datetime(df['Quarter_ts'])
df['Quarter_Label'] = df['Quarter'] + df['Year'].astype(str).str[-2:]

# Create series identifier
df['Series'] = df['Area'] + ' - ' + df['Rooms']

# Filter for top 5 areas by latest price (you can adjust this)
latest_quarter = df[df['Quarter_ts'] == df['Quarter_ts'].max()]
top_areas = latest_quarter.groupby('Area')['Average Price'].mean().nlargest(5).index.tolist()

# Filter data
df_filtered = df[df['Area'].isin(top_areas) & (df['Rooms'] == 'All')]

# Group by quarter and series
trend_data = df_filtered.groupby(['Quarter_ts', 'Quarter_Label', 'Series'])['Average Price'].mean().reset_index()

# Sort by Quarter_ts to ensure proper ordering
trend_data = trend_data.sort_values('Quarter_ts')

# Create the chart
fig = px.line(trend_data, 
             x='Quarter_Label', 
             y='Average Price', 
             color='Series',
             title='Israeli Housing Market - Top 5 Areas',
             labels={'Quarter_Label': 'Quarter', 'Average Price': 'Average Price (₪M)', 'Series': 'Area - Rooms'},
             markers=True)

# Make lines smooth
fig.update_traces(line_shape='spline')

# Update layout for better appearance
fig.update_layout(
    height=600,
    hovermode='x unified',
    template='plotly_white',
    font=dict(family="Arial", size=12),
    title_font=dict(size=20, family="Arial", color='#333'),
    xaxis=dict(
        title_font=dict(size=14),
        tickangle=-45
    ),
    yaxis=dict(
        title_font=dict(size=14),
        gridcolor='#e0e0e0'
    ),
    legend=dict(
        orientation="v",
        yanchor="top",
        y=1,
        xanchor="left",
        x=1.02,
        bgcolor="rgba(255,255,255,0.8)",
        bordercolor="#ccc",
        borderwidth=1
    ),
    plot_bgcolor='white',
    paper_bgcolor='white'
)

# Export to HTML
fig.write_html('housing_chart.html', 
               include_plotlyjs='cdn',
               config={
                   'displayModeBar': True,
                   'displaylogo': False,
                   'modeBarButtonsToRemove': ['pan2d', 'lasso2d', 'select2d']
               })

print("✅ Chart exported to housing_chart.html")
print("📊 You can now embed this file in your Wix website")
print(f"📈 Showing data for: {', '.join(top_areas)}")
