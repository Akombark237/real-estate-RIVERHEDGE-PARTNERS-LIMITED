import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'real_estate_platform.settings')
django.setup()

from properties.models import Property, PropertyImage
from users.models import User
from decimal import Decimal

# Get the admin user
admin = User.objects.get(username='admin')

# Sample properties data
properties_data = [
    {
        'title': 'Luxury 4 Bedroom Duplex in Maitama',
        'description': 'Beautiful modern duplex with spacious rooms, fitted kitchen, and ample parking space. Located in the prestigious Maitama district.',
        'property_type': 'residential',
        'address': 'Plot 123, Maitama District',
        'city': 'Abuja',
        'state': 'FCT',
        'price': Decimal('85000000'),
        'bedrooms': 4,
        'bathrooms': 5,
        'size_sqft': Decimal('3500'),
        'year_built': 2022,
        'parking_spaces': 3,
        'status': 'available',
        'latitude': 9.0820,
        'longitude': 7.4920,
    },
    {
        'title': '3 Bedroom Apartment in Wuse 2',
        'description': 'Fully serviced 3-bedroom apartment with modern amenities, 24/7 security, and backup power supply.',
        'property_type': 'residential',
        'address': '45 Adetokunbo Ademola Crescent, Wuse 2',
        'city': 'Abuja',
        'state': 'FCT',
        'price': Decimal('45000000'),
        'bedrooms': 3,
        'bathrooms': 3,
        'size_sqft': Decimal('2200'),
        'year_built': 2021,
        'parking_spaces': 2,
        'status': 'available',
        'latitude': 9.0643,
        'longitude': 7.4892,
    },
    {
        'title': 'Commercial Office Space in Central Business District',
        'description': 'Prime office space suitable for corporate headquarters. Features include elevator access, central AC, and modern facilities.',
        'property_type': 'commercial',
        'address': 'Central Business District, Plot 789',
        'city': 'Abuja',
        'state': 'FCT',
        'price': Decimal('120000000'),
        'bedrooms': 0,
        'bathrooms': 4,
        'size_sqft': Decimal('5000'),
        'year_built': 2023,
        'parking_spaces': 10,
        'status': 'available',
        'latitude': 9.0765,
        'longitude': 7.3986,
    },
    {
        'title': '5 Bedroom Detached House in Asokoro',
        'description': 'Exquisite 5-bedroom detached house with swimming pool, gym, and beautiful garden. Perfect for families.',
        'property_type': 'residential',
        'address': 'Asokoro Extension, Plot 56',
        'city': 'Abuja',
        'state': 'FCT',
        'price': Decimal('150000000'),
        'bedrooms': 5,
        'bathrooms': 6,
        'size_sqft': Decimal('4500'),
        'year_built': 2023,
        'parking_spaces': 4,
        'status': 'available',
        'latitude': 9.0330,
        'longitude': 7.5340,
    },
    {
        'title': 'Affordable 2 Bedroom Flat in Gwarinpa',
        'description': 'Cozy 2-bedroom flat in a serene environment. Great for young families and first-time buyers.',
        'property_type': 'residential',
        'address': 'Gwarinpa Estate, Block 12',
        'city': 'Abuja',
        'state': 'FCT',
        'price': Decimal('25000000'),
        'bedrooms': 2,
        'bathrooms': 2,
        'size_sqft': Decimal('1500'),
        'year_built': 2020,
        'parking_spaces': 1,
        'status': 'available',
        'latitude': 9.1108,
        'longitude': 7.4125,
    },
    {
        'title': 'Land for Sale in Lugbe',
        'description': 'Prime land for residential or commercial development. Located in a fast-growing area with good road access.',
        'property_type': 'land',
        'address': 'Lugbe District, Plot 234',
        'city': 'Abuja',
        'state': 'FCT',
        'price': Decimal('15000000'),
        'bedrooms': 0,
        'bathrooms': 0,
        'size_sqft': Decimal('10000'),
        'year_built': None,
        'parking_spaces': 0,
        'status': 'available',
        'latitude': 8.9642,
        'longitude': 7.3711,
    },
]

print("\n🏗️ Creating sample properties...\n")

for prop_data in properties_data:
    # Create property
    property_obj = Property.objects.create(
        agent=admin,
        **prop_data
    )
    
    print(f"✅ Created: {property_obj.title}")
    print(f"   Price: ₦{property_obj.price:,}")
    print(f"   Location: {property_obj.city}, {property_obj.state}")
    print(f"   Coordinates: ({property_obj.latitude}, {property_obj.longitude})")
    print()

print(f"\n🎉 Successfully created {len(properties_data)} properties!")
print("\n📝 Note: Properties don't have images yet. You can upload images through the web interface:")
print("   1. Go to http://localhost:5173/properties")
print("   2. Click on any property to view details")
print("   3. Click 'Upload Images' to add property photos")
print()

