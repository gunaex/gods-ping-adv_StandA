# 📝 Deployment Checklist

## Before Deployment

- [ ] All code committed to Git
- [ ] `.env` files are in `.gitignore`
- [ ] Test locally: Backend runs on port 8000
- [ ] Test locally: Frontend connects to backend
- [ ] Database migrations run successfully
- [ ] All dependencies in `requirements.txt`

## Backend Deployment (Render)

- [ ] Repository pushed to GitHub
- [ ] Render account created
- [ ] Web Service created
- [ ] Root directory set to `backend`
- [ ] Environment variables configured:
  - [ ] SECRET_KEY (generate new)
  - [ ] ENCRYPTION_KEY (generate new)
  - [ ] ALGORITHM (HS256)
  - [ ] ACCESS_TOKEN_EXPIRE_MINUTES (43200)
  - [ ] CORS_ORIGINS (add frontend URL later)
- [ ] Build command: `pip install -r requirements.txt`
- [ ] Start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
- [ ] Service deployed successfully
- [ ] Backend URL copied: `https://________.onrender.com`
- [ ] Test endpoint: `https://________.onrender.com/`
- [ ] API docs accessible: `https://________.onrender.com/docs`

## Frontend Deployment (Vercel)

- [ ] Vercel account created
- [ ] Project imported from GitHub
- [ ] Root directory set to `frontend`
- [ ] Framework preset: Vite
- [ ] Environment variables configured:
  - [ ] VITE_API_URL (your Render backend URL)
- [ ] Build command: `npm run build`
- [ ] Output directory: `dist`
- [ ] Deployment successful
- [ ] Frontend URL: `https://________.vercel.app`
- [ ] Can access login page
- [ ] Can login with admin credentials

## Post-Deployment

- [ ] Update backend CORS_ORIGINS with frontend URL
- [ ] Backend redeployed with new CORS settings
- [ ] Test login from deployed frontend
- [ ] Test trading pair selection
- [ ] Test AI recommendations
- [ ] Test Gods Hand execution
- [ ] Verify paper trading works
- [ ] Check all charts load correctly

## Security Checklist

- [ ] Default admin password changed
- [ ] SECRET_KEY is unique and secure
- [ ] ENCRYPTION_KEY is unique and secure
- [ ] API keys stored in user accounts only (not in env)
- [ ] HTTPS enforced (automatic on Render/Vercel)
- [ ] CORS configured correctly

## Monitoring

- [ ] Render dashboard bookmarked
- [ ] Vercel dashboard bookmarked
- [ ] Backend logs accessible
- [ ] Frontend analytics configured (optional)
- [ ] Error tracking set up (optional)

## Optional Upgrades

- [ ] PostgreSQL database instead of SQLite
- [ ] Custom domain configured
- [ ] Email notifications configured
- [ ] Backup strategy implemented
- [ ] Monitoring alerts set up

---

## 🎯 Deployment URLs

**Backend:** https://________.onrender.com  
**Frontend:** https://________.vercel.app  
**Admin Login:** Admin / [your-password]

---

## 📊 Free Tier Limits

**Render:**
- 750 hours/month (1 service = ~720 hours)
- Service sleeps after 15 mins inactivity
- Wakes in ~30 seconds on request

**Vercel:**
- 100 GB bandwidth/month
- No sleep/downtime
- Unlimited deployments

---

## 🚀 Ready to Deploy?

1. Read `DEPLOYMENT.md` thoroughly
2. Complete this checklist step-by-step
3. Test everything after deployment
4. Monitor for first 24 hours

Good luck! 🎉
