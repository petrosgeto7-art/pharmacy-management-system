from django.contrib import admin
from .models import Return, ReturnItem


class ReturnItemInline(admin.TabularInline):
    model = ReturnItem
    extra = 0


@admin.register(Return)
class ReturnAdmin(admin.ModelAdmin):
    list_display = ('return_number', 'sale', 'customer', 'total_refund', 'status', 'date')
    list_filter = ('status',)
    search_fields = ('return_number', 'customer__name', 'sale__sale_number')
    ordering = ('-date',)
    inlines = [ReturnItemInline]
