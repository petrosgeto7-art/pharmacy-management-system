from django.contrib import admin
from .models import Sale, SaleItem


class SaleItemInline(admin.TabularInline):
    model = SaleItem
    extra = 0
    readonly_fields = ('medicine', 'batch', 'quantity', 'unit_price', 'cost_price', 'total')


@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ('sale_number', 'customer', 'total', 'payment_method', 'payment_status', 'date', 'processed_by')
    list_filter = ('status', 'payment_method', 'payment_status')
    search_fields = ('sale_number', 'customer__name')
    ordering = ('-date',)
    inlines = [SaleItemInline]
    date_hierarchy = 'date'
