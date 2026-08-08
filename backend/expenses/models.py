from django.db import models

class Expense(models.Model):
    """Pharmacy expenses."""
    CATEGORY_CHOICES = [
        ('rent', 'Rent'),
        ('electricity', 'Electricity'),
        ('salary', 'Salary'),
        ('transportation', 'Transportation'),
        ('maintenance', 'Maintenance'),
        ('marketing', 'Marketing'),
        ('supplies', 'Office Supplies'),
        ('tax', 'Taxes & Licenses'),
        ('other', 'Other'),
    ]
    
    PAYMENT_METHOD_CHOICES = [
        ('cash', 'Cash'),
        ('bank_transfer', 'Bank Transfer'),
        ('card', 'Credit/Debit Card'),
        ('cheque', 'Cheque'),
        ('other', 'Other'),
    ]

    id = models.AutoField(primary_key=True)
    expense_number = models.CharField(max_length=50, unique=True, db_index=True)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='other')
    description = models.CharField(max_length=255)
    
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    date = models.DateField(db_index=True)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES, default='cash')
    
    created_by = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, null=True, related_name='expenses_created')
    notes = models.TextField(blank=True, default='')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'expenses'
        ordering = ['-date', '-created_at']

    def __str__(self):
        return f"{self.expense_number} - {self.get_category_display()} ({self.amount})"
