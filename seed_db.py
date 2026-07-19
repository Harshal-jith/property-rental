import os
import django

# Setup django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'property_rental.settings')
django.setup()

from django.contrib.auth import get_user_model
from portal.models import Property, PropertyImage, Booking
import datetime

User = get_user_model()

def run_seeding():
    print("Starting database seeding...")
    
    # 1. Create admin / superuser
    admin_email = 'admin@gmail.com'
    if not User.objects.filter(email=admin_email).exists():
        User.objects.create_superuser(
            email=admin_email,
            password='admin123',
            full_name='System Admin',
            phone='+91 94470 99000'
        )
        print(f"Created Admin account: {admin_email} / admin123")
    else:
        print("Admin account already exists.")
        
    # 2. Create demo renter account
    renter_email = 'john@example.com'
    if not User.objects.filter(email=renter_email).exists():
        User.objects.create_user(
            email=renter_email,
            password='john123',
            full_name='John Doe',
            phone='+91 98470 12345'
        )
        print(f"Created Renter account: {renter_email} / john123")
    else:
        print("Renter account already exists.")

    # Remove existing properties to allow fresh seeds
    Property.objects.all().delete()
    print("Cleared existing properties catalog.")

    # 3. Create property listings (Kerala places & Rupee currency values)
    properties_to_create = [
        {
            'title': 'Kochi Heritage Luxury Villa',
            'description': 'A stunning modern villa located near the scenic Marine Drive in Kochi. Features traditional Kerala architectural design touches combined with modern high ceilings, a grand foyer, custom infinity pool, and beautiful sea views.',
            'rent': 450000.00,
            'city': 'Kochi',
            'address': 'Marine Drive Promenade, Kochi',
            'bedrooms': 4,
            'bathrooms': 4,
            'area': 4800,
            'furnished': True,
            'parking': True,
            'available': True,
            'main_image': 'properties/main/Luxury_villa_Kochi_Kerala_India_202607181611.jpeg',
            'gallery': ['properties/gallery/Luxury_villa_Kochi_Kerala_India_202607181615.jpeg', 'properties/gallery/Luxury_villa_Kochi_Kerala_India_202607181618.jpeg']
        },
        {
            'title': 'Trivandrum Skyline Penthouse',
            'description': 'Breathtaking 3-bedroom penthouse with floor-to-ceiling windows offering views of the Arabian Sea and Trivandrum city skyline. Includes premium teakwood work, modern modular kitchen, private elevator access, and secure dual parking.',
            'rent': 1100000.00,
            'city': 'Trivandrum',
            'address': 'Kovalam Beach Road, Trivandrum',
            'bedrooms': 8,
            'bathrooms': 9,
            'area': 6000,
            'furnished': True,
            'parking': True,
            'available': True,
            'main_image': 'properties/main/Penthouse_overlooking_Arabian_Sea_2K_202607181834.jpeg',
            'gallery': ['properties/gallery/penthouse_gallery1.jpg', 'properties/gallery/penthouse_gallery2.jpg']
        },
        {
            'title': 'Kozhikode Downtown Studio Loft',
            'description': 'Compact and highly functional loft-style studio situated in the Kozhikode city center. Close to major IT parks and top restaurants. Fully furnished with high-speed internet connectivity, modular convertible furniture, and balcony.',
            'rent': 12000.00,
            'city': 'Kozhikode',
            'address': 'Mavoor Road, Kozhikode',
            'bedrooms': 1,
            'bathrooms': 1,
            'area': 620,
            'furnished': True,
            'parking': False,
            'available': True,
            'main_image': 'properties/main/studio_main.jpg',
            'gallery': ['properties/gallery/studio_gallery1.jpg', 'properties/gallery/studio_gallery2.jpg']
        },
        {
            'title': 'Thrissur Spacious Family Townhouse',
            'description': 'Beautiful 3-story townhouse with a private garden in Thrissur. Offers a large spacious dining hall, newly polished traditional wood floors, laundry amenities on-site, and dedicated garage space. Close to Thrissur Round and schools.',
            'rent': 160000.00,
            'city': 'Thrissur',
            'address': 'Round North, Thrissur',
            'bedrooms': 3,
            'bathrooms': 2,
            'area': 2100,
            'furnished': False,
            'parking': True,
            'available': True,
            'main_image': 'properties/main/townhouse_main.jpg',
            'gallery': ['properties/gallery/townhouse_gallery1.jpg', 'properties/gallery/townhouse_gallery2.jpg']
        },
        {
            'title': 'Munnar Tea Garden Cottage',
            'description': 'Tranquil cottage overlooking green tea plantations in Munnar. Features private balconies, cozy fireplace setup, and scenic misty valley views. Ideal for residents seeking peace and nature away from the city.',
            'rent': 68000.00,
            'city': 'Munnar',
            'address': 'Munnar Hills View Road, Munnar',
            'bedrooms': 2,
            'bathrooms': 2,
            'area': 1650,
            'furnished': True,
            'parking': True,
            'available': True,
            'main_image': 'properties/main/Tea_garden_cottage_among_plantat_202607181720.jpeg',
            'gallery': ['properties/gallery/Tea_garden_cottage_among_plantat_202607181723.jpeg', 'properties/gallery/Tea_garden_cottage_among_plantat_202607181733.jpeg']
        },
        {
            'title': 'Kochi Central Modern Apartment',
            'description': 'Newly built modern 2-bedroom apartment with a balcony in Ernakulam. Features a contemporary open-concept layout, fully equipped modular kitchen, 24/7 security, power backup, and access to a shared rooftop terrace.',
            'rent': 500000.00,
            'city': 'Kochi',
            'address': 'MG Road, Ernakulam, Kochi',
            'bedrooms': 5,
            'bathrooms': 5,
            'area': 1559,
            'furnished': True,
            'parking': True,
            'available': True,
            'main_image': 'properties/main/apartment_main.jpg',
            'gallery': ['properties/gallery/apartment_gallery1.jpg', 'properties/gallery/apartment_gallery2.jpg']
        }
    ]

    for prop_data in properties_to_create:
        p = Property.objects.create(
            title=prop_data['title'],
            description=prop_data['description'],
            rent=prop_data['rent'],
            city=prop_data['city'],
            address=prop_data['address'],
            bedrooms=prop_data['bedrooms'],
            bathrooms=prop_data['bathrooms'],
            area=prop_data['area'],
            furnished=prop_data['furnished'],
            parking=prop_data['parking'],
            available=prop_data['available'],
            main_image=prop_data['main_image']
        )
        print(f"Created property listing: {p.title}")
        
        # Add secondary gallery images
        for gallery_img in prop_data['gallery']:
            PropertyImage.objects.create(
                property=p,
                image=gallery_img
            )
            print(f"  Added gallery image: {gallery_img}")
            
    print("Database seeding completed successfully!")

if __name__ == '__main__':
    run_seeding()
