from http.server import BaseHTTPRequestHandler
import json
import cgi
import csv
import io
from statistics import mean, stdev
import numpy as np

def find_support_resistance(prices, n_points=5):
    """Find support and resistance levels using local min/max"""
    supports = []
    resistances = []
    
    prices = np.array(prices)
    for i in range(n_points, len(prices) - n_points):
        left_array = prices[i-n_points:i]
        right_array = prices[i+1:i+n_points+1]
        
        if np.all(prices[i] <= left_array) and np.all(prices[i] <= right_array):
            supports.append((i, prices[i]))
        elif np.all(prices[i] >= left_array) and np.all(prices[i] >= right_array):
            resistances.append((i, prices[i]))
    
    # Get most recent levels
    supports = sorted(supports, key=lambda x: x[1])[:3]
    resistances = sorted(resistances, key=lambda x: x[1], reverse=True)[:3]
    
    return {
        'support_levels': [round(price, 2) for _, price in supports],
        'resistance_levels': [round(price, 2) for _, price in resistances]
    }

def analyze_stock_data(headers, data):
    # Convert data
    numeric_data = {}
    dates = []
    for i, header in enumerate(headers):
        try:
            values = [float(row[i]) for row in data]
            numeric_data[header] = values
        except (ValueError, TypeError):
            if header.lower() == 'date':
                dates = [row[i] for row in data]
    
    close_prices = numeric_data.get('close', [])
    
    # Calculate support and resistance
    levels = find_support_resistance(close_prices) if len(close_prices) > 10 else {
        'support_levels': [],
        'resistance_levels': []
    }
    
    # Prepare chart data
    chart_data = {
        'labels': dates,
        'prices': [round(price, 2) for price in close_prices],
        'volumes': numeric_data.get('volume', []),
    }
    
    # Calculate technical levels
    if close_prices:
        price_array = np.array(close_prices)
        ma20 = np.convolve(price_array, np.ones(20)/20, mode='valid')
        ma50 = np.convolve(price_array, np.ones(50)/50, mode='valid')
        
        chart_data['ma20'] = [round(x, 2) for x in ma20]
        chart_data['ma50'] = [round(x, 2) for x in ma50]
    
    analysis = {
        'basic_info': {
            'total_rows': len(data),
            'date_range': f"From {dates[-1]} to {dates[0]}"
        },
        'chart_data': chart_data,
        'technical_levels': {
            'support_levels': levels['support_levels'],
            'resistance_levels': levels['resistance_levels']
        }
    }
    
    if close_prices:
        latest_price = close_prices[0]
        price_change = latest_price - close_prices[-1]
        price_change_pct = (price_change / close_prices[-1]) * 100
        
        analysis['price_analysis'] = {
            'latest_price': round(latest_price, 2),
            'average_price': round(mean(close_prices), 2),
            'highest_price': round(max(close_prices), 2),
            'lowest_price': round(min(close_prices), 2),
            'volatility': round(stdev(close_prices), 2),
            'total_change': round(price_change, 2),
            'total_change_percentage': round(price_change_pct, 2)
        }
    
    if 'volume' in numeric_data:
        volumes = numeric_data['volume']
        analysis['volume_analysis'] = {
            'average_volume': int(mean(volumes)),
            'latest_volume': int(volumes[0])
        }
    
    return analysis

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        html_content = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Stock Market Analysis</title>
            <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    line-height: 1.6;
                    margin: 0;
                    padding: 20px;
                    background-color: #f8f9fa;
                }
                .container {
                    max-width: 1200px;
                    margin: 0 auto;
                    padding: 20px;
                }
                .card {
                    background: white;
                    border-radius: 8px;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                    padding: 20px;
                    margin-top: 20px;
                }
                .chart-container {
                    position: relative;
                    height: 400px;
                    width: 100%;
                }
                h1, h2, h3 {
                    color: #2c3e50;
                    margin-bottom: 20px;
                }
                h1 {
                    text-align: center;
                }
                .metrics-grid {
                    display: grid;
                    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
                    gap: 20px;
                    margin-top: 20px;
                }
                .metric-card {
                    background: #fff;
                    padding: 15px;
                    border-radius: 8px;
                    box-shadow: 0 1px 3px rgba(0,0,0,0.1);
                }
                .metric-value {
                    font-size: 1.5em;
                    font-weight: bold;
                    color: #2c3e50;
                }
                .metric-label {
                    color: #7f8c8d;
                    font-size: 0.9em;
                }
                .positive {
                    color: #27ae60;
                }
                .negative {
                    color: #c0392b;
                }
                .upload-btn {
                    background-color: #3498db;
                    color: white;
                    padding: 12px 24px;
                    border: none;
                    border-radius: 4px;
                    cursor: pointer;
                    font-size: 1em;
                    transition: background-color 0.3s;
                }
                .upload-btn:hover {
                    background-color: #2980b9;
                }
                .technical-levels {
                    margin-top: 20px;
                    padding: 15px;
                    background: #f8f9fa;
                    border-radius: 8px;
                }
                .level-item {
                    display: flex;
                    justify-content: space-between;
                    padding: 5px 0;
                }
                .resistance {
                    color: #e74c3c;
                }
                .support {
                    color: #2ecc71;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Stock Market Analysis</h1>
                
                <div class="card">
                    <h2>Data Upload</h2>
                    <form action="/api" method="post" enctype="multipart/form-data">
                        <div class="form-group">
                            <label>Upload your stock data (CSV):</label><br>
                            <input type="file" name="file" accept=".csv" style="margin: 10px 0;" required>
                        </div>
                        <button type="submit" class="upload-btn">Upload and Analyze</button>
                    </form>
                </div>
                
                <div id="result" style="display: none;">
                    <div class="card">
                        <h2>Price Chart</h2>
                        <div class="chart-container">
                            <canvas id="priceChart"></canvas>
                        </div>
                    </div>
                    
                    <div class="card">
                        <h2>Technical Levels</h2>
                        <div id="technicalLevels" class="technical-levels"></div>
                    </div>
                    
                    <div class="card">
                        <h2>Analysis Results</h2>
                        <div id="resultContent"></div>
                    </div>
                </div>
            </div>
            
            <script>
                let priceChart = null;
                
                function formatNumber(num) {
                    return new Intl.NumberFormat().format(num);
                }
                
                function createChart(data) {
                    const ctx = document.getElementById('priceChart').getContext('2d');
                    
                    if (priceChart) {
                        priceChart.destroy();
                    }
                    
                    priceChart = new Chart(ctx, {
                        type: 'line',
                        data: {
                            labels: data.labels.reverse(),
                            datasets: [
                                {
                                    label: 'Price',
                                    data: data.prices.reverse(),
                                    borderColor: '#2c3e50',
                                    tension: 0.1
                                },
                                {
                                    label: '20-day MA',
                                    data: Array(data.labels.length - data.ma20.length)
                                        .fill(null)
                                        .concat(data.ma20.reverse()),
                                    borderColor: '#e74c3c',
                                    borderWidth: 1,
                                    pointRadius: 0
                                },
                                {
                                    label: '50-day MA',
                                    data: Array(data.labels.length - data.ma50.length)
                                        .fill(null)
                                        .concat(data.ma50.reverse()),
                                    borderColor: '#3498db',
                                    borderWidth: 1,
                                    pointRadius: 0
                                }
                            ]
                        },
                        options: {
                            responsive: true,
                            maintainAspectRatio: false,
                            plugins: {
                                legend: {
                                    position: 'top',
                                }
                            },
                            scales: {
                                y: {
                                    beginAtZero: false
                                }
                            }
                        }
                    });
                }
                
                function formatTechnicalLevels(levels) {
                    let html = '';
                    
                    if (levels.resistance_levels.length > 0) {
                        html += '<h3>Resistance Levels</h3>';
                        levels.resistance_levels.forEach(level => {
                            html += `<div class="level-item">
                                <span>Resistance</span>
                                <span class="resistance">$${level}</span>
                            </div>`;
                        });
                    }
                    
                    if (levels.support_levels.length > 0) {
                        html += '<h3>Support Levels</h3>';
                        levels.support_levels.forEach(level => {
                            html += `<div class="level-item">
                                <span>Support</span>
                                <span class="support">$${level}</span>
                            </div>`;
                        });
                    }
                    
                    return html;
                }
                
                function formatMetrics(analysis) {
                    let html = '<div class="metrics-grid">';
                    
                    if (analysis.price_analysis) {
                        const pa = analysis.price_analysis;
                        const changeClass = pa.total_change >= 0 ? 'positive' : 'negative';
                        const changeSymbol = pa.total_change >= 0 ? '+' : '';
                        
                        html += `
                            <div class="metric-card">
                                <div class="metric-value">$${pa.latest_price}</div>
                                <div class="metric-label">Latest Price</div>
                            </div>
                            <div class="metric-card">
                                <div class="metric-value ${changeClass}">
                                    ${changeSymbol}${pa.total_change_percentage}%
                                </div>
                                <div class="metric-label">Total Change</div>
                            </div>
                            <div class="metric-card">
                                <div class="metric-value">$${pa.average_price}</div>
                                <div class="metric-label">Average Price</div>
                            </div>
                            <div class="metric-card">
                                <div class="metric-value">${pa.volatility}</div>
                                <div class="metric-label">Volatility</div>
                            </div>
                        `;
                    }
                    
                    if (analysis.volume_analysis) {
                        const va = analysis.volume_analysis;
                        html += `
                            <div class="metric-card">
                                <div class="metric-value">${formatNumber(va.latest_volume)}</div>
                                <div class="metric-label">Latest Volume</div>
                            </div>
                            <div class="metric-card">
                                <div class="metric-value">${formatNumber(va.average_volume)}</div>
                                <div class="metric-label">Average Volume</div>
                            </div>
                        `;
                    }
                    
                    html += '</div>';
                    return html;
                }
                
                document.querySelector('form').onsubmit = async (e) => {
                    e.preventDefault();
                    const formData = new FormData(e.target);
                    
                    try {
                        const response = await fetch('/api', {
                            method: 'POST',
                            body: formData
                        });
                        const result = await response.json();
                        
                        if (result.status === 'success') {
                            document.getElementById('result').style.display = 'block';
                            document.getElementById('resultContent').innerHTML = formatMetrics(result.analysis);
                            document.getElementById('technicalLevels').innerHTML = 
                                formatTechnicalLevels(result.analysis.technical_levels);
                            createChart(result.analysis.chart_data);
                        } else {
                            alert('Error: ' + result.message);
                        }
                    } catch (error) {
                        console.error('Error:', error);
                        alert('Error processing file: ' + error.message);
                    }
                };
            </script>
        </body>
        </html>
        """
        
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(html_content.encode('utf-8'))

    def do_POST(self):
        try:
            form = cgi.FieldStorage(
                fp=self.rfile,
                headers=self.headers,
                environ={'REQUEST_METHOD': 'POST'}
            )
            
            if 'file' in form:
                fileitem = form['file']
                if fileitem.filename:
                    file_content = fileitem.file.read().decode('utf-8')
                    csv_reader = csv.reader(io.StringIO(file_content))
                    
                    headers = next(csv_reader)
                    data = list(csv_reader)
                    
                    analysis_result = analyze_stock_data(headers, data)
                    
                    response = {
                        'status': 'success',
                        'filename': fileitem.filename,
                        'analysis': analysis_result
                    }
                else:
                    response = {
                        'status': 'error',
                        'message': 'No file was uploaded'
                    }
            else:
                response = {
                    'status': 'error',
                    'message': 'No file field in form'
                }
        except Exception as e:
            response = {
                'status': 'error',
                'message': f'Error processing file: {str(e)}'
            }

        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(response).encode('utf-8'))