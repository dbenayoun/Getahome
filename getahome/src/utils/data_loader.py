import pandas as pd

def load_data(file_path):
    """Load historical average price data from an Excel file."""
    df = pd.read_excel(file_path)
    return df

def get_area_data(df, area):
    """Filter data for a specific area."""
    return df[df['Area'] == area]

def get_top_gainers(df, n=5):
    """Identify top gainers based on average price increase."""
    df['Price Change'] = df['Average Price'].diff()
    return df.nlargest(n, 'Price Change')

def get_top_losers(df, n=5):
    """Identify top losers based on average price decrease."""
    df['Price Change'] = df['Average Price'].diff()
    return df.nsmallest(n, 'Price Change')

def filter_data_by_timeframe(df, start_year, end_year):
    """Filter data based on a specified time frame."""
    return df[(df['Year'] >= start_year) & (df['Year'] <= end_year)]