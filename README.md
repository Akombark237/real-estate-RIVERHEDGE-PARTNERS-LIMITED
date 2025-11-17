# RIVERHEDGE PARTNERS LIMITED - Real Estate Platform

A comprehensive real estate management platform with building materials price tracking, cost estimation, property management, and investment analysis features.

## Features

### Phase 1 - MVP (Completed)

#### 1. Building Materials Price Tracking
- Real-time price database for construction materials
- Historical price data and trends
- Price alerts and notifications
- Material categories (structural, finishing, electrical, plumbing, roofing, etc.)
- Supplier management

#### 2. Cost Estimation & Calculator
- Construction cost calculator based on current material prices
- Renovation cost estimator
- Custom project builder
- Itemized cost breakdown
- Quality level selection (basic, standard, premium, luxury)

#### 3. Property Management
- Property listings (CRUD operations)
- Multiple image uploads per property
- Document management
- Status tracking (available, pending, sold, rented)
- Advanced search and filtering

#### 4. Transaction Management
- Deal pipeline tracking
- Commission calculations
- Payment tracking
- Transaction history

#### 5. User Management
- JWT-based authentication
- Role-based access control (admin, agent, client, developer, investor)
- User profiles
- Secure password management

## Technology Stack

### Backend
- **Framework**: Django 5.2.7
- **API**: Django REST Framework 3.16.1
- **Authentication**: JWT (djangorestframework-simplejwt)
- **Database**: SQLite (development) / PostgreSQL (production recommended)
- **API Documentation**: drf-yasg (Swagger/OpenAPI)
- **Image Processing**: Pillow
- **CORS**: django-cors-headers

### Frontend (To be implemented)
- **Framework**: React 18+ with Vite
- **UI Library**: Tailwind CSS / Material-UI
- **State Management**: React Context API / Redux
- **Charts**: Chart.js / Recharts
- **HTTP Client**: Axios

## Installation & Setup

### Prerequisites
- Python 3.13+
- Node.js 18+ (for frontend)
- pip (Python package manager)
- npm or yarn (for frontend)

### Backend Setup

1. **Clone the repository** (if applicable)
   ```bash
   cd "c:\Users\JOSHUA\Desktop\real estate RIVERHEDGE PARTNERS LIMITED"
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   # source venv/bin/activate  # Linux/Mac
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run migrations**
   ```bash
   python manage.py migrate
   ```

5. **Create superuser**
   ```bash
   python manage.py createsuperuser
   ```

6. **Run development server**
   ```bash
   python manage.py runserver
   ```

   The API will be available at: `http://localhost:8000`

### Frontend Setup (Coming Soon)

1. **Navigate to frontend directory**
   ```bash
   cd frontend
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Run development server**
   ```bash
   npm run dev
   ```

   The frontend will be available at: `http://localhost:5173`

## API Documentation

Once the server is running, you can access the API documentation at:

- **Swagger UI**: http://localhost:8000/api/docs/
- **ReDoc**: http://localhost:8000/api/redoc/
- **Django Admin**: http://localhost:8000/admin/

## API Endpoints

### Authentication
- `POST /api/auth/register/` - Register new user
- `POST /api/auth/login/` - Login user
- `POST /api/auth/token/refresh/` - Refresh JWT token
- `GET /api/auth/profile/` - Get user profile
- `PUT /api/auth/profile/` - Update user profile

### Materials
- `GET /api/materials/` - List all materials
- `POST /api/materials/` - Create new material
- `GET /api/materials/{id}/` - Get material details
- `PUT /api/materials/{id}/` - Update material
- `DELETE /api/materials/{id}/` - Delete material
- `GET /api/materials/{id}/price-trends/` - Get price trends
- `GET /api/materials/prices/` - List material prices
- `POST /api/materials/prices/` - Add new price entry

### Properties
- `GET /api/properties/` - List all properties
- `POST /api/properties/` - Create new property
- `GET /api/properties/{id}/` - Get property details
- `PUT /api/properties/{id}/` - Update property
- `DELETE /api/properties/{id}/` - Delete property
- `GET /api/properties/my-properties/` - Get current user's properties
- `POST /api/properties/{id}/images/` - Upload property images
- `POST /api/properties/{id}/documents/` - Upload property documents

### Cost Estimates
- `GET /api/estimates/` - List all estimates
- `POST /api/estimates/` - Create new estimate
- `GET /api/estimates/{id}/` - Get estimate details
- `PUT /api/estimates/{id}/` - Update estimate
- `DELETE /api/estimates/{id}/` - Delete estimate
- `POST /api/estimates/calculate/` - Calculate estimate
- `GET /api/estimates/templates/` - List project templates

### Transactions
- `GET /api/properties/transactions/` - List all transactions
- `POST /api/properties/transactions/` - Create new transaction
- `GET /api/properties/transactions/{id}/` - Get transaction details
- `PUT /api/properties/transactions/{id}/` - Update transaction

## Database Schema

### Core Models

1. **User** - Custom user model with roles
2. **Supplier** - Building material suppliers
3. **Material** - Building materials catalog
4. **MaterialPrice** - Time-series price data
5. **PriceAlert** - Price alert notifications
6. **Property** - Property listings
7. **PropertyImage** - Property images
8. **PropertyDocument** - Property documents
9. **Transaction** - Property transactions
10. **CostEstimate** - Cost estimates
11. **EstimateItem** - Individual estimate items
12. **ProjectTemplate** - Pre-defined project templates
13. **Report** - Generated reports

## Project Structure

```
real estate RIVERHEDGE PARTNERS LIMITED/
├── real_estate_platform/      # Django project settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── users/                      # User management app
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   └── urls.py
├── materials/                  # Materials management app
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   └── urls.py
├── properties/                 # Property management app
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   └── urls.py
├── cost_estimates/             # Cost estimation app
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   └── urls.py
├── reports/                    # Reports app
│   ├── models.py
│   └── admin.py
├── media/                      # Uploaded files
├── manage.py
├── requirements.txt
└── README.md
```

## Usage Examples

### Register a new user
```bash
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "username": "johndoe",
    "password": "SecurePass123!",
    "password2": "SecurePass123!",
    "first_name": "John",
    "last_name": "Doe",
    "role": "agent"
  }'
```

### Login
```bash
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "SecurePass123!"
  }'
```

### Create a material (requires authentication)
```bash
curl -X POST http://localhost:8000/api/materials/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -d '{
    "name": "Portland Cement",
    "category": "structural",
    "unit": "bag",
    "description": "50kg bag of Portland cement"
  }'
```

## Development Roadmap

### Phase 2 - Enhanced Features (Planned)
- Advanced price tracking and alerts
- Email/SMS notifications
- Enhanced reporting
- Client management
- Advanced search and filters

### Phase 3 - Advanced Analytics (Planned)
- Investment analysis tools (ROI calculator)
- Market data integration
- Price prediction algorithms
- Mobile application (iOS/Android)

### Phase 4 - Enterprise Features (Planned)
- Multi-company support
- White-label options
- Third-party API integrations
- Advanced permissions and workflows

## Security Features

- JWT-based authentication
- Password hashing with bcrypt
- CORS protection
- CSRF protection
- SQL injection prevention
- XSS protection
- Role-based access control

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is proprietary software for RIVERHEDGE PARTNERS LIMITED.

## 📚 Documentation

This project includes comprehensive documentation:

- **[README.md](README.md)** - Main documentation (this file)
- **[SETUP_GUIDE.md](SETUP_GUIDE.md)** - Detailed setup instructions
- **[PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)** - Complete project overview
- **[TESTING_GUIDE.md](TESTING_GUIDE.md)** - Testing procedures
- **[DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)** - Production deployment guide
- **[frontend/README.md](frontend/README.md)** - Frontend-specific documentation

## 🚀 Quick Start Scripts

### Windows Users

Double-click `START_APP.bat` to start both backend and frontend servers automatically.

Or use individual scripts:
- `run_server.bat` - Start Django backend only

### Manual Start

**Backend**:
```bash
venv\Scripts\activate
python manage.py runserver
```

**Frontend**:
```bash
cd frontend
npm run dev
```

## 📊 Project Status

**Current Phase**: MVP (Phase 1) - ✅ COMPLETE

All core features have been implemented and tested:
- ✅ User authentication and management
- ✅ Materials database and price tracking
- ✅ Property listings and management
- ✅ Cost estimation calculator
- ✅ Transaction tracking
- ✅ REST API with documentation
- ✅ React frontend with responsive design

## 🎯 What's Next?

1. **Test the Application**: Follow the [TESTING_GUIDE.md](TESTING_GUIDE.md)
2. **Add Sample Data**: Use the admin panel to populate the database
3. **Customize**: Modify branding, colors, and features as needed
4. **Deploy**: Follow the [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) when ready

## Support

For support, please contact: support@riverhedgepartners.com

## Authors

- Development Team - RIVERHEDGE PARTNERS LIMITED

## Acknowledgments

- Django REST Framework documentation
- React documentation
- Tailwind CSS
- Vite build tool
