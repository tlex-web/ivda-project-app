# Development environment startup script for Windows PowerShell

Write-Host "🚀 Starting IVDA Project in Development Mode..." -ForegroundColor Green
Write-Host "This will enable hot reloading for both frontend and backend" -ForegroundColor Yellow
Write-Host ""

# Stop any existing containers
Write-Host "📦 Stopping existing containers..." -ForegroundColor Blue
docker-compose down

# Start development environment
Write-Host "🔄 Starting development environment with hot reloading..." -ForegroundColor Blue
docker-compose -f docker-compose.yml -f docker-compose.dev.yml up --build

Write-Host ""
Write-Host "✅ Development environment started!" -ForegroundColor Green
Write-Host "🌐 Frontend (with hot reloading): http://localhost:8080" -ForegroundColor Cyan
Write-Host "🔧 Backend API: http://localhost:5000" -ForegroundColor Cyan
Write-Host "🗄️  MongoDB: localhost:27017" -ForegroundColor Cyan
Write-Host ""
Write-Host "To stop the development environment, press Ctrl+C" -ForegroundColor Yellow