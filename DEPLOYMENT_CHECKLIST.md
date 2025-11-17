# 🚀 DEPLOYMENT CHECKLIST - RIVERHEDGE PARTNERS

## ✅ **PRE-DEPLOYMENT CHECKLIST**

### **1. Code Preparation**
- [ ] All features tested locally
- [ ] All tests passing
- [ ] No console errors in browser
- [ ] Database migrations up to date
- [ ] Git repository is clean (no uncommitted changes)
- [ ] `.gitignore` includes `.env`, `db.sqlite3`, `venv/`, `node_modules/`

### **2. Environment Configuration**
- [ ] `.env.example` file created
- [ ] `.env.production.example` file created
- [ ] `frontend/.env.production.example` file created
- [ ] All sensitive data removed from code
- [ ] SECRET_KEY is environment variable
- [ ] DEBUG is environment variable

### **3. Production Files Created**
- [ ] `Procfile` created
- [ ] `build.sh` created (and made executable)
- [ ] `runtime.txt` created
- [ ] `requirements.txt` up to date

### **4. Settings Configuration**
- [ ] `settings.py` uses environment variables
- [ ] Database configured for PostgreSQL
- [ ] WhiteNoise middleware added
- [ ] CORS settings use environment variables
- [ ] Email settings use environment variables
- [ ] Static files configuration correct
- [ ] Media files configuration correct
- [ ] Security settings for production added

### **5. Frontend Configuration**
- [ ] `vite.config.js` configured for production
- [ ] API URL uses environment variable
- [ ] Build command works: `npm run build`
- [ ] No hardcoded API URLs in code

---

## 🌐 **DEPLOYMENT STEPS (Render.com)**

### **Step 1: Create Render Account**
- [ ] Sign up at https://render.com
- [ ] Verify email address
- [ ] Connect GitHub account

### **Step 2: Push Code to GitHub**
- [ ] Create GitHub repository
- [ ] Push all code to GitHub
- [ ] Verify all files are pushed

```bash
git add .
git commit -m "Prepare for production deployment"
git push origin main
```

### **Step 3: Create PostgreSQL Database**
- [ ] Create new PostgreSQL database on Render
- [ ] Name: `riverhedge-db`
- [ ] Region: Choose closest to users
- [ ] Plan: Free (or paid)
- [ ] Copy Internal Database URL

### **Step 4: Deploy Backend**
- [ ] Create new Web Service on Render
- [ ] Connect GitHub repository
- [ ] Configure build settings:
  - Build Command: `./build.sh`
  - Start Command: `gunicorn real_estate_platform.wsgi:application`
- [ ] Add environment variables (see list below)
- [ ] Deploy and wait for completion

### **Step 5: Backend Environment Variables**
Add these in Render Dashboard:

```
SECRET_KEY=<generate-new-secret-key>
DEBUG=False
ALLOWED_HOSTS=<your-backend-url>.onrender.com
DATABASE_URL=<paste-from-step-3>
CORS_ALLOWED_ORIGINS=https://<your-frontend-url>.onrender.com
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=<your-email@gmail.com>
EMAIL_HOST_PASSWORD=<your-gmail-app-password>
FRONTEND_URL=https://<your-frontend-url>.onrender.com
```

- [ ] All environment variables added
- [ ] SECRET_KEY generated (use command below)
- [ ] Gmail app password created

**Generate SECRET_KEY:**
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### **Step 6: Create Superuser**
- [ ] Go to backend service → Shell tab
- [ ] Run: `python manage.py createsuperuser`
- [ ] Create admin account

### **Step 7: Deploy Frontend**
- [ ] Create new Static Site on Render
- [ ] Connect GitHub repository
- [ ] Configure:
  - Root Directory: `frontend`
  - Build Command: `npm install && npm run build`
  - Publish Directory: `dist`
- [ ] Add environment variable:
  - `VITE_API_URL` = `https://<your-backend-url>.onrender.com`
- [ ] Deploy and wait for completion

### **Step 8: Update CORS Settings**
- [ ] Update backend `CORS_ALLOWED_ORIGINS` with actual frontend URL
- [ ] Redeploy backend if needed

---

## 🧪 **POST-DEPLOYMENT TESTING**

### **Backend Testing**
- [ ] Visit backend URL (should show "Not Found" - this is normal)
- [ ] Visit `<backend-url>/admin` - Admin panel loads
- [ ] Login to admin panel
- [ ] Visit `<backend-url>/api/docs` - API documentation loads

### **Frontend Testing**
- [ ] Visit frontend URL
- [ ] Register a new user
- [ ] Login successfully
- [ ] Test all pages:
  - [ ] Dashboard (admin/agent only)
  - [ ] Materials
  - [ ] Properties
  - [ ] Transactions
  - [ ] Cost Estimates
  - [ ] Reports
  - [ ] Documents
  - [ ] Activity Logs
  - [ ] About (all users)
  - [ ] Profile
- [ ] Test role-based access (client sees only About)
- [ ] Test file uploads
- [ ] Test notifications
- [ ] Check browser console for errors

### **Email Testing**
- [ ] Test password reset email
- [ ] Test notification emails
- [ ] Verify email links work

---

## 🔒 **SECURITY CHECKLIST**

- [ ] `DEBUG=False` in production
- [ ] Strong `SECRET_KEY` generated
- [ ] `ALLOWED_HOSTS` configured correctly
- [ ] HTTPS enabled (automatic on Render)
- [ ] CORS properly configured
- [ ] Database credentials secure
- [ ] No sensitive data in Git repository
- [ ] `.env` file in `.gitignore`
- [ ] Security headers enabled
- [ ] SSL redirect enabled

---

## 📊 **MONITORING**

### **Set Up Monitoring**
- [ ] Check Render logs regularly
- [ ] Set up error notifications
- [ ] Monitor database usage
- [ ] Monitor bandwidth usage

### **Backup Strategy**
- [ ] Database backups enabled (paid plan)
- [ ] Or set up manual backup schedule
- [ ] Test backup restoration

---

## 🎊 **DEPLOYMENT COMPLETE!**

Once all checkboxes are checked, your platform is live! 🚀

**Your URLs:**
- Frontend: `https://<your-frontend>.onrender.com`
- Backend: `https://<your-backend>.onrender.com`
- Admin: `https://<your-backend>.onrender.com/admin`
- API Docs: `https://<your-backend>.onrender.com/api/docs`

---

## 📝 **NEXT STEPS**

- [ ] Share URLs with stakeholders
- [ ] Create user accounts for team
- [ ] Add sample data
- [ ] Set up custom domain (optional)
- [ ] Configure Google Analytics (optional)
- [ ] Set up monitoring/alerts
- [ ] Document any custom configurations
- [ ] Train users on the platform

---

## 🆘 **TROUBLESHOOTING**

### **Backend won't start:**
- Check Render logs for errors
- Verify all environment variables are set
- Verify `build.sh` is executable
- Check database connection

### **Frontend can't connect to backend:**
- Verify `VITE_API_URL` is correct
- Check CORS settings
- Check browser console for errors
- Verify backend is running

### **Static files not loading:**
- Run `python manage.py collectstatic`
- Check WhiteNoise configuration
- Verify `STATIC_ROOT` setting

### **Database errors:**
- Verify `DATABASE_URL` is correct
- Run migrations: `python manage.py migrate`
- Check database connection

---

## 📞 **SUPPORT**

If you encounter issues:
1. Check Render documentation
2. Check Django documentation
3. Check application logs
4. Search for error messages
5. Contact Render support (if platform issue)


