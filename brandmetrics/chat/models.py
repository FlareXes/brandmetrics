from django.db import models
from django.contrib.auth.models import User


class Employee(models.Model):
    STATUS_CHOICES = [
        ('Active', 'Active'),
        ('Inactive', 'Inactive'),
    ]

    emp_id = models.AutoField(primary_key=True)
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="employee_profile")
    email = models.EmailField(
        max_length=100, unique=True, blank=True, null=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    position = models.CharField(max_length=50, blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)
    status = models.CharField(
        max_length=8, choices=STATUS_CHOICES, default='Active')

    class Meta:
        db_table = "employees"
        verbose_name = "Employee"
        verbose_name_plural = "Employees"

    def __str__(self):
        return f"{self.name} ({self.email})"


class Order(models.Model):
    pid = models.AutoField(primary_key=True)
    closer = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True)
    customer_name = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(max_length=100, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    contract_price = models.DecimalField(max_digits=12, decimal_places=2)
    system_size = models.CharField(max_length=50, blank=True, null=True)
    stage = models.CharField(max_length=50, blank=True, null=True)
    redline = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        db_table = "orders"
        verbose_name = "Order"
        verbose_name_plural = "Orders"

    def __str__(self):
        return f"{self.customer_name} ({self.email})"


class Payout(models.Model):
    id = models.AutoField(primary_key=True)
    pid = models.ForeignKey(Order, on_delete=models.CASCADE)
    emp_id = models.ForeignKey(Employee, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    type = models.CharField(max_length=8, choices=[
        ('M1', 'M1'),
        ('M2', 'M2'),
        ('M3', 'M3'),
        ('Clawback', 'Clawback'),
    ])
    paying_date = models.DateField()

    class Meta:
        db_table = "payouts"
        verbose_name = "Payout"
        verbose_name_plural = "Payouts"

    def __str__(self):
        return f"{self.emp_id} - {self.type} - {self.paying_date}"
