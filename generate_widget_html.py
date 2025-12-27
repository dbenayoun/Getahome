import json

# Lire les données JSON
with open('housing_data_lite.json', 'r', encoding='utf-8') as f:
    housing_data = json.load(f)

# Convertir en format compact pour JavaScript
json_data = json.dumps(housing_data, separators=(',', ':'), ensure_ascii=False)

# Créer le HTML complet
html_content = f'''<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Recherche de Prix Immobilier</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: Arial, Helvetica, sans-serif;
            background-color: transparent;
            padding: 0;
        }}

        .widget-container {{
            max-width: 900px;
            margin: 0 auto;
            background: white;
            border-radius: 8px;
            box-shadow: 0 1px 4px rgba(0, 0, 0, 0.08);
            padding: 24px;
        }}

        .widget-header {{
            text-align: center;
            margin-bottom: 24px;
            padding-bottom: 16px;
            border-bottom: 1px solid #f0f0f0;
        }}

        .widget-header h2 {{
            color: #000;
            font-size: 22px;
            margin-bottom: 4px;
            font-weight: 600;
            letter-spacing: -0.5px;
        }}

        .widget-header p {{
            color: #666;
            font-size: 13px;
            font-weight: 400;
        }}

        .widget-content {{
            display: flex;
            gap: 20px;
            align-items: flex-start;
        }}

        .search-section {{
            flex: 0 0 280px;
            display: flex;
            flex-direction: column;
            gap: 12px;
        }}

        .search-inputs {{
            background: #f8f9fa;
            border: 1px solid #e9ecef;
            border-radius: 4px;
            padding: 20px;
            display: flex;
            flex-direction: column;
            gap: 12px;
        }}

        .result-section {{
            flex: 1;
            min-width: 0;
        }}

        .input-group {{
            display: flex;
            flex-direction: column;
        }}

        .input-group label {{
            color: #444;
            font-size: 12px;
            font-weight: 500;
            margin-bottom: 6px;
        }}

        .select-input {{
            padding: 10px 12px;
            border: 1px solid #ddd;
            border-radius: 4px;
            font-size: 14px;
            font-family: Arial, Helvetica, sans-serif;
            background-color: #fafafa;
            cursor: pointer;
            transition: all 0.2s ease;
        }}

        .select-input:hover {{
            background-color: #f5f5f5;
            border-color: #ccc;
        }}

        .select-input:focus {{
            outline: none;
            border-color: #999;
            background-color: white;
        }}

        .result-card {{
            background: #f8f9fa;
            border: 1px solid #e9ecef;
            border-radius: 4px;
            padding: 20px;
            display: none;
            min-height: auto;
        }}

        .result-card.show {{
            display: block;
        }}

        .result-label {{
            font-size: 11px;
            color: #666;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 8px;
        }}

        .result-price {{
            font-size: 36px;
            font-weight: 700;
            color: #000;
            margin-bottom: 8px;
            line-height: 1;
        }}

        .result-location {{
            font-size: 14px;
            color: #444;
            margin-bottom: 8px;
        }}

        .result-change {{
            display: inline-block;
            padding: 4px 10px;
            border-radius: 12px;
            font-size: 12px;
            font-weight: 500;
            color: #495057;
        }}

        .result-change.positive {{
            background: #d4edda;
            color: #155724;
        }}

        .result-change.negative {{
            background: #f8d7da;
            color: #721c24;
        }}

        .no-data {{
            text-align: center;
            padding: 20px;
            color: #666;
            background: #fff3cd;
            border-radius: 4px;
            border: 1px solid #ffeaa7;
            display: none;
            font-size: 13px;
        }}

        .no-data.show {{
            display: block;
        }}

        @media (max-width: 768px) {{
            .widget-content {{
                flex-direction: column;
            }}

            .search-section {{
                flex: 1;
                width: 100%;
            }}

            .result-section {{
                width: 100%;
            }}

            .widget-container {{
                padding: 16px;
            }}
        }}
    </style>
</head>
<body>
    <div class="widget-container">
        <div class="widget-header">
            <h2>Recherche de Prix Immobilier</h2>
            <p>Prix moyens par ville et nombre de pièces</p>
        </div>

        <div class="widget-content">
            <div class="search-section">
                <div class="search-inputs">
                    <div class="input-group">
                        <label for="citySelect">Ville</label>
                        <select id="citySelect" class="select-input">
                            <option value="">Sélectionner...</option>
                        </select>
                    </div>

                    <div class="input-group">
                        <label for="roomSelect">Pièces (salon + chambre(s))</label>
                        <select id="roomSelect" class="select-input">
                            <option value="">Sélectionner...</option>
                        </select>
                    </div>
                </div>
            </div>

            <div class="result-section">
                <div class="result-card" id="resultCard">
                    <div class="result-label" id="resultPeriod">T3 2025</div>
                    <div class="result-price" id="resultPrice">₪4,020,000</div>
                    <div class="result-location" id="resultLocation">Tel Aviv - 4-3.5</div>
                    <div class="result-change" id="resultChange">+5.8% sur 1 an</div>
                </div>

                <div class="no-data" id="noData">
                    <p>Aucune donnée disponible pour cette combinaison</p>
                </div>
            </div>
        </div>
    </div>

    <script>
        // Embedded housing data - Latest quarter and year ago for YoY comparison
        const housingData = {json_data};

        // Load data function - now just initializes the dropdowns
        async function loadData() {{
            try {{
                populateDropdowns();
            }} catch (error) {{
                console.error('Error initializing widget:', error);
            }}
        }}

        // Populate city and room dropdowns
        function populateDropdowns() {{
            // Get unique cities (excluding districts)
            const cities = [...new Set(housingData
                .filter(item => !item.Is_District)
                .map(item => item.Area))]
                .sort();

            // Get unique room types
            const roomTypes = [...new Set(housingData.map(item => item.Rooms))].sort();

            // Populate city dropdown
            const citySelect = document.getElementById('citySelect');
            citySelect.innerHTML = '<option value="">Sélectionner...</option>';
            cities.forEach(city => {{
                const option = document.createElement('option');
                option.value = city;
                option.textContent = city;
                if (city === 'Tel Aviv') option.selected = true;
                citySelect.appendChild(option);
            }});

            // Populate room dropdown
            const roomSelect = document.getElementById('roomSelect');
            roomSelect.innerHTML = '<option value="">Sélectionner...</option>';
            roomTypes.forEach(room => {{
                const option = document.createElement('option');
                option.value = room;
                // Translate "All" to French
                option.textContent = room === 'All' ? 'Tous' : room;
                if (room === '4-3.5') option.selected = true;
                roomSelect.appendChild(option);
            }});

            // Add event listeners
            citySelect.addEventListener('change', updatePrice);
            roomSelect.addEventListener('change', updatePrice);

            // Show initial result
            updatePrice();
        }}

        // Update price display based on selection
        function updatePrice() {{
            const city = document.getElementById('citySelect').value;
            const rooms = document.getElementById('roomSelect').value;

            if (!city || !rooms) {{
                document.getElementById('resultCard').classList.remove('show');
                document.getElementById('noData').classList.remove('show');
                return;
            }}

            // Get latest quarter
            const maxQuarter = Math.max(...housingData.map(item => new Date(item.Quarter_ts).getTime()));

            // Filter data for selected city, rooms, and latest quarter
            const latestData = housingData.filter(item => 
                item.Area === city && 
                item.Rooms === rooms && 
                new Date(item.Quarter_ts).getTime() === maxQuarter
            );

            if (latestData.length === 0) {{
                document.getElementById('resultCard').classList.remove('show');
                document.getElementById('noData').classList.add('show');
                return;
            }}

            const data = latestData[0];
            const price = data['Average Price'];

            // Calculate YoY change
            const yearAgo = new Date(maxQuarter);
            yearAgo.setFullYear(yearAgo.getFullYear() - 1);

            const prevData = housingData.filter(item => 
                item.Area === city && 
                item.Rooms === rooms && 
                Math.abs(new Date(item.Quarter_ts).getTime() - yearAgo.getTime()) < 100 * 24 * 60 * 60 * 1000 // Within 100 days
            );

            // Update display
            document.getElementById('resultPeriod').textContent = `T${{data.Quarter}} ${{data.Year}}`;
            // Display full price in shekels (data is in millions, multiply by 1,000,000)
            const fullPrice = Math.round(price * 1000000);
            document.getElementById('resultPrice').textContent = `₪${{fullPrice.toLocaleString('fr-FR')}}`;
            const roomsLabel = rooms === 'All' ? 'Tous' : rooms;
            document.getElementById('resultLocation').textContent = `${{city}} - ${{roomsLabel}}`;

            const changeEl = document.getElementById('resultChange');
            if (prevData.length > 0) {{
                const prevPrice = prevData[0]['Average Price'];
                const change = ((price - prevPrice) / prevPrice) * 100;
                changeEl.textContent = `${{change > 0 ? '+' : ''}}${{change.toFixed(1)}}% sur 1 an`;
                changeEl.className = 'result-change ' + (change >= 0 ? 'positive' : 'negative');
            }} else {{
                changeEl.textContent = 'Pas de données annuelles';
                changeEl.className = 'result-change';
            }}

            document.getElementById('noData').classList.remove('show');
            document.getElementById('resultCard').classList.add('show');
        }}

        // Load data when page loads
        window.addEventListener('DOMContentLoaded', loadData);
    </script>
</body>
</html>'''

# Écrire le fichier HTML
with open('housing_searchprice.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

print("✅ Fichier HTML créé avec succès!")
print(f"📊 Taille du fichier: {len(html_content):,} caractères")
print(f"📊 Nombre d'enregistrements: {len(housing_data)}")
