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
        :root {
            --primary-color: #2563eb;
            --sidebar-bg: #1a1c23;
            --content-bg: #f3f4f6;
            --card-bg: #ffffff;
            --text-primary: #111827;
            --text-secondary: #6b7280;
            --success-color: #10b981;
            --warning-color: #f59e0b;
            --danger-color: #ef4444;
        }

        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: 'Inter', sans-serif;
        }

        body {
            background: var(--content-bg);
            color: var(--text-primary);
            display: flex;
            min-height: 100vh;
        }

        .sidebar {
            width: 260px;
            background: var(--sidebar-bg);
            padding: 1.5rem;
            display: flex;
            flex-direction: column;
            position: fixed;
            height: 100vh;
            left: 0;
            top: 0;
            z-index: 100;
        }

        .sidebar-brand {
            color: white;
            font-size: 1.25rem;
            font-weight: 600;
            margin-bottom: 2rem;
            display: flex;
            align-items: center;
            gap: 0.75rem;
        }

        .nav-item {
            color: #9ca3af;
            text-decoration: none;
            padding: 0.75rem 1rem;
            border-radius: 0.5rem;
            display: flex;
            align-items: center;
            gap: 0.75rem;
            margin-bottom: 0.5rem;
            transition: all 0.3s;
            cursor: pointer;
        }

        .nav-item:hover, .nav-item.active {
            background: rgba(255, 255, 255, 0.1);
            color: white;
        }

        .main-content {
            margin-left: 260px;
            padding: 2rem;
            width: calc(100% - 260px);
        }

        .page {
            display: none;
            animation: fadeIn 0.3s ease;
        }

        .page.active {
            display: block;
        }

        @keyframes fadeIn {
            from { opacity: 0; }
            to { opacity: 1; }
        }

        .card {
            background: var(--card-bg);
            border-radius: 0.75rem;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
            padding: 1.5rem;
            margin-bottom: 1.5rem;
        }

        .dashboard-header {
            margin-bottom: 2rem;
        }

        .page-title {
            font-size: 1.875rem;
            font-weight: 600;
            color: var(--text-primary);
            margin-bottom: 0.5rem;
        }

        .page-description {
            color: var(--text-secondary);
        }

        .upload-container {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            min-height: 300px;
            border: 2px dashed #e5e7eb;
            border-radius: 0.75rem;
            padding: 2rem;
            text-align: center;
            transition: all 0.3s ease;
            cursor: pointer;
        }

        .upload-container:hover {
            border-color: var(--primary-color);
            background: rgba(37, 99, 235, 0.05);
        }

        .upload-container.highlight {
            border-color: var(--primary-color);
            background: rgba(37, 99, 235, 0.1);
        }

        .upload-icon {
            font-size: 3rem;
            color: var(--primary-color);
            margin-bottom: 1rem;
        }

        .file-input {
            display: none;
        }

        .upload-btn {
            background: var(--primary-color);
            color: white;
            padding: 0.75rem 1.5rem;
            border: none;
            border-radius: 0.5rem;
            font-size: 1rem;
            cursor: pointer;
            transition: background 0.3s;
        }

        .upload-btn:hover {
            background: #1d4ed8;
        }

        .grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 1.5rem;
        }

        .chart-container {
            position: relative;
            height: 400px;
            width: 100%;
            margin-bottom: 1.5rem;
        }

        .sub-chart {
            height: 250px;
        }

        .indicator-card {
            background: var(--sidebar-bg);
            color: white;
            padding: 1.25rem;
            border-radius: 0.75rem;
            margin-bottom: 1rem;
        }

        .signal-bullish { color: var(--success-color); }
        .signal-bearish { color: var(--danger-color); }
        .signal-neutral { color: var(--warning-color); }

        .loading {
            display: none;
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: rgba(0, 0, 0, 0.7);
            z-index: 1000;
            justify-content: center;
            align-items: center;
        }

        .loading.active {
            display: flex;
        }

        .spinner {
            width: 50px;
            height: 50px;
            border: 4px solid #f3f3f3;
            border-top: 4px solid var(--primary-color);
            border-radius: 50%;
            animation: spin 1s linear infinite;
        }

        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
    </style>
</head>
<body>
    <!-- Sidebar -->
    <nav class="sidebar">
        <div class="sidebar-brand">
            <i class="ri-line-chart-line"></i>
            Trading Analysis
        </div>
        <a href="#" class="nav-item active" data-page="upload">
            <i class="ri-upload-cloud-line"></i>
            Upload Data
        </a>
        <a href="#" class="nav-item" data-page="price">
            <i class="ri-stock-line"></i>
            Price Analysis
        </a>
        <a href="#" class="nav-item" data-page="trend">
            <i class="ri-funds-line"></i>
            Trend Analysis
        </a>
        <a href="#" class="nav-item" data-page="patterns">
            <i class="ri-rhythm-line"></i>
            Pattern Recognition
        </a>
        <a href="#" class="nav-item" data-page="technical">
            <i class="ri-bar-chart-box-line"></i>
            Technical Indicators
        </a>
        <a href="#" class="nav-item" data-page="smc">
            <i class="ri-radar-line"></i>
            SMC Analysis
        </a>
    </nav>

    <!-- Main Content -->
    <main class="main-content">
        <!-- Upload Page -->
        <div id="upload-page" class="page active">
            <div class="dashboard-header">
                <h1 class="page-title">Upload Data</h1>
                <p class="page-description">Upload your stock data CSV file to start the analysis</p>
            </div>
            <div class="card">
                <div class="upload-container" id="dropZone">
                    <i class="ri-upload-cloud-line upload-icon"></i>
                    <h2>Drop your CSV file here</h2>
                    <p>or</p>
                    <input type="file" name="file" id="fileInput" accept=".csv" class="file-input">
                    <button type="button" class="upload-btn">Select File</button>
                    <p id="selectedFile" class="selected-file"></p>
                </div>
            </div>
        </div>

        <!-- Price Analysis Page -->
        <div id="price-page" class="page">
            <div class="dashboard-header">
                <h1 class="page-title">Price Analysis</h1>
                <p class="page-description">Market price movement analysis</p>
            </div>
            <div class="card">
                <div class="chart-container">
                    <canvas id="priceChart"></canvas>
                </div>
            </div>
            <div class="card">
                <div id="resultContent"></div>
            </div>
        </div>

        <!-- Other Pages -->
        <div id="trend-page" class="page">
            <div class="dashboard-header">
                <h1 class="page-title">Trend Analysis</h1>
                <p class="page-description">Market trend prediction and analysis</p>
            </div>
            <div id="trend-content" class="grid"></div>
        </div>

        <div id="patterns-page" class="page">
            <div class="dashboard-header">
                <h1 class="page-title">Pattern Recognition</h1>
                <p class="page-description">Chart and candlestick pattern analysis</p>
            </div>
            <div id="patterns-content" class="grid"></div>
        </div>

        <div id="technical-page" class="page">
            <div class="dashboard-header">
                <h1 class="page-title">Technical Indicators</h1>
                <p class="page-description">Technical analysis indicators</p>
            </div>
            <div id="technicalSignals" class="grid"></div>
            <div class="card">
                <div class="chart-container sub-chart">
                    <canvas id="rsiChart"></canvas>
                </div>
            </div>
            <div class="card">
                <div class="chart-container sub-chart">
                    <canvas id="macdChart"></canvas>
                </div>
            </div>
        </div>

        <div id="smc-page" class="page">
            <div class="dashboard-header">
                <h1 class="page-title">SMC Analysis</h1>
                <p class="page-description">Smart Money Concepts analysis</p>
            </div>
            <div id="smc-content" class="grid"></div>
        </div>
    </main>

    <!-- Loading Overlay -->
    <div class="loading">
        <div class="spinner"></div>
    </div>

    <!-- JavaScript -->
    <script>
        // Previous JavaScript code remains the same
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

            // File Upload
            const dropZone = document.getElementById('dropZone');
            const fileInput = document.getElementById('fileInput');
            const selectedFileText = document.getElementById('selectedFile');
            const uploadBtn = document.querySelector('.upload-btn');
            const loading = document.querySelector('.loading');

            uploadBtn.addEventListener('click', () => fileInput.click());

            ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(event => {
                dropZone.addEventListener(event, preventDefaults);
                document.body.addEventListener(event, preventDefaults);
            });

            function preventDefaults(e) {
                e.preventDefault();
                e.stopPropagation();
            }

            ['dragenter', 'dragover'].forEach(event => {
                dropZone.addEventListener(event, () => dropZone.classList.add('highlight'));
            });

            ['dragleave', 'drop'].forEach(event => {
                dropZone.addEventListener(event, () => dropZone.classList.remove('highlight'));
            });

            dropZone.addEventListener('drop', handleDrop);
            fileInput.addEventListener('change', handleFile);

            function handleDrop(e) {
                const file = e.dataTransfer.files[0];
                handleUpload(file);
            }

            function handleFile(e) {
                const file = e.target.files[0];
                handleUpload(file);
            }

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

                    if (!response.ok) throw new Error('Upload failed');

                    const result = await response.json();

                    if (result.status === 'success') {
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

            // Initialize charts object
            window.charts = {};

            // Add chart and formatting functions
            window.createCharts = function(configs) {
                Object.values(window.charts).forEach(chart => chart?.destroy());
                
                if (configs.main) {
                    window.charts.price = new Chart(
                        document.getElementById('priceChart').getContext('2d'),
                        configs.main
                    );
                }
                
                if (configs.rsi) {
                    window.charts.rsi = new Chart(
                        document.getElementById('rsiChart').getContext('2d'),
                        configs.rsi
                    );
                }
                
                if (configs.macd) {
                    window.charts.macd = new Chart(
                        document.getElementById('macdChart').getContext('2d'),
                        configs.macd
                    );
                }
            };
        });
    </script>
</body>
</html>"""