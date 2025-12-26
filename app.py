import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# Page config
st.set_page_config(page_title="GetAHome - Housing Market Analysis", layout="wide", page_icon="🏠")

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

# Header
st.title("🏠 GetAHome - Israeli Housing Market Analysis")
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
    
    # Create the main chart
    fig = px.line(trend_data, 
                 x='Quarter_ts', 
                 y='Average Price', 
                 color='Series',
                 title=f'Housing Prices: {len(selected_areas)} Area(s) × 1 Room Type = {len(trend_data["Series"].unique())} Series',
                 labels={'Quarter_ts': 'Date', 'Average Price': 'Average Price (₪)', 'Series': 'Area - Rooms'},
                 markers=True)
    
    # Make the line smooth
    fig.update_traces(line_shape='spline')
    
    # Format x-axis to show quarters (e.g., 1Q25)
    fig.update_xaxes(
        tickformat="%qQ%y",
        dtick="M3"  # Show tick every quarter
    )
    
    fig.update_layout(
        height=600, 
        hovermode='x unified',
        legend=dict(
            orientation="v",
            yanchor="top",
            y=1,
            xanchor="left",
            x=1.02
        )
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
                     labels={'Average Price': 'Average Price (₪)'},
                     color='Average Price',
                     color_continuous_scale='Viridis')
        
        fig3.update_layout(height=400, xaxis_tickangle=-45)
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
                         color_continuous_scale='Greens')
            
            fig5.update_layout(height=400, xaxis_tickangle=-45)
            st.plotly_chart(fig5, use_container_width=True)
            
            st.dataframe(
                top_gainers[['Area', 'Change %', 'Earliest Price', 'Latest Price']].style.format({
                    'Change %': '{:.2f}%',
                    'Earliest Price': '₪{:,.0f}',
                    'Latest Price': '₪{:,.0f}'
                }),
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
                         color_continuous_scale='Reds')
            
            fig6.update_layout(height=400, xaxis_tickangle=-45)
            st.plotly_chart(fig6, use_container_width=True)
            
            st.dataframe(
                top_losers[['Area', 'Change %', 'Earliest Price', 'Latest Price']].style.format({
                    'Change %': '{:.2f}%',
                    'Earliest Price': '₪{:,.0f}',
                    'Latest Price': '₪{:,.0f}'
                }),
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
st.markdown("💡 **Tip:** Use the sidebar filters to customize your analysis")
