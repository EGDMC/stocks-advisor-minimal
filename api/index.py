from http.server import BaseHTTPRequestHandler
import json
import cgi
import csv
import io
from statistics import mean, stdev

def moving_average(data, window):
    result = []
    for i in range(len(data) - window + 1):
        window_average = sum(data[i:i+window]) / window
        result.append(round(window_average, 2))
    return result

def find_support_resistance(prices, n_points=5):
    supports = []
    resistances = []
    
    for i in range(n_points, len(prices) - n_points):
        current_price = prices[i]
        left_prices = prices[i-n_points:i]
        right_prices = prices[i+1:i+n_points+1]
        
        if all(current_price <= p for p in left_prices) and all(current_price <= p for p in right_prices):
            supports.append(current_price)
        elif all(current_price >= p for p in left_prices) and all(current_price >= p for p in right_prices):
            resistances.append(current_price)
    
    supports = sorted(supports)[:3]
    resistances = sorted(resistances, reverse=True)[:3]
    
    return {
        'support_levels': [round(price, 2) for price in supports],
        'resistance_levels': [round(price, 2) for price in resistances]
    }

def analyze_stock_data(headers, data):
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
    
    levels = find_support_resistance(close_prices) if len(close_prices) > 10 else {
        'support_levels': [],
        'resistance_levels': []
    }
    
    ma20 = moving_average(close_prices, 20) if len(close_prices) >= 20 else []
    ma50 = moving_average(close_prices, 50) if len(close_prices) >= 50 else []
    
    chart_data = {
        'labels': dates,
        'prices': [round(price, 2) for price in close_prices],
        'ma20': ma20,
        'ma50': ma50
    }
    
    analysis = {
        'basic_info': {
            'total_rows': len(data),
            'date_range': f"From {dates[-1]} to {dates[0]}"
        },
        'chart_data': chart_data,
        'technical_levels': levels
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
            'volatility': round(stdev(close_prices), 2) if len(close_prices) > 1 else 0,
            'total_change': round(price_change, 2),
            'total_change_percentage': round(price_change_pct, 2)
        }
    
    if 'volume' in numeric_data:
        volumes = numeric_data['volume']
        avg_volume = mean(volumes)
        analysis['volume_analysis'] = {
            'average_volume': int(avg_volume),
            'latest_volume': int(volumes[0])
        }
    
    return analysis

# Read the HTML template
with open('vercel-deploy/api/index.html', 'r') as f:
    HTML_TEMPLATE = f.read()

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(HTML_TEMPLATE.encode('utf-8'))

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