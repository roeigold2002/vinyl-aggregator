# Phase 3: Production Deployment Guide

## Pre-Deployment Checklist

Before deploying to production, ensure all Phase 3 local tests pass:

- [ ] PostgreSQL local database initialized
- [ ] All 10 stores seeded successfully
- [ ] Single scraper test (DiscCenter) works
- [ ] API endpoints respond correctly
- [ ] Search queries < 500ms
- [ ] Deduplication logic validated
- [ ] All 12 scrapers structurally verified (Phase 2)

## Backend Deployment (Railway)

### Step 1: Prepare Backend for Deployment

```bash
# Create production .env file (with actual values)
cat > backend/.env.production << EOF
DATABASE_URL=postgresql://user:password@db.railway.internal/vinyl
REDIS_URL=redis://default:password@redis.railway.internal:6379
ENVIRONMENT=production
LOG_LEVEL=INFO
CORS_ORIGINS=["https://yourdomain.com", "https://app.yourdomain.com"]
EOF

# Update requirements.txt versions to be specific
pip freeze > backend/requirements.txt
```

### Step 2: Create Dockerfile (If Not Exists)

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY backend/ .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Step 3: Deploy to Railway

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login to Railway
railway login

# Create new project
railway init

# Add PostgreSQL database
railway add --database postgres

# Deploy backend
railway up

# View logs
railway logs

# Get production URL
railway env
```

### Step 4: Backend Environment Variables on Railway

Set these in Railway dashboard:

```
DATABASE_URL: postgresql://[user]:[password]@[host]:[port]/[db]
REDIS_URL: redis://[user]:[password]@[host]:[port]
ENVIRONMENT: production
LOG_LEVEL: INFO
CORS_ORIGINS: ["https://yourdomain.com"]
```

## Frontend Deployment (Vercel)

### Step 1: Prepare Frontend for Production

```bash
# Update API base URL in frontend
cat > frontend/.env.production << EOF
VITE_API_BASE_URL=https://your-railway-backend.up.railway.app
VITE_API_TIMEOUT=30000
VITE_ENVIRONMENT=production
EOF

# Build frontend
cd frontend
npm run build

# Test production build locally
npm run preview
```

### Step 2: Deploy to Vercel

```bash
# Install Vercel CLI
npm install -g vercel

# Login to Vercel
vercel login

# Deploy frontend
vercel --prod

# View deployment URL
# Vercel will provide: https://your-app.vercel.app
```

### Step 3: Configure Vercel Environment Variables

In Vercel dashboard → Project Settings → Environment Variables:

```
VITE_API_BASE_URL: https://your-railway-backend.up.railway.app
VITE_ENVIRONMENT: production
```

## Database Setup on Railway

### Step 1: Initialize Production Database

```bash
# Connect to production database
psql postgresql://[user]:[password]@[host]:[port]/[db]

# Run initialization SQL
\i backend/database.py  # This runs via Python, not SQL

# Or using Python:
python -c "
import os
os.environ['DATABASE_URL'] = 'postgresql://...'
from backend.database import init_db, SessionLocal, seed_stores
db = SessionLocal()
init_db(db)
seed_stores(db)
print('✅ Production database initialized')
"
```

### Step 2: Verify Production Database

```bash
# Connect to production database
psql postgresql://[user]:[password]@[host]:[port]/[db]

# Check stores
SELECT COUNT(*) FROM stores;  # Should be 10

# Check that no records yet (until first scrape)
SELECT COUNT(*) FROM records;  # Should be 0

# Check indexes exist
SELECT indexname FROM pg_indexes WHERE tablename = 'records';
```

## Scraper Schedule Setup

### Step 1: Enable APScheduler in Production

The scheduler is already configured in `backend/services/scheduler.py`:

```python
# Runs daily at 2 AM UTC (approximately 4 AM IST in winter)
scheduler.add_job(
    scrape_all_stores,
    CronTrigger(hour=0, minute=0, timezone='UTC'),
    args=[db_session_factory],
    id='scrape_all_stores',
)
```

### Step 2: Manual Triggers (For Testing)

Once deployed, trigger scrape manually:

```bash
# Via API endpoint
curl -X POST "https://your-backend.up.railway.app/api/stores/scrape"

# Expected response:
# {
#   "status": "Scrape initiated",
#   "message": "Check logs for progress",
#   "stores": 12
# }
```

Monitor logs:
```bash
railway logs --follow
```

## Monitoring & Logging

### Step 1: Set Up Logging

Add logging service integration:

```python
# backend/main.py already includes logging
# In production, logs go to Railway's log service
```

Check logs:
```bash
# View recent logs
railway logs

# Follow logs in real-time
railway logs -f

# Filter by service
railway logs --service backend
```

### Step 2: Monitor Performance

Production dashboard should show:

- API response times (<100ms avg)
- Error rates (<0.1%)
- Database query times (<500ms)
- Scraper job status
- Uptime (target: 99.5%+)

### Step 3: Alert Configuration

Set up alerts in Railway/Vercel for:

- API errors > 1%
- Database connection failures
- Scraper job failures
- High response times (>1s)

## Post-Deployment Verification

### Step 1: Test All Endpoints

```bash
# Search
curl "https://your-app.vercel.app/api/search?q=pink%20floyd"

# Autocomplete
curl "https://your-app.vercel.app/api/search/autocomplete?q=pink"

# Stores
curl "https://your-app.vercel.app/api/stores"

# Trigger scrape
curl -X POST "https://your-app.vercel.app/api/stores/scrape"
```

### Step 2: Verify Frontend

1. Open https://your-app.vercel.app
2. Search for "Pink Floyd"
3. Verify results display correctly
4. Check multiple stores showing in price comparison
5. Verify responsive design on mobile

### Step 3: Monitor First Scrape

```bash
# Watch scraper progress
railway logs -f

# Expected output:
# 🔄 Starting scheduled scrape of 12 stores...
# 📍 Starting disccenter scrape...
# ✅ disccenter: 2500 created, 0 updated, 0 errors
# 📍 Starting thevinylroom scrape...
# ✅ thevinylroom: 1200 created, 0 updated, 0 errors
# ...
# ✅ Scheduled scrape completed in 35.42s: 10/12 stores, 11000 created
```

### Step 4: Verify Database Populated

```bash
# Connect to production database
psql postgresql://[user]:[password]@[host]:[port]/[db]

# Check record count
SELECT COUNT(*) as total_records FROM records;
# Expected: 8000-9000 (after deduplication)

# Check price count
SELECT COUNT(*) as total_prices FROM prices;
# Expected: Similar to records count

# Sample search
SELECT title, artist FROM records LIMIT 5;
```

## Troubleshooting Production Issues

### Issue: Scraper Job Not Running

```bash
# Check logs
railway logs -f | grep "scrape"

# Check APScheduler status
python -c "
from backend.services.scheduler import scheduler
print(scheduler.get_jobs())"

# Manually trigger
curl -X POST "https://your-app.vercel.app/api/stores/scrape"
```

### Issue: Search Returns 0 Results

```bash
# Check database has records
SELECT COUNT(*) FROM records;

# Check search vector is built
SELECT COUNT(*) FROM records WHERE search_vector IS NOT NULL;

# Rebuild if needed
UPDATE records SET search_vector = 
  to_tsvector('english', artist || ' ' || album || ' ' || title);
```

### Issue: High Memory Usage

```bash
# Check process memory
ps aux | grep python

# Optimize queries
VACUUM ANALYZE;

# Check for slow queries
SELECT query, mean_time, calls FROM pg_stat_statements 
ORDER BY mean_time DESC LIMIT 10;
```

### Issue: Slow API Responses

```bash
# Check query times
EXPLAIN ANALYZE SELECT * FROM records WHERE artist ILIKE '%pink%' LIMIT 50;

# Add indexes if missing
CREATE INDEX idx_records_artist ON records(artist);
CREATE INDEX idx_records_album ON records(album);
```

## Scaling Considerations

### Current Capacity

With current setup:
- **Records**: 10,000 (comfortable)
- **Stores**: 12 (scales to 20+)
- **Requests**: 100 req/s (Railway free tier)
- **Storage**: 50-100MB PostgreSQL

### Scaling Timeline

1. **Now (Phase 3)**: Single Railway instance, single Vercel deployment
2. **6 months**: Add Redis cache, CDN for images, monitoring
3. **1 year**: Add search service (Elasticsearch), API caching layer
4. **2+ years**: Microservices, dedicated search service, global CDN

## Maintenance Schedule

### Daily
- Monitor logs for errors
- Check scraper completion

### Weekly
- Database optimization (VACUUM, ANALYZE)
- Review slow queries
- Check storage usage

### Monthly
- Database backup verification
- Performance analysis
- Update security patches

### Quarterly
- Load testing with 2x expected volume
- Disaster recovery drill
- Code optimization review

## Success Criteria for Phase 3

✅ Backend deployed to Railway  
✅ Frontend deployed to Vercel  
✅ Database initialized with all 10 stores  
✅ First scrape completed successfully  
✅ 8,000-9,000 unique vinyls in database  
✅ Search works from production frontend  
✅ All API endpoints responding  
✅ Logs being collected properly  
✅ Performance within targets  
✅ Daily scraper job running automatically  

---
*Last Updated: 2026-03-28*  
*Phase 3 Deployment Guide*

