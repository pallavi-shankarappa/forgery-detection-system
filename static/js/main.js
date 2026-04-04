document.addEventListener('DOMContentLoaded', () => {
    fetchHistory();
});

let selectedFile = null;

function handleFileSelect(event) {
    const file = event.target.files[0];
    if (file) {
        selectedFile = file;
        showFilePreview(file);
    }
}

function handleDrop(event) {
    event.preventDefault();
    const file = event.dataTransfer.files[0];
    if (file && file.type.startsWith('image/')) {
        selectedFile = file;
        showFilePreview(file);
    }
}

function showFilePreview(file) {
    const previewContainer = document.getElementById('file-preview-container');
    const nameDisplay = document.getElementById('file-name-display');
    const uploadArea = document.getElementById('upload-area');
    
    nameDisplay.textContent = file.name;
    previewContainer.classList.remove('d-none');
    uploadArea.classList.add('d-none');
}

function resetUpload() {
    selectedFile = null;
    const previewContainer = document.getElementById('file-preview-container');
    const uploadArea = document.getElementById('upload-area');
    const fileInput = document.getElementById('file-input');
    
    previewContainer.classList.add('d-none');
    uploadArea.classList.remove('d-none');
    fileInput.value = '';
    
    // Hide results if they were showing
    document.getElementById('dashboard').classList.add('d-none');
}

async function startAnalysis() {
    if (!selectedFile) return;

    const dashboard = document.getElementById('dashboard');
    const spinner = document.getElementById('loading-spinner');
    const resultsArea = document.getElementById('results-area');
    
    dashboard.classList.remove('d-none');
    spinner.classList.remove('d-none');
    resultsArea.classList.add('d-none');
    
    // Scroll to dashboard
    dashboard.scrollIntoView({ behavior: 'smooth' });

    const formData = new FormData();
    formData.append('file', selectedFile);

    try {
        const response = await fetch('/api/upload', {
            method: 'POST',
            body: formData
        });

        if (!response.ok) throw new Error('Upload failed');

        const result = await response.json();
        displayResults(result);
        fetchHistory(); // Refresh history table
    } catch (error) {
        console.error('Error:', error);
        alert('An error occurred during analysis: ' + error.message);
        spinner.classList.add('d-none');
    }
}

function displayResults(data) {
    const spinner = document.getElementById('loading-spinner');
    const resultsArea = document.getElementById('results-area');
    
    spinner.classList.add('d-none');
    resultsArea.classList.remove('d-none');

    // Update images
    document.getElementById('original-preview').src = data.original_url;
    document.getElementById('ela-preview').src = data.ela_url;

    // Update status and confidence
    const statusBadge = document.getElementById('status-badge');
    const confidenceVal = document.getElementById('confidence-val');
    const confidenceProgress = document.getElementById('confidence-progress');
    const summaryText = document.getElementById('summary-text');
    const metadataFindings = document.getElementById('metadata-findings');

    const isForged = data.is_forged;
    const confidence = data.confidence_score;

    statusBadge.textContent = isForged ? 'Suspicious' : 'Authentic';
    statusBadge.className = `badge rounded-pill ${isForged ? 'bg-danger' : 'bg-success'}`;
    
    confidenceVal.textContent = `${confidence}%`;
    confidenceVal.className = `display-4 fw-bold mb-0 ${isForged ? 'text-danger' : 'text-success'}`;
    
    confidenceProgress.style.width = `${confidence}%`;
    confidenceProgress.className = `progress-bar ${isForged ? 'bg-danger' : 'bg-success'}`;

    summaryText.textContent = data.analysis_summary;
    summaryText.className = `text-muted p-3 bg-light rounded border-start border-4 ${isForged ? 'border-danger' : 'border-success'}`;

    // Update metadata
    if (data.metadata_markers && data.metadata_markers.length > 0) {
        metadataFindings.textContent = `Found markers for: ${data.metadata_markers}`;
        metadataFindings.className = 'mb-0 text-danger small fw-bold';
    } else {
        metadataFindings.textContent = 'No suspicious software markers found.';
        metadataFindings.className = 'mb-0 text-muted small';
    }
}

async function fetchHistory() {
    try {
        const response = await fetch('/api/history');
        const history = await response.json();
        
        const historyBody = document.getElementById('history-body');
        historyBody.innerHTML = '';

        if (history.length === 0) {
            historyBody.innerHTML = '<tr><td colspan="5" class="text-center text-muted py-4">No recent scans found.</td></tr>';
            return;
        }

        history.forEach(item => {
            const date = new Date(item.timestamp).toLocaleString();
            const statusClass = item.is_forged ? 'text-danger' : 'text-success';
            const badgeClass = item.is_forged ? 'bg-danger' : 'bg-success';
            
            const row = `
                <tr>
                    <td class="small text-muted">${date}</td>
                    <td class="fw-bold">${item.filename}</td>
                    <td><span class="badge ${badgeClass}">${item.is_forged ? 'Suspicious' : 'Authentic'}</span></td>
                    <td><span class="${statusClass} fw-bold">${item.confidence_score}%</span></td>
                    <td class="text-end">
                        <button class="btn btn-sm btn-outline-primary" onclick="viewResult(${item.id})">
                            <i class="fas fa-eye"></i>
                        </button>
                    </td>
                </tr>
            `;
            historyBody.innerHTML += row;
        });
    } catch (error) {
        console.error('Error fetching history:', error);
    }
}

function downloadReport() {
    alert('PDF report generation is being processed. This feature will be available shortly!');
}

function viewResult(id) {
    // This could fetch specific result and update dashboard
    alert('Viewing result ID: ' + id + '. Dashboard will update with this historical data.');
}
