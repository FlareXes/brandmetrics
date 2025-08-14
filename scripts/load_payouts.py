import os
import django

# Setup Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "brandmetrics.settings")
django.setup()

from chat.models import Payout, Order, Employee

# Data: (PID, EmpID, Amount, Type, PayingDate)
records = [
    (1, 1, 500.00, 'M1', '2025-08-01'),
    (2, 2, 800.00, 'M1', '2025-08-02'),
    (3, 1, 600.00, 'M1', '2025-08-03'),
    (4, 3, 750.00, 'M1', '2025-08-04'),
    (5, 2, 900.00, 'M1', '2025-08-05'),
    (6, 1, 450.00, 'M2', '2025-08-06'),
    (7, 2, 1000.00, 'M2', '2025-08-07'),
    (8, 3, 500.00, 'M2', '2025-08-08'),
    (9, 1, 700.00, 'M2', '2025-08-09'),
    (10, 2, 800.00, 'M3', '2025-08-10'),
    (11, 3, 400.00, 'M3', '2025-08-11'),
    (12, 1, 950.00, 'M3', '2025-08-12'),
    (13, 2, 1100.00, 'M3', '2025-08-13'),
    (14, 3, -300.00, 'Clawback', '2025-08-14'),
    (15, 1, 1200.00, 'M1', '2025-08-15'),
    (16, 2, 600.00, 'M2', '2025-08-16'),
    (17, 3, 500.00, 'M3', '2025-08-17'),
    (18, 1, -200.00, 'Clawback', '2025-08-18'),
    (19, 2, 900.00, 'M1', '2025-08-19'),
    (20, 3, 700.00, 'M2', '2025-08-20'),
]

for pid_val, emp_id_val, amount, payout_type, date_str in records:
    order = Order.objects.filter(pid=pid_val).first()
    emp = Employee.objects.filter(emp_id=emp_id_val).first()

    if not order:
        print(f"⚠ Skipping payout — Order with PID={pid_val} not found.")
        continue

    if not emp:
        print(f"⚠ Skipping payout — Employee with EmpID={emp_id_val} not found.")
        continue

    if Payout.objects.filter(pid=order, emp_id=emp, type=payout_type, paying_date=date_str).exists():
        print(f"⚠ Skipping duplicate payout for PID={pid_val}, EmpID={emp_id_val}, Date={date_str}")
        continue

    Payout.objects.create(
        pid=order,
        emp_id=emp,
        amount=amount,
        type=payout_type,
        paying_date=date_str
    )

    print(f"✅ Added payout: PID={pid_val}, EmpID={emp_id_val}, Type={payout_type}, Date={date_str}")

print("🎯 Payouts import complete.")
