# Real Estate Platform - Testing Guide

This guide will help you test all features of the Real Estate Software Platform.

## Prerequisites

Make sure both backend and frontend servers are running:

1. **Backend**: http://localhost:8000
2. **Frontend**: http://localhost:5173

---

## Test 1: User Registration and Authentication

### 1.1 Register a New User

1. Open http://localhost:5173
2. Click "Don't have an account? Register"
3. Fill in the registration form:
   - First Name: John
   - Last Name: Doe
   - Email: john.doe@example.com
   - Username: johndoe
   - Phone: +1234567890 (optional)
   - Role: Agent
   - Password: TestPass123!
   - Confirm Password: TestPass123!
4. Click "Register"

**Expected Result**: You should be redirected to the dashboard with a welcome message.

### 1.2 Logout and Login

1. Click "Logout" in the top right
2. Enter your credentials:
   - Email: john.doe@example.com
   - Password: TestPass123!
3. Click "Sign in"

**Expected Result**: You should be logged in and see the dashboard.

---

## Test 2: Materials Management

### 2.1 Add a New Material

1. Navigate to "Materials" from the top menu
2. Click "Add Material"
3. Fill in the form:
   - Name: Portland Cement
   - Category: Structural
   - Unit: Bag
   - Description: 50kg bag of high-quality Portland cement
4. Click "Create Material"

**Expected Result**: The material should appear in the list below.

### 2.2 Add More Materials

Add these additional materials:

1. **Steel Rebar**
   - Category: Structural
   - Unit: Ton
   - Description: Reinforcement steel bars

2. **Ceramic Tiles**
   - Category: Finishing
   - Unit: Square Meter
   - Description: Premium ceramic floor tiles

3. **PVC Pipes**
   - Category: Plumbing
   - Unit: Piece
   - Description: 4-inch PVC drainage pipes

**Expected Result**: All materials should be visible in the materials list.

---

## Test 3: Property Management

### 3.1 Add a New Property

1. Navigate to "Properties" from the top menu
2. Click "Add Property"
3. Fill in the form:
   - Title: Luxury 3-Bedroom Apartment
   - Description: Modern apartment in prime location with stunning views
   - Property Type: Residential
   - Status: Available
   - Price: 450000
   - Address: 123 Main Street
   - City: New York
   - State: NY
   - Bedrooms: 3
   - Bathrooms: 2
   - Area: 1500
4. Click "Create Property"

**Expected Result**: The property should appear in the grid below.

### 3.2 Add More Properties

Add these additional properties:

1. **Commercial Office Space**
   - Type: Commercial
   - Status: Available
   - Price: 850000
   - Address: 456 Business Ave
   - City: Los Angeles
   - State: CA
   - Area: 3000

2. **Vacant Land**
   - Type: Land
   - Status: Available
   - Price: 200000
   - Address: 789 Country Road
   - City: Austin
   - State: TX
   - Area: 5000

**Expected Result**: All properties should be visible in the properties grid.

---

## Test 4: Cost Estimation

### 4.1 Calculate a Basic Estimate

1. Navigate to "Cost Estimates" from the top menu
2. Click "New Estimate"
3. Fill in the calculator:
   - Project Type: New Construction
   - Quality Level: Basic ($80/sqft)
   - Area: 1000
4. Click "Calculate Cost"

**Expected Result**: You should see:
- Base Cost per sqft: $80.00
- Material Cost (60%): $48,000
- Labor Cost (30%): $24,000
- Overhead Cost (10%): $8,000
- Total Cost: $80,000

### 4.2 Save the Estimate

1. Click "Save Estimate"

**Expected Result**: The estimate should appear in the list below.

### 4.3 Calculate Different Quality Levels

Test each quality level:

1. **Standard Quality**
   - Project Type: Renovation
   - Quality Level: Standard ($120/sqft)
   - Area: 1500
   - Expected Total: $180,000

2. **Premium Quality**
   - Project Type: Extension
   - Quality Level: Premium ($180/sqft)
   - Area: 800
   - Expected Total: $144,000

3. **Luxury Quality**
   - Project Type: Remodeling
   - Quality Level: Luxury ($250/sqft)
   - Area: 2000
   - Expected Total: $500,000

**Expected Result**: Each calculation should show correct breakdown and save successfully.

---

## Test 5: Dashboard Statistics

1. Navigate to "Dashboard" from the top menu
2. Verify the statistics:
   - Properties: Should show 3 (or your count)
   - Materials: Should show 4 (or your count)
   - Cost Estimates: Should show 4 (or your count)
   - Transactions: Should show 0

**Expected Result**: All counts should be accurate.

---

## Test 6: API Documentation

### 6.1 Access Swagger UI

1. Open http://localhost:8000/api/docs/
2. Explore the API endpoints
3. Try the "Try it out" feature on any endpoint

**Expected Result**: You should see comprehensive API documentation.

### 6.2 Test an API Endpoint

1. In Swagger UI, find "GET /api/materials/"
2. Click "Try it out"
3. Click "Execute"

**Expected Result**: You should see a JSON response with your materials.

---

## Test 7: Django Admin Panel

### 7.1 Access Admin Panel

1. Open http://localhost:8000/admin/
2. Login with your superuser credentials
3. Explore the admin interface

**Expected Result**: You should see all models listed.

### 7.2 View Data in Admin

1. Click on "Materials"
2. You should see all materials you created
3. Click on "Properties"
4. You should see all properties you created

**Expected Result**: All data should be visible and editable.

---

## Test 8: Error Handling

### 8.1 Test Invalid Login

1. Logout from the application
2. Try to login with wrong credentials:
   - Email: wrong@example.com
   - Password: wrongpassword

**Expected Result**: You should see an error message.

### 8.2 Test Form Validation

1. Try to create a property without required fields
2. Leave "Title" empty
3. Click "Create Property"

**Expected Result**: Form should show validation errors.

### 8.3 Test Password Mismatch

1. Go to registration page
2. Enter different passwords in "Password" and "Confirm Password"
3. Try to register

**Expected Result**: Should show "Passwords do not match" error.

---

## Test 9: Responsive Design

### 9.1 Test Mobile View

1. Open browser developer tools (F12)
2. Toggle device toolbar (Ctrl+Shift+M)
3. Select a mobile device (e.g., iPhone 12)
4. Navigate through all pages

**Expected Result**: All pages should be responsive and usable on mobile.

### 9.2 Test Tablet View

1. Select a tablet device (e.g., iPad)
2. Navigate through all pages

**Expected Result**: Layout should adapt to tablet screen size.

---

## Test 10: Data Persistence

### 10.1 Test Data Persistence

1. Create some materials, properties, and estimates
2. Close the browser
3. Reopen http://localhost:5173
4. Login again

**Expected Result**: All your data should still be there.

### 10.2 Test JWT Token Refresh

1. Login to the application
2. Wait for 1 hour (or modify JWT settings for shorter expiry)
3. Try to perform an action

**Expected Result**: Token should refresh automatically or prompt for re-login.

---

## Test 11: Search and Filtering

### 11.1 Test Property Filtering

1. Create properties with different statuses (available, pending, sold)
2. Use browser developer tools to check network requests
3. Verify filtering works in the API

**Expected Result**: API should support filtering by status, type, etc.

---

## Test 12: File Uploads (Future Enhancement)

Currently, file upload UI is not implemented in the frontend, but the backend supports it.

### 12.1 Test via API

1. Use Swagger UI or Postman
2. Upload an image to a property
3. Verify it's stored in the media folder

**Expected Result**: Image should be uploaded successfully.

---

## Common Issues and Solutions

### Issue: CORS Error

**Symptom**: Browser console shows CORS policy error

**Solution**:
1. Check that backend is running on port 8000
2. Verify CORS settings in `settings.py`
3. Restart Django server

### Issue: 401 Unauthorized

**Symptom**: API requests return 401 error

**Solution**:
1. Check that you're logged in
2. Verify JWT token in localStorage
3. Try logging out and logging in again

### Issue: Database Locked

**Symptom**: "Database is locked" error

**Solution**:
1. Close all connections to the database
2. Restart the Django server
3. If persists, delete `db.sqlite3` and run migrations again

### Issue: Port Already in Use

**Symptom**: "Port 8000 is already in use"

**Solution**:
1. Find and kill the process using the port
2. Or use a different port: `python manage.py runserver 8001`

---

## Performance Testing

### Load Testing (Optional)

Use tools like Apache JMeter or Locust to test:
- Concurrent user logins
- Multiple API requests
- Database query performance

---

## Security Testing

### Basic Security Checks

1. **SQL Injection**: Try entering SQL in form fields
   - Expected: Should be sanitized by Django ORM

2. **XSS**: Try entering `<script>alert('XSS')</script>` in text fields
   - Expected: Should be escaped

3. **CSRF**: Try making API requests without CSRF token
   - Expected: Should be rejected

---

## Test Checklist

Use this checklist to track your testing:

- [ ] User registration works
- [ ] User login works
- [ ] User logout works
- [ ] Dashboard displays correct statistics
- [ ] Can create materials
- [ ] Can view materials list
- [ ] Can create properties
- [ ] Can view properties grid
- [ ] Cost calculator works correctly
- [ ] Can save estimates
- [ ] Can view estimates list
- [ ] API documentation is accessible
- [ ] Admin panel is accessible
- [ ] Error messages display correctly
- [ ] Form validation works
- [ ] Responsive design works on mobile
- [ ] Responsive design works on tablet
- [ ] Data persists after logout/login
- [ ] All navigation links work

---

## Reporting Issues

If you find any bugs or issues:

1. Note the steps to reproduce
2. Take screenshots if applicable
3. Check browser console for errors
4. Check Django server logs
5. Document the expected vs actual behavior

---

## Next Steps After Testing

Once all tests pass:

1. ✅ Mark "Test and Deploy MVP" task as complete
2. 📝 Document any issues found
3. 🚀 Prepare for production deployment
4. 📊 Gather user feedback
5. 🔄 Plan Phase 2 features

---

**Happy Testing! 🎉**

