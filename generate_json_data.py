"""
Generate JSON data file from Excel for the housing price lookup widget
"""
import pandas as pd
import json

print("🔄 Converting Excel data to JSON...")

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
    
    # Convert Quarter_ts to string format for JSON
    df['Quarter_ts'] = df['Quarter_ts'].dt.strftime('%Y-%m-%d')
    
    # Convert to JSON
    json_data = df.to_dict(orient='records')
    
    # Save to file
    with open('housing_data.json', 'w', encoding='utf-8') as f:
        json.dump(json_data, f, ensure_ascii=False, indent=2)
    
    print(f"✅ Generated housing_data.json with {len(df)} records")
    
    # Print some statistics
    print(f"\n📊 Data Summary:")
    print(f"   - Cities: {df[~df['Is_District']]['Area'].nunique()}")
    print(f"   - Districts: {df[df['Is_District']]['Area'].nunique()}")
    print(f"   - Room types: {df['Rooms'].nunique()}")
    print(f"   - Date range: {df['Year'].min()} - {df['Year'].max()}")
    print(f"   - Latest quarter: {df['Quarter'].iloc[-1]} {df['Year'].iloc[-1]}")
    
    print(f"\n✅ Success! You can now use housing_searchprice.html")
    print(f"   Make sure housing_data.json is in the same directory as the HTML file")
    
except FileNotFoundError:
    print("❌ Error: data_housing_unpivoted.xlsx not found")
    print("   Make sure the Excel file is in the current directory")
except Exception as e:
    print(f"❌ Error: {str(e)}")
    import traceback
    traceback.print_exc()
