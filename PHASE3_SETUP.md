# Phase 3: Local Setup & Integration Testing

## Overview
Phase 3 prepares the system for production deployment by:
1. Setting up local PostgreSQL database
2. Verifying all 12 scrapers can run
3. Testing search/API layer
4. Validating database performance
5. Preparing for production deployment

## Prerequisites

### Required Software
```bash
# PostgreSQL 15+
# Download from: https://www.postgresql.org/download/

# Python 3.11+
# Already installed

# Git (for deployment)
# Download from: https://git-scm.com/
```

### Python Dependencies
```bash
cd backend
pip install -r requirements.txt
```

Expected packages:
- FastAPI 0.104
- SQLAlchemy 2.0
- BeautifulSoup4 4.12
- Requests 2.31
- APScheduler 3.10
- python-dotenv 1.0
- psycopg2 (PostgreSQL driver)

## Step 1: PostgreSQL Setup

### Option A: Local Installation (Recommended for Development)

```bash
# Windows: Download from https://www.postgresql.org/download/windows/
# During installation:
# - Port: 5432 (default)
# - Password: (choose a password, will use in .env)
# - Database: postgres (default)

# After installation, create the database:
psql -U postgres -c "CREATE DATABASE vinyl_aggregator;"
```

### Option B: Docker (Alternative)

```bash
# Pull and run PostgreSQL
docker run -d \
  --name postgres-vinyl \
  -p 5432:5432 \
  -e POSTGRES_PASSWORD=postgres \
  -e POSTGRES_DB=vinyl_aggregator \
  postgres:15

# Verify it's running
docker ps
```

## Step 2: Environment Configuration

Create or update `.env` file in project root:

```env
# Database
DATABASE_URL=postgresql://postgres:YOUR_PASSWORD@localhost/vinyl_aggregator
DB_HOST=localhost
DB_PORT=5432
DB_USER=postgres
DB_PASSWORD=YOUR_PASSWORD
DB_NAME=vinyl_aggregator

# Optional
REDIS_URL=redis://localhost:6379
ENVIRONMENT=development
```

## Step 3: Database Initialization

```bash
cd /path/to/Project\ V

# Run Phase 3 test script
python phase3_local_testing.py
```

This will:
- ✅ Test PostgreSQL connection
- ✅ Initialize database schema (tables, indexes)
- ✅ Seed all 10 stores
- ✅ Verify database structure
- ✅ Generate test report

Expected output:
```
✅ PostgreSQL connection successful
✅ Database schema initialized
✅ Stores seeded
✅ 10 stores verified in database
✅ Database structure verified
```

## Step 4: Test Single Scraper (Phase 1)

Test that scrapers can actually run and populate database:

```bash
# DiscCenter test (Phase 1 - proven, fastest)
python -c "
from backend.scrapers.disccenter import DiscCenterScraper
scraper = DiscCenterScraper()
products = scraper.scrape()
print(f'✅ DiscCenter returned {len(products)} products')
print(f'Sample: {products[0][\"title\"] if products else \"N/A\"}')"
```

Expected time: 30-60 seconds (respects 2-3 sec delays per page)

Expected output:
```
✅ DiscCenter returned 2500 products
Sample: "Artist - Album Title"
```

## Step 5: Test API Layer

```bash
# Run API layer tests
python phase3_api_testing.py
```

This validates:
- ✅ Search service logic
- ✅ API endpoints structure
- ✅ Deduplication algorithm
- ✅ Price aggregation logic

Expected output:
```
✅ Search Service - PASS
✅ API Endpoints - PASS
✅ Deduplication Logic - PASS
✅ Price Aggregation - PASS
```

## Step 6: Run Full Integration Test (Optional)

```bash
# This will scrape all 12 stores and populate database
# Warning: Takes 30+ minutes
# Only run after verifying single scraper works

python -c "
from backend.services.scheduler import scrape_all_stores, SessionLocal
db_session_factory = SessionLocal
scrape_all_stores(db_session_factory)"
```

This will:
- Scrape all 12 stores in sequence
- Return per-store results (created/updated/errors)
- Populate database with ~11,000 initial products
- Post-deduplication: ~8,000-9,000 unique vinyls

## Step 7: Test Search API (Manual)

Once database is populated:

```bash
# Start backend
cd backend
python -m uvicorn main:app --reload --port 8000

# In another terminal, test endpoints:
curl "http://localhost:8000/api/search?q=pink%20floyd"
curl "http://localhost:8000/api/search/autocomplete?q=pink"
curl "http://localhost:8000/api/stores"
curl -X POST "http://localhost:8000/api/stores/scrape"
```

## Step 8: Database Verification Queries

```sql
-- Connect to database
psql -U postgres -d vinyl_aggregator

-- Check stores
SELECT id, name, store_key, is_active, record_count 
FROM stores 
ORDER BY store_key;

-- Expected: 10 rows with is_active=true

-- Check records count
SELECT COUNT(*) as total_records FROM records;

-- Expected: 8000-9000 rows after first full scrape

-- Check prices count
SELECT COUNT(*) as total_prices FROM prices;

-- Expected: Similar to records (most have prices)

-- Sample search
SELECT r.title, r.artist, r.album, COUNT(p.id) as store_count
FROM records r
LEFT JOIN prices p ON r.id = p.record_id
WHERE r.artist ILIKE '%pink floyd%'
GROUP BY r.id, r.title, r.artist, r.album;

-- Expected: Pink Floyd records with prices from multiple stores
```

## Step 9: Performance Testing

```bash
# Query speed test
time python -c "
from backend.database import SessionLocal
from backend.models import Record
db = SessionLocal()
results = db.query(Record).filter(Record.artist.ilike('%pink floyd%')).all()
print(f'Found {len(results)} records')
print(f'Query time: <500ms expected')"

# Search autocomplete speed
time python -c "
from backend.database import SessionLocal
from backend.models import Record
from sqlalchemy import distinct
db = SessionLocal()
artists = db.query(distinct(Record.artist)).limit(10).all()
print(f'Autocomplete: {len(artists)} artists')"
```

Expected: All queries complete in <500ms with 8K+ products

## Step 10: Monitoring & Logs

Check application logs for errors:

```bash
# If running in debug mode, logs appear in console
# For production, logs should be written to file

tail -f logs/vinyl_aggregator.log
```

Key things to check:
- ✅ No database connection errors
- ✅ No scraper failures
- ✅ No search query timeouts
- ✅ No memory leaks (check Python process memory)

## Troubleshooting

### "No module named 'psycopg2'"
```bash
pip install psycopg2-binary
```

### "Database does not exist"
```bash
psql -U postgres -c "CREATE DATABASE vinyl_aggregator;"
```

### "Connection refused on localhost:5432"
```bash
# Check PostgreSQL is running
pg_isready -h localhost -p 5432

# Or restart PostgreSQL
# Windows: Services app → PostgreSQL 15 server → Restart
# macOS: brew services restart postgresql
# Linux: sudo systemctl restart postgresql
```

### "Search returns 0 results despite data in database"
```bash
# Check full-text search index
SELECT COUNT(*) FROM records WHERE search_vector IS NOT NULL;

# If 0, rebuild index:
UPDATE records SET search_vector = 
  to_tsvector('english', artist || ' ' || album || ' ' || title);
CREATE INDEX idx_records_search ON records USING gin(search_vector);
```

## Next Steps After Phase 3

Once local testing is complete and all tests pass:

1. **Push to GitHub**
   ```bash
   git add .
   git commit -m "Phase 3: Local testing and integration verified"
   git push origin main
   ```

2. **Deploy Backend to Railway**
   - Connect GitHub repo to Railway
   - Set environment variables (DATABASE_URL, etc.)
   - Deploy

3. **Deploy Frontend to Vercel**
   - Update API_BASE_URL in frontend/.env
   - Connect GitHub repo to Vercel
   - Deploy

4. **Production Verification**
   - Run scrapers in production
   - Monitor logs
   - Verify search works
   - Test with real users

## Phase 3 Checklist

- [ ] PostgreSQL installed and running
- [ ] `.env` configured with DATABASE_URL
- [ ] `phase3_local_testing.py` runs with all tests passing
- [ ] Single DiscCenter scraper test successful (2500+ products)
- [ ] `phase3_api_testing.py` runs with all tests passing
- [ ] Database contains ~2500 DiscCenter products
- [ ] Search query returns results in <500ms
- [ ] All 10 stores visible in `/api/stores`
- [ ] Frontend can connect to local backend
- [ ] Logs show no errors or warnings

## Performance Targets

Post-Phase 3 with full 12-store scrape:

| Metric | Target | Status |
|--------|--------|--------|
| Total Unique Vinyls | 8,000-9,000 | TBD |
| Search Query Speed | <500ms | TBD |
| Database Size | ~50-100MB | TBD |
| Scrape Time (All 12) | 30-45 min | TBD |
| API Response Time | <100ms | TBD |
| Uptime | 99.5%+ | TBD |

---
*Last Updated: 2026-03-28*  
*Phase 3 Status: Setup & Testing Guide*

