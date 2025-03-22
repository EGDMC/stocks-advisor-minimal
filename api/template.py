HTML_TEMPLATE = """<!DOCTYPE html>
<html>
<!-- Previous head section remains the same until the card section -->

        <div id="result" style="display: none;">
            <div class="card">
                <h2>Price Chart</h2>
                <div class="chart-container">
                    <canvas id="priceChart"></canvas>
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
            
            <!-- Previous sections remain the same -->
        </div>
    </div>
    
    <script>
        // Previous functions remain the same until formatPatterns

        function formatPatterns(patterns) {
            if (!patterns) return '';
            
            // Format candlestick patterns
            let candlestickHtml = '';
            if (patterns.candlestick_patterns && patterns.candlestick_patterns.length > 0) {
                patterns.candlestick_patterns.slice(-3).forEach(pattern => {
                    const patternClass = pattern.significance === 'bullish' ? 'signal-bullish' :
                                       pattern.significance === 'bearish' ? 'signal-bearish' :
                                       'signal-neutral';
                    candlestickHtml += `
                        <div>
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
                        <div>
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
                        <div>
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
        
        // Update form submission handler
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
                    
                    // Update SMC analysis if available
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

        // Previous script sections remain the same
    </script>
</body>
</html>"""