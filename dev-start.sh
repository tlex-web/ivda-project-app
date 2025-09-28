#!/bin/bash
# Development environment startup script

echo "🚀 Starting IVDA Project in Development Mode..."
echo "This will enable hot reloading for both frontend and backend"
echo ""

# Stop any existing containers
echo "📦 Stopping existing containers..."
docker-compose down

# Start development environment
echo "🔄 Starting development environment with hot reloading..."
docker-compose -f docker-compose.yml -f docker-compose.dev.yml up --build

echo ""
echo "✅ Development environment started!"
echo "🌐 Frontend (with hot reloading): http://localhost:8080"
echo "🔧 Backend API: http://localhost:5000"
echo "🗄️  MongoDB: localhost:27017"
echo ""
echo "To stop the development environment, press Ctrl+C"