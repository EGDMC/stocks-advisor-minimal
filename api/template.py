HTML_TEMPLATE = """<!DOCTYPE html>
<html>
<head>
    <title>Trading Analysis Dashboard</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/chartjs-plugin-annotation"></script>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <link href="https://cdn.jsdelivr.net/npm/remixicon@3.5.0/fonts/remixicon.css" rel="stylesheet">
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: 'Inter', sans-serif;
        }
        
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
        }
        
        .sidebar-brand {
            color: white;
            font-size: 1.5rem;
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
        }
        
        .nav-item:hover, .nav-item.active {
            background: rgba(255, 255, 255, 0.1);
            color: white;
        }
        
        .nav-item i {
            font-size: 1.25rem;
        }
        
        .main-content {
            margin-left: 260px;
            padding: 2rem;
            width: calc(100% - 260px);
        }
        
        .page {
            display: none;
        }
        
        .page.active {
            display: block;
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
        
        .card {
            background: var(--card-bg);
            border-radius: 0.75rem;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
            padding: 1.5rem;
            margin-bottom: 1.5rem;
        }
        
        .card-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 1rem;
        }
        
        .card-title {
            font-size: 1.25rem;
            font-weight: 600;
            color: var(--text-primary);
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
        }
        
        .sub-chart {
            height: 250px;
        }
        
        .metrics-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 1rem;
        }
        
        .metric-card {
            background: var(--sidebar-bg);
            color: white;
            padding: 1.25rem;
            border-radius: 0.75rem;
        }
        
        .pattern-card {
            margin-bottom: 0.75rem;
            padding: 1rem;
            border-radius: 0.5rem;
            background: rgba(255, 255, 255, 0.1);
        }
        
        .signal-bullish { color: var(--success-color); font-weight: 600; }
        .signal-bearish { color: var(--danger-color); font-weight: 600; }
        .signal-neutral { color: var(--warning-color); font-weight: 600; }
        
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
        }
        
        .upload-icon {
            font-size: 3rem;
            color: var(--primary-color);
            margin-bottom: 1rem;
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
        
        .file-input {
            display: none;
        }
        
        .loading {
            display: none;
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: rgba(0, 0, 0, 0.5);
            align-items: center;
            justify-content: center;
            z-index: 1000;
        }
        
        .loading.active {
            display: flex;
        }
        
        .spinner {
            width: 40px;
            height: 40px;
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
    <div class="sidebar">
        <div class="sidebar-brand">
            <i class="ri-line-chart-line"></i>
            Trading Analysis
        </div>
        <nav>
            <a href="#" class="nav-item active" data-page="upload">
                <i class="ri-upload-cloud-line"></i>
                Data Upload
            </a>
            <a href="#" class="nav-item" data-page="price">
                <i class="ri-stock-line"></i>
                Price Analysis
            </a>
            <a href="#" class="nav-item" data-page="trend">
                <i class="ri-funds-line"></i>
                Trend Prediction
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
    </div>
    
    <div class="main-content">
        <div id="upload-page" class="page active">
            <div class="dashboard-header">
                <h1 class="page-title">Upload Data</h1>
                <p class="page-description">Upload your stock data CSV file to start the analysis</p>
            </div>
            
            <div class="card">
                <form id="uploadForm">
                    <div class="upload-container">
                        <i class="ri-upload-cloud-line upload-icon"></i>
                        <h2>Drop your file here</h2>
                        <p>or</p>
                        <input type="file" name="file" accept=".csv" class="file-input" required>
                        <button type="button" class="upload-btn" onclick="document.querySelector('.file-input').click()">
                            Select File
                        </button>
                        <p class="selected-file"></p>
                    </div>
                </form>
            </div>
        </div>
        
        <div id="price-page" class="page">
            <div class="dashboard-header">
                <h1 class="page-title">Price Analysis</h1>
                <p class="page-description">Comprehensive price movement analysis</p>
            </div>
            
            <div class="card">
                <div class="card-header">
                    <h2 class="card-title">Price Chart</h2>
                </div>
                <div class="chart-container">
                    <canvas id="priceChart"></canvas>
                </div>
            </div>
            
            <div class="card">
                <div class="card-header">
                    <h2 class="card-title">Price Statistics</h2>
                </div>
                <div id="resultContent"></div>
            </div>
        </div>
        
        <div id="trend-page" class="page">
            <div class="dashboard-header">
                <h1 class="page-title">Trend Prediction</h1>
                <p class="page-description">Market trend analysis and predictions</p>
            </div>
            
            <div class="grid">
                <div class="card">
                    <div class="card-header">
                        <h2 class="card-title">Current Trend</h2>
                    </div>
                    <div id="trendMetrics"></div>
                </div>
                
                <div class="card">
                    <div class="card-header">
                        <h2 class="card-title">Breakout Predictions</h2>
                    </div>
                    <div id="breakoutPredictions"></div>
                </div>
                
                <div class="card">
                    <div class="card-header">
                        <h2 class="card-title">Price Targets</h2>
                    </div>
                    <div id="priceTargets"></div>
                </div>
            </div>
        </div>
        
        <div id="patterns-page" class="page">
            <div class="dashboard-header">
                <h1 class="page-title">Pattern Recognition</h1>
                <p class="page-description">Chart and candlestick pattern analysis</p>
            </div>
            
            <div class="grid">
                <div class="card">
                    <div class="card-header">
                        <h2 class="card-title">Candlestick Patterns</h2>
                    </div>
                    <div id="candlestickPatterns"></div>
                </div>
                
                <div class="card">
                    <div class="card-header">
                        <h2 class="card-title">Chart Patterns</h2>
                    </div>
                    <div id="chartPatterns"></div>
                </div>
                
                <div class="card">
                    <div class="card-header">
                        <h2 class="card-title">Price Action</h2>
                    </div>
                    <div id="priceActionPatterns"></div>
                </div>
            </div>
        </div>
        
        <div id="technical-page" class="page">
            <div class="dashboard-header">
                <h1 class="page-title">Technical Indicators</h1>
                <p class="page-description">Key technical analysis indicators</p>
            </div>
            
            <div class="card">
                <div id="technicalSignals"></div>
            </div>
            
            <div class="card">
                <div class="card-header">
                    <h2 class="card-title">RSI</h2>
                </div>
                <div class="chart-container sub-chart">
                    <canvas id="rsiChart"></canvas>
                </div>
            </div>
            
            <div class="card">
                <div class="card-header">
                    <h2 class="card-title">MACD</h2>
                </div>
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
            
            <div class="card">
                <div id="smcContent"></div>
            </div>
        </div>
    </div>
    
    <div class="loading">
        <div class="spinner"></div>
    </div>
    
    <script>
        // Navigation handling
        document.querySelectorAll('.nav-item').forEach(item => {
            item.addEventListener('click', (e) => {
                e.preventDefault();
                const pageId = item.getAttribute('data-page');
                
                // Update navigation
                document.querySelectorAll('.nav-item').forEach(nav => nav.classList.remove('active'));
                item.classList.add('active');
                
                // Update pages
                document.querySelectorAll('.page').forEach(page => page.classList.remove('active'));
                document.getElementById(pageId + '-page').classList.add('active');
            });
        });
        
        // File upload handling
        const fileInput = document.querySelector('.file-input');
        const selectedFile = document.querySelector('.selected-file');
        const uploadContainer = document.querySelector('.upload-container');
        const loading = document.querySelector('.loading');
        
        fileInput.addEventListener('change', (e) => {
            if (e.target.files[0]) {
                selectedFile.textContent = e.target.files[0].name;
                handleFileUpload(e.target.files[0]);
            }
        });
        
        uploadContainer.addEventListener('dragover', (e) => {
            e.preventDefault();
            uploadContainer.style.borderColor = var('--primary-color');
        });
        
        uploadContainer.addEventListener('dragleave', (e) => {
            e.preventDefault();
            uploadContainer.style.borderColor = '#e5e7eb';
        });
        
        uploadContainer.addEventListener('drop', (e) => {
            e.preventDefault();
            uploadContainer.style.borderColor = '#e5e7eb';
            
            if (e.dataTransfer.files[0]) {
                fileInput.files = e.dataTransfer.files;
                selectedFile.textContent = e.dataTransfer.files[0].name;
                handleFileUpload(e.dataTransfer.files[0]);
            }
        });
        
        async function handleFileUpload(file) {
            const formData = new FormData();
            formData.append('file', file);
            
            loading.classList.add('active');
            
            try {
                const response = await fetch('/api', {
                    method: 'POST',
                    body: formData
                });
                const result = await response.json();
                
                if (result.status === 'success') {
                    // Create charts
                    createCharts(result.analysis.chart_configs);
                    
                    // Update all sections
                    formatTechnicalSignals(result.analysis.technical_signals);
                    formatPatterns(result.analysis.patterns);
                    formatTrendAnalysis(result.analysis.trend_analysis);
                    formatSMCAnalysis(result.analysis.smc_analysis);
                    formatMetrics(result.analysis);
                    
                    // Switch to price analysis page
                    document.querySelector('[data-page="price"]').click();
                } else {
                    alert('Error: ' + result.message);
                }
            } catch (error) {
                console.error('Error:', error);
                alert('Error processing file: ' + error.message);
            } finally {
                loading.classList.remove('active');
            }
        }
        
        // Previous chart and formatting functions remain the same
    </script>
</body>
</html>"""