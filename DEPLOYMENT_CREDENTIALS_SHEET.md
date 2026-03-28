# Production Deployment - Token & Credential Collection Sheet

Use this sheet to gather all credentials before running `python deploy.py`

## 1. GitHub Setup

**GitHub Account**: `_____________________________`

**GitHub Username/Handle**: `_____________________________`

**Get Token**: https://github.com/settings/tokens
- Click "Generate new token (classic)"
- Scopes: `repo`, `workflow`
- Copy and paste below:

**GitHub Personal Access Token (PAT)**:
```
_________________________________________________________________
_________________________________________________________________
```

**GitHub Repository URL** (can be new or existing):
```
https://github.com/YOUR_USERNAME/vinyl-aggregator
```

Check: Is your GitHub repository created? ☐ Yes ☐ No

---

## 2. Railway Setup

**Railway Account**: https://railway.app
- Create free account if needed

**Get Token**: Account Settings → API Tokens

**Railway API Token**:
```
_________________________________________________________________
```

**Railway Project** (use options below):
- ☐ Create new project (enter "new" when prompted)
- ☐ Use existing project ID: `_____________________________`

**PostgreSQL Password** (you choose, must be complex):
```
_________________________________________________________________
```

Requirements:
- At least 16 characters
- Mix of upper, lower, numbers, symbols
- Example: `Vinyl@2024#Agg3g`

---

## 3. Vercel Setup

**Vercel Account**: https://vercel.com
- Create free account if needed

**Get Token**: Settings → Tokens → Create

**Vercel API Token**:
```
_________________________________________________________________
```

**Vercel Project Name** (choose a name):
```
vinyl-aggregator
```

**Vercel Team ID** (optional, leave blank for personal):
```
_____________________________  (leave blank if personal account)
```

---

## 4. Production URLs (Will Be Assigned)

These will be generated automatically by the deployment script.

**Backend URL** (Railway will assign):
```
https://vinyl-aggregator-production-xxxx.railway.app
```

**Frontend URL** (Vercel will assign):
```
https://vinyl-aggregator.vercel.app
```

---

## 5. Deployment Verification Checklist

Before running `python deploy.py`, verify:

- ☐ Git is installed: `git --version`
- ☐ GitHub CLI is installed: `gh --version`
- ☐ Railway CLI is installed: `railway --version`
- ☐ Vercel CLI is installed: `vercel --version`
- ☐ Python 3.11+ is installed: `python --version`
- ☐ GitHub token has `repo` and `workflow` scopes
- ☐ PostgreSQL password is complex and saved securely
- ☐ All three tokens are valid and copied correctly
- ☐ GitHub repository is accessible

---

## 6. Running the Deployment

```bash
cd "e:\Code\Project V"
python deploy.py
```

The script will prompt for:
1. GitHub token
2. GitHub username
3. GitHub repository URL
4. Railway token
5. Railway project ID (or "new")
6. PostgreSQL password
7. Vercel token
8. Vercel project name
9. Vercel team (optional)
10. Backend/Frontend URLs (optional)

---

## 7. Post-Deployment Access

After deployment completes successfully:

**Backend Endpoints**:
```
GET  /api/health              - Health check
GET  /api/stores              - List all stores
GET  /api/search?q=query      - Search products
POST /api/scrape-all          - Trigger full scrape
```

**Frontend**:
- Open your Vercel URL to use the search interface
- No additional setup needed

**Monitoring**:
```bash
# View Railway logs
railway logs --service backend

# View Vercel logs
vercel logs
```

---

## 8. Troubleshooting Reference

If you encounter errors during deployment:

| Error | Solution |
|-------|----------|
| "Tool not found: railway" | Run: `npm install -g railway` |
| "Tool not found: vercel" | Run: `npm install -g vercel` |
| "Invalid token" | Verify token copied correctly without spaces |
| "Repository not found" | Verify GitHub repo URL and token permissions |
| "Database connection failed" | Check PostgreSQL password is correct |
| "Frontend not loading" | Check VITE_API_URL environment variable |

---

## 9. Cost & Quotas

- **Railway Free Tier**: $5/month credit (500 GB-hours)
- **Vercel Free Tier**: Unlimited deployments, 100 GB bandwidth
- **GitHub Free Tier**: Unlimited repos and actions
- **Total Monthly Cost**: $0 (within free limits)

---

## 10. Support URLs

- Railway Docs: https://docs.railway.app
- Vercel Docs: https://vercel.com/docs
- FastAPI Docs: https://fastapi.tiangolo.com
- PostgreSQL: https://www.postgresql.org/docs

---

## Notes

Use this space to add any special configurations:

```
_________________________________________________________________

_________________________________________________________________

_________________________________________________________________
```

---

**Deployment Date**: _______________

**Completed By**: _______________

**Support Contact**: _______________

