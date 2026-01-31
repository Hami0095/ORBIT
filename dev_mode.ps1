# ORBIT Local Dev Setup

Write-Host "🚀 Starting ORBIT Dev Setup..." -ForegroundColor Cyan

# 1. Create Virtual Environment
if (!(Test-Path "venv")) {
    Write-Host "📦 Creating virtual environment..." -ForegroundColor Yellow
    python -m venv venv
}

# 2. Install Dependencies
Write-Host "📥 Installing dependencies..." -ForegroundColor Yellow
& .\venv\Scripts\python.exe -m pip install --upgrade pip
& .\venv\Scripts\pip.exe install -r requirements.txt

# 3. Environment Variables
if (!(Test-Path ".env")) {
    Write-Host "📄 Creating .env from .env.example..." -ForegroundColor Yellow
    Copy-Item .env.example .env
    
    # Update .env to use SQLite for easy local dev
    (Get-Content .env).replace('DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/orbit', '# DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/orbit') | Set-Content .env
}

Write-Host "✅ Dev Environment Ready!" -ForegroundColor Green
Write-Host "💡 To start the server in Dev Mode (SQLite), run: .\venv\Scripts\python.exe dev.py" -ForegroundColor Magenta
Write-Host "🌐 API Docs: http://127.0.0.1:8001/docs" -ForegroundColor Cyan
