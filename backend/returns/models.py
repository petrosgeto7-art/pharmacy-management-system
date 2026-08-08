from django.db import models

class Return(models.Model):
    """Customer returns from sales."""
    STATUS_CHOICES = [
        ('pending', 'Pending Approval'),
        ('approved', 'Approved'),
        ('completed', 'Completed'),
        ('rejected', 'Rejected'),
    ]

    id = models.AutoField(primary_key=True)
    return_number = models.CharField(max_length=50, unique=True, db_index=True)
    sale = models.ForeignKey('sales.Sale', on_delete=models.PROTECT, related_name='returns')
    customer = models.ForeignKey('customers.Customer', on_delete=models.SET_NULL, null=True, blank=True, related_name='returns')
    
    date = models.DateTimeField(auto_now_add=True, db_index=True)
    total_refund = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    
    reason = models.TextField(blank=True, default='')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    processed_by = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, null=True, related_name='returns_processed')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'returns'
        ordering = ['-date']

    def __str__(self):
        return f"Return {self.return_number} (Sale {self.sale.sale_number})"


class ReturnItem(models.Model):
    """Items being returned."""
    id = models.AutoField(primary_key=True)
    return_record = models.ForeignKey(Return, on_delete=models.CASCADE, related_name='items')
    sale_item = models.ForeignKey('sales.SaleItem', on_delete=models.PROTECT, related_name='return_items')
    batch = models.ForeignKey('inventory.Batch', on_delete=models.PROTECT, related_name='return_items')
    
    quantity = models.PositiveIntegerField()
    refund_amount = models.DecimalField(max_digits=10, decimal_places=2)
    restock = models.BooleanField(default=True, help_text="Should this item be added back to inventory?")

    class Meta:
        db_table = 'return_items'
        ordering = ['id']

    def __str__(self):
        return f"{self.quantity}x {self.sale_item.medicine.name} (Return {self.return_record.return_number})"
