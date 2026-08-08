from django.contrib import admin
from .models import Purchase, PurchaseItem

class PurchaseItemInline(admin.TabularInline):
    model = PurchaseItem
    extra = 1

@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    list_display = ['purchase_number', 'supplier', 'date', 'total', 'status', 'payment_status']
    list_filter = ['status', 'payment_status', 'date']
    search_fields = ['purchase_number', 'supplier__name']
    inlines = [PurchaseItemInline]
    date_hierarchy = 'date'
