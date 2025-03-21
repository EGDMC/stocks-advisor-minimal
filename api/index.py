from http.server import BaseHTTPRequestHandler
import json
import cgi
import io
import pandas as pd
import numpy as np

def analyze_stock_data(csv_content):
    # Read CSV from string
    df = pd.read_csv(io.StringIO(csv_content))
    
    # Basic analysis
    analysis = {
        'statistics': {
            'total_rows': len(df),
            'columns': list(df.columns)
        },
        'summary': {}
    }
    
    # Calculate basic statistics for numeric columns
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    for col in numeric_cols:
        analysis['summary'][col] = {
            'mean': float(df[col].mean()),
            'min': float(df[col].min()),
            'max': float(df[col].max())
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
                #result {
                    margin-top: 20px;
                    padding: 15px;
                    border-radius: 4px;
                    background-color: #e9ecef;
                    white-space: pre-wrap;
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
                    <!-- Results will be displayed here -->
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
                        
                        const resultDiv = document.getElementById('result');
                        resultDiv.style.display = 'block';
                        resultDiv.innerHTML = '<h2>Analysis Results</h2>' + 
                                           '<pre>' + JSON.stringify(result, null, 2) + '</pre>';
                    } catch (error) {
                        console.error('Error:', error);
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
        content_type = self.headers.get('Content-Type', '')
        try:
            if 'multipart/form-data' in content_type:
                form = cgi.FieldStorage(
                    fp=self.rfile,
                    headers=self.headers,
                    environ={'REQUEST_METHOD': 'POST'}
                )
                
                if 'file' in form:
                    fileitem = form['file']
                    if fileitem.filename:
                        file_content = fileitem.file.read().decode('utf-8')
                        
                        # Analyze the data
                        analysis_result = analyze_stock_data(file_content)
                        
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
            else:
                response = {
                    'status': 'error',
                    'message': 'Invalid content type'
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