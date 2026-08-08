from django.contrib import admin
from .models import Customer

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['customer_number', 'name', 'phone', 'email', 'outstanding_balance', 'status']
    list_filter = ['status']
    search_fields = ['customer_number', 'name', 'phone', 'email']
