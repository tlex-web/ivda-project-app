# IVDA Tutorial Web App - Docker Setup

This Docker setup provides a complete containerized environment for the IVDA Tutorial Web Application with the following services:

## Services

- **MongoDB**: Database server with automatic data import
- **Backend**: Flask REST API with Python
- **Frontend**: Vue.js application with Vuetify
- **Nginx**: Web server for serving the frontend

## Prerequisites

- Docker Desktop or Docker Engine (20.10+)
- Docker Compose (2.0+)

## Quick Start

1. **Clone/Navigate to the project directory:**

   ```bash
   cd hello-world
   ```

2. **Start all services:**

   ```bash
   docker-compose up -d
   ```

3. **Access the application:**

   - Frontend: http://localhost:8080
   - Backend API: http://localhost:5000
   - MongoDB: localhost:27017

4. **Stop all services:**
   ```bash
   docker-compose down
   ```

## Services Details

### MongoDB (Port 27017)

- **Database**: `companies`
- **Collection**: `companiesdb`
- **Data Source**: Automatically imports from `main_company.json`
- **Persistent Volume**: `mongodb_data`

### Backend API (Port 5000)

- **Framework**: Flask with Flask-RESTx
- **Database**: MongoDB connection
- **Endpoints**:
  - `GET /companies?category={All|tech|health|bank}` - Get companies by category
  - `GET /companies/{id}?algorithm={none|random|regression}` - Get company with profit predictions

### Frontend (Port 8080)

- **Framework**: Vue.js 3 with Vuetify 3
- **Features**: Interactive scatter plot, line plot, configuration panel
- **Build**: Optimized production build served by Nginx

## Data Import

The MongoDB container automatically imports company data from `main_company.json` using a dedicated import service that:

1. Waits for MongoDB to be ready
2. Imports JSON data into `companies.companiesdb` collection
3. Handles data structure with company information and profit history

## Development Commands

### Build individual services:

```bash
# Backend only
docker-compose build backend

# Frontend only
docker-compose build frontend
```

### View logs:

```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f backend
docker-compose logs -f frontend
docker-compose logs -f mongodb
```

### Restart services:

```bash
# Restart all
docker-compose restart

# Restart specific service
docker-compose restart backend
```

## Environment Variables

Configure the application using `.env` file:

```env
MONGO_INITDB_DATABASE=companies
MONGODB_PORT=27017
BACKEND_PORT=5000
FRONTEND_PORT=8080
```

## Troubleshooting

### Backend Connection Issues:

```bash
# Check backend health
curl http://localhost:5000/companies?category=All

# Check MongoDB connection
docker-compose exec mongodb mongosh companies --eval "db.companiesdb.countDocuments()"
```

### Frontend Issues:

```bash
# Rebuild frontend
docker-compose build --no-cache frontend
docker-compose up -d frontend
```

### Data Import Issues:

```bash
# Re-run data import
docker-compose run --rm mongo-import
```

## Clean Up

Remove all containers, networks, and volumes:

```bash
docker-compose down -v --remove-orphans
docker system prune -f
```

## Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │    Backend      │    │    MongoDB      │
│   (Vue.js)      │◄──►│    (Flask)      │◄──►│   (Database)    │
│   Port: 8080    │    │   Port: 5000    │    │   Port: 27017   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         └───────────────────────┼───────────────────────┘
                                 │
                        ┌─────────────────┐
                        │  Docker Network │
                        │  (ivda-network) │
                        └─────────────────┘
```
