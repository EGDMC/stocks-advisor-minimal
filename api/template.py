# Previous template content remains the same until the SMC Analysis section
# Update the SMC page content with:

"""
            <div id="smc-page" class="page">
                <div class="dashboard-header">
                    <h1 class="page-title">Smart Money Analysis</h1>
                    <p class="page-description">Institutional order flow and market structure analysis</p>
                </div>
                
                <div class="grid">
                    <!-- Order Blocks -->
                    <div class="card">
                        <h2>Order Blocks</h2>
                        <div class="chart-container">
                            <canvas id="orderBlocksChart"></canvas>
                        </div>
                        <div id="orderBlocksList"></div>
                    </div>
                    
                    <!-- Volume Profile -->
                    <div class="card">
                        <h2>Volume Profile</h2>
                        <div class="chart-container">
                            <canvas id="volumeProfileChart"></canvas>
                        </div>
                        <div id="volumeProfileMetrics"></div>
                    </div>
                </div>
                
                <div class="grid">
                    <!-- Liquidity Pools -->
                    <div class="card">
                        <h2>Liquidity Pools</h2>
                        <div id="liquidityPoolsList"></div>
                    </div>
                    
                    <!-- Institutional Patterns -->
                    <div class="card">
                        <h2>Institutional Patterns</h2>
                        <div id="institutionalPatterns"></div>
                    </div>
                    
                    <!-- Market Context -->
                    <div class="card">
                        <h2>Market Context</h2>
                        <div id="marketContext"></div>
                    </div>
                </div>
            </div>
"""

# Add the following JavaScript functions to format SMC analysis:

"""
            window.formatSMCAnalysis = function(smc) {
                if (!smc) return '';
                
                // Format Order Blocks
                let orderBlocksHtml = '<div class="grid">';
                if (smc.order_blocks?.length > 0) {
                    smc.order_blocks.forEach(block => {
                        const blockClass = block.type === 'bullish' ? 'signal-bullish' : 'signal-bearish';
                        orderBlocksHtml += `
                            <div class="indicator-card">
                                <span class="${blockClass}">
                                    ${block.type.toUpperCase()} ORDER BLOCK
                                </span>
                                <br>
                                High: $${block.price_high}
                                <br>
                                Low: $${block.price_low}
                                <br>
                                Strength: ${block.strength.toFixed(2)}x
                            </div>
                        `;
                    });
                }
                orderBlocksHtml += '</div>';
                document.getElementById('orderBlocksList').innerHTML = orderBlocksHtml;
                
                // Format Volume Profile
                if (smc.volume_profile) {
                    const vp = smc.volume_profile;
                    document.getElementById('volumeProfileMetrics').innerHTML = `
                        <div class="indicator-card">
                            <h3>Key Levels</h3>
                            <div>Point of Control: $${vp.poc_price.toFixed(2)}</div>
                            <div>Value Area High: $${vp.value_area_high.toFixed(2)}</div>
                            <div>Value Area Low: $${vp.value_area_low.toFixed(2)}</div>
                        </div>
                    `;
                }
                
                // Format Liquidity Pools
                let poolsHtml = '<div class="grid">';
                if (smc.liquidity_pools?.length > 0) {
                    smc.liquidity_pools.forEach(pool => {
                        const poolClass = pool.type === 'support' ? 'signal-bullish' : 'signal-bearish';
                        poolsHtml += `
                            <div class="indicator-card">
                                <span class="${poolClass}">
                                    ${pool.type.toUpperCase()} LIQUIDITY
                                </span>
                                <br>
                                Price: $${pool.price}
                                <br>
                                Strength: ${pool.strength}x
                            </div>
                        `;
                    });
                }
                poolsHtml += '</div>';
                document.getElementById('liquidityPoolsList').innerHTML = poolsHtml;
                
                // Format Institutional Patterns
                let patternsHtml = '<div class="grid">';
                if (smc.institutional_patterns?.length > 0) {
                    smc.institutional_patterns.forEach(pattern => {
                        const patternClass = pattern.direction === 'bullish' ? 'signal-bullish' : 'signal-bearish';
                        patternsHtml += `
                            <div class="indicator-card">
                                <span class="${patternClass}">
                                    ${pattern.type.toUpperCase()}
                                </span>
                                <br>
                                Price: $${pattern.price}
                                <br>
                                Strength: ${pattern.strength.toFixed(2)}x
                            </div>
                        `;
                    });
                }
                patternsHtml += '</div>';
                document.getElementById('institutionalPatterns').innerHTML = patternsHtml;
                
                // Format Market Context
                if (smc.market_context) {
                    const ctx = smc.market_context;
                    let contextClass = ctx.in_value_area ? 'signal-neutral' :
                                     ctx.above_poc ? 'signal-bullish' : 'signal-bearish';
                    
                    document.getElementById('marketContext').innerHTML = `
                        <div class="indicator-card">
                            <div class="${contextClass}">
                                ${ctx.above_poc ? 'Above' : 'Below'} Point of Control
                            </div>
                            <div>${ctx.in_value_area ? 'Inside' : 'Outside'} Value Area</div>
                            <div>${ctx.near_liquidity ? 'Near' : 'Away from'} Liquidity Level</div>
                            ${ctx.active_patterns.length > 0 ? 
                                `<div>Active Patterns: ${ctx.active_patterns.length}</div>` : 
                                ''}
                        </div>
                    `;
                }
                
                // Create or update charts
                if (window.charts.orderBlocks) {
                    window.charts.orderBlocks.destroy();
                }
                if (window.charts.volumeProfile) {
                    window.charts.volumeProfile.destroy();
                }
                
                // Create Order Blocks chart
                const orderBlocksCtx = document.getElementById('orderBlocksChart').getContext('2d');
                window.charts.orderBlocks = new Chart(orderBlocksCtx, {
                    type: 'scatter',
                    data: {
                        datasets: [{
                            label: 'Bullish Blocks',
                            data: smc.order_blocks
                                .filter(b => b.type === 'bullish')
                                .map(b => ({
                                    x: b.index,
                                    y: b.price_low
                                })),
                            backgroundColor: 'rgba(16, 185, 129, 0.5)',
                            borderColor: '#10b981'
                        },
                        {
                            label: 'Bearish Blocks',
                            data: smc.order_blocks
                                .filter(b => b.type === 'bearish')
                                .map(b => ({
                                    x: b.index,
                                    y: b.price_high
                                })),
                            backgroundColor: 'rgba(239, 68, 68, 0.5)',
                            borderColor: '#ef4444'
                        }]
                    },
                    options: {
                        responsive: true,
                        maintainAspectRatio: false,
                        plugins: {
                            title: {
                                display: true,
                                text: 'Order Block Distribution'
                            }
                        },
                        scales: {
                            y: {
                                title: {
                                    display: true,
                                    text: 'Price'
                                }
                            },
                            x: {
                                title: {
                                    display: true,
                                    text: 'Time'
                                }
                            }
                        }
                    }
                });
                
                // Create Volume Profile chart
                if (smc.volume_profile) {
                    const vpCtx = document.getElementById('volumeProfileChart').getContext('2d');
                    window.charts.volumeProfile = new Chart(vpCtx, {
                        type: 'bar',
                        data: {
                            labels: smc.volume_profile.price_levels.map(p => p.toFixed(2)),
                            datasets: [{
                                label: 'Volume',
                                data: smc.volume_profile.volumes,
                                backgroundColor: 'rgba(37, 99, 235, 0.5)',
                                borderColor: '#2563eb'
                            }]
                        },
                        options: {
                            indexAxis: 'y',
                            responsive: true,
                            maintainAspectRatio: false,
                            plugins: {
                                title: {
                                    display: true,
                                    text: 'Volume Profile'
                                }
                            }
                        }
                    });
                }
            };
"""