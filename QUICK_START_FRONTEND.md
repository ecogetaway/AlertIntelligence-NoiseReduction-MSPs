# Quick Start - Frontend Only

## Option 1: Run Frontend Locally (Fastest)

```bash
# Install dependencies
cd /Users/sanjay/msp-alert-app/frontend
npm install

# Start development server
NEXT_PUBLIC_API_URL=http://localhost:8000 npm run dev
```

**Frontend will be available at:** http://localhost:3000

**Note:** Backend must be running separately on port 8000 for API calls to work.

## Option 2: Run with Docker Compose

```bash
cd /Users/sanjay/msp-alert-app

# Start both frontend and backend
docker compose up --build frontend backend

# Or run in detached mode
docker compose up -d --build frontend backend
```

**Links:**
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

## Troubleshooting

### Port 3000 already in use
```bash
# Find and kill process on port 3000
lsof -i :3000
kill -9 <PID>

# Or use alternative port
NEXT_PUBLIC_API_URL=http://localhost:8000 npm run dev -- -p 3001
```

### Blank page / Module not found errors
```bash
# Clean install
cd /Users/sanjay/msp-alert-app/frontend
rm -rf node_modules .next
npm install
npm run dev
```

### Docker issues
```bash
# Stop all containers
docker compose down

# Remove volumes and rebuild
docker compose down -v
docker compose up --build frontend backend
```

## Development Commands

```bash
# Type checking
npm run type-check

# Linting
npm run lint

# Build for production
npm run build

# Run production build
npm run start
```

## Backend Setup (Required)

The frontend needs the backend API running. Quick backend start:

```bash
cd /Users/sanjay/msp-alert-app/backend
python main.py
```

Or use Docker:
```bash
docker compose up backend postgres redis
```

