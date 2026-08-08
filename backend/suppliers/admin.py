from django.contrib import admin
from .models import Supplier


@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ('name', 'contact_person', 'phone', 'email', 'status', 'outstanding_balance')
    list_filter = ('status',)
    search_fields = ('name', 'contact_person', 'email', 'tax_id')
    ordering = ('name',)
