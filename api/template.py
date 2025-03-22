# Previous template content remains the same until the JavaScript section
# Add these functions before the DOMContentLoaded event listener

HTML_TEMPLATE = """<!-- Previous HTML content remains the same -->

    <script>
        // Utility functions
        function formatNumber(num) {
            return new Intl.NumberFormat().format(num);
        }

        // Format technical signals
        function formatTechnicalSignals(signals) {
            if (!signals) return '';
            
            let html = '<div class="grid">';
            
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
            
            html += '</div>';
            return html;
        }

        // Format patterns
        function formatPatterns(patterns) {
            if (!patterns) return '';
            
            let html = '<div class="grid">';
            
            if (patterns.candlestick_patterns?.length > 0) {
                html += '<div class="indicator-card"><h3>Candlestick Patterns</h3>';
                patterns.candlestick_patterns.forEach(pattern => {
                    const patternClass = pattern.significance === 'bullish' ? 'signal-bullish' :
                                       pattern.significance === 'bearish' ? 'signal-bearish' :
                                       'signal-neutral';
                    html += `
                        <div>
                            <span class="${patternClass}">${pattern.type}</span>
                            <br>
                            Reliability: ${(pattern.reliability * 100).toFixed(0)}%
                        </div>
                    `;
                });
                html += '</div>';
            }
            
            if (patterns.chart_patterns?.length > 0) {
                html += '<div class="indicator-card"><h3>Chart Patterns</h3>';
                patterns.chart_patterns.forEach(pattern => {
                    const patternClass = pattern.significance === 'bullish' ? 'signal-bullish' : 'signal-bearish';
                    html += `
                        <div>
                            <span class="${patternClass}">${pattern.type}</span>
                            <br>
                            Target: $${pattern.target.toFixed(2)}
                        </div>
                    `;
                });
                html += '</div>';
            }
            
            html += '</div>';
            return html;
        }

        // Format trend analysis
        function formatTrendAnalysis(analysis) {
            if (!analysis) return '';
            
            const trendClass = analysis.trend.direction === 'bullish' ? 'signal-bullish' :
                             analysis.trend.direction === 'bearish' ? 'signal-bearish' :
                             'signal-neutral';
            
            let html = `
                <div class="indicator-card">
                    <h3>Current Trend</h3>
                    <div class="${trendClass}">
                        ${analysis.trend.direction.toUpperCase()}
                        <br>
                        Strength: ${(analysis.trend.strength * 100).toFixed(0)}%
                        <br>
                        Momentum: ${analysis.metrics.momentum}%
                    </div>
                </div>
            `;
            
            if (analysis.breakouts?.length > 0) {
                html += '<div class="indicator-card"><h3>Potential Breakouts</h3>';
                analysis.breakouts.forEach(breakout => {
                    const breakoutClass = breakout.direction === 'up' ? 'signal-bullish' : 'signal-bearish';
                    html += `
                        <div>
                            <span class="${breakoutClass}">
                                ${breakout.type.toUpperCase()} ${breakout.direction.toUpperCase()}
                            </span>
                            <br>
                            Level: $${breakout.level}
                            <br>
                            Probability: ${(breakout.probability * 100).toFixed(0)}%
                        </div>
                    `;
                });
                html += '</div>';
            }
            
            return html;
        }

        // Format SMC analysis
        function formatSMCAnalysis(smc) {
            if (!smc) return '';
            
            let html = '<div class="grid">';
            
            if (smc.imbalances?.length > 0) {
                html += '<div class="indicator-card"><h3>Recent Imbalances</h3>';
                smc.imbalances.forEach(imb => {
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
            
            if (smc.liquidity_levels?.length > 0) {
                html += '<div class="indicator-card"><h3>Liquidity Levels</h3>';
                smc.liquidity_levels.forEach(level => {
                    const levelClass = level.type === 'support' ? 'signal-bullish' : 'signal-bearish';
                    html += `
                        <div>
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
            
            html += '</div>';
            return html;
        }

        // Format price statistics
        function formatPriceStats(stats) {
            if (!stats) return '';
            
            const changeClass = stats.total_change >= 0 ? 'signal-bullish' : 'signal-bearish';
            const changeSymbol = stats.total_change >= 0 ? '+' : '';
            
            return `
                <div class="grid">
                    <div class="indicator-card">
                        <h3>Current Price</h3>
                        <div>$${stats.latest_price}</div>
                        <div class="${changeClass}">
                            ${changeSymbol}${stats.total_change_percentage.toFixed(2)}%
                        </div>
                    </div>
                    <div class="indicator-card">
                        <h3>Price Range</h3>
                        <div>High: $${stats.highest_price}</div>
                        <div>Low: $${stats.lowest_price}</div>
                        <div>Average: $${stats.average_price}</div>
                    </div>
                </div>
            `;
        }

        // Previous chart management code and event listeners remain the same
        
    </script>
</body>
</html>"""