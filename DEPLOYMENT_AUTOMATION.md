# Production Deployment Guide - Complete Automation

## Overview

The `deploy.py` script handles the complete deployment of the Israeli Vinyl Record Aggregator to production:
- GitHub code push
- Railway backend + PostgreSQL deployment
- Vercel frontend deployment
- Database initialization
- First data scrape
- Production verification

## Prerequisites

### Required Tools
1. **Git** - Version control
2. **GitHub CLI (gh)** - `npm install -g gh` or `brew install gh`
3. **Railway CLI** - `npm install -g railway`
4. **Vercel CLI** - `npm install -g vercel`
5. **Python 3.11+** - Already available

### Required Accounts & Tokens
1. **GitHub**
   - GitHub account with repository access
   - Personal Access Token (Settings → Developer Settings → Personal access tokens)
   - Permissions needed: `repo`, `workflow`, `gist`

2. **Railway**
   - Free Railway account (https://railway.app)
   - API token (Account Settings → API Tokens)
   - Note: Railway offers free tier with generous limits

3. **Vercel**
   - Free Vercel account (https://vercel.com)
   - API token (Settings → Tokens)

## Setup Instructions

### Step 1: Prepare Your GitHub Repository

```bash
# If using new GitHub repo:
gh auth login  # Authenticate with GitHub
gh repo create vinyl-aggregator --public --source=. --remote=origin --push
```

### Step 2: Get Your Tokens

#### GitHub Token
1. Go to https://github.com/settings/tokens
2. Click "Generate new token (classic)"
3. Select scopes: `repo`, `workflow`
4. Copy the token (you'll need it in the script)

#### Railway Token
1. Go to https://railway.app
2. Sign in or create account
3. Go to Account Settings → API Tokens
4. Generate new token
5. Copy the token

#### Vercel Token
1. Go to https://vercel.com/account/settings/tokens
2. Create new token
3. Copy the token

### Step 3: Run Deployment Script

```bash
cd "e:\Code\Project V"
python deploy.py
```

The script will prompt you for:
- GitHub token, username, repository URL
- Railway API token and project ID (use "new" for new project)
- PostgreSQL password (you choose)
- Vercel token, project name, team (optional)
- Backend and frontend URLs (optional, auto-generated)

### Step 4: Monitor Deployment

The script will:
1. ✓ Verify all CLI tools are installed
2. ✓ Push code to GitHub
3. ✓ Deploy backend to Railway with PostgreSQL
4. ✓ Deploy frontend to Vercel
5. ✓ Initialize database schema
6. ✓ Trigger first data scrape (5-10 minutes)
7. ✓ Verify production endpoints
8. ✓ Generate deployment report

Each step creates detailed logs in `DEPLOYMENT_LOG.md`

## What Gets Deployed

### Backend (Railway)
- FastAPI 0.104 server
- Python 3.11 runtime
- PostgreSQL 15 database
- 12 integrated web scrapers
- Automatic daily scheduling (APScheduler)
- Daily scrapes at 2 AM UTC

### Frontend (Vercel)
- React 18.2 SPA
- Vite build optimization
- Search functionality
- Price comparison across all stores
- Zero-config deployment

## Post-Deployment Checklist

After successful deployment:

- [ ] Verify backend responding at Railway URL
- [ ] Verify frontend loading at Vercel URL
- [ ] Check initial scrape completed (view `/api/stores` endpoint)
- [ ] Monitor Railway logs for errors
- [ ] Test search functionality with test queries
- [ ] Monitor daily scraper runs in Railway logs

## Troubleshooting

### Railway Deployment Issues
```bash
# View logs
railway logs --service backend

# Check project status
railway status

# Redeploy
railway up --service backend
```

### Vercel Issues
```bash
# View deployment logs
vercel logs

# Redeploy
vercel --prod
```

### Database Connection Issues
Check Railway PostgreSQL service is running:
```bash
railway logs --service postgres
```

### First Scrape Not Completing
- Check backend logs for scraper errors
- Verify network connectivity to store websites
- Review individual scraper logs at `/api/stores/{store_key}`

## Accessing Production

Once deployed:

1. **Backend API**: `https://<railway-domain>.railway.app`
   - Health: `GET /api/health`
   - Stores: `GET /api/stores`
   - Search: `GET /api/search?q=vinyl+records`
   - Trigger scrape: `POST /api/scrape-all`

2. **Frontend**: `https://<your-project>.vercel.app`
   - Live search interface
   - Price comparison
   - Product details

3. **Daily Automatic Scrapes**: Runs at 2 AM UTC via APScheduler

## Cost Estimate

- **Railway**: Free tier provides 500 hours/month (sufficient)
- **Vercel**: Free tier (sufficient for this project)
- **GitHub**: Free tier (sufficient)
- **Total Cost**: $0/month

## Monitoring & Maintenance

### Check Scraper Health
```bash
# Via API
curl https://<backend>/api/stores

# Via Railway logs
railway logs --service backend --search "scraper"
```

### Manual Trigger Full Scrape
```bash
curl -X POST https://<backend>/api/scrape-all
```

### Update Code & Redeploy
```bash
git push origin main  # Auto-triggers Railway redeploy
vercel --prod         # Redeploy frontend manually if needed
```

## Database Management

PostgreSQL is managed by Railway and automatically backed up. To access database:

```bash
# Via Railway CLI
railway connect postgres

# Then use psql commands
\dt  # List tables
SELECT COUNT(*) FROM records;  # Row count
```

## Security Notes

- ✓ All credentials stored in `.deployment_credentials.json` (git ignored)
- ✓ Environment variables set securely in Railway
- ✓ CORS configured to frontend domain only
- ✓ Database password is custom (you set it)
- ✓ API rate limiting on scraper endpoints

## Getting Help

If deployment fails:
1. Check `DEPLOYMENT_LOG.md` for error details
2. Verify all tokens are correct and have proper permissions
3. Ensure GitHub repository is accessible
4. Check Railway/Vercel account status (not suspended)
5. Review environment variables in Railway console

## Next: Scale & Optimize

After successful production deployment:

1. **Enable Analytics**: Railway provides built-in metrics
2. **Monitor Performance**: Check API response times
3. **Fine-tune Scrapers**: Adjust categories/keywords based on data
4. **Expand Stores**: Add more scrapers following the pattern
5. **Implement Caching**: Redis for frequently searched items


