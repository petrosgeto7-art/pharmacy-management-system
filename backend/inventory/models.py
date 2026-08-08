from django.db import models
from django.core.exceptions import ValidationError

class Batch(models.Model):
    """Batches of medicines representing actual physical stock (FEFO)."""
    id = models.AutoField(primary_key=True)
    batch_number = models.CharField(max_length=100, db_index=True)
    medicine = models.ForeignKey('medicines.Medicine', on_delete=models.PROTECT, related_name='batches')
    supplier = models.ForeignKey('suppliers.Supplier', on_delete=models.SET_NULL, null=True, blank=True, related_name='batches')
    
    purchase_date = models.DateField(null=True, blank=True)
    manufacturing_date = models.DateField(null=True, blank=True)
    expiry_date = models.DateField(db_index=True)
    
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2)
    selling_price = models.DecimalField(max_digits=10, decimal_places=2)
    
    qty_received = models.PositiveIntegerField(default=0)
    current_qty = models.PositiveIntegerField(default=0)
    damaged_qty = models.PositiveIntegerField(default=0)
    reserved_qty = models.PositiveIntegerField(default=0)
    
    location = models.CharField(max_length=100, blank=True, default='')
    status = models.CharField(max_length=20, choices=[
        ('active', 'Active'),
        ('expired', 'Expired'),
        ('empty', 'Empty'),
        ('quarantine', 'Quarantine'),
    ], default='active')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'batches'
        unique_together = ('batch_number', 'medicine')
        ordering = ['expiry_date', 'created_at']
        verbose_name_plural = 'batches'

    def __str__(self):
        return f"{self.medicine.name} - {self.batch_number} (Exp: {self.expiry_date})"

    def clean(self):
        if self.manufacturing_date and self.expiry_date and self.manufacturing_date >= self.expiry_date:
            raise ValidationError("Manufacturing date must be before expiry date.")

    @property
    def available_qty(self):
        return self.current_qty - self.reserved_qty


class StockMovement(models.Model):
    """Audit trail of all inventory changes."""
    MOVEMENT_TYPES = [
        ('purchase', 'Purchase (In)'),
        ('sale', 'Sale (Out)'),
        ('return_in', 'Customer Return (In)'),
        ('return_out', 'Supplier Return (Out)'),
        ('adjustment_up', 'Manual Adjustment (Up)'),
        ('adjustment_down', 'Manual Adjustment (Down)'),
        ('damage', 'Damage/Spoilage (Out)'),
        ('expiry', 'Expiry (Out)'),
        ('transfer_in', 'Transfer (In)'),
        ('transfer_out', 'Transfer (Out)'),
    ]

    id = models.AutoField(primary_key=True)
    batch = models.ForeignKey(Batch, on_delete=models.PROTECT, related_name='movements')
    movement_type = models.CharField(max_length=20, choices=MOVEMENT_TYPES)
    quantity = models.IntegerField(help_text="Positive for inward, negative for outward")
    
    # Polymorphic-like reference (optional, keeping it simple with string type and integer ID)
    reference_type = models.CharField(max_length=50, blank=True, default='', help_text="e.g., 'sale', 'purchase', 'adjustment'")
    reference_id = models.IntegerField(null=True, blank=True)
    
    notes = models.TextField(blank=True, default='')
    created_by = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, null=True, related_name='stock_movements')
    timestamp = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        db_table = 'stock_movements'
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.get_movement_type_display()} - {self.batch.batch_number} ({self.quantity})"
