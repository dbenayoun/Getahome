"""
Generate a lightweight version of housing data with only the latest quarter
and one year ago for YoY comparison
"""
import pandas as pd
import json

print("🔄 Creating lightweight housing data...")

try:
    # Load the Excel data
    df = pd.read_excel('data_housing_unpivoted.xlsx')
    
    print(f"✅ Loaded {len(df)} records from Excel")
    
    # Ensure Quarter_ts is datetime
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
    
    # Get the latest quarter
    latest_quarter = df['Quarter_ts'].max()
    year_ago = latest_quarter - pd.DateOffset(years=1)
    
    # Filter for only latest quarter and year ago
    df_filtered = df[
        (df['Quarter_ts'] == latest_quarter) | 
        (df['Quarter_ts'] == year_ago)
    ].copy()
    
    # Select only necessary columns
    df_filtered = df_filtered[[
        'Area', 'Rooms', 'Year', 'Quarter', 
        'Average Price', 'Quarter_ts', 'Is_District'
    ]]
    
    # Convert Quarter_ts to string format for JSON
    df_filtered['Quarter_ts'] = df_filtered['Quarter_ts'].dt.strftime('%Y-%m-%d')
    
    # Convert to JSON
    json_data = df_filtered.to_dict(orient='records')
    
    # Save to file (for reference)
    with open('housing_data_lite.json', 'w', encoding='utf-8') as f:
        json.dump(json_data, f, ensure_ascii=False, indent=2)
    
    print(f"✅ Generated lightweight data with {len(df_filtered)} records")
    print(f"   Original: {len(df)} records")
    print(f"   Reduced by: {(1 - len(df_filtered)/len(df)) * 100:.1f}%")
    
    # Print some statistics
    print(f"\n📊 Data Summary:")
    print(f"   - Latest quarter: {df_filtered[df_filtered['Quarter_ts'] == df_filtered['Quarter_ts'].max()]['Quarter'].iloc[0]} {df_filtered[df_filtered['Quarter_ts'] == df_filtered['Quarter_ts'].max()]['Year'].iloc[0]}")
    print(f"   - Cities (excluding districts): {df_filtered[~df_filtered['Is_District']]['Area'].nunique()}")
    print(f"   - Room types: {df_filtered['Rooms'].nunique()}")
    
    # Create JavaScript data string
    js_data = json.dumps(json_data, ensure_ascii=False)
    
    print(f"\n✅ JSON data size: {len(js_data):,} characters")
    print(f"✅ Ready to embed in HTML!")
    
except FileNotFoundError:
    print("❌ Error: data_housing_unpivoted.xlsx not found")
except Exception as e:
    print(f"❌ Error: {str(e)}")
    import traceback
    traceback.print_exc()
