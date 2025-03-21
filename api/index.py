from http.server import BaseHTTPRequestHandler

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        html_content = """
        <html>
            <head>
                <title>Stock Advisor</title>
            </head>
            <body>
                <h1>Stock Advisor App</h1>
                <p>This is a placeholder page. The full application functionality will be added soon.</p>
                <div style="padding: 1rem; background-color: #e3f2fd; border-radius: 4px;">
                    The application is being configured. Please check back later.
                </div>
            </body>
        </html>
        """
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(html_content.encode('utf-8'))