#!/bin/bash

# E-commerce Chatbot Docker Setup Script
# This script sets up and runs the entire application stack using Docker

set -e

echo "🚀 E-commerce Chatbot Docker Setup"
echo "=================================="

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "⚠️  .env file not found. Creating from template..."
    cp docker.env .env
    echo "📝 Please edit .env file and add your GROQ_API_KEY"
    echo "   Then run this script again."
    exit 1
fi

# Check if GROQ_API_KEY is set
if ! grep -q "GROQ_API_KEY=your_groq_api_key_here" .env; then
    echo "✅ Environment configuration looks good"
else
    echo "❌ Please set your GROQ_API_KEY in the .env file"
    echo "   Get your API key from: https://console.groq.com/"
    exit 1
fi

echo "🔧 Building and starting services..."

# Build and start all services
docker-compose up --build -d

echo "⏳ Waiting for services to start..."

# Wait for MySQL to be ready
echo "📊 Waiting for MySQL database..."
until docker-compose exec -T mysql mysqladmin ping -h localhost --silent; do
    echo "   MySQL is starting..."
    sleep 2
done
echo "✅ MySQL is ready"

# Wait for backend to be ready
echo "🔧 Waiting for backend API..."
until curl -f http://localhost:8000/health > /dev/null 2>&1; do
    echo "   Backend is starting..."
    sleep 5
done
echo "✅ Backend API is ready"

# Wait for frontend to be ready
echo "🎨 Waiting for frontend..."
until curl -f http://localhost:3000 > /dev/null 2>&1; do
    echo "   Frontend is starting..."
    sleep 2
done
echo "✅ Frontend is ready"

echo ""
echo "🎉 Setup Complete!"
echo "=================="
echo "🌐 Frontend: http://localhost:3000"
echo "🔧 Backend API: http://localhost:8000"
echo "📚 API Documentation: http://localhost:8000/docs"
echo "🗄️  Database: localhost:3306"
echo ""
echo "📋 Useful Commands:"
echo "   View logs: docker-compose logs -f"
echo "   Stop services: docker-compose down"
echo "   Restart services: docker-compose restart"
echo "   View running containers: docker-compose ps"
echo ""
echo "🚀 Your e-commerce chatbot is now running!" 