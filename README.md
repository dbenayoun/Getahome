# GetAHome - Israeli Housing Market Analysis

Interactive web application for analyzing Israeli housing market trends and prices.

## Features

- 📊 Historical average price trends
- 🏘️ Area comparison and analysis
- 📈 Top gainers and losers tracking
- 🔍 Filter by time period, district, area, and room type
- 📉 Interactive charts with smooth spline curves

## Data

The app analyzes housing market data across Israeli cities and districts, showing:
- Average prices by quarter
- Room type distributions (2-7+ rooms)
- District-level aggregations
- Year-over-year changes

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```bash
streamlit run app.py
```

## Deployment

This app is ready to deploy on Streamlit Cloud. Simply:
1. Push to GitHub
2. Connect to Streamlit Cloud
3. Deploy!

## Data Source

Data file: `data_housing_unpivoted.xlsx`
