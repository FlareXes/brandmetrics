from django.contrib import admin
from .models import Employee, Order, Payout

# Register your models here.
admin.site.register(Employee)
admin.site.register(Order)
admin.site.register(Payout)
