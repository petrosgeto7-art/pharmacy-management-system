from django.contrib import admin
from .models import Batch, StockMovement

@admin.register(Batch)
class BatchAdmin(admin.ModelAdmin):
    list_display = ['batch_number', 'medicine', 'supplier', 'expiry_date', 'qty_received', 'current_qty', 'status']
    list_filter = ['status', 'medicine__category']
    search_fields = ['batch_number', 'medicine__name']
    date_hierarchy = 'expiry_date'

@admin.register(StockMovement)
class StockMovementAdmin(admin.ModelAdmin):
    list_display = ['batch', 'movement_type', 'quantity', 'timestamp', 'created_by']
    list_filter = ['movement_type']
    search_fields = ['batch__batch_number', 'batch__medicine__name']
    date_hierarchy = 'timestamp'
