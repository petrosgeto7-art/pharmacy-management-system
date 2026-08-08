from django.db import models

class AuditLog(models.Model):
    """Immutable audit trail of important system actions."""
    ACTION_CHOICES = [
        ('login', 'Login'),
        ('logout', 'Logout'),
        ('create', 'Create'),
        ('update', 'Update'),
        ('delete', 'Delete'),
        ('deactivate', 'Deactivate'),
        ('approve', 'Approve'),
        ('reject', 'Reject'),
        ('process', 'Process'),
        ('cancel', 'Cancel'),
    ]

    id = models.AutoField(primary_key=True)
    user = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, null=True, related_name='audit_logs')
    
    action = models.CharField(max_length=50, choices=ACTION_CHOICES)
    entity_type = models.CharField(max_length=100, help_text="Model name, e.g., 'Medicine', 'Sale'")
    entity_id = models.CharField(max_length=100, help_text="ID of the entity")
    
    old_values = models.JSONField(null=True, blank=True)
    new_values = models.JSONField(null=True, blank=True)
    
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    description = models.TextField(blank=True, default='')
    
    timestamp = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        db_table = 'audit_logs'
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.user} {self.action} {self.entity_type} ({self.entity_id})"
