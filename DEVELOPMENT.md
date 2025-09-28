# Development Environment Setup

This document explains how to set up and use the development environment with hot reloading for the IVDA Project.

## 🚀 Quick Start (Development Mode)

### Option 1: Using the startup scripts

**Windows (PowerShell):**

```powershell
.\dev-start.ps1
```

**Linux/macOS (Bash):**

```bash
chmod +x dev-start.sh
./dev-start.sh
```

### Option 2: Manual Docker Compose

```bash
# Stop any existing containers
docker-compose down

# Start development environment
docker-compose -f docker-compose.yml -f docker-compose.dev.yml up --build
```

## 🔥 Development Features

### Frontend Hot Reloading

- **Port**: http://localhost:8080
- **Features**:
  - Automatic browser refresh on file changes
  - Source code changes are reflected immediately
  - WebSocket-based hot module replacement
  - File watching with polling for Docker compatibility

### Backend Development

- **Port**: http://localhost:5000
- **Features**:
  - Flask development mode enabled
  - Debug mode for detailed error messages
  - Source code mounting for file changes

## 📁 Watched Files

The following files and directories are watched for changes:

### Frontend:

- `src/**/*` - All Vue.js source files
- `public/**/*` - Static assets
- `vue.config.js` - Vue configuration
- `babel.config.js` - Babel configuration

### Backend:

- All Python files in the backend directory
- Flask will automatically restart on changes

## 🛠️ Development vs Production

| Feature       | Development  | Production         |
| ------------- | ------------ | ------------------ |
| Hot Reloading | ✅ Enabled   | ❌ Disabled        |
| File Watching | ✅ Real-time | ❌ N/A             |
| Build Process | ❌ No build  | ✅ Optimized build |
| Bundle Size   | ❌ Larger    | ✅ Minified        |
| Source Maps   | ✅ Enabled   | ❌ Disabled        |
| Debug Mode    | ✅ Enabled   | ❌ Disabled        |

## 🐛 Troubleshooting

### Hot Reloading Not Working

1. **Check file permissions**: Ensure files are readable
2. **Restart containers**: `docker-compose down && docker-compose -f docker-compose.yml -f docker-compose.dev.yml up`
3. **Clear browser cache**: Hard refresh (Ctrl+Shift+R)
4. **Check logs**: `docker logs ivda-frontend-dev`

### Performance Issues

- **Increase memory**: Node.js memory is set to 4GB (`NODE_OPTIONS="--max-old-space-size=4096"`)
- **Disable file watching**: Remove `CHOKIDAR_USEPOLLING=true` if on native Docker
- **Check CPU usage**: Large files like Plotly.js may cause slower compilation

### Port Conflicts

If port 8080 is already in use:

1. Stop other services using the port
2. Or modify the port in `docker-compose.dev.yml`

## 📝 Making Changes

1. **Frontend changes**: Edit files in `services/frontend/src/`
2. **Backend changes**: Edit files in `services/backend/`
3. **Configuration changes**: Restart the development environment

## 🔄 Switching Between Modes

### Switch to Production:

```bash
docker-compose down
docker-compose up --build
```

### Switch to Development:

```bash
docker-compose down
docker-compose -f docker-compose.yml -f docker-compose.dev.yml up --build
```

## 📊 Accessing Services

- **Frontend**: http://localhost:8080 (with hot reloading)
- **Backend API**: http://localhost:5000
- **MongoDB**: localhost:27017
- **API Docs**: http://localhost:5000/companies?category=All (example endpoint)

Happy coding! 🎉
