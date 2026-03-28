# ⚡ NETLIFY DRAG & DROP - 3 MINUTES TO LIVE

**Fastest deployment method - just drag and drop!**

---

## Step 1: Build Your Site (1 minute)

```bash
cd frontend
npm install
npm run build
```

This creates a `dist/` folder with your optimized website.

---

## Step 2: Drag & Drop (30 seconds)

1. Go to: **https://app.netlify.com/drop**
2. **Drag the `frontend/dist/` folder** into the drop zone
3. Watch it deploy in real-time
4. **Your URL is ready!** 🚀

Example: `https://vinyl-aggregator-xxxx.netlify.app`

---

## Step 3: Configure Backend (1 minute)

Your frontend needs to know where the backend is. Choose a backend option:

### Option A: Render.com (Recommended - Permanently Free)
1. Go to https://render.com
2. Deploy `backend/` folder (free tier, no credit card needed)
3. Copy your Render URL: `https://your-app.onrender.com`
4. Configure in Netlify:
   - Go to your Netlify site dashboard
   - Click **"Site Settings"** → **"Build & Deploy"** → **"Environment"**
   - Add: `VITE_API_URL=https://your-app.onrender.com`
   - Trigger redeploy

### Option B: Railway (After Free 30 Days)
- First 30 days: Free
- After: $5/month minimum
- Use only if you're committed to paying

### Option C: Heroku Alternative
- Replit, Fly.io, or other free options available

---

## That's It! 

Your site is now live and can talk to your backend! ✨

---

## Verification

Open your live URL and:
- [ ] Page loads
- [ ] Search bar appears
- [ ] No console errors
- [ ] Click search test

🎵 Done!

---

**Cost**: Free  
**Time**: 3 minutes  
**HTTPS**: Automatic  
**CDN**: Global  
**Ready to go**: Yes!
