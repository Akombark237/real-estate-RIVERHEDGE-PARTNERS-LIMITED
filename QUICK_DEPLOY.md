# ⚡ QUICK DEPLOY GUIDE - 15 MINUTES TO PRODUCTION

## 🎯 **FASTEST WAY TO DEPLOY**

This guide will get your RIVERHEDGE PARTNERS platform live in **15 minutes**.

---

## 📋 **WHAT YOU NEED**

1. ✅ GitHub account
2. ✅ Gmail account (for email notifications)
3. ✅ 15 minutes of time

---

## 🚀 **STEP-BY-STEP (15 MINUTES)**

### **STEP 1: Push to GitHub (2 minutes)**

```bash
# In your project root directory
git init
git add .
git commit -m "Initial commit - Ready for deployment"

# Create a new repository on GitHub, then:
git remote add origin https://github.com/YOUR-USERNAME/riverhedge-platform.git
git branch -M main
git push -u origin main
```

---

### **STEP 2: Sign Up for Render (1 minute)**

1. Go to https://render.com
2. Click **"Get Started"**
3. Sign up with GitHub
4. Authorize Render to access your repositories

---

### **STEP 3: Create Database (2 minutes)**

1. Click **"New +"** → **"PostgreSQL"**
2. Settings:
   - **Name:** `riverhedge-db`
   - **Database:** `riverhedge_db`
   - **Region:** Choose closest to you
   - **Plan:** **Free**
3. Click **"Create Database"**
4. **IMPORTANT:** Copy the **Internal Database URL** (starts with `postgresql://`)

---

### **STEP 4: Deploy Backend (5 minutes)**

1. Click **"New +"** → **"Web Service"**
2. Select your GitHub repository
3. Settings:
   - **Name:** `riverhedge-backend`
   - **Region:** Same as database
   - **Branch:** `main`
   - **Runtime:** `Python 3`
   - **Build Command:** `./build.sh`
   - **Start Command:** `gunicorn real_estate_platform.wsgi:application`
   - **Plan:** **Free**

4. Click **"Advanced"** → **"Add Environment Variable"**

5. Add these variables (click "+ Add Environment Variable" for each):

```
SECRET_KEY
<paste-the-key-generated-below>

DEBUG
False

ALLOWED_HOSTS
riverhedge-backend.onrender.com

DATABASE_URL
<paste-the-database-url-from-step-3>

CORS_ALLOWED_ORIGINS
https://riverhedge-frontend.onrender.com

FRONTEND_URL
https://riverhedge-frontend.onrender.com

EMAIL_BACKEND
django.core.mail.backends.smtp.EmailBackend

EMAIL_HOST
smtp.gmail.com

EMAIL_PORT
587

EMAIL_USE_TLS
True

EMAIL_HOST_USER
your-email@gmail.com

EMAIL_HOST_PASSWORD
<your-gmail-app-password>
```

**Generate SECRET_KEY:**
Open Python and run:
```python
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

**Get Gmail App Password:**
1. Go to https://myaccount.google.com/apppasswords
2. Create app password for "Mail"
3. Copy the 16-character password

6. Click **"Create Web Service"**
7. Wait 5 minutes for deployment

---

### **STEP 5: Create Admin User (1 minute)**

1. Go to your backend service
2. Click **"Shell"** tab
3. Run:
```bash
python manage.py createsuperuser
```
4. Enter email, username, password

---

### **STEP 6: Deploy Frontend (3 minutes)**

1. Click **"New +"** → **"Static Site"**
2. Select your GitHub repository
3. Settings:
   - **Name:** `riverhedge-frontend`
   - **Branch:** `main`
   - **Root Directory:** `frontend`
   - **Build Command:** `npm install && npm run build`
   - **Publish Directory:** `dist`

4. Add Environment Variable:
```
VITE_API_URL
https://riverhedge-backend.onrender.com
```

5. Click **"Create Static Site"**
6. Wait 3 minutes for deployment

---

### **STEP 7: Update CORS (1 minute)**

1. Go back to your **backend service**
2. Go to **"Environment"** tab
3. Update `CORS_ALLOWED_ORIGINS` to your actual frontend URL:
```
https://riverhedge-frontend.onrender.com
```
4. Click **"Save Changes"**
5. Backend will auto-redeploy

---

## ✅ **DONE! YOUR PLATFORM IS LIVE!**

**Your URLs:**
- 🌐 **Frontend:** https://riverhedge-frontend.onrender.com
- 🔧 **Backend:** https://riverhedge-backend.onrender.com
- 👨‍💼 **Admin:** https://riverhedge-backend.onrender.com/admin
- 📚 **API Docs:** https://riverhedge-backend.onrender.com/api/docs

---

## 🧪 **TEST YOUR DEPLOYMENT**

1. Visit your frontend URL
2. Click **"Register"**
3. Create a new account
4. Login
5. Test the platform!

**Note:** Client users will only see the About page (as configured).

To test as admin:
1. Go to admin panel: `https://riverhedge-backend.onrender.com/admin`
2. Login with superuser credentials
3. Go to **Users**
4. Change a user's role to **"admin"**
5. Login as that user on the frontend

---

## 💰 **COST**

**FREE for 90 days!**
- Backend: FREE (spins down after 15 min inactivity)
- Frontend: FREE
- Database: FREE for 90 days

After 90 days:
- Database: $7/month
- Backend (always on): $7/month (optional)
- **Total: $7-14/month**

---

## 🎊 **CONGRATULATIONS!**

Your RIVERHEDGE PARTNERS Real Estate Platform is now live and accessible worldwide! 🚀

**What's Next?**
- Share the URL with your team
- Add sample properties and data
- Configure a custom domain (optional)
- Set up monitoring and backups
- Train users on the platform

---

## 🆘 **TROUBLESHOOTING**

### **Backend deployment failed:**
- Check the logs in Render dashboard
- Verify all environment variables are set
- Make sure `build.sh` is in your repository

### **Frontend can't connect to backend:**
- Verify `VITE_API_URL` matches your backend URL
- Check CORS settings in backend
- Clear browser cache

### **Database connection error:**
- Verify `DATABASE_URL` is correct
- Make sure database is in the same region as backend

### **Email not working:**
- Verify Gmail app password is correct
- Check EMAIL_HOST_USER is your Gmail address
- Make sure 2-Step Verification is enabled on Gmail

---

## 📞 **NEED HELP?**

Check the full deployment guide: `PRODUCTION_DEPLOYMENT_GUIDE.md`

Or the detailed checklist: `DEPLOYMENT_CHECKLIST.md`


