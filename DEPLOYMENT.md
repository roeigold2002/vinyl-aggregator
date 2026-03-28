# Deployment Guide - Vinyl Record Aggregator

Complete guide for deploying the Vinyl Aggregator to production.

## Architecture

```
┌─────────────┐         ┌──────────────┐         ┌────────────┐
│   Vercel    │ ────────┤  Railway     │ ────────┤ PostgreSQL │
│  (Frontend) │         │  (Backend)   │         │  (Railway) │
└─────────────┘         └──────────────┘         └────────────┘
   React SPA            FastAPI + APScheduler          DB
  Development           Production API              Managed
                        + Scrapers
```

## Deploy to Railway (Backend)

Railway is recommended for simplicity and integrated PostgreSQL.

### Prerequisites
- Railway account (free tier available at railway.app)
- GitHub account with code repository

### Steps

1. **Create Railway Project**
   - Go to railway.app, sign in with GitHub
   - Create new project
   - Select "Deploy from GitHub repo"
   - Connect your repository

2. **Configure Environment**
   - Go to Project Settings → Variables
   - Add variables:
     ```
     DATABASE_URL=postgresql://postgres:PASSWORD@localhost:5432/vinyl_aggregator
     DEBUG=False
     REDIS_URL=redis://redis:6379
     ```

3. **Add PostgreSQL Service**
   - Add a service → PostgreSQL
   - Railway auto-generates DATABASE_URL

4. **Add Redis Service** (optional)
   - Add a service → Redis
   - Railway auto-generates REDIS_URL

5. **Configure Start Command**
   - Settings → Start Command:
     ```
     cd backend && pip install -r requirements.txt && python main.py
     ```

6. **Deploy**
   - Push to GitHub
   - Railway auto-deploys on commit to main branch
   - Monitor in Railway dashboard

### Enable Background Jobs
```python
# In main.py, make sure scheduler starts
from services.scheduler import init_scheduler
init_scheduler(SessionLocal)
```

## Deploy to Vercel (Frontend)

### Prerequisites
- Vercel account (free at vercel.com)
- GitHub repository with code

### Steps

1. **Prepare Frontend**
   ```bash
   cd frontend
   npm run build  # Test build locally
   ```

2. **Deploy to Vercel**
   - Go to vercel.com, sign in with GitHub
   - Click "New Project"
   - Select your repository
   - Framework: Vite
   - Root Directory: `./frontend`
   - Build Command: `npm run build`
   - Output Directory: `dist`

3. **Configure Environment Variables**
   - Project Settings → Environment Variables
   - Add:
     ```
     VITE_API_BASE=https://your-railway-backend.up.railway.app
     ```

4. **Deploy**
   - Click "Deploy"
   - Vercel builds and deploys frontend
   - Get URL: `https://your-project.vercel.app`

## Set API Base URL

Update frontend API client to point to production backend:

**frontend/src/services/api.js**
```javascript
const API_BASE = process.env.VITE_API_BASE || '/api'
```

**vercel.json** (if needed)
```json
{
  "env": {
    "VITE_API_BASE": "@api_base_url"
  },
  "rewrites": [
    {
      "source": "/api/:path*",
      "destination": "https://your-backend.up.railway.app/api/:path*"
    }
  ]
}
```

## Custom Domain

### Frontend (Vercel)
1. Project Settings → Domains
2. Add custom domain
3. Update DNS records at your registrar

### Backend (Railway)
1. Settings → Domains
2. Add custom domain
3. Update DNS records

## Database Backups

### PostgreSQL on Railway
- Railroad provides automated backups
- Access in railway dashboard → Database → Backups
- Download backups for archiving

### Manual Backup
```bash
# From your local machine
pg_dump -h $RAILWAY_POSTGRES_HOST -U postgres -d vinyl_aggregator > backup.sql

# Restore
psql -h $HOST -U postgres -d vinyl_aggregator < backup.sql
```

## Monitoring

### Railway Dashboard
- View logs: Project → Deployment ID
- Monitor metrics: CPU, memory, requests
- View errors in real-time

### Error Tracking
```python
# In main.py, add Sentry for error tracking
import sentry_sdk
sentry_sdk.init("your-sentry-dsn")
```

### Health Checks
Configure Railway to monitor health endpoint:
- HTTP GET `https://your-backend/health`
- Expected response: `{"status": "healthy"}`

## Scaling

### Frontend (Vercel)
- Auto-scales based on traffic
- No configuration needed
- Edge caching automatically enabled

### Backend (Railway)
1. Increase CPU/Memory:
   - Project Settings → Resource Class
   - Scale up as needed

2. Enable auto-scaling:
   - Set up multiple replicas
   - Configure load balancing

3. Optimize database:
   - Add indexes for slow queries
   - Monitor query performance

## Continuous Deployment

### GitHub Actions (Auto Deploy)

Create `.github/workflows/deploy.yml`:

```yaml
name: Deploy to Railway

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Deploy to Railway
        run: |
          npm i -g @railway/cli
          railway deploy
        env:
          RAILWAY_TOKEN: ${{ secrets.RAILWAY_TOKEN }}
```

## SSL/TLS

Both Vercel and Railway provide free SSL certificates by default.

- Vercel: Auto-issued, auto-renewed
- Railway: Auto-issued, auto-renewed

## Troubleshooting

### Frontend can't reach backend
- Check CORS is enabled in FastAPI
- Verify `VITE_API_BASE` environment variable
- Check API is responding: `curl https://your-api.com/health`

### Database connection failed
- Verify DATABASE_URL environment variable
- Check PostgreSQL service is running
- Test connection locally first

### Scraper not running
- Check scheduler initialization in main.py
- Monitor logs for errors
- Verify database connection
- Check file permissions for temp directories

### Slow searches
- Add database indexes
- Optimize full-text search queries
- Enable caching layer (Redis)
- Monitor database query performance

## Production Checklist

- [ ] Environment variables configured
- [ ] Database backups enabled
- [ ] SSL/TLS certificates active
- [ ] Health checks working
- [ ] Monitoring/logging configured
- [ ] Error tracking enabled (Sentry)
- [ ] CORS properly configured
- [ ] Rate limiting implemented
- [ ] API documentation available
- [ ] Frontend build optimized
- [ ] Contact info in error messages
- [ ] Capacity plan for data growth

## Cost Estimation

- **Vercel Frontend**: Free-$20/month (pro)
- **Railway Backend**: ~$5-15/month (with PostgreSQL)
- **PostgreSQL**: Included in Railway
- **Domain**: ~$10-15/year (yours)

**Total**: ~$70-100/year for production

## Rollback Procedure

### Railway
1. Go to Deployments tab
2. Find previous stable deployment
3. Click "Redeploy"

### Vercel
1. Go to Deployments tab
2. Find previous version
3. Click "Promote to Production"

---

Need help? Check Railway docs (railway.app/docs) and Vercel docs (vercel.com/docs).

