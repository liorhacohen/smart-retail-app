# Inventory Management System

A comprehensive inventory management system for retail store chains built with Flask, PostgreSQL, Docker, and Kubernetes.

## Features

- **Real-time Stock Tracking**: Monitor inventory levels across all products
- **Low Stock Alerts**: Automatic notifications when items fall below threshold
- **Restocking Management**: Easy restocking operations with full audit trail
- **Analytics Dashboard**: Stock trends and analytics for better decision making
- **RESTful API**: Complete REST API for all operations
- **Containerized Deployment**: Docker & Kubernetes deployment for production scaling
- **High Availability**: Multiple replicas and health checks

## Technology Stack

- **Backend**: Flask (Python)
- **Database**: PostgreSQL
- **Containerization**: Docker & Docker Compose
- **Orchestration**: Kubernetes (Minikube/EKS)
- **API**: RESTful endpoints with JSON responses

## Deployment Options

### Option 1: Local Development (Docker Compose)
### Option 2: Production-Ready (Kubernetes)

---

## 🚀 Quick Start - Docker Compose (Development)

### Prerequisites
- Docker and Docker Compose installed
- Git (for cloning the repository)
- curl or Postman (for testing API endpoints)

### Steps

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd inventory-management-system
   ```

2. **Build and start the application**
   ```bash
   docker-compose up --build
   ```

3. **Access the application**
   - API: http://localhost:5000
   - pgAdmin (optional): http://localhost:8080
   - Health Check: http://localhost:5000/api/health

---

## ⚙️ Production Deployment - Kubernetes

### Prerequisites
- **macOS**: 
  ```bash
  brew install minikube kubectl docker
  ```
- **Linux/Windows**: Install Docker Desktop, Minikube, kubectl
- Docker Hub account (for storing images)

### Step 1: Build and Push Docker Image

```bash
# Build the image
docker buildx build -t your-username/smart-retail-app:latest .

# Login to Docker Hub
docker login

# Push to Docker Hub
docker push your-username/smart-retail-app:latest
```

### Step 2: Start Kubernetes Cluster

```bash
# Start Minikube
minikube start

# Enable Ingress
minikube addons enable ingress

# Verify cluster is running
kubectl get nodes
```

### Step 3: Deploy to Kubernetes

```bash
# Navigate to k8s directory
cd k8s

# Deploy all components (order matters!)
kubectl apply -f configs/configmap.yaml
kubectl apply -f secrets/secrets.yaml
kubectl apply -f deployments/postgres-deployment.yaml

# Wait for PostgreSQL to be ready
kubectl get pods -w
# Wait until postgres pod shows "1/1 Running"

# Deploy services and backend
kubectl apply -f services/services.yaml
kubectl apply -f deployments/flask-deployment.yaml
kubectl apply -f ingress/ingress.yaml
```

### Step 4: Access the Application

```bash
# Start tunnel for external access
minikube tunnel
# Keep this terminal open!

# In a new terminal, test the API
curl http://localhost/api/health
curl http://localhost/api/products
```

### Step 5: Create Test Data

```bash
# Create a product
curl -X POST http://localhost/api/products \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test Product",
    "sku": "TEST-001",
    "stock_level": 50,
    "price": 29.99
  }'

# View analytics
curl http://localhost/api/products/analytics
```

---

## 📁 Project Structure

```
inventory-management-system/
├── app.py                    # Flask application
├── requirements.txt          # Python dependencies
├── Dockerfile               # Container configuration
├── docker-compose.yml       # Development setup
├── init.sql                # Database initialization
├── k8s/                    # Kubernetes manifests
│   ├── configs/
│   │   └── configmap.yaml
│   ├── secrets/
│   │   └── secrets.yaml
│   ├── deployments/
│   │   ├── flask-deployment.yaml
│   │   └── postgres-deployment.yaml
│   ├── services/
│   │   └── services.yaml
│   └── ingress/
│       └── ingress.yaml
├── test_api.py             # API testing script
└── README.md               # This file
```

---

## 🔧 API Endpoints

### Inventory Management

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/products` | Get all products with stock levels |
| GET | `/api/products/<id>` | Get specific product details |
| POST | `/api/products` | Add new product |
| PUT | `/api/products/<id>` | Update product details |
| DELETE | `/api/products/<id>` | Delete product |

### Restocking Operations

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/products/<id>/restock` | Restock specific product |
| GET | `/api/restocks` | Get restocking history |

### Analytics

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/products/low-stock` | Get low stock products |
| GET | `/api/products/analytics` | Get stock analytics |

---

## 📊 API Usage Examples

### Create a New Product
```bash
curl -X POST http://localhost/api/products \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Gaming Mouse",
    "sku": "GM001",
    "description": "High-performance gaming mouse",
    "stock_level": 50,
    "min_stock_threshold": 10,
    "price": 79.99
  }'
```

### Restock a Product
```bash
curl -X POST http://localhost/api/products/1/restock \
  -H "Content-Type: application/json" \
  -d '{
    "quantity": 25,
    "notes": "Weekly restock delivery"
  }'
```

### Get Low Stock Products
```bash
curl http://localhost/api/products/low-stock
```

### Get Analytics
```bash
curl http://localhost/api/products/analytics
```

---

## 🗄️ Database Schema

### Products Table
- `id`: Primary key
- `name`: Product name
- `sku`: Stock keeping unit (unique)
- `description`: Product description
- `stock_level`: Current stock quantity
- `min_stock_threshold`: Low stock alert threshold
- `price`: Product price
- `created_at`: Creation timestamp
- `updated_at`: Last update timestamp

### Restock Logs Table
- `id`: Primary key
- `product_id`: Foreign key to products
- `quantity_added`: Amount restocked
- `previous_stock`: Stock level before restock
- `new_stock`: Stock level after restock
- `restocked_at`: Restock timestamp
- `notes`: Optional notes

---

## 🔍 Troubleshooting

### Docker Compose Issues

1. **Port already in use**
   ```bash
   docker-compose down
   # Change ports in docker-compose.yml if needed
   ```

2. **Database connection failed**
   ```bash
   docker-compose logs db
   docker-compose restart db
   ```

### Kubernetes Issues

1. **Pods not starting**
   ```bash
   kubectl get pods
   kubectl describe pod <pod-name>
   kubectl logs <pod-name>
   ```

2. **Cannot access application**
   ```bash
   # Check if tunnel is running
   minikube tunnel
   
   # Check ingress status
   kubectl get ingress
   
   # Alternative: use port-forward
   kubectl port-forward svc/flask-service 5000:5000
   # Then access: http://localhost:5000
   ```

3. **Image pull errors**
   ```bash
   # Make sure image exists on Docker Hub
   docker pull your-username/smart-retail-app:latest
   
   # Update deployment with correct image name
   kubectl set image deployment/flask-deployment flask-backend=your-username/smart-retail-app:latest
   ```

### Useful Commands

#### Docker Compose
```bash
# View running containers
docker-compose ps

# View logs
docker-compose logs -f backend

# Clean restart
docker-compose down -v
docker-compose up --build
```

#### Kubernetes
```bash
# View all resources
kubectl get all

# View pod details
kubectl describe pod <pod-name>

# View logs
kubectl logs -f deployment/flask-deployment

# Delete all resources
kubectl delete -f k8s/

# Reset Minikube
minikube delete
minikube start
```

---

## 🧪 Testing

### Automated Testing
```bash
# Run the included test script
python3 test_api.py
```

### Manual Testing
```bash
# Health check
curl http://localhost/api/health

# Create and test products
curl -X POST http://localhost/api/products \
  -H "Content-Type: application/json" \
  -d '{"name": "Test Product", "sku": "TEST001", "stock_level": 100}'

# Check analytics
curl http://localhost/api/products/analytics
```

---

## 🚀 For Your Project Partner

### Quick Setup Instructions

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd inventory-management-system
   ```

2. **Choose deployment method:**

   **Option A: Simple Docker Setup**
   ```bash
   docker-compose up --build
   # Access: http://localhost:5000
   ```

   **Option B: Full Kubernetes Setup**
   ```bash
   # Install prerequisites (macOS)
   brew install minikube kubectl docker
   
   # Start Kubernetes
   minikube start
   minikube addons enable ingress
   
   # Deploy application
   cd k8s
   kubectl apply -f configs/
   kubectl apply -f secrets/
   kubectl apply -f deployments/postgres-deployment.yaml
   # Wait for postgres...
   kubectl apply -f services/
   kubectl apply -f deployments/flask-deployment.yaml
   kubectl apply -f ingress/
   
   # Access application
   minikube tunnel  # Keep running
   # Test: curl http://localhost/api/health
   ```

3. **Test the API**
   ```bash
   python3 test_api.py
   ```

---

## 📝 Environment Variables

### Docker Compose
Variables are set in `docker-compose.yml` - no additional setup needed.

### Kubernetes
Configured via ConfigMaps and Secrets:
- **ConfigMap**: `inventory-config` (non-sensitive settings)
- **Secret**: `inventory-secrets` (passwords)

---

## 🔐 Security Considerations

### Development
- Default passwords are used (fine for development)
- No authentication required
- All traffic is HTTP

### Production Recommendations
1. **Change default passwords** in secrets
2. **Enable HTTPS** with proper certificates
3. **Add API authentication** (JWT tokens)
4. **Set up proper firewall** rules
5. **Use managed databases** (AWS RDS, Google Cloud SQL)
6. **Implement monitoring** (Prometheus, Grafana)

---

## 📈 Monitoring and Maintenance

### Health Checks
- **Backend**: `/api/health`
- **Database**: Built-in PostgreSQL health checks
- **Kubernetes**: Liveness and readiness probes

### Backup Strategy
```bash
# Docker Compose
docker-compose exec db pg_dump -U inventory_user inventory_db > backup.sql

# Kubernetes
kubectl exec deployment/postgres-deployment -- pg_dump -U inventory_user inventory_db > backup.sql
```

---

## 🎯 Next Steps (Optional Enhancements)

1. **Monitoring**: Add Prometheus + Grafana
2. **CI/CD**: GitHub Actions pipeline
3. **Frontend**: React dashboard
4. **Authentication**: JWT-based API security
5. **Cloud Deployment**: AWS EKS, Google GKE
6. **Load Testing**: Stress testing with k6

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-feature`)
3. Make your changes
4. Test thoroughly (both Docker and Kubernetes)
5. Commit your changes (`git commit -am 'Add new feature'`)
6. Push to the branch (`git push origin feature/new-feature`)
7. Create a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## 🆘 Support

For questions and support:
- Create an issue in the GitHub repository
- Check the troubleshooting section above
- Review Docker and Kubernetes documentation

**Happy coding! 🎉**