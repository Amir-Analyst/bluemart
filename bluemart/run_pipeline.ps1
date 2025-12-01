# BlueMart Data Pipeline Execution Script

# Ensure we are running from the script's directory so relative paths work
Set-Location $PSScriptRoot

Write-Host "Starting BlueMart Data Pipeline..." -ForegroundColor Cyan

# 1. Generate Data
Write-Host "Step 1: Generating Synthetic Data (5000 SKUs)..." -ForegroundColor Yellow
python scripts/generate_data.py
if ($LASTEXITCODE -ne 0) {
    Write-Error "Data generation failed!"
    exit 1
}

# 2. Process Data
Write-Host "Step 2: Processing Data (Aggregating by Month)..." -ForegroundColor Yellow
python scripts/process_data.py
if ($LASTEXITCODE -ne 0) {
    Write-Error "Data processing failed!"
    exit 1
}

Write-Host "Pipeline Completed Successfully!" -ForegroundColor Green
Write-Host "You can now run the dashboard using: streamlit run app.py" -ForegroundColor Cyan
