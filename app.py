import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# Page config
st.set_page_config(page_title="GetAHome - Housing Market Analysis", layout="wide", page_icon="🏠")

# Custom CSS to match professional Wix-style design
st.markdown("""
<style>
    /* Main color scheme */
    :root {
        --primary-color: #116DFF;
        --secondary-color: #5F6360;
        --background-color: #FFFFFF;
        --text-color: #000000;
        --light-gray: #F5F5F5;
        --border-color: #E0E0E0;
    }
    
    /* Global styling */
    .stApp {
        background-color: var(--background-color);
    }
    
    /* Header styling */
    h1 {
        color: var(--text-color) !important;
        font-family: 'Arial', 'Helvetica', sans-serif !important;
        font-weight: 700 !important;
        padding-bottom: 0.5rem;
        font-size: 2.5rem !important;
    }
    
    h2, h3 {
        color: var(--text-color) !important;
        font-family: 'Arial', 'Helvetica', sans-serif !important;
        font-weight: 600 !important;
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background-color: var(--light-gray);
        padding: 2rem 1rem;
    }
    
    [data-testid="stSidebar"] h1, 
    [data-testid="stSidebar"] h2, 
    [data-testid="stSidebar"] h3 {
        color: var(--text-color) !important;
    }
    
    /* Metric cards */
    [data-testid="stMetricValue"] {
        font-size: 32px;
        color: var(--primary-color) !important;
        font-weight: 700 !important;
    }
    
    [data-testid="stMetricLabel"] {
        color: var(--secondary-color) !important;
        font-size: 16px !important;
        font-weight: 500 !important;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    [data-testid="stMetricDelta"] {
        font-size: 14px !important;
    }
    
    /* Button styling */
    .stButton>button {
        background-color: var(--primary-color);
        color: white;
        border-radius: 24px;
        border: none;
        padding: 0.5rem 2rem;
        font-weight: 600;
        transition: all 0.3s ease;
        font-family: 'Arial', 'Helvetica', sans-serif;
    }
    
    .stButton>button:hover {
        background-color: #0D5DD6;
        box-shadow: 0 4px 12px rgba(17, 109, 255, 0.3);
        transform: translateY(-2px);
    }
    
    /* Tabs styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 2rem;
        border-bottom: 2px solid var(--light-gray);
    }
    
    .stTabs [data-baseweb="tab"] {
        color: var(--secondary-color);
        font-weight: 600;
        padding-bottom: 1rem;
        font-size: 16px;
    }
    
    .stTabs [aria-selected="true"] {
        color: var(--primary-color) !important;
        border-bottom: 3px solid var(--primary-color);
    }
    
    /* Selectbox and multiselect */
    .stSelectbox, .stMultiSelect {
        font-family: 'Arial', 'Helvetica', sans-serif;
    }
    
    /* Dataframe styling */
    [data-testid="stDataFrame"] {
        border: 1px solid var(--border-color);
        border-radius: 8px;
    }
    
    /* Info boxes */
    .stAlert {
        border-radius: 8px;
        border-left: 4px solid var(--primary-color);
    }
    
    /* Custom card styling */
    .custom-card {
        background-color: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
        border: 1px solid var(--border-color);
        margin-bottom: 1rem;
    }
    
    /* Price lookup styling */
    .price-display {
        background: linear-gradient(135deg, #116DFF 0%, #0D5DD6 100%);
        color: white;
        padding: 2rem;
        border-radius: 12px;
        text-align: center;
        box-shadow: 0 4px 16px rgba(17, 109, 255, 0.2);
    }
    
    .price-value {
        font-size: 3rem;
        font-weight: 700;
        margin: 0.5rem 0;
    }
    
    .price-label {
        font-size: 1.1rem;
        opacity: 0.9;
        margin-bottom: 0.5rem;
    }
    
    /* Divider */
    hr {
        margin: 2rem 0;
        border: none;
        border-top: 2px solid var(--light-gray);
    }
    
    /* Download button */
    .stDownloadButton>button {
        background-color: #00B894;
        color: white;
        border-radius: 24px;
        border: none;
        padding: 0.5rem 2rem;
        font-weight: 600;
    }
    
    .stDownloadButton>button:hover {
        background-color: #00A383;
        box-shadow: 0 4px 12px rgba(0, 184, 148, 0.3);
    }
</style>
""", unsafe_allow_html=True)

# Load data
@st.cache_data
def load_data():
    df = pd.read_excel('data_housing_unpivoted.xlsx')
    # Check if Quarter_ts exists, if not create it
    if 'Quarter_ts' not in df.columns:
        df['Quarter_ts'] = pd.PeriodIndex(
            year=df['Year'], 
            quarter=df['Quarter'].str[0].astype(int), 
            freq='Q'
        ).to_timestamp()
    else:
        df['Quarter_ts'] = pd.to_datetime(df['Quarter_ts'])
    
    # Ensure Is_District column exists
    if 'Is_District' not in df.columns:
        df['Is_District'] = df['Area'].str.contains("District", case=False, na=False)
    
    # Ensure District column exists
    if 'District' not in df.columns:
        df['District'] = ''
    
    return df

df = load_data()

# Header with professional styling
col1, col2 = st.columns([3, 1])
with col1:
    st.title("🏠 GetAHome")
    st.markdown("### Israeli Housing Market Analysis")
with col2:
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(f"**Last Updated:** {df['Quarter_ts'].max().strftime('%B %Y')}")

st.markdown("---")

# Quick Price Lookup Widget
st.markdown("### 💰 Quick Price Lookup")
st.markdown("*Get the latest average price for any city and room size*")

lookup_col1, lookup_col2, lookup_col3 = st.columns([2, 2, 3])

with lookup_col1:
    # Get all cities (excluding districts)
    all_cities = sorted([area for area in df['Area'].unique() if not df[df['Area'] == area]['Is_District'].iloc[0]])
    lookup_city = st.selectbox(
        "Select City",
        options=all_cities,
        key="lookup_city",
        index=all_cities.index('Tel Aviv') if 'Tel Aviv' in all_cities else 0
    )

with lookup_col2:
    # Get all room types
    all_room_types = sorted(df['Rooms'].unique())
    lookup_rooms = st.selectbox(
        "Select Room Size",
        options=all_room_types,
        index=all_room_types.index('All') if 'All' in all_room_types else 0,
        key="lookup_rooms"
    )

with lookup_col3:
    if lookup_city and lookup_rooms:
        # Get the latest quarter data
        latest_quarter = df['Quarter_ts'].max()
        lookup_data = df[
            (df['Area'] == lookup_city) & 
            (df['Rooms'] == lookup_rooms) & 
            (df['Quarter_ts'] == latest_quarter)
        ]
        
        if not lookup_data.empty:
            price = lookup_data['Average Price'].iloc[0]
            quarter_str = lookup_data['Quarter'].iloc[0]
            year_str = lookup_data['Year'].iloc[0]
            
            # Calculate YoY change if available
            year_ago = latest_quarter - pd.DateOffset(years=1)
            prev_data = df[
                (df['Area'] == lookup_city) & 
                (df['Rooms'] == lookup_rooms) & 
                (df['Quarter_ts'] == year_ago)
            ]
            
            st.markdown("<br>", unsafe_allow_html=True)
            if not prev_data.empty:
                prev_price = prev_data['Average Price'].iloc[0]
                change = ((price - prev_price) / prev_price) * 100
                st.metric(
                    label=f"Average Price ({quarter_str} {year_str})",
                    value=f"₪{price*1000:,.0f}K",
                    delta=f"{change:+.1f}% YoY"
                )
            else:
                st.metric(
                    label=f"Average Price ({quarter_str} {year_str})",
                    value=f"₪{price*1000:,.0f}K"
                )
        else:
            st.markdown("<br>", unsafe_allow_html=True)
            st.warning("⚠️ No data available for this combination")

st.markdown("---")

# Sidebar filters
st.sidebar.header("🔍 Filters")

# Date range filter
max_date = df['Quarter_ts'].max()
min_date = df['Quarter_ts'].min()

time_period = st.sidebar.selectbox(
    "Select Time Period",
    options=["All Time", "Last Quarter", "YTD", "Last Year", "Last 5 Years"],
    index=0
)

# Calculate date range based on selection
if time_period == "Last Quarter":
    start_date = max_date - pd.DateOffset(months=3)
    df_filtered = df[df['Quarter_ts'] >= start_date]
elif time_period == "YTD":
    start_date = pd.Timestamp(f"{max_date.year}-01-01")
    df_filtered = df[df['Quarter_ts'] >= start_date]
elif time_period == "Last Year":
    start_date = max_date - pd.DateOffset(years=1)
    df_filtered = df[df['Quarter_ts'] >= start_date]
elif time_period == "Last 5 Years":
    start_date = max_date - pd.DateOffset(years=5)
    df_filtered = df[df['Quarter_ts'] >= start_date]
else:  # All Time
    df_filtered = df

# District filter (if District column has values)
if 'District' in df_filtered.columns:
    # Get all non-empty, non-null district values
    all_districts = sorted([
        str(d) for d in df_filtered['District'].unique() 
        if pd.notna(d) and str(d).strip() and str(d).lower() != 'nan'
    ])
    if all_districts:
        selected_districts = st.sidebar.multiselect(
            "Select Districts",
            options=all_districts,
            default=all_districts,
            help="Filter by district (cities will be filtered accordingly)"
        )
        if selected_districts:
            df_filtered = df_filtered[df_filtered['District'].isin(selected_districts)]

# District filter
if 'Is_District' in df.columns:
    show_districts_only = st.sidebar.checkbox(
        "Show Districts Only",
        value=False,
        help="Filter to show only district-level data"
    )
    
    if show_districts_only:
        df_filtered = df_filtered[df_filtered['Is_District'] == True]
        st.sidebar.info(f"Showing {len(df_filtered['Area'].unique())} districts")
else:
    st.sidebar.warning("Is_District column not found. Please regenerate data.")
    show_districts_only = False

# Area filter
all_areas = sorted(df_filtered['Area'].unique())
selected_areas = st.sidebar.multiselect(
    "Select Areas",
    options=all_areas,
    default=all_areas[:5] if len(all_areas) > 5 else all_areas
)

# Rooms filter
all_rooms = sorted(df['Rooms'].unique())
selected_room = st.sidebar.selectbox(
    "Select Room Type",
    options=all_rooms,
    index=all_rooms.index('All') if 'All' in all_rooms else 0
)

# Apply filters
if selected_areas:
    df_filtered = df_filtered[df_filtered['Area'].isin(selected_areas)]
if selected_room:
    df_filtered = df_filtered[df_filtered['Rooms'] == selected_room]

# Main content
if df_filtered.empty:
    st.warning("No data available for the selected filters. Please adjust your selection.")
else:
    # Key Metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        latest_avg = df_filtered[df_filtered['Quarter_ts'] == df_filtered['Quarter_ts'].max()]['Average Price'].mean()
        st.metric("Latest Avg Price", f"₪{latest_avg:,.0f}" if pd.notna(latest_avg) else "N/A")
    
    with col2:
        earliest_avg = df_filtered[df_filtered['Quarter_ts'] == df_filtered['Quarter_ts'].min()]['Average Price'].mean()
        if pd.notna(latest_avg) and pd.notna(earliest_avg):
            change = ((latest_avg - earliest_avg) / earliest_avg) * 100
            st.metric("Total Change", f"{change:,.1f}%", delta=f"{change:,.1f}%")
        else:
            st.metric("Total Change", "N/A")
    
    with col3:
        st.metric("Areas Selected", len(selected_areas))
    
    with col4:
        st.metric("Time Period", f"{len(df_filtered['Quarter_ts'].unique())} Quarters")
    
    st.markdown("---")
    
    # Main Chart - Combined view
    st.subheader("📈 Housing Price Trends")
    
    # Create a combined identifier for each unique combination of Area and Rooms
    df_filtered['Series'] = df_filtered['Area'] + ' - ' + df_filtered['Rooms']
    
    # Group by quarter and series
    trend_data = df_filtered.groupby(['Quarter_ts', 'Series', 'Area', 'Rooms'])['Average Price'].mean().reset_index()
    
    # Professional color palette
    colors = ['#116DFF', '#0D5DD6', '#00B894', '#FF6B6B', '#4ECDC4', 
              '#FFD93D', '#6C5CE7', '#FD79A8', '#74B9FF', '#FDCB6E']
    
    # Create the main chart
    fig = px.line(trend_data, 
                 x='Quarter_ts', 
                 y='Average Price', 
                 color='Series',
                 title=f'Housing Prices Over Time: {len(selected_areas)} Area(s) × {selected_room}',
                 labels={'Quarter_ts': 'Quarter', 'Average Price': 'Average Price (₪ Thousands)', 'Series': 'Location - Room Size'},
                 markers=True,
                 color_discrete_sequence=colors)
    
    # Professional styling
    fig.update_traces(line_shape='spline', line=dict(width=3), marker=dict(size=8))
    
    # Format x-axis to show quarters
    fig.update_xaxes(
        tickformat="%qQ%y",
        dtick="M3",
        gridcolor='#F5F5F5',
        showgrid=True,
        title_font=dict(size=14, color='#5F6360', family='Arial, Helvetica, sans-serif')
    )
    
    fig.update_yaxes(
        gridcolor='#F5F5F5',
        showgrid=True,
        title_font=dict(size=14, color='#5F6360', family='Arial, Helvetica, sans-serif')
    )
    
    fig.update_layout(
        height=600, 
        hovermode='x unified',
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(family="Arial, Helvetica, sans-serif", size=13, color="#000000"),
        title_font=dict(size=20, color='#000000', family="Arial, Helvetica, sans-serif"),
        legend=dict(
            orientation="v",
            yanchor="top",
            y=1,
            xanchor="left",
            x=1.02,
            bgcolor="rgba(255,255,255,0.9)",
            bordercolor="#E0E0E0",
            borderwidth=1,
            font=dict(size=12)
        ),
        margin=dict(l=60, r=200, t=80, b=60)
    )
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    # Secondary tabs for detailed analysis
    tab1, tab2, tab3 = st.tabs(["🔄 Area Comparison", "🏆 Top Gainers/Losers", "📊 Detailed Data"])
    
    with tab1:
        st.subheader("Area Comparison")
        
        # Latest prices by area
        latest_prices = df_filtered[df_filtered['Quarter_ts'] == df_filtered['Quarter_ts'].max()]
        avg_by_area = latest_prices.groupby('Area')['Average Price'].mean().sort_values(ascending=False).reset_index()
        
        fig3 = px.bar(avg_by_area, 
                     x='Area', 
                     y='Average Price',
                     title='Latest Average Prices by Area',
                     labels={'Average Price': 'Average Price (₪ Thousands)'},
                     color='Average Price',
                     color_continuous_scale=[[0, '#E3F2FD'], [0.5, '#116DFF'], [1, '#0D5DD6']])
        
        fig3.update_layout(
            height=500,
            plot_bgcolor='white',
            paper_bgcolor='white',
            font=dict(family="Arial, Helvetica, sans-serif", size=13),
            xaxis=dict(gridcolor='#F5F5F5', tickangle=-45, title_font=dict(size=14, color='#5F6360')),
            yaxis=dict(gridcolor='#F5F5F5', title_font=dict(size=14, color='#5F6360')),
            title_font=dict(size=18, color='#000000', family="Arial, Helvetica, sans-serif"),
            showlegend=False
        )
        fig3.update_traces(marker_line_color='#E0E0E0', marker_line_width=1)
        st.plotly_chart(fig3, use_container_width=True)
    
    with tab2:
        st.subheader("Top Gainers and Losers")
        
        # Calculate percentage change for each area
        def calculate_change(group):
            if len(group) < 2:
                return pd.Series({'Change %': None})
            earliest = group[group['Quarter_ts'] == group['Quarter_ts'].min()]['Average Price'].mean()
            latest = group[group['Quarter_ts'] == group['Quarter_ts'].max()]['Average Price'].mean()
            if pd.notna(earliest) and pd.notna(latest) and earliest != 0:
                change_pct = ((latest - earliest) / earliest) * 100
                return pd.Series({
                    'Change %': change_pct,
                    'Earliest Price': earliest,
                    'Latest Price': latest
                })
            return pd.Series({'Change %': None, 'Earliest Price': None, 'Latest Price': None})
        
        changes = df_filtered.groupby('Area').apply(calculate_change).reset_index()
        changes = changes.dropna(subset=['Change %']).sort_values('Change %', ascending=False)
        
        col_g, col_l = st.columns(2)
        
        with col_g:
            st.markdown("### 🚀 Top 10 Gainers")
            top_gainers = changes.head(10)
            
            fig5 = px.bar(top_gainers, 
                         x='Area', 
                         y='Change %',
                         title='Areas with Highest Price Growth',
                         labels={'Change %': 'Price Change (%)'},
                         color='Change %',
                         color_continuous_scale=[[0, '#C8E6C9'], [0.5, '#4CAF50'], [1, '#2E7D32']])
            
            fig5.update_layout(
                height=450,
                xaxis_tickangle=-45,
                plot_bgcolor='white',
                paper_bgcolor='white',
                font=dict(family="Arial, Helvetica, sans-serif", size=12),
                xaxis=dict(gridcolor='#F5F5F5', title_font=dict(size=13)),
                yaxis=dict(gridcolor='#F5F5F5', title_font=dict(size=13)),
                title_font=dict(size=16, color='#000000'),
                showlegend=False
            )
            fig5.update_traces(marker_line_color='#E0E0E0', marker_line_width=1)
            st.plotly_chart(fig5, use_container_width=True)
            
            st.dataframe(
                top_gainers[['Area', 'Change %', 'Earliest Price', 'Latest Price']].style.format({
                    'Change %': '{:.2f}%',
                    'Earliest Price': '₪{:,.0f}K',
                    'Latest Price': '₪{:,.0f}K'
                }).background_gradient(subset=['Change %'], cmap='Greens'),
                hide_index=True,
                use_container_width=True
            )
        
        with col_l:
            st.markdown("### 📉 Top 10 Losers")
            top_losers = changes.tail(10).sort_values('Change %', ascending=True)
            
            fig6 = px.bar(top_losers, 
                         x='Area', 
                         y='Change %',
                         title='Areas with Lowest Price Growth',
                         labels={'Change %': 'Price Change (%)'},
                         color='Change %',
                         color_continuous_scale=[[0, '#EF5350'], [0.5, '#E57373'], [1, '#FFCDD2']])
            
            fig6.update_layout(
                height=450,
                xaxis_tickangle=-45,
                plot_bgcolor='white',
                paper_bgcolor='white',
                font=dict(family="Arial, Helvetica, sans-serif", size=12),
                xaxis=dict(gridcolor='#F5F5F5', title_font=dict(size=13)),
                yaxis=dict(gridcolor='#F5F5F5', title_font=dict(size=13)),
                title_font=dict(size=16, color='#000000'),
                showlegend=False
            )
            fig6.update_traces(marker_line_color='#E0E0E0', marker_line_width=1)
            st.plotly_chart(fig6, use_container_width=True)
            
            st.dataframe(
                top_losers[['Area', 'Change %', 'Earliest Price', 'Latest Price']].style.format({
                    'Change %': '{:.2f}%',
                    'Earliest Price': '₪{:,.0f}K',
                    'Latest Price': '₪{:,.0f}K'
                }).background_gradient(subset=['Change %'], cmap='Reds_r'),
                hide_index=True,
                use_container_width=True
            )
    
    with tab3:
        st.subheader("Detailed Data Table")
        
        # Display options
        show_all = st.checkbox("Show all columns", value=False)
        
        if show_all:
            display_df = df_filtered
        else:
            display_df = df_filtered[['Area', 'Rooms', 'Year', 'Quarter', 'Average Price', 'Quarter_ts']]
        
        # Sort options
        sort_col = st.selectbox("Sort by", options=display_df.columns.tolist())
        sort_order = st.radio("Order", options=['Ascending', 'Descending'], horizontal=True)
        
        display_df_sorted = display_df.sort_values(
            sort_col, 
            ascending=(sort_order == 'Ascending')
        )
        
        st.dataframe(
            display_df_sorted.style.format({
                'Average Price': '₪{:,.0f}'
            }),
            use_container_width=True,
            height=400
        )
        
        # Download button
        csv = display_df_sorted.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download filtered data as CSV",
            data=csv,
            file_name='housing_data_filtered.csv',
            mime='text/csv'
        )

# Footer
st.markdown("---")
col_f1, col_f2, col_f3 = st.columns(3)
with col_f1:
    st.markdown("💡 **Tip:** Use the sidebar filters to customize your analysis")
with col_f2:
    st.markdown(f"📊 **Data Source:** Israeli Housing Market Data")
with col_f3:
    st.markdown(f"🕒 **Last Refresh:** {datetime.now().strftime('%d/%m/%Y %H:%M')}")
