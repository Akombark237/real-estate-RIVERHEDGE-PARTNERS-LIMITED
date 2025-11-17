# Real Estate Platform - Deployment Guide

This guide covers deploying the Real Estate Software Platform to production.

## Pre-Deployment Checklist

Before deploying to production, ensure:

- [ ] All features have been tested locally
- [ ] Database migrations are up to date
- [ ] Environment variables are configured
- [ ] Static files are collected
- [ ] HTTPS/SSL certificate is ready
- [ ] Domain name is configured
- [ ] Backup strategy is in place

---

## Part 1: Backend Deployment (Django)

### Option A: Deploy to Heroku

#### 1. Install Heroku CLI

Download from: https://devcenter.heroku.com/articles/heroku-cli

#### 2. Prepare Django for Heroku

Create `Procfile` in project root:
```
web: gunicorn real_estate_platform.wsgi
```

Create `runtime.txt`:
```
python-3.13.7
```

Update `requirements.txt`:
```bash
pip install gunicorn psycopg2-binary dj-database-url whitenoise
pip freeze > requirements.txt
```

#### 3. Update settings.py

Add to `settings.py`:
```python
import dj_database_url

# Production settings
if not DEBUG:
    # Database
    DATABASES['default'] = dj_database_url.config(conn_max_age=600)
    
    # Static files
    MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
    
    # Security
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    X_FRAME_OPTIONS = 'DENY'
```

#### 4. Deploy to Heroku

```bash
heroku login
heroku create your-app-name
heroku addons:create heroku-postgresql:hobby-dev
git push heroku main
heroku run python manage.py migrate
heroku run python manage.py createsuperuser
heroku open
```

### Option B: Deploy to DigitalOcean

#### 1. Create a Droplet

1. Sign up at https://www.digitalocean.com
2. Create a new Droplet (Ubuntu 22.04)
3. Choose a plan ($6/month minimum)
4. Add SSH key
5. Create Droplet

#### 2. Connect to Server

```bash
ssh root@your-server-ip
```

#### 3. Install Dependencies

```bash
apt update
apt upgrade -y
apt install python3-pip python3-venv nginx postgresql postgresql-contrib -y
```

#### 4. Setup PostgreSQL

```bash
sudo -u postgres psql
CREATE DATABASE real_estate_db;
CREATE USER real_estate_user WITH PASSWORD 'your-secure-password';
GRANT ALL PRIVILEGES ON DATABASE real_estate_db TO real_estate_user;
\q
```

#### 5. Deploy Application

```bash
cd /var/www
git clone your-repository-url real_estate
cd real_estate
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install gunicorn
```

#### 6. Configure Environment Variables

Create `.env` file:
```bash
SECRET_KEY=your-secret-key-here
DEBUG=False
DATABASE_URL=postgresql://real_estate_user:your-secure-password@localhost/real_estate_db
ALLOWED_HOSTS=your-domain.com,www.your-domain.com
```

#### 7. Run Migrations

```bash
python manage.py migrate
python manage.py collectstatic
python manage.py createsuperuser
```

#### 8. Configure Gunicorn

Create `/etc/systemd/system/gunicorn.service`:
```ini
[Unit]
Description=gunicorn daemon
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/real_estate
ExecStart=/var/www/real_estate/venv/bin/gunicorn \
    --workers 3 \
    --bind unix:/var/www/real_estate/gunicorn.sock \
    real_estate_platform.wsgi:application

[Install]
WantedBy=multi-user.target
```

Start Gunicorn:
```bash
systemctl start gunicorn
systemctl enable gunicorn
```

#### 9. Configure Nginx

Create `/etc/nginx/sites-available/real_estate`:
```nginx
server {
    listen 80;
    server_name your-domain.com www.your-domain.com;

    location = /favicon.ico { access_log off; log_not_found off; }
    
    location /static/ {
        root /var/www/real_estate;
    }
    
    location /media/ {
        root /var/www/real_estate;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/var/www/real_estate/gunicorn.sock;
    }
}
```

Enable site:
```bash
ln -s /etc/nginx/sites-available/real_estate /etc/nginx/sites-enabled
nginx -t
systemctl restart nginx
```

#### 10. Setup SSL with Let's Encrypt

```bash
apt install certbot python3-certbot-nginx -y
certbot --nginx -d your-domain.com -d www.your-domain.com
```

---

## Part 2: Frontend Deployment (React)

### Option A: Deploy to Vercel (Recommended)

#### 1. Install Vercel CLI

```bash
npm install -g vercel
```

#### 2. Build Frontend

```bash
cd frontend
npm run build
```

#### 3. Deploy

```bash
vercel
```

Follow the prompts to deploy.

#### 4. Configure Environment Variables

In Vercel dashboard:
- Add `VITE_API_URL` = `https://your-backend-domain.com`

### Option B: Deploy to Netlify

#### 1. Build Frontend

```bash
cd frontend
npm run build
```

#### 2. Deploy via Netlify CLI

```bash
npm install -g netlify-cli
netlify deploy --prod --dir=dist
```

Or drag and drop the `dist` folder to Netlify dashboard.

#### 3. Configure Redirects

Create `frontend/public/_redirects`:
```
/*    /index.html   200
```

### Option C: Deploy to AWS S3 + CloudFront

#### 1. Create S3 Bucket

1. Go to AWS S3 Console
2. Create a new bucket
3. Enable static website hosting
4. Upload `dist` folder contents

#### 2. Create CloudFront Distribution

1. Go to CloudFront Console
2. Create distribution
3. Set origin to S3 bucket
4. Configure SSL certificate
5. Set default root object to `index.html`

#### 3. Update DNS

Point your domain to CloudFront distribution.

---

## Part 3: Database Migration

### Migrate from SQLite to PostgreSQL

#### 1. Backup SQLite Data

```bash
python manage.py dumpdata > backup.json
```

#### 2. Configure PostgreSQL

Update `settings.py`:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'real_estate_db',
        'USER': 'real_estate_user',
        'PASSWORD': 'your-password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

#### 3. Run Migrations

```bash
python manage.py migrate
```

#### 4. Load Data

```bash
python manage.py loaddata backup.json
```

---

## Part 4: Environment Variables

### Production Environment Variables

Create `.env` file:
```bash
# Django
SECRET_KEY=your-very-secret-key-here
DEBUG=False
ALLOWED_HOSTS=your-domain.com,www.your-domain.com

# Database
DATABASE_URL=postgresql://user:password@host:port/database

# Email (for notifications)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
EMAIL_USE_TLS=True

# AWS (for file storage)
AWS_ACCESS_KEY_ID=your-access-key
AWS_SECRET_ACCESS_KEY=your-secret-key
AWS_STORAGE_BUCKET_NAME=your-bucket-name
AWS_S3_REGION_NAME=us-east-1

# CORS
CORS_ALLOWED_ORIGINS=https://your-frontend-domain.com
```

---

## Part 5: Monitoring and Logging

### Setup Sentry for Error Tracking

```bash
pip install sentry-sdk
```

Add to `settings.py`:
```python
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

sentry_sdk.init(
    dsn="your-sentry-dsn",
    integrations=[DjangoIntegration()],
    traces_sample_rate=1.0,
)
```

### Setup Logging

Add to `settings.py`:
```python
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': '/var/log/django/error.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'ERROR',
            'propagate': True,
        },
    },
}
```

---

## Part 6: Backup Strategy

### Database Backups

#### Automated Daily Backups

Create `/usr/local/bin/backup_db.sh`:
```bash
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
pg_dump real_estate_db > /backups/db_$DATE.sql
find /backups -name "db_*.sql" -mtime +7 -delete
```

Add to crontab:
```bash
0 2 * * * /usr/local/bin/backup_db.sh
```

### Media Files Backup

Sync to S3:
```bash
aws s3 sync /var/www/real_estate/media s3://your-backup-bucket/media
```

---

## Part 7: Performance Optimization

### Enable Caching

Install Redis:
```bash
apt install redis-server
pip install django-redis
```

Add to `settings.py`:
```python
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}
```

### Enable Compression

Already configured with WhiteNoise for static files.

### Database Optimization

Add indexes to frequently queried fields in models.

---

## Part 8: Security Checklist

- [ ] DEBUG = False in production
- [ ] SECRET_KEY is secure and not in version control
- [ ] HTTPS/SSL is enabled
- [ ] ALLOWED_HOSTS is configured
- [ ] CORS is properly configured
- [ ] Database credentials are secure
- [ ] File upload validation is in place
- [ ] Rate limiting is configured
- [ ] Security headers are set
- [ ] Regular security updates are applied

---

## Part 9: Post-Deployment

### 1. Test Production Site

- [ ] Test user registration
- [ ] Test login/logout
- [ ] Test all CRUD operations
- [ ] Test file uploads
- [ ] Test API endpoints
- [ ] Test on mobile devices

### 2. Monitor Performance

- Check response times
- Monitor database queries
- Check error rates
- Monitor server resources

### 3. Setup Alerts

Configure alerts for:
- Server downtime
- High error rates
- Database issues
- Disk space warnings

---

## Troubleshooting

### Static Files Not Loading

```bash
python manage.py collectstatic --clear
systemctl restart gunicorn
systemctl restart nginx
```

### Database Connection Issues

Check PostgreSQL is running:
```bash
systemctl status postgresql
```

### 502 Bad Gateway

Check Gunicorn is running:
```bash
systemctl status gunicorn
journalctl -u gunicorn
```

---

## Maintenance

### Regular Updates

```bash
# Update system packages
apt update && apt upgrade -y

# Update Python packages
pip install --upgrade -r requirements.txt

# Run migrations
python manage.py migrate

# Restart services
systemctl restart gunicorn
```

### Database Maintenance

```bash
# Vacuum database
sudo -u postgres psql real_estate_db -c "VACUUM ANALYZE;"
```

---

## Cost Estimates

### Heroku
- Hobby Dyno: $7/month
- Postgres: $9/month
- **Total**: ~$16/month

### DigitalOcean
- Droplet: $6-12/month
- Managed Database: $15/month (optional)
- **Total**: ~$6-27/month

### AWS
- EC2: $5-20/month
- RDS: $15-50/month
- S3: $1-5/month
- **Total**: ~$21-75/month

---

**Your application is now ready for production! 🚀**

