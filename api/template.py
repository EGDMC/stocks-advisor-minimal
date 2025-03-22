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
        .pattern-card {
            margin-bottom: 10px;
            padding: 10px;
            border-radius: 4px;
            background: rgba(255, 255, 255, 0.1);
        }
        h1, h2, h3 {
            color: #2c3e50;
            margin-bottom: 20px;
        }
        h1 { text-align: center; }
        .signal-bullish { color: #2ecc71; font-weight: bold; }
        .signal-bearish { color: #e74c3c; font-weight: bold; }
        .signal-neutral { color: #f1c40f; font-weight: bold; }
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
                <h2>Price Chart</h2>
                <div class="chart-container">
                    <canvas id="priceChart"></canvas>
                </div>
            </div>
            
            <div class="card">
                <h2>Trend Prediction</h2>
                <div class="metrics-grid">
                    <div class="indicator-card">
                        <h3>Current Trend</h3>
                        <div id="trendMetrics"></div>
                    </div>
                    <div class="indicator-card">
                        <h3>Potential Breakouts</h3>
                        <div id="breakoutPredictions"></div>
                    </div>
                    <div class="indicator-card">
                        <h3>Price Targets</h3>
                        <div id="priceTargets"></div>
                    </div>
                </div>
            </div>
            
            <div class="card">
                <h2>Pattern Recognition</h2>
                <div class="metrics-grid" id="patternAnalysis">
                    <div class="indicator-card">
                        <h3>Candlestick Patterns</h3>
                        <div id="candlestickPatterns"></div>
                    </div>
                    <div class="indicator-card">
                        <h3>Chart Patterns</h3>
                        <div id="chartPatterns"></div>
                    </div>
                    <div class="indicator-card">
                        <h3>Price Action</h3>
                        <div id="priceActionPatterns"></div>
                    </div>
                </div>
            </div>
            
            <div class="card">
                <h2>Technical Indicators</h2>
                <div id="technicalSignals"></div>
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
        
        function formatNumber(num) {
            return new Intl.NumberFormat().format(num);
        }
        
        function formatTrendAnalysis(analysis) {
            if (!analysis) return;
            
            // Format trend metrics
            let trendHtml = '';
            const trendClass = analysis.trend.direction === 'bullish' ? 'signal-bullish' :
                             analysis.trend.direction === 'bearish' ? 'signal-bearish' :
                             'signal-neutral';
            
            trendHtml += `
                <div class="pattern-card">
                    <span class="${trendClass}">
                        ${analysis.trend.direction.toUpperCase()}
                    </span>
                    <br>
                    Strength: ${(analysis.trend.strength * 100).toFixed(0)}%
                    <br>
                    Momentum: ${analysis.metrics.momentum}%
                    <br>
                    Volume: ${analysis.metrics.volume_trend}
                </div>
            `;
            document.getElementById('trendMetrics').innerHTML = trendHtml;
            
            // Format breakout predictions
            let breakoutHtml = '';
            if (analysis.breakouts && analysis.breakouts.length > 0) {
                analysis.breakouts.forEach(breakout => {
                    const breakoutClass = breakout.direction === 'up' ? 'signal-bullish' : 'signal-bearish';
                    breakoutHtml += `
                        <div class="pattern-card">
                            <span class="${breakoutClass}">
                                ${breakout.type.toUpperCase()} ${breakout.direction.toUpperCase()}
                            </span>
                            <br>
                            Level: $${breakout.level}
                            <br>
                            Probability: ${(breakout.probability * 100).toFixed(0)}%
                            <br>
                            ${breakout.volume_confirmed ? '✓ Volume Confirmed' : ''}
                        </div>
                    `;
                });
            }
            document.getElementById('breakoutPredictions').innerHTML = 
                breakoutHtml || 'No breakouts detected';
            
            // Format price targets
            let targetsHtml = '';
            if (analysis.targets && analysis.targets.length > 0) {
                analysis.targets.forEach(target => {
                    const confidenceClass = target.confidence > 0.7 ? 'signal-bullish' :
                                         target.confidence > 0.4 ? 'signal-neutral' :
                                         'signal-bearish';
                    targetsHtml += `
                        <div class="pattern-card">
                            <span class="${confidenceClass}">
                                ${target.timeframe.toUpperCase()} (${target.method})
                            </span>
                            <br>
                            Target: $${target.target}
                            <br>
                            Confidence: ${(target.confidence * 100).toFixed(0)}%
                        </div>
                    `;
                });
            }
            document.getElementById('priceTargets').innerHTML = 
                targetsHtml || 'No targets available';
        }
        
        function formatPatterns(patterns) {
            if (!patterns) return;
            
            // Format candlestick patterns
            let candlestickHtml = '';
            if (patterns.candlestick_patterns && patterns.candlestick_patterns.length > 0) {
                patterns.candlestick_patterns.slice(-3).forEach(pattern => {
                    const patternClass = pattern.significance === 'bullish' ? 'signal-bullish' :
                                       pattern.significance === 'bearish' ? 'signal-bearish' :
                                       'signal-neutral';
                    candlestickHtml += `
                        <div class="pattern-card">
                            <span class="${patternClass}">
                                ${pattern.type}
                            </span>
                            <br>
                            Reliability: ${(pattern.reliability * 100).toFixed(0)}%
                        </div>
                    `;
                });
            }
            document.getElementById('candlestickPatterns').innerHTML = 
                candlestickHtml || 'No recent patterns detected';
            
            // Format chart patterns
            let chartHtml = '';
            if (patterns.chart_patterns && patterns.chart_patterns.length > 0) {
                patterns.chart_patterns.slice(-3).forEach(pattern => {
                    const patternClass = pattern.significance === 'bullish' ? 'signal-bullish' : 'signal-bearish';
                    chartHtml += `
                        <div class="pattern-card">
                            <span class="${patternClass}">
                                ${pattern.type}
                            </span>
                            <br>
                            Target: $${pattern.target.toFixed(2)}
                            <br>
                            Reliability: ${(pattern.reliability * 100).toFixed(0)}%
                        </div>
                    `;
                });
            }
            document.getElementById('chartPatterns').innerHTML = 
                chartHtml || 'No patterns detected';
            
            // Format price action patterns
            let priceActionHtml = '';
            if (patterns.price_action_patterns && patterns.price_action_patterns.length > 0) {
                patterns.price_action_patterns.slice(-3).forEach(pattern => {
                    const patternClass = pattern.significance === 'bullish' ? 'signal-bullish' : 'signal-bearish';
                    priceActionHtml += `
                        <div class="pattern-card">
                            <span class="${patternClass}">
                                ${pattern.type}
                            </span>
                            <br>
                            Target: $${pattern.target.toFixed(2)}
                            <br>
                            Reliability: ${(pattern.reliability * 100).toFixed(0)}%
                        </div>
                    `;
                });
            }
            document.getElementById('priceActionPatterns').innerHTML = 
                priceActionHtml || 'No patterns detected';
        }
        
        function formatTechnicalSignals(signals) {
            if (!signals) return '';
            
            let html = '<div class="metrics-grid">';
            
            if (signals.rsi) {
                const rsiClass = signals.rsi.condition === 'oversold' ? 'signal-bullish' :
                               signals.rsi.condition === 'overbought' ? 'signal-bearish' :
                               'signal-neutral';
                html += `
                    <div class="indicator-card">
                        <h3>RSI</h3>
                        <div class="${rsiClass}">
                            ${signals.rsi.value.toFixed(2)} (${signals.rsi.condition})
                        </div>
                    </div>
                `;
            }
            
            if (signals.macd) {
                const macdClass = signals.macd.trend === 'bullish' ? 'signal-bullish' : 'signal-bearish';
                html += `
                    <div class="indicator-card">
                        <h3>MACD</h3>
                        <div class="${macdClass}">
                            ${signals.macd.trend.toUpperCase()}
                            <br>
                            Strength: ${signals.macd.strength}
                        </div>
                    </div>
                `;
            }
            
            if (signals.bollinger) {
                html += `
                    <div class="indicator-card">
                        <h3>Bollinger Bands</h3>
                        <div>
                            Width: ${signals.bollinger.width.toFixed(2)}
                            <br>
                            Position: ${signals.bollinger.position}
                        </div>
                    </div>
                `;
            }
            
            html += '</div>';
            return html;
        }
        
        function formatSMCAnalysis(smc) {
            if (!smc) return '';
            
            let html = '<div class="metrics-grid">';
            
            // Format imbalances
            if (smc.imbalances && smc.imbalances.length > 0) {
                html += '<div class="indicator-card">';
                html += '<h3>Recent Imbalances</h3>';
                smc.imbalances.slice(-3).forEach(imb => {
                    const imbalanceClass = imb.type === 'bullish' ? 'signal-bullish' : 'signal-bearish';
                    html += `
                        <div class="pattern-card">
                            <span class="${imbalanceClass}">
                                ${imb.type.toUpperCase()} (${imb.strength}x)
                            </span>
                            <br>
                            Price: $${imb.price}
                        </div>
                    `;
                });
                html += '</div>';
            }
            
            // Format liquidity levels
            if (smc.liquidity_levels && smc.liquidity_levels.length > 0) {
                html += '<div class="indicator-card">';
                html += '<h3>Liquidity Levels</h3>';
                smc.liquidity_levels.forEach(level => {
                    const levelClass = level.type === 'support' ? 'signal-bullish' : 'signal-bearish';
                    html += `
                        <div class="pattern-card">
                            <span class="${levelClass}">
                                ${level.type.toUpperCase()} (${level.strength}x)
                            </span>
                            <br>
                            Price: $${level.price}
                        </div>
                    `;
                });
                html += '</div>';
            }
            
            // Format Fair Value Gaps (FVGs)
            if (smc.fvgs && smc.fvgs.length > 0) {
                html += '<div class="indicator-card">';
                html += '<h3>Fair Value Gaps</h3>';
                smc.fvgs.forEach(fvg => {
                    const fvgClass = fvg.type === 'bullish' ? 'signal-bullish' : 'signal-bearish';
                    html += `
                        <div class="pattern-card">
                            <span class="${fvgClass}">
                                ${fvg.type.toUpperCase()}
                            </span>
                            <br>
                            Price: $${fvg.price} (Gap: ${fvg.gap_size})
                        </div>
                    `;
                });
                html += '</div>';
            }
            
            html += '</div>';
            return html;
        }
        
        function formatMetrics(analysis) {
            let html = '<div class="metrics-grid">';
            
            if (analysis.price_analysis) {
                const pa = analysis.price_analysis;
                const changeClass = pa.total_change >= 0 ? 'signal-bullish' : 'signal-bearish';
                const changeSymbol = pa.total_change >= 0 ? '+' : '';
                
                html += `
                    <div class="indicator-card">
                        <h3>Latest Price</h3>
                        <div class="metric-value">$${pa.latest_price}</div>
                        <div class="${changeClass}">
                            ${changeSymbol}${pa.total_change_percentage.toFixed(2)}%
                        </div>
                    </div>
                `;
            }
            
            if (analysis.volume_analysis) {
                const va = analysis.volume_analysis;
                html += `
                    <div class="indicator-card">
                        <h3>Volume</h3>
                        <div>Current: ${formatNumber(va.latest_volume)}</div>
                        <div>Average: ${formatNumber(va.average_volume)}</div>
                    </div>
                `;
            }
            
            html += '</div>';
            return html;
        }
        
        function createCharts(configs) {
            Object.values(charts).forEach(chart => chart?.destroy());
            
            charts.price = new Chart(
                document.getElementById('priceChart').getContext('2d'),
                configs.main
            );
            
            charts.rsi = new Chart(
                document.getElementById('rsiChart').getContext('2d'),
                configs.rsi
            );
            
            charts.macd = new Chart(
                document.getElementById('macdChart').getContext('2d'),
                configs.macd
            );
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
                    
                    // Update pattern analysis
                    formatPatterns(result.analysis.patterns);
                    
                    // Update trend analysis
                    formatTrendAnalysis(result.analysis.trend_analysis);
                    
                    // Update SMC analysis
                    const smcAnalysis = document.getElementById('smc-analysis');
                    if (result.analysis.smc_analysis) {
                        smcAnalysis.style.display = 'block';
                        document.getElementById('smcContent').innerHTML = 
                            formatSMCAnalysis(result.analysis.smc_analysis);
                    } else {
                        smcAnalysis.style.display = 'none';
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
    </script>
</body>
</html>"""