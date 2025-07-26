# Simple E-commerce Chatbot Docker Deployment Script
Write-Host "🚀 E-commerce Chatbot Docker Setup" -ForegroundColor Green
Write-Host "==================================" -ForegroundColor Green

# Check if Docker is installed
try {
    docker --version | Out-Null
    Write-Host "✅ Docker is installed" -ForegroundColor Green
}
catch {
    Write-Host "❌ Docker is not installed. Please install Docker Desktop first." -ForegroundColor Red
    Write-Host "   Download from: https://www.docker.com/products/docker-desktop/" -ForegroundColor Yellow
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

Write-Host "✅ Environment configuration looks good" -ForegroundColor Green

Write-Host "🔧 Building and starting services..." -ForegroundColor Cyan

# Try Docker Compose V2 first, then V1
try {
    docker compose up --build -d
    Write-Host "✅ Using Docker Compose V2" -ForegroundColor Green
}
catch {
    try {
        docker-compose up --build -d
        Write-Host "✅ Using Docker Compose V1" -ForegroundColor Green
    }
    catch {
        Write-Host "❌ Failed to start services. Check Docker is running." -ForegroundColor Red
        exit 1
    }
}

Write-Host "⏳ Waiting for services to start..." -ForegroundColor Yellow
Start-Sleep -Seconds 30

Write-Host ""
Write-Host "🎉 Setup Complete!" -ForegroundColor Green
Write-Host "==================" -ForegroundColor Green
Write-Host "🌐 Frontend: http://localhost:3000" -ForegroundColor Cyan
Write-Host "🔧 Backend API: http://localhost:8000" -ForegroundColor Cyan
Write-Host "📚 API Documentation: http://localhost:8000/docs" -ForegroundColor Cyan
Write-Host "🗄️  Database: localhost:3306" -ForegroundColor Cyan
Write-Host ""
Write-Host "📋 Useful Commands:" -ForegroundColor Yellow
Write-Host "   View logs: docker compose logs -f" -ForegroundColor Gray
Write-Host "   Stop services: docker compose down" -ForegroundColor Gray
Write-Host "   View containers: docker compose ps" -ForegroundColor Gray
Write-Host ""
Write-Host "🚀 Your e-commerce chatbot is now running!" -ForegroundColor Green 