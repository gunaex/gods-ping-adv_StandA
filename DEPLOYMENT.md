# 🚀 Gods Ping Deployment Guide

## 📋 Prerequisites

- GitHub account
- Render account (https://render.com)
- Vercel account (https://vercel.com)
- Git installed locally

---

## 🔧 Backend Deployment (Render)

### Step 1: Prepare Repository

1. **Push to GitHub:**
   ```bash
   cd d:\git\gods-ping
   git add .
   git commit -m "Prepare for deployment"
   git push origin main
   ```

### Step 2: Deploy on Render

1. **Go to Render Dashboard:**
   - Visit https://dashboard.render.com
   - Click **"New +"** → **"Web Service"**

2. **Connect Repository:**
   - Connect your GitHub account
   - Select `gods-ping` repository
   - Click **"Connect"**

3. **Configure Service:**
   - **Name:** `gods-ping-backend`
   - **Region:** Singapore (or closest to you)
   - **Branch:** `main`
   - **Root Directory:** `backend`
   - **Environment:** `Python 3`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

4. **Set Environment Variables:**
   
   Click **"Advanced"** → **"Add Environment Variable"**:
   
   ```
   SECRET_KEY = [Generate random 32-char string]
   ALGORITHM = HS256
   ACCESS_TOKEN_EXPIRE_MINUTES = 43200
   ENCRYPTION_KEY = [Generate random 32-char base64 string]
   CORS_ORIGINS = https://your-frontend.vercel.app
   ```

   **Generate SECRET_KEY:**
   ```python
   import secrets
   print(secrets.token_urlsafe(32))
   ```

   **Generate ENCRYPTION_KEY:**
   ```python
   from cryptography.fernet import Fernet
   print(Fernet.generate_key().decode())
   ```

5. **Deploy:**
   - Click **"Create Web Service"**
   - Wait for deployment (5-10 minutes)
   - Copy the service URL: `https://gods-ping-backend.onrender.com`

---

## 🎨 Frontend Deployment (Vercel)

### Step 1: Update API URL

1. **Edit `frontend/vite.config.ts`:**
   ```typescript
   export default defineConfig({
     server: {
       proxy: {
         '/api': {
           target: 'https://gods-ping-backend.onrender.com', // Your Render URL
           changeOrigin: true,
         }
       }
     }
   })
   ```

2. **Or use environment variable:**
   
   Create `frontend/.env.production`:
   ```
   VITE_API_URL=https://gods-ping-backend.onrender.com
   ```

### Step 2: Deploy on Vercel

1. **Go to Vercel Dashboard:**
   - Visit https://vercel.com/new
   - Click **"Import Project"**

2. **Connect Repository:**
   - Connect GitHub account
   - Select `gods-ping` repository
   - Click **"Import"**

3. **Configure Project:**
   - **Framework Preset:** Vite
   - **Root Directory:** `frontend`
   - **Build Command:** `npm run build`
   - **Output Directory:** `dist`

4. **Set Environment Variables:**
   ```
   VITE_API_URL = https://gods-ping-backend.onrender.com
   ```

5. **Deploy:**
   - Click **"Deploy"**
   - Wait for deployment (2-5 minutes)
   - Your app will be live at: `https://gods-ping.vercel.app`

---

## 🔄 Update Backend CORS

After frontend is deployed, update backend environment variables on Render:

1. Go to Render Dashboard → Your Service → Environment
2. Update `CORS_ORIGINS`:
   ```
   CORS_ORIGINS = https://gods-ping.vercel.app,http://localhost:5173
   ```
3. Save (this will trigger a redeploy)

---

## ✅ Post-Deployment Checklist

### Test Backend
- [ ] Visit: `https://gods-ping-backend.onrender.com/`
- [ ] Should see: `{"message": "Gods Ping API"}`
- [ ] Check: `https://gods-ping-backend.onrender.com/docs`

### Test Frontend
- [ ] Visit: `https://gods-ping.vercel.app`
- [ ] Login with admin credentials
- [ ] Check all features work
- [ ] Test trading operations

### Database
- [ ] Backend automatically creates SQLite database
- [ ] First deployment creates admin user
- [ ] For production, consider PostgreSQL:
  - Render provides free PostgreSQL
  - Update `DATABASE_URL` environment variable

---

## 🔐 Security Notes

### 1. Change Default Credentials
After first deployment, immediately change admin password!

### 2. Secure API Keys
- Never commit `.env` files
- Use Render's environment variables
- Each user sets their own Binance API keys

### 3. HTTPS Only
- Both Render and Vercel provide free SSL
- All communication is encrypted

---

## 📊 Database Migration (Optional - PostgreSQL)

If you want persistent database instead of SQLite:

### 1. Create PostgreSQL Database on Render

1. Render Dashboard → **"New +"** → **"PostgreSQL"**
2. Name: `gods-ping-db`
3. Region: Same as backend
4. Plan: Free
5. Create database

### 2. Update Backend Environment

1. Copy **Internal Database URL** from PostgreSQL dashboard
2. Update backend environment variable:
   ```
   DATABASE_URL = postgresql://user:pass@host/dbname
   ```

### 3. Update `backend/app/db.py`

```python
# Change from:
SQLALCHEMY_DATABASE_URL = "sqlite:///./gods_ping.db"

# To:
import os
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./gods_ping.db")
```

### 4. Install PostgreSQL Driver

Add to `requirements.txt`:
```
psycopg2-binary>=2.9.9
```

---

## 🔄 Continuous Deployment

Both Render and Vercel auto-deploy when you push to GitHub:

```bash
# Make changes
git add .
git commit -m "Update feature"
git push origin main

# Render and Vercel automatically redeploy!
```

---

## 🐛 Troubleshooting

### Backend Issues

**Problem:** Service won't start
- Check logs in Render Dashboard
- Verify all environment variables are set
- Check `requirements.txt` syntax

**Problem:** CORS errors
- Update `CORS_ORIGINS` with frontend URL
- Don't include trailing slash

**Problem:** Database errors
- Delete `gods_ping.db` and redeploy (recreates DB)
- Or migrate to PostgreSQL

### Frontend Issues

**Problem:** Can't connect to backend
- Check `VITE_API_URL` is correct
- Verify backend is running
- Check browser console for errors

**Problem:** Build fails
- Check `package.json` dependencies
- Run `npm install` locally first
- Check Node version (should be 18+)

---

## 💰 Cost Breakdown

### Free Tier (Recommended for Testing)

**Render Free:**
- ✅ 750 hours/month (enough for 1 service)
- ✅ Auto-sleep after 15 mins inactivity
- ✅ Wakes up in ~30 seconds
- ❌ Spins down daily

**Vercel Free:**
- ✅ 100 GB bandwidth/month
- ✅ Unlimited deployments
- ✅ Always on (no sleep)
- ✅ Global CDN

**Total: $0/month** 🎉

### Production (Paid)

**Render Starter ($7/month):**
- ✅ No sleep
- ✅ Always on
- ✅ 400 build minutes

**Vercel Pro ($20/month):**
- ✅ 1 TB bandwidth
- ✅ Priority support
- ✅ Custom domains

**Total: ~$27/month**

---

## 🎯 Next Steps

1. **Deploy Backend** → Get Render URL
2. **Update Frontend** → Point to Render URL
3. **Deploy Frontend** → Get Vercel URL
4. **Update CORS** → Add Vercel URL to backend
5. **Test Everything** → Login, trade, verify
6. **Monitor** → Check logs regularly
7. **Optimize** → Consider PostgreSQL for production

---

## 📞 Support

- **Render Docs:** https://render.com/docs
- **Vercel Docs:** https://vercel.com/docs
- **FastAPI Docs:** https://fastapi.tiangolo.com
- **Vite Docs:** https://vitejs.dev

---

## 🎉 You're Ready!

Your trading bot will be live and accessible from anywhere in the world! 🌍🚀

Good luck with your deployment! 📈💰
