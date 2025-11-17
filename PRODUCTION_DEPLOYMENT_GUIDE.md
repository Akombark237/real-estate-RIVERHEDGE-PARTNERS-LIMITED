# 🚀 RIVERHEDGE PARTNERS - PRODUCTION DEPLOYMENT GUIDE

## 📋 **DEPLOYMENT OPTIONS**

Choose the deployment option that best fits your needs:

### **Option 1: Render.com (RECOMMENDED - Easiest)** ⭐⭐⭐⭐⭐
- ✅ **FREE tier available**
- ✅ **Automatic HTTPS**
- ✅ **Easy setup (15 minutes)**
- ✅ **PostgreSQL included**
- ✅ **Auto-deploy from Git**
- ✅ **Best for beginners**

### **Option 2: Railway.app** ⭐⭐⭐⭐
- ✅ **$5/month starter**
- ✅ **Very easy setup**
- ✅ **Great developer experience**
- ✅ **PostgreSQL included**

### **Option 3: DigitalOcean App Platform** ⭐⭐⭐⭐
- 💰 **$12/month**
- ✅ **Scalable**
- ✅ **Good performance**
- ✅ **Database included**

### **Option 4: Heroku** ⭐⭐⭐
- 💰 **$7/month minimum**
- ✅ **Well-documented**
- ⚠️ **More expensive**

### **Option 5: VPS (DigitalOcean Droplet, AWS EC2)** ⭐⭐
- 💰 **$6-10/month**
- ⚠️ **Requires server management**
- ⚠️ **More complex setup**
- ✅ **Full control**

---

## 🎯 **RECOMMENDED: DEPLOY TO RENDER.COM**

This guide will walk you through deploying to **Render.com** (FREE tier).

---

## 📦 **PRE-DEPLOYMENT CHECKLIST**

Before deploying, ensure:

- ✅ All features tested locally
- ✅ Database migrations are up to date
- ✅ Git repository is set up
- ✅ Environment variables are documented
- ✅ Static files configuration is correct
- ✅ CORS settings are configured
- ✅ Email settings are configured (optional)

---

## 🔧 **STEP 1: PREPARE YOUR PROJECT**

### **1.1 Create Production Requirements**

Create `requirements-prod.txt`:
```bash
# Copy from requirements.txt and add production dependencies
gunicorn==21.2.0
whitenoise==6.6.0
dj-database-url==2.1.0
```

### **1.2 Create Procfile**

Create a file named `Procfile` (no extension) in the root directory:
```
web: gunicorn real_estate_platform.wsgi --log-file -
```

### **1.3 Create build.sh Script**

Create `build.sh` in the root directory:
```bash
#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt
pip install gunicorn whitenoise dj-database-url

python manage.py collectstatic --no-input
python manage.py migrate
```

### **1.4 Update settings.py for Production**

We'll add production-specific settings that activate when `DEBUG=False`.

### **1.5 Create .env for Production**

You'll configure environment variables in Render's dashboard.

---

## 🌐 **STEP 2: DEPLOY BACKEND TO RENDER.COM**

### **2.1 Create Render Account**

1. Go to https://render.com
2. Sign up with GitHub (recommended)
3. Verify your email

### **2.2 Create PostgreSQL Database**

1. Click **"New +"** → **"PostgreSQL"**
2. Configure:
   - **Name:** `riverhedge-db`
   - **Database:** `riverhedge_db`
   - **User:** `riverhedge_user`
   - **Region:** Choose closest to your users
   - **Plan:** **Free** (or paid for better performance)
3. Click **"Create Database"**
4. **Copy the Internal Database URL** (you'll need this)

### **2.3 Create Web Service**

1. Click **"New +"** → **"Web Service"**
2. Connect your GitHub repository
3. Configure:
   - **Name:** `riverhedge-backend`
   - **Region:** Same as database
   - **Branch:** `main` (or your branch)
   - **Root Directory:** Leave empty
   - **Runtime:** `Python 3`
   - **Build Command:** `./build.sh`
   - **Start Command:** `gunicorn real_estate_platform.wsgi:application`
   - **Plan:** **Free** (or paid)

### **2.4 Add Environment Variables**

In the **Environment** section, add:

```
SECRET_KEY=your-super-secret-key-generate-a-new-one
DEBUG=False
ALLOWED_HOSTS=your-app-name.onrender.com
DATABASE_URL=<paste-internal-database-url-from-step-2.2>
CORS_ALLOWED_ORIGINS=https://your-frontend-url.onrender.com
FRONTEND_URL=https://your-frontend-url.onrender.com
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

**Generate SECRET_KEY:**
```python
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

4. Click **"Create Web Service"**
5. Wait for deployment (5-10 minutes)

### **2.5 Create Superuser**

After deployment:
1. Go to your service → **Shell** tab
2. Run:
```bash
python manage.py createsuperuser
```

---

## 🎨 **STEP 3: DEPLOY FRONTEND TO RENDER.COM**

### **3.1 Update Frontend Configuration**

Update `frontend/vite.config.js`:
```javascript
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    proxy: {
      '/api': {
        target: process.env.VITE_API_URL || 'http://localhost:8000',
        changeOrigin: true,
      },
    },
  },
  build: {
    outDir: 'dist',
    sourcemap: false,
  },
})
```

Create `frontend/.env.production`:
```
VITE_API_URL=https://your-backend-url.onrender.com
```

### **3.2 Create Static Site on Render**

1. Click **"New +"** → **"Static Site"**
2. Connect your GitHub repository
3. Configure:
   - **Name:** `riverhedge-frontend`
   - **Branch:** `main`
   - **Root Directory:** `frontend`
   - **Build Command:** `npm install && npm run build`
   - **Publish Directory:** `dist`
4. Add Environment Variable:
   - `VITE_API_URL` = `https://your-backend-url.onrender.com`
5. Click **"Create Static Site"**

---

## ✅ **STEP 4: POST-DEPLOYMENT CONFIGURATION**

### **4.1 Update Backend CORS Settings**

Update your backend environment variables with the actual frontend URL:
```
CORS_ALLOWED_ORIGINS=https://your-frontend-url.onrender.com
```

### **4.2 Update Frontend API URL**

Update `frontend/src/context/AuthContext.jsx` to use environment variable:
```javascript
const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'
axios.defaults.baseURL = API_URL
```

### **4.3 Test Your Deployment**

1. Visit your frontend URL
2. Register a new user
3. Login
4. Test all features
5. Check admin panel: `https://your-backend-url.onrender.com/admin`

---

## 🔒 **STEP 5: SECURITY CHECKLIST**

- ✅ `DEBUG=False` in production
- ✅ Strong `SECRET_KEY` generated
- ✅ `ALLOWED_HOSTS` configured
- ✅ HTTPS enabled (automatic on Render)
- ✅ CORS properly configured
- ✅ Database credentials secure
- ✅ Environment variables not in code

---

## 📊 **STEP 6: MONITORING & MAINTENANCE**

### **6.1 Monitor Logs**

- Render Dashboard → Your Service → **Logs** tab
- Check for errors regularly

### **6.2 Database Backups**

Render Free tier: Manual backups
Render Paid tier: Automatic daily backups

**Manual Backup:**
```bash
# In Render Shell
pg_dump $DATABASE_URL > backup.sql
```

### **6.3 Update Deployment**

Render auto-deploys when you push to GitHub:
```bash
git add .
git commit -m "Update feature"
git push origin main
```

---

## 💰 **COST BREAKDOWN**

### **Free Tier (Render.com):**
- Backend: FREE (spins down after 15 min inactivity)
- Frontend: FREE
- Database: FREE (90 days, then $7/month)
- **Total: $0/month** (first 90 days)

### **Paid Tier (Recommended for Production):**
- Backend: $7/month (always on)
- Frontend: FREE
- Database: $7/month
- **Total: $14/month**

---

## 🎊 **DEPLOYMENT COMPLETE!**

Your RIVERHEDGE PARTNERS platform is now live! 🚀

**Next Steps:**
1. Share the URL with users
2. Monitor performance
3. Set up custom domain (optional)
4. Configure email notifications
5. Add analytics (Google Analytics)


