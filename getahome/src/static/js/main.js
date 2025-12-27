// This file contains the JavaScript code for the web application. It handles user interactions, such as adjusting the time frame, comparing areas, and displaying top gainers and losers.

document.addEventListener('DOMContentLoaded', function() {
    const areaSelect = document.getElementById('area-select');
    const timeframeSelect = document.getElementById('timeframe-select');
    const compareButton = document.getElementById('compare-button');
    const resultsDiv = document.getElementById('results');

    // Load data from the server
    async function loadData() {
        const response = await fetch('/api/data');
        return await response.json();
    }

    // Update the visualization based on selected area and timeframe
    async function updateVisualization() {
        const selectedArea = areaSelect.value;
        const selectedTimeframe = timeframeSelect.value;
        const data = await loadData();

        // Filter data based on user selection
        const filteredData = data.filter(item => 
            item.Area === selectedArea && 
            item.Quarter_ts >= selectedTimeframe.start && 
            item.Quarter_ts <= selectedTimeframe.end
        );

        // Display results
        displayResults(filteredData);
    }

    // Display results in the resultsDiv
    function displayResults(data) {
        resultsDiv.innerHTML = ''; // Clear previous results
        if (data.length === 0) {
            resultsDiv.innerHTML = '<p>No data available for the selected criteria.</p>';
            return;
        }

        // Create a table to display the data
        const table = document.createElement('table');
        const headerRow = document.createElement('tr');
        headerRow.innerHTML = '<th>Area</th><th>Rooms</th><th>Average Price</th>';
        table.appendChild(headerRow);

        data.forEach(item => {
            const row = document.createElement('tr');
            row.innerHTML = `<td>${item.Area}</td><td>${item.Rooms}</td><td>${item['Average Price']}</td>`;
            table.appendChild(row);
        });

        resultsDiv.appendChild(table);
    }

    // Event listener for the compare button
    compareButton.addEventListener('click', updateVisualization);
});