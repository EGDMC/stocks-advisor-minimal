from http.server import BaseHTTPRequestHandler
import json
import cgi
import csv
import io
from statistics import mean, stdev
from .smc_analyzer import analyze_smc
from .technical_indicators import analyze_technicals
from .pattern_recognition import analyze_patterns
from .charts import get_chart_config
from .template import HTML_TEMPLATE

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
    
    # Extract OHLCV data
    closes = numeric_data.get('close', [])
    opens = numeric_data.get('open', [])
    highs = numeric_data.get('high', [])
    lows = numeric_data.get('low', [])
    volumes = numeric_data.get('volume', [])
    
    # Calculate moving averages
    ma20 = moving_average(closes, 20) if len(closes) >= 20 else []
    ma50 = moving_average(closes, 50) if len(closes) >= 50 else []
    
    # Technical Analysis
    technical_analysis = analyze_technicals(closes)
    
    # Pattern Recognition
    if all(x is not None for x in [opens, highs, lows, closes, volumes]):
        pattern_analysis = analyze_patterns(highs, lows, opens, closes, volumes)
    else:
        pattern_analysis = {
            'candlestick_patterns': [],
            'price_action_patterns': [],
            'chart_patterns': []
        }
    
    chart_data = {
        'labels': list(dates),
        'prices': [round(price, 2) for price in closes],
        'ma20': list(ma20),
        'ma50': list(ma50),
        'indicators': technical_analysis
    }
    
    analysis = {
        'basic_info': {
            'total_rows': len(data),
            'date_range': f"From {dates[-1]} to {dates[0]}"
        },
        'chart_data': chart_data,
        'technical_signals': technical_analysis.get('signals', {}),
        'patterns': pattern_analysis
    }
    
    # Add SMC analysis
    if closes and volumes:
        smc_results = analyze_smc(closes, volumes)
        analysis['smc_analysis'] = smc_results
        
        # Add SMC markers to chart
        analysis['chart_data']['smc_markers'] = {
            'imbalances': [
                {
                    'index': imb['index'],
                    'price': imb['price'],
                    'type': imb['type'],
                    'strength': imb['strength']
                } for imb in smc_results['imbalances']
            ],
            'fvgs': [
                {
                    'index': fvg['index'],
                    'price': fvg['price'],
                    'type': fvg['type'],
                    'gap_size': fvg['gap_size']
                } for fvg in smc_results['fvgs']
            ],
            'liquidity_levels': [
                {
                    'index': level['index'],
                    'price': level['price'],
                    'type': level['type'],
                    'strength': level['strength']
                } for level in smc_results['liquidity_levels']
            ]
        }
    
    # Get chart configurations
    analysis['chart_configs'] = get_chart_config(chart_data)
    
    if closes:
        latest_price = closes[0]
        price_change = latest_price - closes[-1]
        price_change_pct = (price_change / closes[-1]) * 100
        
        analysis['price_analysis'] = {
            'latest_price': round(latest_price, 2),
            'average_price': round(mean(closes), 2),
            'highest_price': round(max(closes), 2),
            'lowest_price': round(min(closes), 2),
            'volatility': round(stdev(closes), 2) if len(closes) > 1 else 0,
            'total_change': round(price_change, 2),
            'total_change_percentage': round(price_change_pct, 2)
        }
    
    if volumes:
        avg_volume = mean(volumes)
        analysis['volume_analysis'] = {
            'average_volume': int(avg_volume),
            'latest_volume': int(volumes[0])
        }
    
    return analysis

def moving_average(data, window):
    result = []
    for i in range(len(data) - window + 1):
        window_average = sum(data[i:i+window]) / window
        result.append(round(window_average, 2))
    return result

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