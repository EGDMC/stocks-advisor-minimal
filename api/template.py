HTML_TEMPLATE = """<!DOCTYPE html>
<html>
<head>
    <title>Trading Analysis Dashboard</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/chartjs-plugin-annotation"></script>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <link href="https://cdn.jsdelivr.net/npm/remixicon@3.5.0/fonts/remixicon.css" rel="stylesheet">
    
    <!-- Previous styles remain the same -->
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
        
        /* Add all previous CSS styles here */
    </style>
</head>
<body>
    <nav class="sidebar">
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
    </nav>

    <main class="main-content">
        <!-- Upload Page -->
        <div id="upload-page" class="page active">
            <div class="dashboard-header">
                <h1 class="page-title">Upload Data</h1>
                <p class="page-description">Upload your stock data CSV file to start the analysis</p>
            </div>
            
            <div class="card">
                <form id="uploadForm" action="/api" method="post" enctype="multipart/form-data">
                    <div class="upload-container" id="dropZone">
                        <i class="ri-upload-cloud-line upload-icon"></i>
                        <h2>Drop your file here</h2>
                        <p>or</p>
                        <input type="file" name="file" id="fileInput" accept=".csv" class="file-input" required>
                        <button type="button" class="upload-btn" onclick="document.getElementById('fileInput').click()">
                            Select File
                        </button>
                        <p id="selectedFile" class="selected-file"></p>
                    </div>
                </form>
            </div>
        </div>

        <!-- Analysis Pages -->
        <div id="price-page" class="page">
            <!-- Price Analysis Content -->
            <div class="dashboard-header">
                <h1 class="page-title">Price Analysis</h1>
                <p class="page-description">Comprehensive price movement analysis</p>
            </div>
            
            <div class="grid">
                <div class="card">
                    <div class="chart-container">
                        <canvas id="priceChart"></canvas>
                    </div>
                </div>
                
                <div class="card">
                    <div id="resultContent"></div>
                </div>
            </div>
        </div>

        <!-- Add other pages with their respective content -->
        <!-- Include all previous page content -->

        <!-- Loading Spinner -->
        <div class="loading">
            <div class="spinner"></div>
        </div>
    </main>

    <script>
        // Navigation
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

        // File Upload Handling
        const dropZone = document.getElementById('dropZone');
        const fileInput = document.getElementById('fileInput');
        const selectedFileText = document.getElementById('selectedFile');
        const uploadForm = document.getElementById('uploadForm');
        const loading = document.querySelector('.loading');

        // Prevent default drag behaviors
        ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
            dropZone.addEventListener(eventName, preventDefaults, false);
            document.body.addEventListener(eventName, preventDefaults, false);
        });

        function preventDefaults(e) {
            e.preventDefault();
            e.stopPropagation();
        }

        // Handle file selection
        fileInput.addEventListener('change', handleFileSelect);
        dropZone.addEventListener('drop', handleDrop);

        function handleFileSelect(e) {
            const file = e.target.files[0];
            if (file) {
                selectedFileText.textContent = file.name;
                handleFileUpload(file);
            }
        }

        function handleDrop(e) {
            const file = e.dataTransfer.files[0];
            if (file) {
                fileInput.files = e.dataTransfer.files;
                selectedFileText.textContent = file.name;
                handleFileUpload(file);
            }
        }

        async function handleFileUpload(file) {
            const formData = new FormData();
            formData.append('file', file);
            
            loading.classList.add('active');
            
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
                    updateAnalysis(result.analysis);
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

        function updateAnalysis(analysis) {
            // Create charts
            createCharts(analysis.chart_configs);
            
            // Update all sections
            document.getElementById('technicalSignals').innerHTML = 
                formatTechnicalSignals(analysis.technical_signals);
            formatPatterns(analysis.patterns);
            formatTrendAnalysis(analysis.trend_analysis);
            
            // Update SMC analysis
            const smcAnalysis = document.getElementById('smc-analysis');
            if (analysis.smc_analysis) {
                smcAnalysis.style.display = 'block';
                document.getElementById('smcContent').innerHTML = 
                    formatSMCAnalysis(analysis.smc_analysis);
            } else {
                smcAnalysis.style.display = 'none';
            }
            
            // Update price statistics
            document.getElementById('resultContent').innerHTML = 
                formatMetrics(analysis);
        }

        // Include all previous JavaScript functions
        // (formatTechnicalSignals, formatPatterns, formatTrendAnalysis, etc.)
    </script>
</body>
</html>"""