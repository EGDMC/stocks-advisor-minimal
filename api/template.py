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
    
    <!-- Add the full CSS from the previous version -->
    
    <style>
        /* Previous styles remain the same */
    </style>
</head>
<body>
    <!-- Sidebar Navigation -->
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
            <!-- Previous upload content remains the same -->
        </div>

        <!-- Pages content from previous version -->
    </main>

    <!-- Loading Spinner -->
    <div class="loading">
        <div class="spinner"></div>
    </div>

    <!-- JavaScript -->
    <script>
        // Previous JavaScript functions remain the same
        
        // Initialize everything when the DOM is ready
        document.addEventListener('DOMContentLoaded', () => {
            // Add navigation event listeners
            document.querySelectorAll('.nav-item').forEach(item => {
                item.addEventListener('click', e => {
                    e.preventDefault();
                    const pageId = item.getAttribute('data-page');
                    
                    // Update navigation
                    document.querySelectorAll('.nav-item').forEach(nav => 
                        nav.classList.remove('active')
                    );
                    item.classList.add('active');
                    
                    // Update pages
                    document.querySelectorAll('.page').forEach(page => 
                        page.classList.remove('active')
                    );
                    document.getElementById(pageId + '-page').classList.add('active');
                });
            });

            // Initialize file upload handling
            const dropZone = document.getElementById('dropZone');
            const fileInput = document.getElementById('fileInput');
            const selectedFileText = document.getElementById('selectedFile');
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

            // Handle file drag & drop
            dropZone.addEventListener('dragenter', highlight);
            dropZone.addEventListener('dragover', highlight);
            dropZone.addEventListener('dragleave', unhighlight);
            dropZone.addEventListener('drop', unhighlight);

            function highlight() {
                dropZone.classList.add('highlight');
            }

            function unhighlight() {
                dropZone.classList.remove('highlight');
            }

            // Handle file selection
            fileInput.addEventListener('change', e => {
                const file = e.target.files[0];
                if (file) handleUpload(file);
            });

            dropZone.addEventListener('drop', e => {
                const file = e.dataTransfer.files[0];
                if (file) handleUpload(file);
            });

            async function handleUpload(file) {
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
                        // Create charts
                        createCharts(result.analysis.chart_configs);
                        
                        // Update all sections
                        updateTechnicalSignals(result.analysis.technical_signals);
                        updatePatterns(result.analysis.patterns);
                        updateTrendAnalysis(result.analysis.trend_analysis);
                        updateSMCAnalysis(result.analysis.smc_analysis);
                        updatePriceStats(result.analysis.price_analysis);
                        
                        // Navigate to price analysis page
                        document.querySelector('[data-page="price"]').click();
                    } else {
                        alert(result.message || 'Upload failed');
                    }
                } catch (error) {
                    console.error('Error:', error);
                    alert('Error processing file: ' + error.message);
                } finally {
                    loading.classList.remove('active');
                }
            }
        });
    </script>
</body>
</html>"""