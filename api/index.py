from http.server import BaseHTTPRequestHandler
import json
import cgi
import csv
import io

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
                
                <div id="result" class="card" style="display: none; margin-top: 20px;">
                    <h2>Analysis Results</h2>
                    <pre id="resultContent" style="white-space: pre-wrap;"></pre>
                </div>
            </div>
            
            <script>
                document.querySelector('form').onsubmit = async (e) => {
                    e.preventDefault();
                    const formData = new FormData(e.target);
                    
                    try {
                        const response = await fetch('/api', {
                            method: 'POST',
                            body: formData
                        });
                        const result = await response.json();
                        
                        document.getElementById('result').style.display = 'block';
                        document.getElementById('resultContent').textContent = 
                            JSON.stringify(result, null, 2);
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
                    # Read CSV content
                    file_content = fileitem.file.read().decode('utf-8')
                    csv_reader = csv.reader(io.StringIO(file_content))
                    
                    # Get headers and first few rows
                    headers = next(csv_reader)
                    data_preview = []
                    for i, row in enumerate(csv_reader):
                        if i < 5:  # Get first 5 rows
                            data_preview.append(row)
                        else:
                            break
                    
                    response = {
                        'status': 'success',
                        'filename': fileitem.filename,
                        'headers': headers,
                        'preview': data_preview,
                        'total_columns': len(headers)
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