from django.db import models

class Notification(models.Model):
    """System notifications for users."""
    TYPE_CHOICES = [
        ('low_stock', 'Low Stock'),
        ('out_of_stock', 'Out of Stock'),
        ('expiring_soon', 'Expiring Soon'),
        ('expired', 'Expired'),
        ('large_transaction', 'Large Transaction'),
        ('failed_payment', 'Failed Payment'),
        ('pending_prescription', 'Pending Prescription'),
        ('system', 'System Message'),
    ]

    id = models.AutoField(primary_key=True)
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='notifications', null=True, blank=True, help_text="Null means broadcast to all/admins based on type")
    
    type = models.CharField(max_length=50, choices=TYPE_CHOICES)
    title = models.CharField(max_length=255)
    message = models.TextField()
    
    is_read = models.BooleanField(default=False)
    
    # Optional polymorphic link to related entity
    entity_type = models.CharField(max_length=50, blank=True, default='')
    entity_id = models.CharField(max_length=50, blank=True, default='')
    
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        db_table = 'notifications'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.get_type_display()} - {self.title}"
