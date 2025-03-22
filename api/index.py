from http.server import BaseHTTPRequestHandler
import json
import io
import csv
from urllib.parse import parse_header
from statistics import mean, stdev
from .technical_indicators import analyze_technicals
from .pattern_recognition import analyze_patterns
from .trend_prediction import analyze_trend
from .smc_analyzer import analyze_smc
from .charts import get_chart_config
from .template import HTML_TEMPLATE

def parse_multipart_form(headers, rfile):
    """Parse multipart form data without using cgi module"""
    content_type = headers.get('content-type', '')
    if not content_type:
        return None
    
    boundary = None
    for item in content_type.split(';'):
        if 'boundary=' in item:
            boundary = item.split('=', 1)[1].strip('"')
            break
    
    if not boundary:
        return None
    
    content_length = int(headers.get('content-length', 0))
    data = rfile.read(content_length)
    
    # Split at boundary and process parts
    parts = data.split(('--' + boundary).encode())
    
    for part in parts:
        # Skip empty parts and boundary end
        if not part or part.strip() == b'--':
            continue
        
        # Split headers from content
        try:
            headers_end = part.index(b'\r\n\r\n')
            part_headers = part[:headers_end].decode()
            part_content = part[headers_end + 4:]
            
            if 'filename=' in part_headers:
                # Found the file part
                return io.StringIO(part_content.decode('utf-8'))
        except:
            continue
    
    return None

def analyze_stock_data(headers, data):
    numeric_data = {}
    dates = []
    
    # Extract data from CSV
    for i, header in enumerate(headers):
        try:
            values = [float(row[i]) for row in data]
            numeric_data[header.lower()] = values
        except (ValueError, TypeError):
            if header.lower() == 'date':
                dates = [row[i] for row in data]
    
    # Get required data series
    closes = numeric_data.get('close', [])
    opens = numeric_data.get('open', [])
    highs = numeric_data.get('high', [])
    lows = numeric_data.get('low', [])
    volumes = numeric_data.get('volume', [])
    
    # Perform analyses
    analysis = {}
    
    # Basic price analysis
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
    
    # Volume analysis
    if volumes:
        avg_volume = mean(volumes)
        analysis['volume_analysis'] = {
            'average_volume': int(avg_volume),
            'latest_volume': int(volumes[0])
        }
    
    # Technical analysis
    if closes:
        technical_analysis = analyze_technicals(closes)
        analysis['technical_signals'] = technical_analysis.get('signals', {})
    
    # Pattern recognition
    if all(x is not None for x in [opens, highs, lows, closes, volumes]):
        analysis['patterns'] = analyze_patterns(highs, lows, opens, closes, volumes)
    
    # SMC analysis
    if closes and volumes:
        smc_results = analyze_smc(closes, volumes)
        analysis['smc_analysis'] = smc_results
        
        # Get support/resistance levels for trend analysis
        support_resistance_levels = [
            {'price': level['price'], 'type': level['type']}
            for level in smc_results.get('liquidity_levels', [])
        ]
        
        # Trend analysis
        analysis['trend_analysis'] = analyze_trend(
            closes, 
            volumes, 
            analysis.get('patterns', {}).get('chart_patterns', []),
            support_resistance_levels
        )
    
    # Chart configurations
    chart_data = {
        'labels': dates,
        'prices': [round(p, 2) for p in closes] if closes else [],
        'volumes': volumes if volumes else [],
        'indicators': technical_analysis if 'technical_analysis' in locals() else {}
    }
    analysis['chart_configs'] = get_chart_config(chart_data)
    
    return analysis

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(HTML_TEMPLATE.encode())

    def do_POST(self):
        try:
            file_content = parse_multipart_form(self.headers, self.rfile)
            
            if file_content:
                csv_reader = csv.reader(file_content)
                headers = next(csv_reader)
                data = list(csv_reader)
                
                analysis = analyze_stock_data(headers, data)
                response = {
                    'status': 'success',
                    'analysis': analysis
                }
            else:
                response = {
                    'status': 'error',
                    'message': 'No file was uploaded'
                }
                
        except Exception as e:
            response = {
                'status': 'error',
                'message': str(e)
            }

        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(response).encode('utf-8'))