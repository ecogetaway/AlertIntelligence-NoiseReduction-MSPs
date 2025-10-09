#!/bin/bash

# MSP Alert Intelligence Platform - Simple Demo Setup
# This script sets up a minimal demo environment

set -e

echo "🚀 Setting up MSP Alert Intelligence Platform (Simple Demo)..."

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

echo "✅ Prerequisites check passed"

# Create environment file if it doesn't exist
if [ ! -f .env ]; then
    echo "📝 Creating environment file..."
    cp env.example .env
    echo "⚠️  Demo mode: Using simulated AI agents (no AWS credentials required)"
fi

# Setup backend with minimal dependencies
echo "🐍 Setting up Python backend (Minimal Setup)..."
cd backend
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi
source venv/bin/activate

# Install only essential dependencies
echo "📦 Installing essential dependencies..."
pip install --upgrade pip
pip install fastapi uvicorn sqlalchemy sqlmodel python-dotenv pyyaml

# Install optional dependencies if available
echo "📦 Installing optional dependencies..."
pip install boto3 botocore || echo "⚠️  AWS SDK not available (demo mode)"
pip install redis || echo "⚠️  Redis not available (demo mode)"
pip install psycopg2-binary || echo "⚠️  PostgreSQL not available (demo mode)"

cd ..

# Setup frontend with legacy peer deps
echo "⚛️  Setting up React frontend (with legacy peer deps)..."
cd frontend

# Clean any existing node_modules
rm -rf node_modules package-lock.json

# Install with legacy peer deps to resolve conflicts
npm install --legacy-peer-deps || {
    echo "⚠️  npm install failed, trying with --force..."
    npm install --force || {
        echo "⚠️  Frontend setup failed, but backend will still work"
        cd ..
        echo "✅ Backend setup completed"
        echo "⚠️  Frontend setup had issues, but you can still run the backend"
        echo "🚀 To start backend only: cd backend && source venv/bin/activate && python main.py"
        exit 0
    }
}

cd ..

# Create basic configuration files
echo "📊 Creating configuration files..."
mkdir -p monitoring/grafana/dashboards
mkdir -p monitoring/grafana/datasources
mkdir -p nginx/ssl

# Create basic nginx configuration
cat > nginx/nginx.conf << 'EOF'
events {
    worker_connections 1024;
}

http {
    upstream backend {
        server backend:8000;
    }
    
    upstream frontend {
        server frontend:3000;
    }
    
    server {
        listen 80;
        server_name localhost;
        
        location /api/ {
            proxy_pass http://backend;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
        }
        
        location / {
            proxy_pass http://frontend;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
        }
    }
}
EOF

# Create Prometheus configuration
cat > monitoring/prometheus.yml << 'EOF'
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'msp-alert-backend'
    static_configs:
      - targets: ['backend:8000']
    metrics_path: '/metrics'
    scrape_interval: 30s
EOF

# Create Grafana datasource configuration
cat > monitoring/grafana/datasources/prometheus.yml << 'EOF'
apiVersion: 1

datasources:
  - name: Prometheus
    type: prometheus
    access: proxy
    url: http://prometheus:9090
    isDefault: true
EOF

echo "✅ Simple demo setup completed!"
echo ""
echo "🎯 What's Working:"
echo "- ✅ Backend API (Python FastAPI)"
echo "- ✅ Simulated AI Agents"
echo "- ✅ Database models and services"
echo "- ✅ Docker configuration"
echo ""
echo "🚀 Next steps:"
echo "1. Run 'docker-compose up -d' to start services"
echo "2. Backend API will be available at http://localhost:8000"
echo "3. API docs at http://localhost:8000/docs"
echo ""
echo "🔧 Manual frontend setup (if needed):"
echo "cd frontend && npm install --legacy-peer-deps && npm run dev"
echo ""
echo "📝 Note: This is a minimal demo setup focusing on backend functionality."
