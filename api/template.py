HTML_TEMPLATE = """<!DOCTYPE html>
<html>
<head>
    <title>Stock Market Analysis</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/chartjs-plugin-annotation"></script>
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
            margin-bottom: 20px;
        }
        .sub-chart {
            height: 200px;
        }
        h1, h2, h3 {
            color: #2c3e50;
            margin-bottom: 20px;
        }
        h1 { text-align: center; }
        .metrics-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-top: 20px;
        }
        .indicator-card {
            background: #34495e;
            color: white;
            padding: 15px;
            border-radius: 8px;
            margin-top: 10px;
        }
        .signal-bullish { color: #2ecc71; }
        .signal-bearish { color: #e74c3c; }
        .signal-neutral { color: #f1c40f; }
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
                <h2>Price Analysis</h2>
                <div class="chart-container">
                    <canvas id="priceChart"></canvas>
                </div>
            </div>
            
            <div class="card">
                <h2>Technical Indicators</h2>
                <div class="metrics-grid" id="technicalSignals"></div>
                <div class="chart-container sub-chart">
                    <canvas id="rsiChart"></canvas>
                </div>
                <div class="chart-container sub-chart">
                    <canvas id="macdChart"></canvas>
                </div>
            </div>
            
            <div id="smc-analysis" class="card">
                <h2>SMC Analysis</h2>
                <div id="smcContent"></div>
            </div>
            
            <div class="card">
                <h2>Price Statistics</h2>
                <div id="resultContent"></div>
            </div>
        </div>
    </div>
    
    <script>
        let charts = {};
        
        function createCharts(configs) {
            // Destroy existing charts
            Object.values(charts).forEach(chart => chart?.destroy());
            
            // Create main price chart
            charts.price = new Chart(
                document.getElementById('priceChart').getContext('2d'),
                configs.main
            );
            
            // Create RSI chart
            charts.rsi = new Chart(
                document.getElementById('rsiChart').getContext('2d'),
                configs.rsi
            );
            
            // Create MACD chart
            charts.macd = new Chart(
                document.getElementById('macdChart').getContext('2d'),
                configs.macd
            );
        }
        
        function formatTechnicalSignals(signals) {
            if (!signals) return '';
            
            let html = '';
            
            if (signals.rsi) {
                const signalClass = signals.rsi.condition === 'oversold' ? 'signal-bullish' :
                                  signals.rsi.condition === 'overbought' ? 'signal-bearish' :
                                  'signal-neutral';
                html += `
                    <div class="indicator-card">
                        <h3>RSI</h3>
                        <div class="${signalClass}">
                            ${signals.rsi.value} (${signals.rsi.condition})
                        </div>
                    </div>
                `;
            }
            
            if (signals.macd) {
                const signalClass = signals.macd.trend === 'bullish' ? 'signal-bullish' : 'signal-bearish';
                html += `
                    <div class="indicator-card">
                        <h3>MACD</h3>
                        <div class="${signalClass}">
                            ${signals.macd.trend.toUpperCase()}
                            <br>Strength: ${signals.macd.strength}
                        </div>
                    </div>
                `;
            }
            
            if (signals.bollinger) {
                html += `
                    <div class="indicator-card">
                        <h3>Bollinger Bands</h3>
                        <div>
                            Width: ${signals.bollinger.width}<br>
                            Position: ${signals.bollinger.position}
                        </div>
                    </div>
                `;
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
                
                if (result.status === 'success') {
                    document.getElementById('result').style.display = 'block';
                    
                    // Create charts using configurations
                    createCharts(result.analysis.chart_configs);
                    
                    // Update technical signals
                    document.getElementById('technicalSignals').innerHTML = 
                        formatTechnicalSignals(result.analysis.technical_signals);
                    
                    // Update SMC analysis if available
                    if (result.analysis.smc_analysis) {
                        document.getElementById('smc-analysis').style.display = 'block';
                        document.getElementById('smcContent').innerHTML = 
                            formatSMCAnalysis(result.analysis.smc_analysis);
                    }
                    
                    // Update price statistics
                    document.getElementById('resultContent').innerHTML = 
                        formatMetrics(result.analysis);
                } else {
                    alert('Error: ' + result.message);
                }
            } catch (error) {
                console.error('Error:', error);
                alert('Error processing file: ' + error.message);
            }
        };
        
        // Previous helper functions (formatMetrics, formatSMCAnalysis) remain unchanged
    </script>
</body>
</html>"""