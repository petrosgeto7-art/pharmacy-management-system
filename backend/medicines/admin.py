from django.contrib import admin
from .models import Medicine, Category, Manufacturer

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_active', 'created_at']
    search_fields = ['name']

@admin.register(Manufacturer)
class ManufacturerAdmin(admin.ModelAdmin):
    list_display = ['name', 'country', 'is_active']
    search_fields = ['name']

@admin.register(Medicine)
class MedicineAdmin(admin.ModelAdmin):
    list_display = ['name', 'generic_name', 'category', 'dosage_form', 'strength',
                    'selling_price', 'requires_prescription', 'status']
    list_filter = ['category', 'dosage_form', 'status', 'requires_prescription']
    search_fields = ['name', 'generic_name', 'brand_name', 'barcode', 'sku']
