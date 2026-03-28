# Quick Reference - Vinyl Aggregator Developer Guide

Fast lookup for common tasks and commands.

## 🚀 Quick Start

```bash
# Start all services (requires Docker)
docker-compose up -d

# Terminal 1: Backend
cd backend && python main.py

# Terminal 2: Frontend
cd frontend && npm run dev

# URLs
# Frontend: http://localhost:3000
# API: http://localhost:8000
# Docs: http://localhost:8000/docs
```

## 📦 Backend Commands

```bash
# Setup
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Run
python main.py

# Tests (when added)
pytest tests/

# Database
psql -h localhost -U user vinyl_aggregator
```

## 🎨 Frontend Commands

```bash
# Setup
cd frontend
npm install

# Development
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview

# Lint
npm run lint
```

## 🛠️ Common API Calls

```bash
# Search
curl "http://localhost:8000/api/search?q=Beatles"

# Get record
curl "http://localhost:8000/api/records/1"

# List stores
curl "http://localhost:8000/api/stores"

# Trigger scrape
curl -X POST "http://localhost:8000/api/stores/trigger-scrape"

# Health check
curl "http://localhost:8000/health"

# API docs
open http://localhost:8000/docs
```

## 🗄️ Database Queries

```sql
-- Connect to database
psql -h localhost -U user -d vinyl_aggregator

-- View tables
\dt

-- Count records
SELECT COUNT(*) FROM records;    -- Total products
SELECT COUNT(*) FROM prices;     -- Total prices
SELECT COUNT(*) FROM stores;     -- Total stores

-- Find records
SELECT * FROM records WHERE artist LIKE 'Beatles%' LIMIT 5;

-- View prices for a record
SELECT p.*, s.name FROM prices p JOIN stores s ON p.store_id = s.id 
WHERE p.record_id = 1;

-- Check stores
SELECT * FROM stores;

-- Last scrape time
SELECT store_id, MAX(last_updated) FROM prices GROUP BY store_id;

-- Reset database (careful!)
DROP TABLE IF EXISTS prices;
DROP TABLE IF EXISTS records;
DROP TABLE IF EXISTS stores;
```

## 🔍 Debugging

### Backend
```python
# Enable debug logging in config.py
DEBUG=True

# Test database connection
from database import test_db_connection
test_db_connection()

# Test scraper
from scrapers.disccenter import DiscCenterScraper
scraper = DiscCenterScraper()
products = scraper.scrape()
print(f"Scraped {len(products)} products")
```

### Frontend
```javascript
// Open DevTools: F12 or Cmd+Opt+I
// Console: View API calls and errors
// Network: Monitor requests to backend
// Storage: Check localStorage for any cached data

// Check API client
import { searchAPI } from '@/services/api'
searchAPI.search('Beatles').then(console.log)
```

## 📝 Code Structure Cheat Sheet

### Adding a New Scraper

1. Create `backend/scrapers/newstore.py`:
   ```python
   from .base import BaseScraper
   
   class NewStoreScraper(BaseScraper):
       def __init__(self):
           config = {"name": "Store", "base_url": "..."}
           super().__init__("store_key", "url", config)
       
       def scrape(self):
           # Implementation
           return products
   ```

2. Register in `backend/services/scheduler.py` (in `scrape_all_stores`)

3. Add store config entry in `backend/config.py` (STORE_CONFIGS dict)

4. Update database by running scraper

### Adding a New API Endpoint

1. Create method in `backend/routes/routename.py`:
   ```python
   from fastapi import APIRouter, Depends
   from database import get_db
   
   router = APIRouter(prefix="/api/name")
   
   @router.get("/endpoint")
   def my_endpoint(db: Session = Depends(get_db)):
       # Implementation
       return result
   ```

2. Include router in `backend/main.py`:
   ```python
   from routes import my_router
   app.include_router(my_router)
   ```

### Adding a New React Component

1. Create `frontend/src/components/MyComponent.jsx`:
   ```jsx
   import React from 'react'
   
   export const MyComponent = ({ props }) => {
     return <div>Component</div>
   }
   
   export default MyComponent
   ```

2. Import and use in `App.jsx` or another component

## 🚨 Troubleshooting

| Problem | Solution |
|---------|----------|
| `ModuleNotFoundError` | Run `pip install -r requirements.txt` |
| `npm ERR!` | Run `npm install` in frontend/ |
| `psql: connection refused` | Start PostgreSQL: `docker-compose up -d postgres` |
| API 404 errors | Check endpoint path in browser/postman |
| CORS errors | Verify CORS origins in `config.py` |
| Scraper finds 0 products | CSS selectors may have changed, update in scraper code |
| Frontend shows loading forever | Check browser console for API errors (F12) |
| Database doesn't exist | Run `python main.py` (creates tables) |

## 📊 Performance Monitoring

```bash
# Monitor backend
docker logs -f vinyl_backend

# Monitor database
psql -U user -d vinyl_aggregator
SELECT * FROM pg_stat_statements ORDER BY total_time DESC LIMIT 10;

# Monitor frontend bundle size
cd frontend && npm run build
# Check dist/ folder size

# Test search performance
curl "http://localhost:8000/api/search?q=test" -w "\nTime: %{time_total}s\n"
```

## 🔐 Security Checklist

- [ ] `.env` file never committed (in .gitignore)
- [ ] DATABASE_URL never exposed in Frontend
- [ ] API keys stored in environment variables only
- [ ] CORS origins restricted (not `*`)
- [ ] Input validation on all API endpoints (Pydantic)
- [ ] SQL injection prevented via ORM
- [ ] Rate limiting on scraper requests (2-3 sec delays)

## 📚 File Reference

| File | Purpose |
|------|---------|
| `main.py` | FastAPI app startup, liveness |
| `config.py` | Settings, store metadata, constants |
| `models.py` | Database schemas, Pydantic models |
| `database.py` | DB connection, initialization |
| `scrapers/base.py` | Common scraping utilities |
| `services/aggregator.py` | Data deduplication, upsert logic |
| `services/scheduler.py` | Scheduled scraping jobs |
| `routes/search.py` | Search API endpoints |
| `routes/records.py` | Record detail API |
| `routes/stores.py` | Store management API |
| `App.jsx` | React root component |
| `api.js` | Backend API client wrapper |
| `useSearch.js` | Search state management hook |

## 💡 Tips

- Use `http://localhost:8000/docs` for interactive API docs
- Press `Ctrl+K Ctrl+K` in Vercel docs to search
- Backend auto-reloads with `DEBUG=True` in `.env`
- Frontend auto-reloads with Vite HMR
- Use `pytest` for unit tests (setup needed)
- Monitor scraper errors in console output
- Use `explain` in PostgreSQL to optimize slow queries
- Cache frequently accessed records in Redis (future)

---

**Need more help?** Check README.md or DEPLOYMENT.md

