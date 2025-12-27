from flask import Flask, render_template, request, jsonify
import pandas as pd

app = Flask(__name__)

# Load the data
data_file = '../data/data_housing_unpivoted.xlsx'
df = pd.read_excel(data_file)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/data', methods=['GET'])
def get_data():
    area = request.args.get('area')
    start_year = request.args.get('start_year', type=int)
    end_year = request.args.get('end_year', type=int)

    filtered_data = df

    if area:
        filtered_data = filtered_data[filtered_data['Area'] == area]

    if start_year:
        filtered_data = filtered_data[filtered_data['Year'] >= start_year]

    if end_year:
        filtered_data = filtered_data[filtered_data['Year'] <= end_year]

    return jsonify(filtered_data.to_dict(orient='records'))

@app.route('/api/top_gainers', methods=['GET'])
def top_gainers():
    gainers = df.groupby('Area')['Average Price'].last() - df.groupby('Area')['Average Price'].first()
    top_gainers = gainers.nlargest(5).reset_index()
    return jsonify(top_gainers.to_dict(orient='records'))

@app.route('/api/top_losers', methods=['GET'])
def top_losers():
    losers = df.groupby('Area')['Average Price'].last() - df.groupby('Area')['Average Price'].first()
    top_losers = losers.nsmallest(5).reset_index()
    return jsonify(top_losers.to_dict(orient='records'))

if __name__ == '__main__':
    app.run(debug=True)