# E-commerce Chatbot Docker Setup Script for Windows
# This script sets up and runs the entire application stack using Docker

param(
    [switch]$SkipChecks
)

Write-Host "🚀 E-commerce Chatbot Docker Setup" -ForegroundColor Green
Write-Host "==================================" -ForegroundColor Green

if (-not $SkipChecks) {
    # Check if Docker is installed
    try {
        docker --version | Out-Null
        Write-Host "✅ Docker is installed" -ForegroundColor Green
    }
    catch {
        Write-Host "❌ Docker is not installed. Please install Docker Desktop first." -ForegroundColor Red
        exit 1
    }

    # Check if Docker Compose is installed
    try {
        docker-compose --version | Out-Null
        Write-Host "✅ Docker Compose is installed" -ForegroundColor Green
    }
    catch {
        Write-Host "❌ Docker Compose is not installed. Please install Docker Compose first." -ForegroundColor Red
        exit 1
    }

    # Check if .env file exists
    if (-not (Test-Path ".env")) {
        Write-Host "⚠️  .env file not found. Creating from template..." -ForegroundColor Yellow
        Copy-Item "docker.env" ".env"
        Write-Host "📝 Please edit .env file and add your GROQ_API_KEY" -ForegroundColor Yellow
        Write-Host "   Then run this script again." -ForegroundColor Yellow
        exit 1
    }

    # Check if GROQ_API_KEY is set
    $envContent = Get-Content ".env"
    if ($envContent -match "GROQ_API_KEY=your_groq_api_key_here") {
        Write-Host "❌ Please set your GROQ_API_KEY in the .env file" -ForegroundColor Red
        Write-Host "   Get your API key from: https://console.groq.com/" -ForegroundColor Yellow
        exit 1
    }
    else {
        Write-Host "✅ Environment configuration looks good" -ForegroundColor Green
    }
}

Write-Host "🔧 Building and starting services..." -ForegroundColor Cyan

# Build and start all services
docker-compose up --build -d

Write-Host "⏳ Waiting for services to start..." -ForegroundColor Yellow

# Wait for MySQL to be ready
Write-Host "📊 Waiting for MySQL database..." -ForegroundColor Yellow
do {
    Start-Sleep -Seconds 2
    Write-Host "   MySQL is starting..." -ForegroundColor Gray
} while (-not (docker-compose exec -T mysql mysqladmin ping -h localhost --silent 2>$null))
Write-Host "✅ MySQL is ready" -ForegroundColor Green

# Wait for backend to be ready
Write-Host "🔧 Waiting for backend API..." -ForegroundColor Yellow
do {
    Start-Sleep -Seconds 5
    Write-Host "   Backend is starting..." -ForegroundColor Gray
} while (-not (Invoke-WebRequest -Uri "http://localhost:8000/health" -UseBasicParsing -ErrorAction SilentlyContinue))
Write-Host "✅ Backend API is ready" -ForegroundColor Green

# Wait for frontend to be ready
Write-Host "🎨 Waiting for frontend..." -ForegroundColor Yellow
do {
    Start-Sleep -Seconds 2
    Write-Host "   Frontend is starting..." -ForegroundColor Gray
} while (-not (Invoke-WebRequest -Uri "http://localhost:3000" -UseBasicParsing -ErrorAction SilentlyContinue))
Write-Host "✅ Frontend is ready" -ForegroundColor Green

Write-Host ""
Write-Host "🎉 Setup Complete!" -ForegroundColor Green
Write-Host "==================" -ForegroundColor Green
Write-Host "🌐 Frontend: http://localhost:3000" -ForegroundColor Cyan
Write-Host "🔧 Backend API: http://localhost:8000" -ForegroundColor Cyan
Write-Host "📚 API Documentation: http://localhost:8000/docs" -ForegroundColor Cyan
Write-Host "🗄️  Database: localhost:3306" -ForegroundColor Cyan
Write-Host ""
Write-Host "📋 Useful Commands:" -ForegroundColor Yellow
Write-Host "   View logs: docker-compose logs -f" -ForegroundColor Gray
Write-Host "   Stop services: docker-compose down" -ForegroundColor Gray
Write-Host "   Restart services: docker-compose restart" -ForegroundColor Gray
Write-Host "   View running containers: docker-compose ps" -ForegroundColor Gray
Write-Host ""
Write-Host "🚀 Your e-commerce chatbot is now running!" -ForegroundColor Green 