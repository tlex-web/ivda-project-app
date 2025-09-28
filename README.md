# IVDA Vue.js Application with Docker

A full-stack web application built with Vue.js, Vuetify, Flask, and MongoDB, fully containerized with Docker.

## Features

- **Frontend**: Vue.js 3 with Vuetify 3 Material Design components
- **Interactive Visualizations**: Scatter plots and line charts with Plotly.js
- **Category-based Data Filtering**: Dynamic data visualization with category differentiation
- **Backend API**: Flask REST API with MongoDB integration
- **Full Docker Support**: Complete containerization with Docker Compose

## Technologies Used

### Frontend
- Vue.js 3.2.13
- Vuetify 3.10.3 (Material Design)
- Plotly.js 3.1.0 (Interactive charts)
- Nginx (Production web server)

### Backend
- Python Flask
- Flask-RESTx (API documentation)
- PyMongo (MongoDB integration)
- Flask-CORS (Cross-origin support)

### Database
- MongoDB 7.0

### DevOps
- Docker & Docker Compose
- Multi-stage Docker builds
- Nginx reverse proxy

## Quick Start with Docker

### Prerequisites
- Docker Desktop installed and running
- Docker Compose

### Running the Application

1. Clone the repository:
```bash
git clone <your-repo-url>
cd ivda-project-app
```

2. Start all services:
```bash
docker-compose up -d
```

3. Access the application:
- **Frontend**: http://localhost:8080
- **Backend API**: http://localhost:5000
- **MongoDB**: localhost:27017

### Services

The application consists of 4 Docker services:

1. **MongoDB** (`mongodb`): Database server with automatic data import
2. **Data Importer** (`mongo-import`): One-time data import service
3. **Backend API** (`backend`): Flask REST API server
4. **Frontend** (`frontend`): Vue.js application served by Nginx

## API Endpoints

- `GET /companies?category=All` - Get all companies
- `GET /companies?category={category}` - Get companies by category
- `GET /companies/{id}?algorithm={algorithm}` - Get company details with prediction

## Development

### Local Development Setup

1. **Frontend Development**:
```bash
cd services/frontend
npm install
npm run serve
```

2. **Backend Development**:
```bash
cd services/backend
pip install -r requirements.txt
python app.py
```

### Project Structure

```
ivda-project-app/
├── docker-compose.yml          # Docker services configuration
├── .env                        # Environment variables
├── README-Docker.md            # Docker-specific documentation
└── services/
    ├── frontend/               # Vue.js frontend application
    │   ├── Dockerfile         # Frontend container build
    │   ├── nginx.conf         # Nginx configuration
    │   ├── package.json       # Node.js dependencies
    │   └── src/               # Vue.js source code
    │       ├── components/    # Vue components
    │       │   ├── ConfigurationPanel.vue
    │       │   ├── ScatterPlot.vue
    │       │   └── LinePlot.vue
    │       └── App.vue        # Main application component
    └── backend/               # Flask backend API
        ├── Dockerfile         # Backend container build
        ├── requirements.txt   # Python dependencies
        ├── app.py            # Flask application entry point
        ├── main_company.json # Sample company data
        └── src/              # Python source code
            ├── __init__.py   # Flask app and API routes
            └── model.py      # Data models
```

## Features in Detail

### Interactive Scatter Plot
- Category-based color coding for data points
- Interactive legend with category filtering
- Click-to-select functionality
- Dynamic axis titles and scaling

### Configuration Panel
- Material Design interface with Vuetify components
- Category and algorithm selection
- Real-time data filtering
- Responsive design

### Data Visualization
- Plotly.js integration for interactive charts
- Multiple visualization types (scatter, line plots)
- Responsive and mobile-friendly charts

## Docker Configuration

### Environment Variables
Configure the application using the `.env` file:

```env
# MongoDB Configuration
MONGO_INITDB_DATABASE=companies
MONGODB_PORT=27017

# Backend Configuration
BACKEND_PORT=5000
FLASK_ENV=development

# Frontend Configuration
FRONTEND_PORT=8080
NODE_ENV=development
```

### Container Health Checks
- Backend health check via API endpoint
- Automatic service dependency management
- Restart policies for production reliability

## Troubleshooting

### Common Issues

1. **Empty white screen on frontend**:
   - Ensure all containers are running: `docker-compose ps`
   - Check frontend logs: `docker-compose logs frontend`

2. **API returns empty data**:
   - Verify MongoDB data import: `docker-compose logs mongo-import`
   - Check backend logs: `docker-compose logs backend`

3. **Port conflicts**:
   - Modify ports in `docker-compose.yml` if needed
   - Ensure ports 8080, 5000, and 27017 are available

### Useful Commands

```bash
# View all container logs
docker-compose logs

# Restart specific service
docker-compose restart frontend

# Rebuild containers
docker-compose build --no-cache

# Stop all services
docker-compose down

# View container status
docker-compose ps
```

## License

This project is part of the IVDA (Interactive Visual Data Analysis) tutorial series.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test with Docker
5. Submit a pull request