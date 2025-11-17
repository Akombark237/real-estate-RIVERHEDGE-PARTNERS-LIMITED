import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'real_estate_platform.settings')
django.setup()

from properties.models import Property

# Abuja coordinates for different areas
abuja_locations = {
    'Maitama': {'lat': 9.0820, 'lng': 7.4920},
    'Asokoro': {'lat': 9.0330, 'lng': 7.5340},
    'Wuse': {'lat': 9.0643, 'lng': 7.4892},
    'Garki': {'lat': 9.0354, 'lng': 7.4870},
    'Gwarinpa': {'lat': 9.1108, 'lng': 7.4125},
    'Jabi': {'lat': 9.0698, 'lng': 7.4514},
    'Kubwa': {'lat': 9.1372, 'lng': 7.3378},
    'Lugbe': {'lat': 8.9642, 'lng': 7.3711},
    'Karu': {'lat': 9.0078, 'lng': 7.6328},
    'Nyanya': {'lat': 8.9967, 'lng': 7.5833},
}

properties = Property.objects.all()

print(f"\nFound {properties.count()} properties in database\n")

for prop in properties:
    # Try to match city/address to a location
    location_found = False
    for location_name, coords in abuja_locations.items():
        if location_name.lower() in prop.city.lower() or location_name.lower() in prop.address.lower():
            prop.latitude = coords['lat']
            prop.longitude = coords['lng']
            location_found = True
            break
    
    # If no match, use default Abuja coordinates
    if not location_found:
        prop.latitude = 9.0765
        prop.longitude = 7.3986
    
    prop.save()
    
    print(f"✅ Updated: {prop.title}")
    print(f"   Location: {prop.city}, {prop.state}")
    print(f"   Coordinates: {prop.latitude}, {prop.longitude}")
    print(f"   Images: {prop.images.count()}")
    print()

print("\n✅ All properties updated with coordinates!")

