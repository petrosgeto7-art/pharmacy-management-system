from django.contrib import admin
from .models import AuditLog

@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ['user', 'action', 'entity_type', 'entity_id', 'timestamp']
    list_filter = ['action', 'entity_type', 'timestamp']
    search_fields = ['user__username', 'entity_type', 'entity_id', 'description']
    date_hierarchy = 'timestamp'
    readonly_fields = ['user', 'action', 'entity_type', 'entity_id', 'old_values', 'new_values', 'ip_address', 'description', 'timestamp']

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
