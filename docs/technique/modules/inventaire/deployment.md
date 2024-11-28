# Configuration et Déploiement du Module Inventaire

## Configuration

### Variables d'environnement

```bash
# Base de données
INVENTORY_DB_HOST=localhost
INVENTORY_DB_PORT=5432
INVENTORY_DB_NAME=inventory
INVENTORY_DB_USER=inventory_user
INVENTORY_DB_PASSWORD=secret

# Cache Redis
INVENTORY_REDIS_HOST=localhost
INVENTORY_REDIS_PORT=6379
INVENTORY_REDIS_DB=0

# ML Service
INVENTORY_ML_HOST=localhost
INVENTORY_ML_PORT=8000
INVENTORY_ML_API_KEY=secret

# IoT Service
INVENTORY_IOT_HOST=localhost
INVENTORY_IOT_PORT=8001
INVENTORY_IOT_API_KEY=secret
```

### Configuration application

```python
class InventoryConfig:
    """Configuration du module inventaire"""
    
    # Cache
    CACHE_TTL = 300  # 5 minutes
    CACHE_PREFIX = "inventory:"
    
    # Batch
    BATCH_SIZE = 1000
    MAX_WORKERS = 4
    
    # ML
    ML_UPDATE_INTERVAL = 3600  # 1 heure
    ML_CONFIDENCE_THRESHOLD = 0.95
    
    # IoT
    IOT_POLLING_INTERVAL = 60  # 1 minute
    IOT_ALERT_THRESHOLD = 0.8
```

## Déploiement

### Docker

```dockerfile
FROM python:3.11-slim

# Installation dépendances
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copie application
COPY . /app
WORKDIR /app

# Configuration
ENV PYTHONPATH=/app
ENV INVENTORY_CONFIG=/app/config/production.py

# Démarrage
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Docker Compose

```yaml
version: '3.8'

services:
  inventory-api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - INVENTORY_DB_HOST=db
      - INVENTORY_REDIS_HOST=redis
    depends_on:
      - db
      - redis
      
  inventory-ml:
    build: ./ml
    ports:
      - "8001:8000"
    volumes:
      - ./models:/app/models
      
  db:
    image: postgres:14
    environment:
      - POSTGRES_DB=inventory
      - POSTGRES_USER=inventory_user
      - POSTGRES_PASSWORD=secret
      
  redis:
    image: redis:7
```

## Infrastructure

### Kubernetes

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: inventory-api
spec:
  replicas: 3
  selector:
    matchLabels:
      app: inventory-api
  template:
    metadata:
      labels:
        app: inventory-api
    spec:
      containers:
      - name: inventory-api
        image: inventory-api:latest
        ports:
        - containerPort: 8000
        env:
        - name: INVENTORY_DB_HOST
          valueFrom:
            configMapKeyRef:
              name: inventory-config
              key: db_host
```

### Monitoring

```yaml
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: inventory-monitor
spec:
  selector:
    matchLabels:
      app: inventory-api
  endpoints:
  - port: metrics
```

## CI/CD

### GitHub Actions

```yaml
name: Inventory CI/CD

on:
  push:
    branches: [ main ]
    paths:
      - 'inventory/**'
      
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run tests
        run: |
          pip install -r requirements.txt
          pytest tests/
          
  deploy:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - name: Deploy to production
        run: |
          kubectl apply -f k8s/
```

## Points d'attention

### Sécurité
- Secrets sécurisés
- HTTPS/TLS
- Network policies
- RBAC

### Performance
- Autoscaling
- Cache distribué
- Load balancing
- CDN

### Monitoring
- Métriques
- Logs
- Alertes
- Dashboards

### Maintenance
- Backups
- Updates
- Rollback
- Documentation
