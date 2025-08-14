import os
import django

# 1. Set up Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "brandmetrics.settings")
django.setup()

from django.contrib.auth.models import User
from chat.models import Employee

# 2. Data to import
records = [
    ("John Doe", "john@example.com", "9876543210", "Sales Closer", "New York", "Active", "hashed_pass1"),
    ("Jane Smith", "jane@example.com", "9876543211", "Sales Manager", "Los Angeles", "Active", "hashed_pass2"),
    ("Mike Brown", "mike@example.com", "9876543212", "Installer", "Chicago", "Inactive", "hashed_pass3"),
]

# 3. Insert data
for name, email, phone, position, city, status, raw_pass in records:
    first_name, *last_name = name.split(" ", 1)
    last_name = last_name[0] if last_name else ""

    if User.objects.filter(email=email).exists():
        print(f"⚠ Skipping {email} — already exists.")
        continue

    # Create User with password hashing
    user = User.objects.create_user(
        username=email,
        email=email,
        password=raw_pass,
        first_name=first_name,
        last_name=last_name
    )

    Employee.objects.create(
        user=user,
        name=name,
        email=email,
        phone=phone,
        position=position,
        city=city,
        status=status
    )

    print(f"✅ Added employee: {name} ({email})")

print("🎯 Import complete.")
