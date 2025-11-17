# Real Estate Platform - Quick Reference Card

## 🚀 Quick Start

### Start Application (Windows)
```bash
# Double-click START_APP.bat
# Or manually:
venv\Scripts\activate
python manage.py runserver

# In new terminal:
cd frontend
npm run dev
```

### Access Points
- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/api/docs/
- **Admin Panel**: http://localhost:8000/admin/

---

## 📁 Project Structure

```
real estate RIVERHEDGE PARTNERS LIMITED/
├── Backend (Django)
│   ├── users/              # User management
│   ├── materials/          # Materials & prices
│   ├── properties/         # Property listings
│   ├── cost_estimates/     # Cost calculator
│   └── reports/            # Reports module
│
├── frontend/               # React application
│   └── src/
│       ├── pages/          # Main pages
│       ├── components/     # Reusable components
│       └── context/        # State management
│
└── Documentation
    ├── README.md           # Main docs
    ├── SETUP_GUIDE.md      # Setup instructions
    ├── TESTING_GUIDE.md    # Testing procedures
    └── DEPLOYMENT_GUIDE.md # Deployment guide
```

---

## 🔑 Common Commands

### Backend (Django)

```bash
# Activate virtual environment
venv\Scripts\activate                    # Windows
source venv/bin/activate                 # Mac/Linux

# Run server
python manage.py runserver

# Database
python manage.py makemigrations          # Create migrations
python manage.py migrate                 # Apply migrations
python manage.py createsuperuser         # Create admin

# Shell
python manage.py shell                   # Django shell
python manage.py dbshell                 # Database shell

# Utilities
python manage.py collectstatic           # Collect static files
python manage.py test                    # Run tests
```

### Frontend (React)

```bash
# Install dependencies
npm install

# Development
npm run dev                              # Start dev server
npm run build                            # Build for production
npm run preview                          # Preview production build
```

---

## 🔐 Default Credentials

### Superuser (Create with createsuperuser)
- Email: (your choice)
- Username: (your choice)
- Password: (your choice)

### Test User (After registration)
- Email: test@example.com
- Password: TestPass123!

---

## 📡 API Endpoints

### Authentication
```
POST   /api/auth/register/              # Register user
POST   /api/auth/login/                 # Login
POST   /api/auth/token/refresh/         # Refresh token
GET    /api/auth/profile/               # Get profile
PUT    /api/auth/profile/               # Update profile
```

### Materials
```
GET    /api/materials/                  # List materials
POST   /api/materials/                  # Create material
GET    /api/materials/{id}/             # Get material
PUT    /api/materials/{id}/             # Update material
DELETE /api/materials/{id}/             # Delete material
GET    /api/materials/{id}/price-trends/ # Price trends
```

### Properties
```
GET    /api/properties/                 # List properties
POST   /api/properties/                 # Create property
GET    /api/properties/{id}/            # Get property
PUT    /api/properties/{id}/            # Update property
DELETE /api/properties/{id}/            # Delete property
GET    /api/properties/my-properties/   # User's properties
```

### Cost Estimates
```
GET    /api/estimates/                  # List estimates
POST   /api/estimates/                  # Create estimate
GET    /api/estimates/{id}/             # Get estimate
POST   /api/estimates/calculate/        # Calculate cost
GET    /api/estimates/templates/        # List templates
```

---

## 🎨 Frontend Routes

```
/login                                   # Login page
/register                                # Registration page
/                                        # Dashboard (protected)
/materials                               # Materials page (protected)
/properties                              # Properties page (protected)
/estimates                               # Cost estimates (protected)
```

---

## 🗄️ Database Models

### Core Models
1. **User** - Custom user with roles
2. **Supplier** - Material suppliers
3. **Material** - Building materials
4. **MaterialPrice** - Price history
5. **PriceAlert** - Price notifications
6. **Property** - Property listings
7. **PropertyImage** - Property photos
8. **PropertyDocument** - Property files
9. **Transaction** - Sales/rentals
10. **CostEstimate** - Cost calculations
11. **EstimateItem** - Estimate items
12. **ProjectTemplate** - Templates
13. **Report** - Generated reports

---

## 🔧 Configuration Files

### Backend
- `settings.py` - Django settings
- `urls.py` - URL routing
- `requirements.txt` - Python dependencies
- `.env` - Environment variables (create this)

### Frontend
- `vite.config.js` - Vite configuration
- `tailwind.config.js` - Tailwind CSS config
- `package.json` - Node dependencies

---

## 🐛 Troubleshooting

### Backend Issues

**Port 8000 in use**
```bash
python manage.py runserver 8001
```

**Database locked**
```bash
# Close all connections and restart server
```

**Module not found**
```bash
pip install -r requirements.txt
```

### Frontend Issues

**Port 5173 in use**
```bash
# Edit vite.config.js and change port
```

**Dependencies error**
```bash
rm -rf node_modules package-lock.json
npm install
```

**CORS error**
```bash
# Check backend CORS settings in settings.py
# Restart Django server
```

---

## 📊 Quality Levels (Cost Calculator)

| Level    | Cost/sqft | Use Case              |
|----------|-----------|----------------------|
| Basic    | $80       | Budget construction  |
| Standard | $120      | Average quality      |
| Premium  | $180      | High-end finishes    |
| Luxury   | $250      | Luxury properties    |

**Cost Breakdown**:
- Materials: 60%
- Labor: 30%
- Overhead: 10%

---

## 🔒 Security Features

- ✅ JWT authentication
- ✅ Password hashing (bcrypt)
- ✅ CSRF protection
- ✅ XSS protection
- ✅ SQL injection prevention
- ✅ CORS configuration
- ✅ Role-based access control

---

## 📦 Tech Stack

### Backend
- Python 3.13.7
- Django 5.2.7
- Django REST Framework 3.16.1
- SQLite (dev) / PostgreSQL (prod)

### Frontend
- React 18.2.0
- Vite 5.0.8
- Tailwind CSS 3.3.6
- Axios 1.6.2

---

## 📝 Environment Variables

Create `.env` file in project root:

```bash
# Django
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database (for production)
DATABASE_URL=postgresql://user:pass@host:port/db

# Email (optional)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-password
```

---

## 🎯 User Roles

| Role      | Description                    |
|-----------|--------------------------------|
| admin     | Full system access             |
| agent     | Manage properties & clients    |
| client    | View properties, get estimates |
| developer | Manage projects & estimates    |
| investor  | View analytics & reports       |

---

## 📈 Next Steps

1. ✅ Complete setup (see SETUP_GUIDE.md)
2. ✅ Test features (see TESTING_GUIDE.md)
3. ⏳ Add sample data
4. ⏳ Customize branding
5. ⏳ Deploy to production (see DEPLOYMENT_GUIDE.md)

---

## 📞 Support

- **Email**: support@riverhedgepartners.com
- **Documentation**: See README.md
- **API Docs**: http://localhost:8000/api/docs/

---

## 🔗 Useful Links

- [Django Documentation](https://docs.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [React Documentation](https://react.dev/)
- [Tailwind CSS](https://tailwindcss.com/)
- [Vite](https://vitejs.dev/)

---

**Built for RIVERHEDGE PARTNERS LIMITED** 🏢

