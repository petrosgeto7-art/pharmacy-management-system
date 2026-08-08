from django.contrib import admin
from .models import Supplier

@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ['name', 'contact_person', 'phone', 'email', 'outstanding_balance', 'status']
    list_filter = ['status']
    search_fields = ['name', 'contact_person', 'phone', 'email', 'tax_id']
