#!/bin/bash

# MSP Alert Intelligence Platform - Demo Setup Script
# This script sets up the demo environment with simulated AI agents

set -e

echo "🚀 Setting up MSP Alert Intelligence Platform (Demo Version)..."

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

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js 18+ first."
    exit 1
fi

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.11+ first."
    exit 1
fi

echo "✅ Prerequisites check passed"

# Create environment file if it doesn't exist
if [ ! -f .env ]; then
    echo "📝 Creating environment file..."
    cp env.example .env
    echo "⚠️  Demo mode: Using simulated AI agents (no AWS credentials required)"
fi

# Setup backend with demo mode
echo "🐍 Setting up Python backend (Demo Mode)..."
cd backend
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi
source venv/bin/activate

# Install core dependencies only
echo "📦 Installing core dependencies..."
pip install --upgrade pip
pip install fastapi uvicorn sqlalchemy sqlmodel alembic psycopg2-binary redis python-dotenv pyyaml

# Install optional dependencies if available
echo "📦 Installing optional dependencies..."
pip install boto3 botocore || echo "⚠️  AWS SDK not available (demo mode)"
pip install openai anthropic || echo "⚠️  AI SDKs not available (demo mode)"
pip install prometheus-client structlog || echo "⚠️  Monitoring not available (demo mode)"

cd ..

# Setup frontend
echo "⚛️  Setting up React frontend..."
cd frontend
npm install
cd ..

# Create demo data
echo "📊 Creating demo configuration..."
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

echo "✅ Demo setup completed successfully!"
echo ""
echo "🎯 Demo Features:"
echo "- ✅ Alert Management (CRUD operations)"
echo "- ✅ Real-time Dashboard"
echo "- ✅ Simulated AI Agents (Bedrock AgentCore & Strands)"
echo "- ✅ YAML Workflows"
echo "- ✅ Noise Reduction Simulation"
echo "- ✅ Alert Correlation Simulation"
echo "- ✅ Responsive UI"
echo ""
echo "🚀 Next steps:"
echo "1. Run 'docker-compose up -d' to start all services"
echo "2. Access the application at http://localhost"
echo "3. Access Grafana at http://localhost:3001 (admin/admin)"
echo "4. Access Prometheus at http://localhost:9090"
echo ""
echo "📝 Note: This is a demo version with simulated AI agents."
echo "   For production, configure AWS credentials and real AI services."
echo ""
echo "🔧 Development commands:"
echo "- Backend: cd backend && source venv/bin/activate && python main.py"
echo "- Frontend: cd frontend && npm run dev"
echo "- Tests: npm run test:e2e"
