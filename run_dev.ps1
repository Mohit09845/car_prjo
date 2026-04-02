# Create .venv if missing, install requirements, start FastAPI (Windows PowerShell)
$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot

if (-not (Test-Path ".venv\Scripts\Activate.ps1")) {
    Write-Host "Creating virtual environment .venv ..."
    python -m venv .venv
}

Write-Host "Activating .venv and installing dependencies ..."
& .\.venv\Scripts\Activate.ps1
pip install --upgrade pip
pip install -r requirements.txt

Write-Host "Starting FastAPI (uvicorn main:app --reload) ..."
uvicorn main:app --reload --host 0.0.0.0 --port 8000
