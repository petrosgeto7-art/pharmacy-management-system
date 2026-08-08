from django.contrib import admin
from .models import Medicine, Category, Manufacturer


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'created_at')
    search_fields = ('name',)
    ordering = ('name',)


@admin.register(Manufacturer)
class ManufacturerAdmin(admin.ModelAdmin):
    list_display = ('name', 'country', 'created_at')
    search_fields = ('name', 'country')
    ordering = ('name',)


@admin.register(Medicine)
class MedicineAdmin(admin.ModelAdmin):
    list_display = ('name', 'generic_name', 'category', 'manufacturer', 'selling_price', 'status', 'requires_prescription')
    list_filter = ('status', 'category', 'manufacturer', 'dosage_form', 'requires_prescription')
    search_fields = ('name', 'generic_name', 'sku', 'barcode')
    ordering = ('name',)
    list_per_page = 25
