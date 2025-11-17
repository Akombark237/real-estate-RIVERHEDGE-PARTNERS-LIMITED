# Real Estate Platform - Frontend

React-based frontend for the Real Estate Software Platform.

## Features

- User authentication (login/register)
- Dashboard with statistics
- Materials management
- Property listings
- Cost estimation calculator
- Responsive design with Tailwind CSS

## Prerequisites

- Node.js 18+ and npm
- Backend API running on http://localhost:8000

## Installation

1. **Install dependencies**
   ```bash
   npm install
   ```

2. **Run development server**
   ```bash
   npm run dev
   ```

   The application will be available at: http://localhost:5173

3. **Build for production**
   ```bash
   npm run build
   ```

## Project Structure

```
frontend/
├── src/
│   ├── components/
│   │   ├── Layout.jsx          # Main layout with navigation
│   │   └── PrivateRoute.jsx    # Protected route wrapper
│   ├── context/
│   │   └── AuthContext.jsx     # Authentication context
│   ├── pages/
│   │   ├── Login.jsx           # Login page
│   │   ├── Register.jsx        # Registration page
│   │   ├── Dashboard.jsx       # Dashboard with stats
│   │   ├── Materials.jsx       # Materials management
│   │   ├── Properties.jsx      # Property listings
│   │   └── CostEstimates.jsx   # Cost calculator
│   ├── App.jsx                 # Main app component
│   ├── main.jsx                # Entry point
│   └── index.css               # Global styles
├── index.html
├── package.json
├── vite.config.js
└── tailwind.config.js
```

## Technologies Used

- **React 18** - UI library
- **React Router** - Routing
- **Axios** - HTTP client
- **Tailwind CSS** - Styling
- **Vite** - Build tool
- **Chart.js** - Data visualization (ready to use)

## API Integration

The frontend communicates with the Django backend API at `http://localhost:8000/api/`.

API endpoints are proxied through Vite configuration for development.

## Authentication

JWT tokens are stored in localStorage and automatically included in API requests.

## Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build

