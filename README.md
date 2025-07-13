# 🛍️ Smart Retail App

A comprehensive inventory management system for retail store chains built with Flask, React, PostgreSQL, Docker, and Kubernetes.

[![CI/CD Pipeline](https://github.com/your-username/smart-retail-app/workflows/CI/CD%20Pipeline/badge.svg)](https://github.com/your-username/smart-retail-app/actions)
[![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/)
[![Kubernetes](https://img.shields.io/badge/kubernetes-%23326ce5.svg?style=for-the-badge&logo=kubernetes&logoColor=white)](https://kubernetes.io/)
[![Flask](https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![React](https://img.shields.io/badge/react-%2320232a.svg?style=for-the-badge&logo=react&logoColor=%2361DAFB)](https://reactjs.org/)

## 🚀 Features

- **📦 Real-time Stock Tracking**: Monitor inventory levels across all products
- **⚠️ Low Stock Alerts**: Automatic notifications when items fall below threshold
- **📈 Restocking Management**: Easy restocking operations with full audit trail
- **📊 Analytics Dashboard**: Stock trends and analytics for better decision making
- **🔌 RESTful API**: Complete REST API for all operations
- **🐳 Containerized Deployment**: Docker & Kubernetes deployment for production scaling
- **📈 High Availability**: Multiple replicas and health checks
- **🔍 Monitoring**: Prometheus metrics and Grafana dashboards
- **🔄 CI/CD Pipeline**: Automated testing, building, and deployment

## 🏗️ Project Structure

```
smart-retail-app/
├── backend/                  # Flask backend application
│   ├── app.py               # Main Flask application
│   ├── requirements.txt     # Production dependencies
│   ├── requirements-dev.txt # Development dependencies
│   ├── Dockerfile          # Backend container configuration
│   ├── tests/              # Unit tests
│   ├── locustfile.py       # Performance testing
│   ├── init.sql            # Database initialization
│   └── sample_products.json # Sample data
│
├── frontend/                # React frontend application
│   ├── src/                # React source code
│   ├── public/             # Static assets
│   ├── package.json        # Node.js dependencies
│   ├── Dockerfile          # Frontend container configuration
│   └── nginx.conf          # Nginx configuration
│
├── k8s/                     # Kubernetes manifests
│   ├── configs/            # ConfigMaps
│   ├── deployments/        # Application deployments
│   ├── services/           # Service definitions
│   ├── ingress/            # Ingress rules
│   ├── monitoring/         # Prometheus & Grafana
│   └── secrets/            # Kubernetes secrets
│
├── scripts/                 # Utility scripts
│   ├── setup-ci-cd.sh      # CI/CD setup script
│   ├── test-pipeline-local.sh # Local testing script
│   ├── load_sample_data.py # Data loading utilities
│   └── health_check.py     # Health check utilities
│
├── docs/                    # Documentation
│   ├── README.md           # Detailed documentation
│   ├── CI_CD_SETUP_GUIDE.md # CI/CD setup guide
│   ├── COMPLETE_GUIDE.md   # Complete user guide
│   └── TESTING_GUIDE.md    # Testing documentation
│
├── .github/workflows/       # CI/CD pipeline
│   └── ci-cd-pipeline.yml  # GitHub Actions workflow
│
├── docker-compose.yml       # Local development setup
├── start.sh                # Quick start script
└── README.md               # This file
```

## 🛠️ Technology Stack

### Backend
- **Flask**: Python web framework
- **PostgreSQL**: Primary database
- **SQLAlchemy**: ORM for database operations
- **Prometheus**: Metrics collection
- **Gunicorn**: WSGI server for production

### Frontend
- **React**: JavaScript framework
- **Axios**: HTTP client
- **Recharts**: Data visualization
- **React Router**: Client-side routing
- **Nginx**: Web server for production

### Infrastructure
- **Docker**: Containerization
- **Kubernetes**: Container orchestration
- **Prometheus**: Monitoring and alerting
- **Grafana**: Metrics visualization
- **GitHub Actions**: CI/CD pipeline

## 🚀 Quick Start

### Prerequisites
- Docker and Docker Compose
- Git
- Node.js (for frontend development)
- Python 3.11+ (for backend development)

### Option 1: Docker Compose (Recommended for Development)

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/smart-retail-app.git
   cd smart-retail-app
   ```

2. **Start the application**
   ```bash
   docker-compose up --build
   ```

3. **Access the application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:5000
   - API Health Check: http://localhost:5000/api/health
   - pgAdmin (optional): http://localhost:8080

### Option 2: Local Development

1. **Setup Backend**
   ```bash
   cd backend
   pip install -r requirements-dev.txt
   python app.py
   ```

2. **Setup Frontend**
   ```bash
   cd frontend
   npm install
   npm start
   ```

3. **Setup Database**
   ```bash
   # Start PostgreSQL (using Docker)
   docker run -d --name postgres \
     -e POSTGRES_DB=inventory_db \
     -e POSTGRES_USER=inventory_user \
     -e POSTGRES_PASSWORD=inventory_pass \
     -p 5432:5432 \
     postgres:15-alpine
   ```

## 📚 API Documentation

### Core Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/health` | Health check |
| GET | `/api/products` | Get all products |
| POST | `/api/products` | Create new product |
| GET | `/api/products/<id>` | Get specific product |
| PUT | `/api/products/<id>` | Update product |
| DELETE | `/api/products/<id>` | Delete product |
| POST | `/api/products/<id>/restock` | Restock product |
| GET | `/api/restocks` | Get restock history |
| GET | `/api/products/low-stock` | Get low stock products |
| GET | `/api/products/analytics` | Get analytics |

### Example Usage

```bash
# Create a product
curl -X POST http://localhost:5000/api/products \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Gaming Mouse",
    "sku": "GM001",
    "description": "High-performance gaming mouse",
    "stock_level": 50,
    "min_stock_threshold": 10,
    "price": 79.99
  }'

# Get all products
curl http://localhost:5000/api/products

# Get analytics
curl http://localhost:5000/api/products/analytics
```

## 🏭 Production Deployment

### Kubernetes Deployment

1. **Setup Kubernetes Cluster**
   ```bash
   # For local development
   minikube start
   minikube addons enable ingress
   
   # For production (EKS)
   # Follow AWS EKS setup guide
   ```

2. **Deploy Application**
   ```bash
   # Apply Kubernetes manifests
   kubectl apply -f k8s/configs/
   kubectl apply -f k8s/secrets/
   kubectl apply -f k8s/deployments/
   kubectl apply -f k8s/services/
   kubectl apply -f k8s/ingress/
   kubectl apply -f k8s/monitoring/
   ```

3. **Access the Application**
   ```bash
   # Get external IP
   kubectl get ingress
   
   # Access via external IP
   curl http://<external-ip>/api/health
   ```

### CI/CD Pipeline

The project includes a comprehensive CI/CD pipeline with:

- **Code Quality**: Linting and formatting checks
- **Testing**: Unit and integration tests
- **Security**: Vulnerability scanning
- **Building**: Docker image creation
- **Deployment**: Kubernetes deployment
- **Monitoring**: Health checks and metrics

To setup the CI/CD pipeline:

```bash
# Run the setup script
./scripts/setup-ci-cd.sh

# Configure GitHub secrets (see docs/github-secrets-template.txt)
# Push to main branch to trigger pipeline
```

## 📊 Monitoring

### Prometheus Metrics

The application exposes Prometheus metrics at `/metrics`:

- HTTP request rates and latencies
- Database connection health
- Business metrics (stock levels, restock operations)
- Custom application metrics

### Grafana Dashboards

Access Grafana dashboards for:

- Application performance metrics
- Database performance
- Business analytics
- System health monitoring

## 🧪 Testing

### Running Tests

```bash
# Backend tests
cd backend
pytest tests/ -v --cov=app

# Frontend tests
cd frontend
npm test

# Local pipeline test
./scripts/test-pipeline-local.sh
```

### Test Coverage

- Backend: Unit tests for all API endpoints
- Frontend: Component and integration tests
- E2E: API testing against live deployment
- Performance: Load testing with Locust

## 🔧 Development

### Code Quality

```bash
# Lint Python code
cd backend
flake8 .
black .
isort .

# Lint React code
cd frontend
npm run lint
```

### Adding New Features

1. Create feature branch
2. Implement changes
3. Add tests
4. Update documentation
5. Submit pull request

## 📖 Documentation

- **[Complete Guide](docs/COMPLETE_GUIDE.md)**: Comprehensive user guide
- **[CI/CD Setup Guide](docs/CI_CD_SETUP_GUIDE.md)**: Pipeline configuration
- **[Testing Guide](docs/TESTING_GUIDE.md)**: Testing strategies
- **[API Documentation](docs/README.md)**: Detailed API reference

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

- **Issues**: [GitHub Issues](https://github.com/your-username/smart-retail-app/issues)
- **Documentation**: [docs/](docs/)
- **Discussions**: [GitHub Discussions](https://github.com/your-username/smart-retail-app/discussions)

## 🏆 Acknowledgments

- Flask community for the excellent web framework
- React team for the powerful frontend library
- Kubernetes community for container orchestration
- Prometheus and Grafana for monitoring solutions

---

**Made with ❤️ for smart retail management** 