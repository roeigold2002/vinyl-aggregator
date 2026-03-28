# 🚀 DEPLOYMENT CHEAT SHEET

## TL;DR - Deploy in 3 Commands

```bash
# 1. Get tokens (do this in browser):
# - GitHub: https://github.com/settings/tokens (scopes: repo, workflow)
# - Railway: https://railway.app (Account Settings → API Tokens)
# - Vercel: https://vercel.com/account/settings/tokens

# 2. Run deployment (provide tokens when prompted)
cd "e:\Code\Project V"
python quick_deploy.py

# 3. Done! Access your system at the provided URLs
```

## What You Need (Copy-Paste Checklist)

- [ ] GitHub token (20+ characters, starts with `ghp_`)
- [ ] GitHub username (e.g., `john_doe`)
- [ ] GitHub repo URL (e.g., `https://github.com/john_doe/vinyl-aggregator`)
- [ ] Railway token (20+ characters)
- [ ] Railway project ID (or type `new` to create one)
- [ ] PostgreSQL password (choose one, e.g., `VinylAgg@2024#Sec`)
- [ ] Vercel token (20+ characters)
- [ ] Vercel project name (e.g., `vinyl-aggregator`)

## Getting Tokens (5 Minutes Total)

### GitHub Token
1. https://github.com/settings/tokens
2. "Generate new token (classic)"
3. Check: `repo`, `workflow`
4. Click "Generate token"
5. Copy immediately (won't show again)

### Railway Token
1. https://railway.app (create account if needed)
2. Profile → Account Settings
3. "API Tokens"
4. "Create New"
5. Copy token

### Vercel Token
1. https://vercel.com/account/settings/tokens
2. "Create Token"
3. Copy immediately

## One-Command Deploy

```bash
python quick_deploy.py
```

Then answer the prompts with your credentials.

**That's it. System will be live in 15-25 minutes.**

## After Deployment

### See Your URLs
```
Backend: https://vinyl-aggregator-xxxx.railway.app
Frontend: https://vinyl-xxx.vercel.app
```

### Test It Works
```bash
# In PowerShell:
curl https://your-backend-url/api/health
curl https://your-backend-url/api/stores
```

### View Logs
```bash
# Backend logs (real-time)
railway logs --service backend

# Frontend logs
vercel logs
```

### Trigger Manual Scrape
```bash
curl -X POST https://your-backend-url/api/scrape-all
```

## Files in Folder

```
e:\Code\Project V\
├── quick_deploy.py              ← START HERE (interactive)
├── deploy.py                    ← Alternative full control
├── DEPLOY_README.md             ← Detailed guide
├── YOUR_ACTION_ITEMS.md         ← What you need to do
├── DEPLOYMENT_AUTOMATION.md     ← Technical deep-dive
├── DEPLOYMENT_CREDENTIALS_SHEET.md ← Credential tracker
├── DEPLOYMENT_LOG.md            ← Created during deploy (full logs)
│
├── backend/                     ← Java/Python backend
├── frontend/                    ← React frontend
└── ... (other project files)
```

## Troubleshooting Quick Links

| Issue | File to Check | Command |
|-------|---------------|---------|
| Deployment failed | `DEPLOYMENT_LOG.md` | `cat DEPLOYMENT_LOG.md` |
| Backend won't start | Railway logs | `railway logs --service backend` |
| Frontend won't load | Vercel logs | `vercel logs` |
| Database error | PostgreSQL logs | `railway logs --service postgres` |
| Token invalid | Credentials file | Check `.deployment_credentials.json` |

## Expected Timeline

```
0m    - Start script
0-5m  - Enter credentials
5-7m  - Git push to GitHub
7-12m - Railway deploy (backend + DB)
12-15m - Vercel deploy (frontend)
15-17m - Database initialization
17-27m - First data scrape (normal, expected)
27-28m - Verify and complete
```

## What Gets Deployed

```
┌─────────────────────────────────────┐
│     PRODUCTION SYSTEM DEPLOYED      │
├─────────────────────────────────────┤
│ Frontend: React SPA on Vercel       │
│ Backend: FastAPI API on Railway     │
│ Database: PostgreSQL on Railway     │
│ Scrapers: 12 Israeli record stores  │
│ Data: 8,000-9,000 vinyl records     │
│ Updates: Daily at 2 AM UTC          │
│ Cost: $0/month (free tier)          │
└─────────────────────────────────────┘
```

## API Endpoints (After Deploy)

```
GET  /api/health              # Health check
GET  /api/stores              # List all stores
GET  /api/search?q=vinyl      # Search products
POST /api/scrape-all          # Manual full scrape
```

## Success = When You See This

```
✓ Backend deployed to Railway
✓ Frontend deployed to Vercel
✓ Database initialized
✓ First scrape completed
✓ All endpoints responding

🎉 DEPLOYMENT SUCCESSFUL!
Backend: https://...railway.app
Frontend: https://...vercel.app
```

## Environment Variables (Auto-Set)

```
DATABASE_URL=postgresql://...
API_ENV=production
VITE_API_URL=<your-backend-url>
VITE_ENV=production
```

## Daily Automatic Updates

✓ Runs at 2 AM UTC every day
✓ Scrapes all 12 stores
✓ Takes 5-10 minutes
✓ Updates with new prices
✓ Automatic error recovery

## Cost Summary

- Railway (backend + PostgreSQL): $0
- Vercel (frontend): $0
- GitHub: $0
- Total: $0/month

## One Last Thing

If anything goes wrong:

1. Stop the script (Ctrl+C)
2. Check `DEPLOYMENT_LOG.md`
3. Read the error carefully
4. Consult `DEPLOY_README.md` troubleshooting section
5. Most common: token typo or missing permissions

## Run Deployment Now

```powershell
cd "e:\Code\Project V"
python quick_deploy.py
```

Questions? See:
- `DEPLOY_README.md` - Comprehensive guide
- `DEPLOYMENT_AUTOMATION.md` - Technical details
- `YOUR_ACTION_ITEMS.md` - Step-by-step walkthrough

Good luck! 🚀

