#!/bin/bash

# Setup script for E2E testing with Playwright
# This script installs all dependencies and prepares the environment

set -e

echo "🧪 Setting up E2E Testing Environment"
echo "======================================"

# Check if we're in the right directory
if [ ! -f "package.json" ]; then
    echo "❌ Error: package.json not found. Run this script from project root."
    exit 1
fi

# Install Node dependencies
echo ""
echo "📦 Installing Node.js dependencies..."
npm install

# Install Playwright
echo ""
echo "🎭 Installing Playwright..."
npm install -D @playwright/test

# Install Playwright browsers
echo ""
echo "🌐 Installing Playwright browsers..."
npx playwright install --with-deps

# Setup Python backend
echo ""
echo "🐍 Setting up Python backend..."
cd backend

if [ ! -d "venv" ]; then
    echo "  Creating Python virtual environment..."
    python3 -m venv venv
fi

echo "  Activating virtual environment..."
source venv/bin/activate

echo "  Installing Python dependencies..."
pip install -q -r requirements.txt

# Initialize test database
echo "  Initializing test database..."
python -c "from core.database import init_db; import asyncio; asyncio.run(init_db())" || true

cd ..

# Create test environment file
echo ""
echo "📝 Creating test environment configuration..."
cat > .env.test << EOF
# E2E Test Environment Configuration
API_BASE_URL=http://localhost:8000
FRONTEND_URL=http://localhost:3000
DATABASE_URL=sqlite:///./test_e2e.db
DEBUG=true
KEEP_WEBHOOK_SECRET=test-secret-e2e
BEDROCK_AGENTCORE_ENABLED=false
STRANDS_AGENTS_ENABLED=false
EOF

echo "  Created .env.test"

# Make test scripts executable
echo ""
echo "🔧 Making test scripts executable..."
chmod +x test-backend-locally.sh test-full-flow.sh test-keep-integration.sh || true

# Run Playwright codegen instructions
echo ""
echo "✅ E2E Testing Environment Setup Complete!"
echo ""
echo "📋 Next Steps:"
echo ""
echo "1. Run all tests:"
echo "   npx playwright test"
echo ""
echo "2. Run tests in headed mode (watch tests run):"
echo "   npx playwright test --headed"
echo ""
echo "3. Run specific test file:"
echo "   npx playwright test tests/e2e/api/health.spec.ts"
echo ""
echo "4. Run tests in specific browser:"
echo "   npx playwright test --project=chromium"
echo "   npx playwright test --project=firefox"
echo "   npx playwright test --project=webkit"
echo ""
echo "5. Open Playwright UI for debugging:"
echo "   npx playwright test --ui"
echo ""
echo "6. Generate test report:"
echo "   npx playwright show-report"
echo ""
echo "7. Record new tests with codegen:"
echo "   npx playwright codegen http://localhost:3000/frontend-demo.html"
echo ""
echo "📖 For more info, see: E2E_TESTING_GUIDE.md"

