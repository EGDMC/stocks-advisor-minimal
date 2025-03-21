from http.server import BaseHTTPRequestHandler
import json
import cgi
import csv
import io
from statistics import mean, stdev
from datetime import datetime

def calculate_trend(prices):
    if len(prices) < 2:
        return "Insufficient data"
    
    first_price = prices[-1]  # Oldest price
    last_price = prices[0]    # Latest price
    price_change = last_price - first_price
    price_change_pct = (price_change / first_price) * 100
    
    # Determine trend strength
    if price_change_pct > 5:
        return "Strong Upward"
    elif price_change_pct > 2:
        return "Moderate Upward"
    elif price_change_pct > -2:
        return "Sideways"
    elif price_change_pct > -5:
        return "Moderate Downward"
    else:
        return "Strong Downward"

def analyze_stock_data(headers, data):
    # Convert numeric data
    numeric_data = {}
    for i, header in enumerate(headers):
        try:
            values = [float(row[i]) for row in data]
            numeric_data[header] = values
        except (ValueError, TypeError):
            continue
    
    # Calculate statistics
    analysis = {
        'basic_info': {
            'total_rows': len(data),
            'columns': headers,
            'date_range': f"From {data[-1][0]} to {data[0][0]}"
        },
        'price_analysis': {},
        'trend_analysis': {}
    }
    
    # Price analysis
    if 'close' in numeric_data:
        close_prices = numeric_data['close']
        price_change = close_prices[0] - close_prices[-1]
        price_change_pct = (price_change / close_prices[-1]) * 100
        
        analysis['price_analysis'] = {
            'latest_price': round(close_prices[0], 2),
            'average_price': round(mean(close_prices), 2),
            'highest_price': round(max(close_prices), 2),
            'lowest_price': round(min(close_prices), 2),
            'price_volatility': round(stdev(close_prices), 2) if len(close_prices) > 1 else 0,
            'total_change': round(price_change, 2),
            'total_change_percentage': round(price_change_pct, 2)
        }
        
        analysis['trend_analysis'] = {
            'overall_trend': calculate_trend(close_prices),
            'recent_trend': calculate_trend(close_prices[:10])  # Last 10 days
        }
    
    # Volume analysis
    if 'volume' in numeric_data:
        volumes = numeric_data['volume']
        avg_volume = mean(volumes)
        analysis['volume_analysis'] = {
            'average_volume': int(round(avg_volume, 0)),
            'highest_volume': int(max(volumes)),
            'lowest_volume': int(min(volumes)),
            'volume_trend': 'Above Average' if volumes[0] > avg_volume else 'Below Average'
        }
    
    return analysis

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        html_content = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Stock Market Analysis</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    line-height: 1.6;
                    margin: 0;
                    padding: 20px;
                    background-color: #f8f9fa;
                }
                .container {
                    max-width: 800px;
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
                h1, h2, h3 {
                    color: #333;
                    margin-bottom: 20px;
                }
                h1 {
                    text-align: center;
                    color: #2c3e50;
                }
                .form-group {
                    margin-bottom: 20px;
                }
                .upload-btn {
                    background-color: #007bff;
                    color: white;
                    padding: 10px 20px;
                    border: none;
                    border-radius: 4px;
                    cursor: pointer;
                    transition: background-color 0.3s;
                }
                .upload-btn:hover {
                    background-color: #0056b3;
                }
                .analysis-section {
                    margin-top: 15px;
                    padding: 15px;
                    border-bottom: 1px solid #eee;
                }
                .analysis-section:last-child {
                    border-bottom: none;
                }
                .analysis-section h3 {
                    color: #2c3e50;
                    font-size: 1.2em;
                    margin-bottom: 15px;
                }
                .metric {
                    display: flex;
                    justify-content: space-between;
                    margin-bottom: 10px;
                    padding: 5px 0;
                }
                .metric-label {
                    color: #666;
                }
                .metric-value {
                    font-weight: bold;
                    color: #2c3e50;
                }
                .trend-positive {
                    color: #27ae60;
                }
                .trend-negative {
                    color: #c0392b;
                }
                .trend-neutral {
                    color: #7f8c8d;
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
                
                <div id="result" class="card" style="display: none;">
                    <h2>Analysis Results</h2>
                    <div id="resultContent"></div>
                </div>
            </div>
            
            <script>
                function getTrendClass(value) {
                    if (value.includes('Upward') || value.includes('Above')) return 'trend-positive';
                    if (value.includes('Downward') || value.includes('Below')) return 'trend-negative';
                    return 'trend-neutral';
                }
                
                function formatMetric(label, value, isTrend = false) {
                    const valueClass = isTrend ? getTrendClass(value) : '';
                    return `
                        <div class="metric">
                            <span class="metric-label">${label}:</span>
                            <span class="metric-value ${valueClass}">${value}</span>
                        </div>
                    `;
                }
                
                function formatAnalysis(data) {
                    let html = '';
                    
                    if (data.basic_info) {
                        html += '<div class="analysis-section">';
                        html += '<h3>Basic Information</h3>';
                        html += formatMetric('Total Rows', data.basic_info.total_rows);
                        html += formatMetric('Date Range', data.basic_info.date_range);
                        html += '</div>';
                    }
                    
                    if (data.price_analysis) {
                        html += '<div class="analysis-section">';
                        html += '<h3>Price Analysis</h3>';
                        html += formatMetric('Latest Price', `$${data.price_analysis.latest_price}`);
                        html += formatMetric('Average Price', `$${data.price_analysis.average_price}`);
                        html += formatMetric('Highest Price', `$${data.price_analysis.highest_price}`);
                        html += formatMetric('Lowest Price', `$${data.price_analysis.lowest_price}`);
                        html += formatMetric('Price Change', 
                            `$${data.price_analysis.total_change} (${data.price_analysis.total_change_percentage}%)`,
                            true);
                        html += formatMetric('Price Volatility', data.price_analysis.price_volatility);
                        html += '</div>';
                    }
                    
                    if (data.trend_analysis) {
                        html += '<div class="analysis-section">';
                        html += '<h3>Trend Analysis</h3>';
                        html += formatMetric('Overall Trend', data.trend_analysis.overall_trend, true);
                        html += formatMetric('Recent Trend', data.trend_analysis.recent_trend, true);
                        html += '</div>';
                    }
                    
                    if (data.volume_analysis) {
                        html += '<div class="analysis-section">';
                        html += '<h3>Volume Analysis</h3>';
                        html += formatMetric('Average Volume', data.volume_analysis.average_volume.toLocaleString());
                        html += formatMetric('Highest Volume', data.volume_analysis.highest_volume.toLocaleString());
                        html += formatMetric('Lowest Volume', data.volume_analysis.lowest_volume.toLocaleString());
                        html += formatMetric('Current Volume Trend', data.volume_analysis.volume_trend, true);
                        html += '</div>';
                    }
                    
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
                        
                        const resultDiv = document.getElementById('result');
                        const resultContent = document.getElementById('resultContent');
                        
                        if (result.status === 'success') {
                            resultContent.innerHTML = formatAnalysis(result.analysis);
                        } else {
                            resultContent.innerHTML = `<p class="error">Error: ${result.message}</p>`;
                        }
                        
                        resultDiv.style.display = 'block';
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