from django.contrib import admin
from .models import Purchase, PurchaseItem


class PurchaseItemInline(admin.TabularInline):
    model = PurchaseItem
    extra = 0


@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    list_display = ('purchase_number', 'supplier', 'total', 'status', 'payment_status', 'date', 'created_by')
    list_filter = ('status', 'payment_status')
    search_fields = ('purchase_number', 'supplier__name')
    ordering = ('-date',)
    inlines = [PurchaseItemInline]
