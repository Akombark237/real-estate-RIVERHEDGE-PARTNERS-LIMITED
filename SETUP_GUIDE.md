# Real Estate Platform - Complete Setup Guide

This guide will walk you through setting up the complete Real Estate Software Platform from scratch.

## System Requirements

- **Python**: 3.13 or higher
- **Node.js**: 18 or higher
- **npm**: 9 or higher
- **Operating System**: Windows, macOS, or Linux

## Part 1: Backend Setup (Django)

### Step 1: Verify Python Installation

```bash
python --version
```

You should see Python 3.13.x or higher.

### Step 2: Navigate to Project Directory

```bash
cd "c:\Users\JOSHUA\Desktop\real estate RIVERHEDGE PARTNERS LIMITED"
```

### Step 3: Create Virtual Environment

```bash
python -m venv venv
```

### Step 4: Activate Virtual Environment

**Windows:**
```bash
venv\Scripts\activate
```

**macOS/Linux:**
```bash
source venv/bin/activate
```

You should see `(venv)` in your terminal prompt.

### Step 5: Install Python Dependencies

```bash
pip install -r requirements.txt
```

This will install:
- Django 5.2.7
- Django REST Framework
- JWT authentication
- CORS headers
- Image processing (Pillow)
- API documentation (drf-yasg)
- And other dependencies

### Step 6: Run Database Migrations

```bash
python manage.py migrate
```

This creates all necessary database tables.

### Step 7: Create Superuser (Admin Account)

```bash
python manage.py createsuperuser
```

Follow the prompts to create an admin account:
- Email: your-email@example.com
- Username: admin (or your choice)
- Password: (choose a strong password)

### Step 8: Start Django Development Server

```bash
python manage.py runserver
```

The backend API should now be running at: **http://localhost:8000**

### Step 9: Verify Backend is Running

Open your browser and visit:
- **API Documentation**: http://localhost:8000/api/docs/
- **Django Admin**: http://localhost:8000/admin/

You should see the Swagger API documentation and be able to login to the admin panel.

**Keep this terminal window open** - the backend server needs to keep running.

---

## Part 2: Frontend Setup (React)

### Step 1: Open a New Terminal

Open a **new terminal window** (keep the backend server running in the first terminal).

### Step 2: Navigate to Frontend Directory

```bash
cd "c:\Users\JOSHUA\Desktop\real estate RIVERHEDGE PARTNERS LIMITED\frontend"
```

### Step 3: Verify Node.js Installation

```bash
node --version
npm --version
```

You should see Node.js v18.x or higher and npm v9.x or higher.

### Step 4: Install Frontend Dependencies

```bash
npm install
```

This will install:
- React 18
- React Router
- Axios
- Tailwind CSS
- Vite
- Chart.js
- And other dependencies

This may take a few minutes.

### Step 5: Start Frontend Development Server

```bash
npm run dev
```

The frontend should now be running at: **http://localhost:5173**

### Step 6: Open the Application

Open your browser and visit: **http://localhost:5173**

You should see the login page for the Real Estate Platform.

---

## Part 3: Using the Application

### First Time Setup

1. **Register a New Account**
   - Click "Don't have an account? Register"
   - Fill in your details
   - Choose your role (Agent, Client, Developer, or Investor)
   - Click "Register"

2. **Login**
   - Enter your email and password
   - Click "Sign in"

3. **Explore the Dashboard**
   - View statistics
   - Access quick actions

### Adding Materials

1. Navigate to **Materials** from the top menu
2. Click **Add Material**
3. Fill in the material details:
   - Name (e.g., "Portland Cement")
   - Category (Structural, Finishing, etc.)
   - Unit (Bag, Ton, etc.)
   - Description
4. Click **Create Material**

### Adding Properties

1. Navigate to **Properties** from the top menu
2. Click **Add Property**
3. Fill in the property details:
   - Title
   - Description
   - Property Type
   - Price
   - Address, City, State
   - Bedrooms, Bathrooms, Area
4. Click **Create Property**

### Creating Cost Estimates

1. Navigate to **Cost Estimates** from the top menu
2. Click **New Estimate**
3. Use the calculator:
   - Select Project Type
   - Choose Quality Level
   - Enter Area in square feet
4. Click **Calculate Cost**
5. Review the breakdown
6. Click **Save Estimate** to save it

---

## Part 4: Admin Panel

The Django admin panel provides full control over the database.

1. Visit: **http://localhost:8000/admin/**
2. Login with your superuser credentials
3. You can:
   - View all users
   - Manage materials, properties, estimates
   - View transactions
   - Manage suppliers
   - Configure price alerts

---

## Troubleshooting

### Backend Issues

**Problem**: `ModuleNotFoundError`
**Solution**: Make sure virtual environment is activated and run `pip install -r requirements.txt`

**Problem**: Database errors
**Solution**: Delete `db.sqlite3` and run `python manage.py migrate` again

**Problem**: Port 8000 already in use
**Solution**: Run `python manage.py runserver 8001` to use a different port

### Frontend Issues

**Problem**: `npm install` fails
**Solution**: Delete `node_modules` folder and `package-lock.json`, then run `npm install` again

**Problem**: Port 5173 already in use
**Solution**: Edit `vite.config.js` and change the port number

**Problem**: API connection errors
**Solution**: Make sure the backend server is running on http://localhost:8000

### CORS Issues

If you see CORS errors in the browser console:
1. Check that `django-cors-headers` is installed
2. Verify `CORS_ALLOWED_ORIGINS` in `settings.py` includes your frontend URL
3. Restart the Django server

---

## Development Workflow

### Daily Development

1. **Start Backend**:
   ```bash
   cd "c:\Users\JOSHUA\Desktop\real estate RIVERHEDGE PARTNERS LIMITED"
   venv\Scripts\activate
   python manage.py runserver
   ```

2. **Start Frontend** (in a new terminal):
   ```bash
   cd "c:\Users\JOSHUA\Desktop\real estate RIVERHEDGE PARTNERS LIMITED\frontend"
   npm run dev
   ```

3. **Make Changes**:
   - Backend changes: Edit Python files, server auto-reloads
   - Frontend changes: Edit React files, browser auto-refreshes

### Running Tests

**Backend Tests**:
```bash
python manage.py test
```

**Frontend Tests** (when implemented):
```bash
npm test
```

---

## Production Deployment

### Backend Deployment

1. Set `DEBUG = False` in `settings.py`
2. Configure a production database (PostgreSQL recommended)
3. Set up environment variables for secrets
4. Collect static files: `python manage.py collectstatic`
5. Use a production server (Gunicorn, uWSGI)
6. Set up HTTPS with SSL certificate

### Frontend Deployment

1. Build the production bundle:
   ```bash
   npm run build
   ```

2. Deploy the `dist` folder to:
   - Netlify
   - Vercel
   - AWS S3 + CloudFront
   - Or any static hosting service

3. Update API URL in production build

---

## Next Steps

1. **Add Sample Data**: Use the admin panel to add sample materials, properties, and suppliers
2. **Customize**: Modify colors, branding, and features to match your needs
3. **Add Features**: Implement additional features from the roadmap
4. **Test**: Thoroughly test all functionality
5. **Deploy**: Deploy to production when ready

---

## Support

For issues or questions:
- Check the main README.md
- Review API documentation at http://localhost:8000/api/docs/
- Contact: support@riverhedgepartners.com

---

## Quick Reference

### Important URLs

- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/api/docs/
- **Admin Panel**: http://localhost:8000/admin/

### Important Commands

```bash
# Backend
python manage.py runserver          # Start server
python manage.py migrate            # Run migrations
python manage.py createsuperuser    # Create admin
python manage.py makemigrations     # Create migrations

# Frontend
npm run dev                         # Start dev server
npm run build                       # Build for production
npm install                         # Install dependencies
```

---

**Congratulations!** You now have a fully functional Real Estate Software Platform running locally.

