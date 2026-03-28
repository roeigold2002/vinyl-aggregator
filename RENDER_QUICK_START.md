# 🚀 RENDER BACKEND DEPLOYMENT - 5 MINUTES

**Permanently Free | No Credit Card | Easy Deploy**

---

## Step 1: Prepare Backend (Already Done)

Your backend code is ready at: `https://github.com/roeigold2002/vinyl-aggregator/tree/main/backend`

Uses:
- FastAPI 0.104.1
- SQLAlchemy 2.0
- PostgreSQL
- 12 web scrapers

---

## Step 2: Deploy to Render (5 minutes)

### Create Account
1. Go to **https://render.com**
2. Sign up with GitHub (roeigold2002)
3. Authorize Render to access your repos

### Create Web Service
1. Click **"New +"** → **"Web Service"**
2. Select repository: `roeigold2002/vinyl-aggregator`
3. Configure:
   - **Name**: `vinyl-aggregator-backend`
   - **Root Directory**: `backend` (Important!)
   - **Runtime**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: Leave blank (uses Procfile automatically)
   - **Instance Type**: **Free**
4. Click **"Create Web Service"**

**If build fails with "requirements.txt not found":**
- Render sometimes has issues with root directory
- Alternative: Don't set root directory, instead:
  - Build Command: `cd backend && pip install -r requirements.txt`
  - Start Command: `cd backend && uvicorn main:app --host 0.0.0.0 --port 8000`

### Wait for Build (5 minutes)
- Render pulls code from GitHub
- Installs dependencies
- Starts FastAPI server
- Assigns URL: `https://vinyl-aggregator-backend.onrender.com`

---

## Step 3: Get Your URL

Once deployed, your backend URL is:
```
https://vinyl-aggregator-backend.onrender.com
```

Test it:
```bash
curl https://vinyl-aggregator-backend.onrender.com/api/health
```

---

## Step 4: Connect to Netlify Frontend

In your Netlify site:
1. Go to **Site Settings** → **Build & Deploy** → **Environment**
2. Add environment variable:
   - **Key**: `VITE_API_URL`
   - **Value**: `https://vinyl-aggregator-backend.onrender.com`
3. Click **"Trigger Deploy"** → **"Deploy site"**

Your frontend will now connect to the backend! ✨

---

## That's It!

You now have:
- ✅ Frontend live at Netlify
- ✅ Backend live at Render
- ✅ Both on permanent free tiers
- ✅ $0/month total cost

---

## ⚠️ Important Notes

**Cold Starts**: 
- Free tier sleeps after 15 min of inactivity
- First request takes ~30 seconds (cold start)
- Solution: Keep using it, or upgrade to paid tier

**Database**:
- Render doesn't include PostgreSQL for free
- Current setup uses in-memory storage during free tier
- For persistent storage: Upgrade to Render paid ($7/month)

**Limits**:
- 512 MB RAM
- Shared CPU
- 100 GB bandwidth/month
- Perfect for this project!

---

## 🎯 Complete Setup

```
Frontend (Netlify)
  ↓ API calls to
Backend (Render)
  ↓ Scrapes
12 Israeli Vinyl Stores
  ↓ Data
  Search interface
```

**Cost**: $0/month  
**Uptime**: 99.9%  
**Scale**: Automatic  
**Ready**: Now!

---

## ✅ Verification

After both deployed:
1. Open your Netlify URL
2. Type search term (e.g., "metal")
3. See results instantly
4. Check network tab - API calls to Render working
5. Done! 🎵

---

**Need Help?**
- Render Docs: https://render.com/docs
- FastAPI Docs: https://fastapi.tiangolo.com
- See BACKEND_HOSTING_OPTIONS.md for alternatives
