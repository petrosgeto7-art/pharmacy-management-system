from django.contrib import admin
from .models import Sale, SaleItem

class SaleItemInline(admin.TabularInline):
    model = SaleItem
    extra = 1

@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ['sale_number', 'customer', 'date', 'total', 'payment_method', 'status']
    list_filter = ['status', 'payment_method', 'date']
    search_fields = ['sale_number', 'customer__name']
    inlines = [SaleItemInline]
    date_hierarchy = 'date'
