from django.contrib import admin
from .models import Return, ReturnItem

class ReturnItemInline(admin.TabularInline):
    model = ReturnItem
    extra = 1

@admin.register(Return)
class ReturnAdmin(admin.ModelAdmin):
    list_display = ['return_number', 'sale', 'customer', 'date', 'total_refund', 'status']
    list_filter = ['status', 'date']
    search_fields = ['return_number', 'sale__sale_number', 'customer__name']
    inlines = [ReturnItemInline]
    date_hierarchy = 'date'
