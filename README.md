# Inventory Management System

A comprehensive inventory management system for retail store chains built with Flask, PostgreSQL, and Docker.

## Features

- **Real-time Stock Tracking**: Monitor inventory levels across all products
- **Low Stock Alerts**: Automatic notifications when items fall below threshold
- **Restocking Management**: Easy restocking operations with full audit trail
- **Analytics Dashboard**: Stock trends and analytics for better decision making
- **RESTful API**: Complete REST API for all operations
- **Containerized Deployment**: Docker-based deployment for easy scaling

## Technology Stack

- **Backend**: Flask (Python)
- **Database**: PostgreSQL
- **Containerization**: Docker & Docker Compose
- **API**: RESTful endpoints with JSON responses

## Prerequisites

- Docker and Docker Compose installed
- Git (for cloning the repository)
- curl or Postman (for testing API endpoints)

## Quick Start

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd inventory-management-system
   ```

2. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env file with your preferred settings
   ```

3. **Build and start the application**
   ```bash
   docker-compose up --build
   ```

4. **Access the application**
   - API: http://localhost:5000
   - pgAdmin (optional): http://localhost:8080
   - Health Check: http://localhost:5000/api/health

## API Endpoints

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

## API Usage Examples

### Create a New Product
```bash
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
```

### Restock a Product
```bash
curl -X POST http://localhost:5000/api/products/1/restock \
  -H "Content-Type: application/json" \
  -d '{
    "quantity": 25,
    "notes": "Weekly restock delivery"
  }'
```

### Get Low Stock Products
```bash
curl http://localhost:5000/api/products/low-stock
```

### Get Analytics
```bash
curl http://localhost:5000/api/products/analytics
```

## Database Schema

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

## Development

### Running in Development Mode

1. **Start services**
   ```bash
   docker-compose up
   ```

2. **View logs**
   ```bash
   docker-compose logs -f backend
   ```

3. **Access database**
   - Use pgAdmin at http://localhost:8080
   - Login: admin@inventory.com / admin123
   - Or connect directly: localhost:5432

### Code Structure

```
inventory-management-system/
├── app.py                 # Flask application
├── requirements.txt       # Python dependencies
├── Dockerfile            # Backend container
├── docker-compose.yml    # Multi-container setup
├── init.sql             # Database initialization
├── .env.example         # Environment variables template
└── README.md           # This file
```

### Making Changes

1. **Backend changes**: Modify `app.py` and restart container
2. **Database changes**: Update `init.sql` and recreate containers
3. **Dependencies**: Update `requirements.txt` and rebuild image

## Production Deployment

### Security Considerations

1. **Change default passwords** in `.env` file
2. **Use HTTPS** in production
3. **Set up proper firewall** rules
4. **Enable authentication** for API endpoints
5. **Use secrets management** for sensitive data

### Scaling

- **Horizontal scaling**: Add more backend containers
- **Database scaling**: Use PostgreSQL replicas
- **Load balancing**: Add nginx or similar load balancer
- **Monitoring**: Add logging and monitoring tools

### Environment Variables for Production

```bash
FLASK_ENV=production
FLASK_DEBUG=false
DATABASE_URL=postgresql://user:pass@prod-db:5432/inventory
SECRET_KEY=your-super-secret-production-key
```

## Troubleshooting

### Common Issues

1. **Database connection failed**
   - Check if PostgreSQL container is running
   - Verify DATABASE_URL in environment variables

2. **Port already in use**
   - Change port mapping in docker-compose.yml
   - Or stop conflicting services

3. **Container build fails**
   - Ensure Docker has enough resources
   - Check Dockerfile syntax

### Useful Commands

```bash
# View running containers
docker-compose ps

# Stop all services
docker-compose down

# Rebuild containers
docker-compose up --build

# View backend logs
docker-compose logs -f backend

# View database logs
docker-compose logs -f db

# Execute commands in running container
docker-compose exec backend bash
docker-compose exec db psql -U inventory_user -d inventory_db

# Clean up (remove containers and volumes)
docker-compose down -v

# Reset database (remove volume and restart)
docker-compose down -v db
docker-compose up db
```

## Testing

### Manual Testing

Test all endpoints to ensure functionality:

```bash
# Health check
curl http://localhost:5000/api/health

# Get all products
curl http://localhost:5000/api/products

# Create product
curl -X POST http://localhost:5000/api/products \
  -H "Content-Type: application/json" \
  -d '{"name": "Test Product", "sku": "TEST001", "stock_level": 100}'

# Update product
curl -X PUT http://localhost:5000/api/products/1 \
  -H "Content-Type: application/json" \
  -d '{"stock_level": 75}'

# Restock product
curl -X POST http://localhost:5000/api/products/1/restock \
  -H "Content-Type: application/json" \
  -d '{"quantity": 25}'

# Check low stock
curl http://localhost:5000/api/products/low-stock

# Get analytics
curl http://localhost:5000/api/products/analytics
```

## Monitoring and Maintenance

### Health Checks

The application includes built-in health checks:
- Backend: `/api/health`
- Database: PostgreSQL health check in docker-compose

### Backup Strategy

```bash
# Backup database
docker-compose exec db pg_dump -U inventory_user inventory_db > backup.sql

# Restore database
docker-compose exec -T db psql -U inventory_user inventory_db < backup.sql
```

### Log Management

Logs are available through Docker Compose:
```bash
# View all logs
docker-compose logs

# Follow specific service logs
docker-compose logs -f backend
docker-compose logs -f db
```

## API Response Examples

### Successful Product Creation
```json
{
  "success": true,
  "message": "Product created successfully",
  "product": {
    "id": 1,
    "name": "Gaming Mouse",
    "sku": "GM001",
    "description": "High-performance gaming mouse",
    "stock_level": 50,
    "min_stock_threshold": 10,
    "price": 79.99,
    "created_at": "2025-06-03T10:30:00",
    "updated_at": "2025-06-03T10:30:00",
    "is_low_stock": false
  }
}
```

### Low Stock Alert Response
```json
{
  "success": true,
  "low_stock_products": [
    {
      "id": 3,
      "name": "Office Chair",
      "sku": "CHR001",
      "stock_level": 2,
      "min_stock_threshold": 3,
      "is_low_stock": true
    }
  ],
  "count": 1
}
```

### Analytics Response
```json
{
  "success": true,
  "analytics": {
    "total_products": 10,
    "low_stock_count": 2,
    "out_of_stock_count": 0,
    "total_stock_value": 25847.50,
    "recent_restocks_30_days": 15,
    "low_stock_percentage": 20.0,
    "top_stock_products": [
      {
        "name": "USB-C Cable",
        "sku": "CBL001",
        "stock_level": 200
      }
    ]
  }
}
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-feature`)
3. Make your changes
4. Test thoroughly
5. Commit your changes (`git commit -am 'Add new feature'`)
6. Push to the branch (`git push origin feature/new-feature`)
7. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support and questions:
- Create an issue in the GitHub repository
- Check the troubleshooting section above
- Review Docker and Flask documentation

---

**Note**: This is a development setup. For production deployment, additional security measures, monitoring, and performance optimizations should be implemented.