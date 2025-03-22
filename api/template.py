HTML_TEMPLATE = """<!DOCTYPE html>
<html>
<!-- Previous head and style sections remain the same -->

<script>
    let charts = {};
    
    function formatNumber(num) {
        return new Intl.NumberFormat().format(num);
    }
    
    function formatTechnicalSignals(signals) {
        if (!signals) return '';
        
        let html = '<div class="metrics-grid">';
        
        // RSI Signal
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
        
        // MACD Signal
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
        
        // Bollinger Bands Signal
        if (signals.bollinger) {
            const width = signals.bollinger.width;
            const volatilityClass = width > 2 ? 'signal-bearish' : 
                                  width < 1 ? 'signal-bullish' : 
                                  'signal-neutral';
            html += `
                <div class="indicator-card">
                    <h3>Bollinger Bands</h3>
                    <div>
                        Width: <span class="${volatilityClass}">${width.toFixed(2)}</span>
                        <br>
                        Position: ${signals.bollinger.position}
                    </div>
                </div>
            `;
        }
        
        html += '</div>';
        return html;
    }
    
    // Previous formatting functions remain the same
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
                
                <div class="indicator-card">
                    <h3>Price Range</h3>
                    <div>High: $${pa.highest_price}</div>
                    <div>Low: $${pa.lowest_price}</div>
                    <div>Avg: $${pa.average_price}</div>
                </div>
                
                <div class="indicator-card">
                    <h3>Volatility</h3>
                    <div>${pa.volatility}</div>
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
                    <div>
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
        
        // Previous SMC formatting remains the same
        
        html += '</div>';
        return html;
    }
    
    function createCharts(configs) {
        // Previous chart creation code remains the same
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
    
    // Form submission handler
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
                document.getElementById('technical-analysis').style.display = 'block';
                
                // Create charts using configurations
                createCharts(result.analysis.chart_configs);
                
                // Update technical signals
                document.getElementById('technicalSignals').innerHTML = 
                    formatTechnicalSignals(result.analysis.technical_signals);
                
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
</script>
</body>
</html>"""