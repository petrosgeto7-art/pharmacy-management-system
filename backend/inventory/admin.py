from django.contrib import admin
from .models import Batch, StockMovement


@admin.register(Batch)
class BatchAdmin(admin.ModelAdmin):
    list_display = ('batch_number', 'medicine', 'supplier', 'current_qty', 'expiry_date', 'status')
    list_filter = ('status', 'supplier')
    search_fields = ('batch_number', 'medicine__name')
    ordering = ('expiry_date',)
    date_hierarchy = 'expiry_date'
    list_per_page = 25


@admin.register(StockMovement)
class StockMovementAdmin(admin.ModelAdmin):
    list_display = ('batch', 'movement_type', 'quantity', 'reference_type', 'timestamp', 'created_by')
    list_filter = ('movement_type', 'reference_type')
    search_fields = ('batch__batch_number', 'notes')
    ordering = ('-timestamp',)
    readonly_fields = ('timestamp',)
