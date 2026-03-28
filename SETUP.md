# Vinyl Aggregator - Setup & Development Guide

Quick reference for setting up and running the project locally.

## Prerequisites

- Docker & Docker Compose (recommended)
- OR PostgreSQL 15+ + Python 3.11+ + Node.js 18+

## Quick Start with Docker

```bash
# Start all services
docker-compose up -d

# Wait for services to be healthy (10-15 seconds)
docker-compose ps

# Check logs
docker-compose logs -f
```

Services will be available at:
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **PostgreSQL**: localhost:5432
- **Redis**: localhost:6379

## Manual Setup (Linux/Mac)

### 1. Start PostgreSQL & Redis

```bash
# Using Docker (if installed)
docker run -d --name vinyl_postgres -e POSTGRES_PASSWORD=password \
  -e POSTGRES_USER=user -e POSTGRES_DB=vinyl_aggregator -p 5432:5432 postgres:15

docker run -d --name vinyl_redis -p 6379:6379 redis:7
```

### 2. Setup Backend

```bash
cd backend

# Create virtual environment
python3.11 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env

# Run app
python main.py
```

Backend running at: http://localhost:8000

### 3. Setup Frontend

```bash
cd frontend

# Install dependencies
npm install

# Start dev server
npm run dev
```

Frontend running at: http://localhost:3000

## Testing the Integration

1. **Check Backend Health**: Visit http://localhost:8000/health
2. **View API Docs**: Visit http://localhost:8000/docs
3. **Try Search**: Go to http://localhost:3000 and search for a vinyl record
4. **Trigger Scrape**: `curl -X POST http://localhost:8000/api/stores/trigger-scrape`

## Database Verification

```bash
# Connect to PostgreSQL
psql -h localhost -U user -d vinyl_aggregator

# View tables
\dt

# Count records
SELECT COUNT(*) FROM records;
SELECT COUNT(*) FROM prices;

# View stores
SELECT * FROM stores;
```

## Common Issues

### Database Connection Failed
```bash
# Verify PostgreSQL is running
docker ps | grep postgres

# Or manually:
psql -h localhost -U user -d vinyl_aggregator

# If not running, start it:
docker run -d --name vinyl_postgres -e POSTGRES_PASSWORD=password \
  -p 5432:5432 postgres:15
```

### Frontend can't connect to backend
```bash
# Check backend is running
curl http://localhost:8000/health

# Check CORS is enabled
# Modify frontend vite.config.js proxy if needed
```

### No products in database
```bash
# Trigger a manual scrape
curl -X POST http://localhost:8000/api/stores/trigger-scrape

# Check scraper logs
# Or wait for scheduled job at 2 AM IST
```

## Development Workflow

```bash
# Terminal 1: Start Docker services
docker-compose up -d

# Terminal 2: Start backend
cd backend && python main.py

# Terminal 3: Start frontend
cd frontend && npm run dev

# Now you have full stack running at:
# - Frontend: http://localhost:3000
# - Backend: http://localhost:8000
# - Docs: http://localhost:8000/docs
```

## Useful Commands

```bash
# View backend logs
docker-compose logs -f postgres
docker-compose logs -f redis

# Stop all services
docker-compose down

# Rebuild services
docker-compose down && docker-compose up -d --build

# Run backend tests (if you add them)
cd backend && pytest

# Build frontend for production
cd frontend && npm run build

# Deploy frontend to Vercel
cd frontend && npm install -g vercel && vercel
```

## Environment Variables

### Backend (.env)
```
DATABASE_URL=postgresql://user:password@localhost:5432/vinyl_aggregator
REDIS_URL=redis://localhost:6379
DEBUG=True
```

### Frontend (.env.local) - Optional
```
VITE_API_BASE=http://localhost:8000
```

## Next Steps

1. ✅ Local development environment running
2. 🔄 Trigger manual scrape to populate database
3. 🔍 Search for records in frontend
4. 📊 Monitor scraping logs
5. 🚀 Add more stores to scrapers (see Phase 2 tasks)

## Resources

- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [React Docs](https://react.dev/)
- [Vite Docs](https://vitejs.dev/)
- [PostgreSQL Docs](https://www.postgresql.org/docs/)
- [BeautifulSoup Docs](https://www.crummy.com/software/BeautifulSoup/)

---

Need help? Check README.md for more detailed information.

