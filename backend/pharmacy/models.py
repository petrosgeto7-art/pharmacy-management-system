from django.db import models

class Pharmacy(models.Model):
    """Global pharmacy settings and info."""
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    address = models.TextField(blank=True, default='')
    phone = models.CharField(max_length=50, blank=True, default='')
    email = models.EmailField(blank=True, default='')
    website = models.URLField(blank=True, default='')
    
    license_number = models.CharField(max_length=100, blank=True, default='')
    tax_id = models.CharField(max_length=100, blank=True, default='')
    
    logo = models.ImageField(upload_to='pharmacy/', null=True, blank=True)
    
    # Store dynamic settings like currency, timezone, etc.
    settings = models.JSONField(default=dict, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'pharmacy'
        verbose_name_plural = 'Pharmacies'

    def __str__(self):
        return self.name
