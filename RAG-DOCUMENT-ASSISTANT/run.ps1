$ErrorActionPreference = "Stop"

$ProjectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path

Set-Location $ProjectRoot

if (-not (Test-Path ".venv")) {
    python -m venv .venv
}

& ".\.venv\Scripts\Activate.ps1"

python -m pip install --upgrade pip

python -m pip install -r requirements.txt

New-Item -ItemType Directory -Force -Path "data\uploads" | Out-Null
New-Item -ItemType Directory -Force -Path "data\documents" | Out-Null
New-Item -ItemType Directory -Force -Path "data\processed" | Out-Null

python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload