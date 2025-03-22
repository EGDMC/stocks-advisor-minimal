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
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }

        .card:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
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
            margin-top: 1rem;
        }

        .upload-btn:hover {
            background: #1d4ed8;
        }

        .selected-file {
            margin-top: 1rem;
            color: var(--text-secondary);
        }

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

        .metrics-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 1rem;
        }

        .indicator-card {
            background: var(--sidebar-bg);
            color: white;
            padding: 1.25rem;
            border-radius: 0.75rem;
            transition: transform 0.3s ease;
        }

        .indicator-card:hover {
            transform: translateY(-2px);
        }

        .signal-bullish { color: var(--success-color); font-weight: 600; }
        .signal-bearish { color: var(--danger-color); font-weight: 600; }
        .signal-neutral { color: var(--warning-color); font-weight: 600; }
    </style>
</head>
<body>
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

    <main class="main-content">
        <div id="upload-page" class="page active">
            <div class="dashboard-header">
                <h1 class="page-title">Upload Data</h1>
                <p class="page-description">Upload your stock data CSV file to start the analysis</p>
            </div>
            
            <div class="card">
                <form id="uploadForm">
                    <div class="upload-container" id="dropZone">
                        <i class="ri-upload-cloud-line upload-icon"></i>
                        <h2>Drop your CSV file here</h2>
                        <p>or</p>
                        <input type="file" name="file" id="fileInput" accept=".csv" class="file-input" required>
                        <button type="button" class="upload-btn">Select File</button>
                        <p id="selectedFile" class="selected-file"></p>
                    </div>
                </form>
            </div>
        </div>

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
                <h2>Price Statistics</h2>
                <div id="resultContent"></div>
            </div>
        </div>

        <!-- Other pages... -->
    </main>

    <div class="loading">
        <div class="spinner"></div>
    </div>

    <script>
        // Navigation
        document.querySelectorAll('.nav-item').forEach(item => {
            item.addEventListener('click', e => {
                e.preventDefault();
                const pageId = item.getAttribute('data-page');
                
                document.querySelectorAll('.nav-item').forEach(nav => nav.classList.remove('active'));
                item.classList.add('active');
                
                document.querySelectorAll('.page').forEach(page => page.classList.remove('active'));
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
            dropZone.addEventListener(event, preventDefaults, false);
            document.body.addEventListener(event, preventDefaults, false);
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
            const dt = e.dataTransfer;
            const file = dt.files[0];
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
                    createCharts(result.analysis.chart_configs);
                    updateAnalysis(result.analysis);
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

        function updateAnalysis(analysis) {
            if (analysis.chart_configs) createCharts(analysis.chart_configs);
            if (analysis.technical_signals) updateTechnicalSignals(analysis.technical_signals);
            if (analysis.patterns) updatePatterns(analysis.patterns);
            if (analysis.trend_analysis) updateTrendAnalysis(analysis.trend_analysis);
            if (analysis.smc_analysis) updateSMCAnalysis(analysis.smc_analysis);
            if (analysis.price_analysis) updatePriceStats(analysis.price_analysis);
        }

        // Add other update functions here...
    </script>
</body>
</html>"""