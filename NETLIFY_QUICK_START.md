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

Your frontend needs to know where the backend is:

1. Go to your Netlify site dashboard
2. Click **"Site Settings"** → **"Build & Deploy"** → **"Environment"**
3. Click **"Edit variables"**
4. Add new variable:
   - **Key**: `VITE_API_URL`
   - **Value**: `https://your-railway-backend.railway.app`
5. Trigger redeploy: Click **"Trigger Deploy"** → **"Deploy site"**

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
