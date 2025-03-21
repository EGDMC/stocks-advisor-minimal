from http.server import BaseHTTPRequestHandler
import json

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        data = {
            "title": "Stock Market Analysis",
            "sections": [
                {
                    "type": "header",
                    "content": "Stock Market Analysis"
                },
                {
                    "type": "text",
                    "content": "Welcome to the Stock Market Analysis Tool"
                },
                {
                    "type": "card",
                    "title": "Data Upload",
                    "content": "Use this section to upload your stock data"
                }
            ]
        }
        
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        
        response_data = json.dumps(data)
        self.wfile.write(response_data.encode('utf-8'))