import os
import django

# Setup Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "brandmetrics.settings")
django.setup()

from chat.models import Order, Employee

# Order data: (CustomerName, Email, Phone, CloserEmpID, ContractPrice, SystemSize, Stage, Redline)
records = [
    ("Alice Johnson", "alice@example.com", "9998887777", 1, 15000.00, "6kW", "PTO", "Yes"),
    ("Bob Williams", "bob@example.com", "8887776666", 2, 20000.00, "8kW", "Installation", "No"),
    ("Charlie Green", "charlie@example.com", "7776665555", 1, 18000.00, "7kW", "Design", "Yes"),
    ("Diana Rose", "diana@example.com", "6665554444", 3, 22000.00, "9kW", "Site Survey", "No"),
    ("Ethan Clark", "ethan@example.com", "5554443333", 2, 25000.00, "10kW", "Permitting", "Yes"),
    ("Fiona Lee", "fiona@example.com", "4443332222", 1, 12000.00, "5kW", "Installation", "Yes"),
    ("George Adams", "george@example.com", "3332221111", 2, 30000.00, "12kW", "PTO", "No"),
    ("Hannah Scott", "hannah@example.com", "2221110000", 3, 14000.00, "6kW", "Design", "Yes"),
    ("Ian Thomas", "ian@example.com", "1110009999", 1, 19000.00, "7.5kW", "Installation", "No"),
    ("Julia White", "julia@example.com", "0009998888", 2, 21000.00, "8kW", "Site Survey", "Yes"),
    ("Kevin Harris", "kevin@example.com", "9998887776", 3, 17500.00, "6.5kW", "Design", "No"),
    ("Laura Young", "laura@example.com", "8887776665", 1, 26000.00, "11kW", "Installation", "Yes"),
    ("Michael King", "michael@example.com", "7776665554", 2, 28000.00, "12kW", "PTO", "Yes"),
    ("Nina Baker", "nina@example.com", "6665554443", 3, 13500.00, "5.5kW", "Permitting", "No"),
    ("Oliver Perez", "oliver@example.com", "5554443332", 1, 24000.00, "10kW", "Installation", "Yes"),
    ("Paula Reed", "paula@example.com", "4443332221", 2, 15500.00, "6.5kW", "Design", "No"),
    ("Quinn Foster", "quinn@example.com", "3332221110", 3, 20000.00, "8kW", "Site Survey", "Yes"),
    ("Rachel Evans", "rachel@example.com", "2221110009", 1, 17000.00, "7kW", "Installation", "No"),
    ("Samuel Price", "samuel@example.com", "1110009998", 2, 22500.00, "9.5kW", "PTO", "Yes"),
    ("Tina Ward", "tina@example.com", "0009998887", 3, 15000.00, "6kW", "Permitting", "No"),
]

for cust_name, email, phone, closer_id, price, system_size, stage, redline in records:
    closer = Employee.objects.filter(emp_id=closer_id).first()
    if not closer:
        print(f"⚠ Skipping {cust_name} — closer with EmpID={closer_id} not found.")
        continue

    if Order.objects.filter(customer_name=cust_name, email=email).exists():
        print(f"⚠ Skipping {cust_name} — order already exists.")
        continue

    Order.objects.create(
        customer_name=cust_name,
        email=email,
        phone=phone,
        closer=closer,
        contract_price=price,
        system_size=system_size,
        stage=stage,
        redline=redline
    )
    print(f"✅ Added order for {cust_name}")

print("🎯 Orders import complete.")
