from http.server import BaseHTTPRequestHandler
import json
import cgi
import csv
import io
from statistics import mean, stdev

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
        'price_analysis': {}
    }
    
    # Analyze price data
    if 'close' in numeric_data:
        close_prices = numeric_data['close']
        analysis['price_analysis'] = {
            'latest_price': close_prices[0],
            'average_price': round(mean(close_prices), 2),
            'highest_price': round(max(close_prices), 2),
            'lowest_price': round(min(close_prices), 2),
            'price_volatility': round(stdev(close_prices), 2) if len(close_prices) > 1 else 0
        }
    
    # Volume analysis
    if 'volume' in numeric_data:
        volumes = numeric_data['volume']
        analysis['volume_analysis'] = {
            'average_volume': round(mean(volumes), 0),
            'highest_volume': max(volumes),
            'lowest_volume': min(volumes)
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
                h1, h2 {
                    color: #333;
                    margin-bottom: 20px;
                }
                h1 {
                    text-align: center;
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
                }
                .upload-btn:hover {
                    background-color: #0056b3;
                }
                .analysis-section {
                    margin-top: 15px;
                    padding: 10px;
                    border-bottom: 1px solid #eee;
                }
                .analysis-section h3 {
                    color: #0056b3;
                    margin-bottom: 10px;
                }
                pre {
                    background-color: #f8f9fa;
                    padding: 15px;
                    border-radius: 4px;
                    overflow-x: auto;
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
                function formatAnalysis(data) {
                    let html = '';
                    
                    if (data.basic_info) {
                        html += '<div class="analysis-section">';
                        html += '<h3>Basic Information</h3>';
                        html += `<p>Total Rows: ${data.basic_info.total_rows}</p>`;
                        html += `<p>Date Range: ${data.basic_info.date_range}</p>`;
                        html += '</div>';
                    }
                    
                    if (data.price_analysis) {
                        html += '<div class="analysis-section">';
                        html += '<h3>Price Analysis</h3>';
                        html += `<p>Latest Price: ${data.price_analysis.latest_price}</p>`;
                        html += `<p>Average Price: ${data.price_analysis.average_price}</p>`;
                        html += `<p>Highest Price: ${data.price_analysis.highest_price}</p>`;
                        html += `<p>Lowest Price: ${data.price_analysis.lowest_price}</p>`;
                        html += `<p>Price Volatility: ${data.price_analysis.price_volatility}</p>`;
                        html += '</div>';
                    }
                    
                    if (data.volume_analysis) {
                        html += '<div class="analysis-section">';
                        html += '<h3>Volume Analysis</h3>';
                        html += `<p>Average Volume: ${data.volume_analysis.average_volume}</p>`;
                        html += `<p>Highest Volume: ${data.volume_analysis.highest_volume}</p>`;
                        html += `<p>Lowest Volume: ${data.volume_analysis.lowest_volume}</p>`;
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