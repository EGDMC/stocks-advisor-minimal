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
        .metric-card {
            background: #fff;
            padding: 15px;
            border-radius: 8px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        }
        .smc-card {
            background: #2c3e50;
            color: white;
            padding: 15px;
            border-radius: 8px;
            margin-top: 20px;
        }
        .metric-value {
            font-size: 1.5em;
            font-weight: bold;
            color: #2c3e50;
        }
        .metric-label {
            color: #7f8c8d;
            font-size: 0.9em;
        }
        .positive { color: #27ae60; }
        .negative { color: #c0392b; }
        .bullish { color: #27ae60; }
        .bearish { color: #c0392b; }
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
        .smc-levels {
            margin-top: 20px;
            padding: 15px;
            background: #f8f9fa;
            border-radius: 8px;
        }
        .level-item {
            display: flex;
            justify-content: space-between;
            padding: 5px 0;
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
                <h2>Price Chart</h2>
                <div class="chart-container">
                    <canvas id="priceChart"></canvas>
                </div>
            </div>
            
            <div id="smc-analysis" class="card">
                <h2>SMC Analysis</h2>
                <div id="smcContent" class="smc-card"></div>
            </div>
            
            <div class="card">
                <h2>Analysis Results</h2>
                <div id="resultContent"></div>
            </div>
        </div>
    </div>
    
    <script>
        let priceChart = null;
        
        function formatNumber(num) {
            return new Intl.NumberFormat().format(num);
        }
        
        function createChart(data) {
            const ctx = document.getElementById('priceChart').getContext('2d');
            
            if (priceChart) {
                priceChart.destroy();
            }
            
            const annotations = {};
            
            // Add SMC markers if available
            if (data.smc_markers) {
                data.smc_markers.imbalances.forEach((imb, i) => {
                    annotations[`imbalance${i}`] = {
                        type: 'point',
                        xValue: data.labels.length - 1 - imb.index,
                        yValue: imb.price,
                        backgroundColor: imb.type === 'bullish' ? '#27ae60' : '#c0392b',
                        radius: 6 * imb.strength,
                        borderColor: 'white',
                        borderWidth: 2
                    };
                });
                
                data.smc_markers.liquidity_levels.forEach((level, i) => {
                    annotations[`liquidity${i}`] = {
                        type: 'line',
                        yMin: level.price,
                        yMax: level.price,
                        borderColor: level.type === 'support' ? '#2ecc71' : '#e74c3c',
                        borderWidth: 2 * level.strength,
                        borderDash: [5, 5]
                    };
                });
                
                data.smc_markers.fvgs.forEach((fvg, i) => {
                    annotations[`fvg${i}`] = {
                        type: 'box',
                        xMin: data.labels.length - 1 - fvg.index - 0.5,
                        xMax: data.labels.length - 1 - fvg.index + 0.5,
                        yMin: fvg.price - fvg.gap_size,
                        yMax: fvg.price + fvg.gap_size,
                        backgroundColor: fvg.type === 'bullish' ? 'rgba(39, 174, 96, 0.2)' : 'rgba(192, 57, 43, 0.2)',
                        borderColor: fvg.type === 'bullish' ? '#27ae60' : '#c0392b',
                        borderWidth: 1
                    };
                });
            }
            
            priceChart = new Chart(ctx, {
                type: 'line',
                data: {
                    labels: data.labels.reverse(),
                    datasets: [
                        {
                            label: 'Price',
                            data: data.prices.reverse(),
                            borderColor: '#2c3e50',
                            tension: 0.1
                        },
                        {
                            label: '20-day MA',
                            data: Array(data.labels.length - data.ma20.length)
                                .fill(null)
                                .concat(data.ma20.reverse()),
                            borderColor: '#e74c3c',
                            borderWidth: 1,
                            pointRadius: 0
                        },
                        {
                            label: '50-day MA',
                            data: Array(data.labels.length - data.ma50.length)
                                .fill(null)
                                .concat(data.ma50.reverse()),
                            borderColor: '#3498db',
                            borderWidth: 1,
                            pointRadius: 0
                        }
                    ]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: {
                            position: 'top'
                        },
                        annotation: {
                            annotations: annotations
                        }
                    },
                    scales: {
                        y: {
                            beginAtZero: false
                        }
                    }
                }
            });
        }
        
        function formatSMCAnalysis(smc) {
            if (!smc) return '';
            
            let html = '';
            
            if (smc.trend) {
                html += `
                    <div class="metric-card">
                        <div class="metric-value ${smc.trend.direction}">
                            ${smc.trend.direction.toUpperCase()}
                        </div>
                        <div class="metric-label">
                            Market Structure (Strength: ${smc.trend.strength})
                        </div>
                    </div>
                `;
            }
            
            if (smc.imbalances.length > 0) {
                html += '<h3>Recent Imbalances</h3>';
                smc.imbalances.slice(-3).forEach(imb => {
                    html += `
                        <div class="level-item">
                            <span>${imb.type.toUpperCase()}</span>
                            <span class="${imb.type}">
                                $${imb.price} (${imb.strength}x)
                            </span>
                        </div>
                    `;
                });
            }
            
            if (smc.liquidity_levels.length > 0) {
                html += '<h3>Key Liquidity Levels</h3>';
                smc.liquidity_levels.forEach(level => {
                    html += `
                        <div class="level-item">
                            <span>${level.type.toUpperCase()}</span>
                            <span class="${level.type}">
                                $${level.price} (${level.strength}x)
                            </span>
                        </div>
                    `;
                });
            }
            
            return html;
        }
        
        function formatMetrics(analysis) {
            let html = '<div class="metrics-grid">';
            
            if (analysis.price_analysis) {
                const pa = analysis.price_analysis;
                const changeClass = pa.total_change >= 0 ? 'positive' : 'negative';
                const changeSymbol = pa.total_change >= 0 ? '+' : '';
                
                html += `
                    <div class="metric-card">
                        <div class="metric-value">$${pa.latest_price}</div>
                        <div class="metric-label">Latest Price</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-value ${changeClass}">
                            ${changeSymbol}${pa.total_change_percentage}%
                        </div>
                        <div class="metric-label">Total Change</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-value">$${pa.average_price}</div>
                        <div class="metric-label">Average Price</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-value">${pa.volatility}</div>
                        <div class="metric-label">Volatility</div>
                    </div>
                `;
            }
            
            if (analysis.volume_analysis) {
                const va = analysis.volume_analysis;
                html += `
                    <div class="metric-card">
                        <div class="metric-value">${formatNumber(va.latest_volume)}</div>
                        <div class="metric-label">Latest Volume</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-value">${formatNumber(va.average_volume)}</div>
                        <div class="metric-label">Average Volume</div>
                    </div>
                `;
            }
            
            html += '</div>';
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
                    document.getElementById('resultContent').innerHTML = formatMetrics(result.analysis);
                    
                    if (result.analysis.smc_analysis) {
                        document.getElementById('smc-analysis').style.display = 'block';
                        document.getElementById('smcContent').innerHTML = 
                            formatSMCAnalysis(result.analysis.smc_analysis);
                    }
                    
                    createChart(result.analysis.chart_data);
                } else {
                    alert('Error: ' + result.message);
                }
            } catch (error) {
                console.error('Error:', error);
                alert('Error processing file: ' + error.message);
            }
        };
    </script>
</body>
</html>"""