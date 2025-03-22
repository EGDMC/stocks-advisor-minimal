HTML_TEMPLATE = """<!DOCTYPE html>
<html>
<head>
    <title>Trading Analysis Dashboard</title>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/chartjs-plugin-annotation"></script>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <link href="https://cdn.jsdelivr.net/npm/remixicon@3.5.0/fonts/remixicon.css" rel="stylesheet">
    <style>
        /* Previous styles remain the same */
    </style>
</head>
<body>
    <!-- Previous HTML structure remains the same -->

    <script>
        // Chart management
        let charts = {};

        // Utility functions
        function formatNumber(num) {
            return new Intl.NumberFormat().format(num);
        }

        function createCharts(configs) {
            // Destroy existing charts
            Object.values(charts).forEach(chart => chart?.destroy());
            
            // Create main price chart
            if (configs.main) {
                const ctx = document.getElementById('priceChart').getContext('2d');
                charts.price = new Chart(ctx, configs.main);
            }
            
            // Create RSI chart
            if (configs.rsi) {
                const ctx = document.getElementById('rsiChart').getContext('2d');
                charts.rsi = new Chart(ctx, configs.rsi);
            }
            
            // Create MACD chart
            if (configs.macd) {
                const ctx = document.getElementById('macdChart').getContext('2d');
                charts.macd = new Chart(ctx, configs.macd);
            }
        }

        // Analysis update functions remain the same
        
        // Initialize when DOM is ready
        document.addEventListener('DOMContentLoaded', () => {
            // Navigation
            document.querySelectorAll('.nav-item').forEach(item => {
                item.addEventListener('click', e => {
                    e.preventDefault();
                    const pageId = item.getAttribute('data-page');
                    
                    document.querySelectorAll('.nav-item').forEach(nav => 
                        nav.classList.remove('active')
                    );
                    item.classList.add('active');
                    
                    document.querySelectorAll('.page').forEach(page => 
                        page.classList.remove('active')
                    );
                    document.getElementById(pageId + '-page').classList.add('active');
                });
            });

            // File upload
            const dropZone = document.getElementById('dropZone');
            const fileInput = document.getElementById('fileInput');
            const selectedFileText = document.getElementById('selectedFile');
            const uploadBtn = document.querySelector('.upload-btn');
            const loading = document.querySelector('.loading');

            // Add click handler for the upload button
            uploadBtn.addEventListener('click', () => fileInput.click());

            // Prevent defaults for drag and drop
            ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
                dropZone.addEventListener(eventName, preventDefaults, false);
                document.body.addEventListener(eventName, preventDefaults, false);
            });

            function preventDefaults(e) {
                e.preventDefault();
                e.stopPropagation();
            }

            // Add drag and drop handlers
            ['dragenter', 'dragover'].forEach(eventName => {
                dropZone.addEventListener(eventName, () => 
                    dropZone.classList.add('highlight')
                );
            });

            ['dragleave', 'drop'].forEach(eventName => {
                dropZone.addEventListener(eventName, () => 
                    dropZone.classList.remove('highlight')
                );
            });

            // Handle file selection
            fileInput.addEventListener('change', e => {
                const file = e.target.files[0];
                if (file) handleUpload(file);
            });

            // Handle file drop
            dropZone.addEventListener('drop', e => {
                const file = e.dataTransfer.files[0];
                if (file) handleUpload(file);
            });

            // File upload handler
            async function handleUpload(file) {
                if (!file) return;
                
                selectedFileText.textContent = file.name;
                loading.classList.add('active');

                const formData = new FormData();
                formData.append('file', file);

                try {
                    const response = await fetch('/api', {
                        method: 'POST',
                        body: formData
                    });

                    if (!response.ok) {
                        throw new Error(`HTTP error! status: ${response.status}`);
                    }

                    const result = await response.json();

                    if (result.status === 'success') {
                        // Update analysis
                        if (result.analysis.chart_configs) {
                            createCharts(result.analysis.chart_configs);
                        }
                        
                        if (result.analysis.technical_signals) {
                            document.getElementById('technicalSignals').innerHTML = 
                                formatTechnicalSignals(result.analysis.technical_signals);
                        }
                        
                        if (result.analysis.patterns) {
                            document.getElementById('patterns-content').innerHTML = 
                                formatPatterns(result.analysis.patterns);
                        }
                        
                        if (result.analysis.trend_analysis) {
                            document.getElementById('trend-content').innerHTML = 
                                formatTrendAnalysis(result.analysis.trend_analysis);
                        }
                        
                        if (result.analysis.smc_analysis) {
                            document.getElementById('smc-content').innerHTML = 
                                formatSMCAnalysis(result.analysis.smc_analysis);
                        }
                        
                        if (result.analysis.price_analysis) {
                            document.getElementById('resultContent').innerHTML = 
                                formatPriceStats(result.analysis.price_analysis);
                        }
                        
                        // Navigate to price analysis page
                        document.querySelector('[data-page="price"]').click();
                    } else {
                        alert(result.message || 'Upload failed');
                    }
                } catch (error) {
                    console.error('Error:', error);
                    alert('Error uploading file: ' + error.message);
                } finally {
                    loading.classList.remove('active');
                }
            }
        });
    </script>
</body>
</html>"""