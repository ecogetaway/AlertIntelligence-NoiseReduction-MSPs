.PHONY: help demo demo-backend demo-full test clean install

help:
	@echo "MSP Alert Intelligence Platform - Commands"
	@echo "=========================================="
	@echo "make demo        - Run frontend demo"
	@echo "make demo-backend - Run backend demo"
	@echo "make demo-full   - Run both frontend and backend"
	@echo "make install     - Install dependencies"
	@echo "make test        - Run tests"
	@echo "make clean       - Clean up resources"

demo:
	@echo "Starting frontend demo..."
	./start-demo-safe.sh

demo-backend:
	@echo "Starting backend demo..."
	./start-demo.sh

demo-full:
	@echo "Starting full demo (backend + frontend)..."
	cd backend && source venv/bin/activate && python demo_main.py &
	sleep 3
	python3 -m http.server 3000

install:
	@echo "Installing dependencies..."
	cd backend && python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt
	cd frontend && npm install
	@echo "Dependencies installed successfully!"

test:
	@echo "Running tests..."
	cd tests && npx playwright test

test-e2e:
	@echo "Running E2E tests with UI..."
	cd tests && npx playwright test --ui

clean:
	@echo "Cleaning up..."
	pkill -f "python demo_main.py" || true
	pkill -f "http.server" || true
	rm -rf backend/__pycache__ backend/venv
	rm -rf frontend/node_modules frontend/build
	rm -rf tests/test-results
	@echo "Cleanup complete!"

setup:
	@echo "Setting up MSP Alert Intelligence Platform..."
	make install
	@echo "Copying environment file..."
	cp env.example .env
	@echo "Setup complete! Edit .env with your configuration."

status:
	@echo "Checking system status..."
	@echo "Backend processes:"
	@pgrep -f "python demo_main.py" && echo "✓ Backend running" || echo "✗ Backend not running"
	@echo "HTTP servers:"
	@pgrep -f "http.server" && echo "✓ HTTP server running" || echo "✗ HTTP server not running"
	@echo "WebSocket connections:"
	@curl -s http://localhost:8000/api/v1/processing/stats 2>/dev/null | grep -o '"websocket_connections":[0-9]*' || echo "Backend not accessible"

logs:
	@echo "Showing backend logs..."
	@tail -f backend/logs/app.log 2>/dev/null || echo "No log file found"

restart:
	@echo "Restarting services..."
	make clean
	sleep 2
	make demo-full
