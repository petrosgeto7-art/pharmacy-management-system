from django.contrib import admin
from .models import AuditLog


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'action', 'entity_type', 'entity_id', 'timestamp', 'ip_address')
    list_filter = ('action', 'entity_type')
    search_fields = ('entity_type', 'entity_id', 'description', 'user__username')
    ordering = ('-timestamp',)
    readonly_fields = ('user', 'action', 'entity_type', 'entity_id', 'description', 'timestamp', 'ip_address')
    
    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False
    
    def has_delete_permission(self, request, obj=None):
        return False
