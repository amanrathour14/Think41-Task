# E-commerce Chatbot Docker Deployment Script
Write-Host "🚀 E-commerce Chatbot Docker Setup" -ForegroundColor Green
Write-Host "==================================" -ForegroundColor Green

# Check if Docker is installed
try {
    docker --version | Out-Null
    Write-Host "✅ Docker is installed" -ForegroundColor Green
}
catch {
    Write-Host "❌ Docker is not installed. Please install Docker Desktop first." -ForegroundColor Red
    exit 1
}

# Check if Docker Compose is available (try both V1 and V2)
$dockerComposeCmd = $null
try {
    docker compose version | Out-Null
    $dockerComposeCmd = "docker compose"
    Write-Host "✅ Docker Compose V2 is available" -ForegroundColor Green
}
catch {
    try {
        docker-compose --version | Out-Null
        $dockerComposeCmd = "docker-compose"
        Write-Host "✅ Docker Compose V1 is available" -ForegroundColor Green
    }
    catch {
        Write-Host "❌ Docker Compose is not available. Please install Docker Compose." -ForegroundColor Red
        Write-Host "   Try: docker compose version" -ForegroundColor Yellow
        exit 1
    }
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

Write-Host "🔧 Building and starting services..." -ForegroundColor Cyan

# Build and start all services using the detected command
& $dockerComposeCmd up --build -d

Write-Host "⏳ Waiting for services to start..." -ForegroundColor Yellow

# Wait for MySQL to be ready
Write-Host "📊 Waiting for MySQL database..." -ForegroundColor Yellow
Start-Sleep -Seconds 10
Write-Host "✅ MySQL should be ready" -ForegroundColor Green

# Wait for backend to be ready
Write-Host "🔧 Waiting for backend API..." -ForegroundColor Yellow
Start-Sleep -Seconds 15
Write-Host "✅ Backend API should be ready" -ForegroundColor Green

# Wait for frontend to be ready
Write-Host "🎨 Waiting for frontend..." -ForegroundColor Yellow
Start-Sleep -Seconds 10
Write-Host "✅ Frontend should be ready" -ForegroundColor Green

Write-Host ""
Write-Host "🎉 Setup Complete!" -ForegroundColor Green
Write-Host "==================" -ForegroundColor Green
Write-Host "🌐 Frontend: http://localhost:3000" -ForegroundColor Cyan
Write-Host "🔧 Backend API: http://localhost:8000" -ForegroundColor Cyan
Write-Host "📚 API Documentation: http://localhost:8000/docs" -ForegroundColor Cyan
Write-Host "🗄️  Database: localhost:3306" -ForegroundColor Cyan
Write-Host ""
Write-Host "📋 Useful Commands:" -ForegroundColor Yellow
Write-Host "   View logs: $dockerComposeCmd logs -f" -ForegroundColor Gray
Write-Host "   Stop services: $dockerComposeCmd down" -ForegroundColor Gray
Write-Host "   Restart services: $dockerComposeCmd restart" -ForegroundColor Gray
Write-Host "   View running containers: $dockerComposeCmd ps" -ForegroundColor Gray
Write-Host ""
Write-Host "🚀 Your e-commerce chatbot is now running!" -ForegroundColor Green 