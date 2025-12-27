# Project Title: Get A Home

## Overview
Get A Home is a web application designed to visualize and interact with historical average price data for apartments. Users can compare prices across different areas, identify top gainers and losers, and adjust the time frame for analysis.

## Features
- Interactive visualization of historical average prices
- Comparison between different areas
- Identification of top gainers and losers
- Adjustable time frame for data analysis

## Project Structure
```
getahome
├── src
│   ├── app.py              # Main entry point of the web application
│   ├── static
│   │   ├── css
│   │   │   └── style.css   # Styles for the web application
│   │   └── js
│   │       └── main.js     # JavaScript for user interactions
│   ├── templates
│   │   └── index.html      # Main HTML template
│   └── utils
│       └── data_loader.py   # Functions for loading and processing data
├── data
│   └── data_housing_unpivoted.xlsx  # Unpivoted historical average price data
├── notebooks
│   └── data_parser.ipynb   # Jupyter notebook for data parsing and transformation
├── requirements.txt         # Project dependencies
└── README.md                # Project documentation
```

## Installation
1. Clone the repository:
   ```
   git clone <repository-url>
   cd getahome
   ```

2. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

## Usage
1. Run the application:
   ```
   python src/app.py
   ```

2. Open your web browser and navigate to `http://127.0.0.1:5000` to access the application.

## Contributing
Contributions are welcome! Please submit a pull request or open an issue for any suggestions or improvements.

## License
This project is licensed under the MIT License. See the LICENSE file for details.