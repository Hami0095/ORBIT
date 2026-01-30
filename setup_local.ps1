# ORBIT Local Setup Script

Write-Host "🚀 Starting ORBIT Local Setup..." -ForegroundColor Cyan

# 1. Create Virtual Environment
if (!(Test-Path "venv")) {
    Write-Host "📦 Creating virtual environment..." -ForegroundColor Yellow
    python -m venv venv
}

# 2. Activate and Install Dependencies
Write-Host "📥 Installing dependencies..." -ForegroundColor Yellow
& .\venv\Scripts\python.exe -m pip install --upgrade pip
& .\venv\Scripts\pip.exe install -r requirements.txt

# 3. Environment Variables
if (!(Test-Path ".env")) {
    Write-Host "📄 Creating .env from .env.example..." -ForegroundColor Yellow
    Copy-Item .env.example .env
}

Write-Host "✅ Setup Complete!" -ForegroundColor Green
Write-Host "💡 To start the server, run: .\venv\Scripts\uvicorn.exe backend.app.main:app --reload" -ForegroundColor Magenta
Write-Host "⚠️  Note: Ensure you have a local PostgreSQL running on localhost:5432" -ForegroundColor Red
