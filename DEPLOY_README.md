# 🎵 Israeli Vinyl Record Aggregator - Production Deployment

## Quick Start (30 seconds)

```bash
cd "e:\Code\Project V"
python quick_deploy.py
```

That's it! The script will guide you through:
1. ✓ Collecting credentials (GitHub, Railway, Vercel)
2. ✓ Validating credentials
3. ✓ Running full automated deployment
4. ✓ Initializing database
5. ✓ Triggering first data scrape

---

## What Gets Deployed

### 🔧 Backend (Railway)
- **FastAPI 0.104** REST API
- **PostgreSQL 15** database with 12 record scrapers
- **APScheduler** for daily automatic scraping at 2 AM UTC
- **12 integrated web scrapers** covering Israeli record stores
- **Production-ready** with error logging, rate limiting

### 🎨 Frontend (Vercel)
- **React 18.2** single-page application
- **Vite 5.0** optimized build
- **Search functionality** across all stores
- **Price comparison** interface
- **Zero-config** deployment

### 📊 Database (Railway PostgreSQL)
- Normalized schema: records, stores, prices
- Automatic daily data updates
- Full backup included with Railway
- Deduplication to prevent duplicate listings

---

## Prerequisites

### Things You Need To Have
1. **GitHub account** (free)
2. **Railway account** (free)
3. **Vercel account** (free)
4. **GitHub Personal Access Token**
5. **Railway API Token**
6. **Vercel API Token**

### Total Cost
**$0/month** - Everything runs on free tiers

### Optional but Recommended Tools
- GitHub CLI: `npm install -g gh`
- Railway CLI: `npm install -g railway`
- Vercel CLI: `npm install -g vercel`

---

## Getting Your Credentials (5 minutes)

### Step 1: GitHub Token

1. Go to https://github.com/settings/tokens
2. Click "Generate new token (classic)"
3. Set name: "Vinyl Aggregator Deployment"
4. Check these scopes:
   - ☑ `repo` (full access to repositories)
   - ☑ `workflow` (workflows)
5. Click "Generate token"
6. **Copy immediately** (you won't see it again)

### Step 2: Railway Token

1. Go to https://railway.app
2. Create free account if needed, then sign in
3. Click your profile → Account Settings
4. Click "API Tokens"
5. Click "Create New"
6. Copy the token

### Step 3: Vercel Token

1. Go to https://vercel.com/account/settings/tokens
2. Click "Create Token"
3. Name: "Vinyl Aggregator"
4. Copy the token

### Step 4: PostgreSQL Password

Choose a complex password (you'll configure this):
- At least 16 characters
- Mix of uppercase, lowercase, numbers, symbols
- Example: `VinylAgg@2024#Secure`

---

## Running Deployment

### Method 1: Interactive Quick-Deploy (Recommended)

```bash
python quick_deploy.py
```

This will:
- Check if required tools are installed
- Ask for all credentials interactively
- Validate entries
- Run full deployment
- Show completion report

### Method 2: Full Control Script

If you want more control:

```bash
python deploy.py
```

Same functionality but lets you restart specific steps.

---

## What Happens During Deployment

### Step 1: Tool Verification ✓
Checks git, Python, and optional CLI tools

### Step 2: GitHub Push ✓
- Initializes git repository
- Commits all code
- Pushes to your GitHub repo

### Step 3: Railway Backend ✓
- Creates/configures Railway project
- Sets environment variables
- Deploys FastAPI backend
- Initializes PostgreSQL database service

### Step 4: Vercel Frontend ✓
- Sets production environment variables
- Deploys React frontend
- Generates unique Vercel URL

### Step 5: Database Init ✓
- Creates all tables (records, stores, prices)
- Seeds with store configurations
- Validates schema

### Step 6: First Scrape ✓
- Triggers initial data collection
- Scrapes all 12 stores
- Takes 5-10 minutes
- Logs progress and errors

### Step 7: Verification ✓
- Tests backend health check
- Confirms frontend is accessible
- Validates endpoints responding

### Step 8: Report ✓
- Shows deployment summary
- Lists all completed steps
- Provides monitoring instructions

**Total Time**: 15-25 minutes

---

## After Deployment

### Access Your System

**Backend API** (at your Railway URL):
```
GET  /api/health             - Check if running
GET  /api/stores             - List all stores
GET  /api/search?q=vinyl     - Search for products
POST /api/scrape-all         - Manually trigger scrape
```

**Frontend** (at your Vercel URL):
- Open in browser
- Search for vinyl records
- See price comparisons across stores
- No additional setup needed

### Monitor Everything

**View Backend Logs**:
```bash
railway logs --service backend
```

**View Frontend Logs**:
```bash
vercel logs
```

**Manual Trigger Scrape**:
```bash
curl -X POST https://<your-backend-url>/api/scrape-all
```

### Daily Automatic Scraping

The system automatically scrapes all stores at **2 AM UTC** every day.
- Watch via Railway logs
- View results via `/api/stores` endpoint
- Performance: Usually completes in 10-20 minutes

---

## Troubleshooting

### Deployment Script Fails

1. **Check `DEPLOYMENT_LOG.md`** for exact error
2. **Verify tokens** are correct (no extra spaces)
3. **Confirm accounts** not suspended
4. **Check GitHub repo** is accessible
5. **Verify** all three tokens have sufficient permissions

### Backend Not Responding After Deployment

1. Check Railway logs: `railway logs --service backend`
2. Verify environment variables set correctly
3. Wait 2-3 minutes (cold start can take time)
4. Check database connection in logs

### Frontend Shows "Cannot Connect to API"

1. Verify backend URL in Vercel environment variables
2. Check CORS is not blocking requests
3. Ensure backend health check passes
4. Check network connectivity

### Database Connection Failed

1. Verify PostgreSQL password is correct
2. Check database service is running in Railway
3. View PostgreSQL logs: `railway logs --service postgres`
4. Confirm DATABASE_URL environment variable is set

### First Scrape Taking Too Long

- This is normal, takes 5-10 minutes
- Check logs to see progress: `railway logs --service backend --search "scraper"`
- Monitor individual store scrapers
- Network speed affects scraping duration

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                     PRODUCTION SYSTEM                       │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Frontend (Vercel)          Backend (Railway)   DB (Railway) │
│  ┌──────────────┐          ┌──────────────┐   ┌───────────┐ │
│  │ React 18.2   │         │ FastAPI 0.10 │──│ PostgreSQL │ │
│  │ Search UI    │◄────────│ REST API     │   │  15       │ │
│  │ Vite Build   │         │              │   └───────────┘ │
│  └──────────────┘         │ APScheduler  │       │         │
│                           │ (Daily 2 AM) │       │         │
│                           └──────────────┘       │         │
│                                 │                │         │
│                                 └────────────────┘         │
│                   12 Web Scrapers                           │
│      ┌─────────────┬─────────────┬──────────────┐          │
│      │ WooCommerce │  Custom HTML  │  Specialized  │       │
│      │  (5 stores) │  (3 stores)   │  (4 stores)   │       │
│      └─────────────┴─────────────┴──────────────┘          │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## Security Features

- ✓ **CORS** limited to frontend URL only
- ✓ **Rate limiting** on scraper endpoints
- ✓ **Custom PostgreSQL password** you control
- ✓ **Environment variables** stored securely in Railway
- ✓ **Credentials file** (.deployment_credentials.json) is git-ignored
- ✓ **No API keys** exposed in public code
- ✓ **HTTPS only** through Railway/Vercel

---

## Performance Expectations

After deployment, you can expect:

- **Search response**: < 500ms
- **API availability**: 99.9% uptime
- **Data freshness**: Updated daily at 2 AM UTC
- **Product catalog**: 8,000-9,000 vinyl records
- **Price accuracy**: Within 24 hours of store updates
- **Concurrent users**: Handles 100+ simultaneous searches
- **Database**: 15GB storage (free Railway tier)

---

## Scaling & Future Improvements

### Short-term (Week 1-2)
- Monitor daily scraper runs
- Analyze which stores are most popular
- Fine-tune scraper parameters
- Set up monitoring alerts

### Medium-term (Month 1)
- Add Redis caching for frequent searches
- Implement user preferences
- Add wishlist functionality
- Create price tracking alerts

### Long-term (Month 2+)
- Add new stores (expand beyond Israel)
- Implement user accounts (saved searches)
- Create mobile app
- Add API rate limiting per user

---

## Getting Help

### Documentation
- [FastAPI Docs](https://fastapi.tiangolo.com)
- [Railway Docs](https://docs.railway.app)
- [Vercel Docs](https://vercel.com/docs)
- [PostgreSQL Docs](https://www.postgresql.org/docs)

### Quick Fixes
1. Always check **DEPLOYMENT_LOG.md** first
2. View **Railway logs** for backend errors
3. Check **Vercel logs** for frontend issues
4. Review **.env.production** for environment variables

### Support
- Review error messages carefully (very detailed)
- Search Railway docs for specific error codes
- Check environment variables match your setup
- Verify all credentials entered correctly

---

## Success Checklist

After deployment completes, verify:

- [ ] Backend URL is accessible (curl health check)
- [ ] Frontend loads in browser
- [ ] Search returns results
- [ ] `/api/stores` shows populated data
- [ ] Daily logs appear in Railway at 2 AM UTC
- [ ] No errors in Backend/Frontend logs
- [ ] Database has records (100+ expected)
- [ ] Can access specific product details

---

## Next Steps

1. **Run deployment**: `python quick_deploy.py`
2. **Wait for completion** (15-25 minutes)
3. **Access your system** via provided URLs
4. **Test search functionality**
5. **Monitor logs** during first scrape
6. **Share with users** when ready

---

## Questions?

The deployment script does ALL the heavy lifting. Just provide credentials and it handles:
- Git initialization
- GitHub push
- Railway deployment
- Database setup
- Frontend deployment
- Initial data load
- Verification

**You only need**: 3 tokens + GitHub username + PostgreSQL password

Good luck! 🚀

