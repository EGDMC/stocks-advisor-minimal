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

        .card {
            background: var(--card-bg);
            border-radius: 0.75rem;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
            padding: 1.5rem;
            margin-bottom: 1.5rem;
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
        }

        .upload-container.highlight {
            border-color: var(--primary-color);
            background-color: rgba(37, 99, 235, 0.1);
        }

        .file-input {
            display: none;
        }

        /* Rest of your existing CSS */
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
        <!-- Pages -->
        <div id="upload-page" class="page active">
            <div class="dashboard-header">
                <h1 class="page-title">Upload Data</h1>
                <p class="page-description">Upload your stock data CSV file to start the analysis</p>
            </div>
            
            <div class="card">
                <form id="uploadForm" enctype="multipart/form-data">
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

        <!-- Other pages -->
        <div id="price-page" class="page">
            <!-- Price Analysis Content -->
        </div>

        <div id="trend-page" class="page">
            <!-- Trend Analysis Content -->
        </div>

        <div id="patterns-page" class="page">
            <!-- Pattern Recognition Content -->
        </div>

        <div id="technical-page" class="page">
            <!-- Technical Analysis Content -->
        </div>

        <div id="smc-page" class="page">
            <!-- SMC Analysis Content -->
        </div>
    </main>

    <div class="loading">
        <div class="spinner"></div>
    </div>

    <!-- Include chart formatting functions -->
    <script src="https://cdn.jsdelivr.net/npm/chartjs-plugin-annotation"></script>
    <script>
        // Formatting functions
        function formatNumber(num) {
            return new Intl.NumberFormat().format(num);
        }

        function formatTrendAnalysis(analysis) {
            // Your existing trend analysis formatting code
        }

        function formatPatterns(patterns) {
            // Your existing pattern formatting code
        }

        function formatTechnicalSignals(signals) {
            // Your existing technical signals formatting code
        }

        function formatSMCAnalysis(smc) {
            // Your existing SMC analysis formatting code
        }

        function formatMetrics(analysis) {
            // Your existing metrics formatting code
        }

        function createCharts(configs) {
            // Your existing chart creation code
        }
    </script>

    <!-- Include main functionality -->
    <script>
        // Load the static.js content here directly
        // Copy the content from static.js here
    </script>
</body>
</html>"""