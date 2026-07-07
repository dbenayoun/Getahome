# GetAHome — Israeli Housing Market Analysis

A data pipeline and interactive web app for analyzing apartment price trends
across Israeli cities and districts (data sourced from Yad2 listings).

## Features

- Historical average price trends by quarter
- Area/district comparison and top gainers/losers tracking
- Filters by time period, district, area, and room type
- Interactive charts with smooth spline curves

## Project structure

```
scrapper.py                 # Pulls raw listing data from Yad2
data_housing_fullhisto.xlsx # Raw scraped history
data_housing_unpivoted.xlsx # Cleaned, unpivoted dataset used by the app
data_parser.ipynb           # Exploration/cleaning notebook

app.py                      # Main Streamlit app (reads data_housing_unpivoted.xlsx)

generate_json_data.py       # Exports the dataset to housing_data.json
generate_lite_data.py       # Exports a lighter dataset to housing_data_lite.json
generate_widget_html.py     # Builds housing_searchprice.html (standalone price lookup widget)
export_chart.py             # Builds housing_chart.html (standalone Plotly chart)
getahome.html / getahome_withchart.html  # Standalone HTML exports, embeddable outside Streamlit (e.g. on a website)

test_api.py                 # Quick checks against the Yad2 API
simulateur_rules.txt        # Spec notes for a budget/total-cost simulator (in French)
```

The standalone `.html` files are self-contained widgets with the data
embedded directly in the page — they don't need a Python server, just open
them in a browser or embed them in an existing site.

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```bash
streamlit run app.py
```

## Deployment

Ready to deploy on Streamlit Cloud:
1. Push to GitHub
2. Connect to Streamlit Cloud
3. Deploy

## Data source

Listings are scraped from Yad2 (`scrapper.py`) and processed into
`data_housing_unpivoted.xlsx`, the single source of truth used by the app and
by every export script above.
