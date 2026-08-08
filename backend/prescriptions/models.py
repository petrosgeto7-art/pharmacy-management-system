from django.db import models

class Prescription(models.Model):
    """Prescriptions for customers/patients."""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('partially_dispensed', 'Partially Dispensed'),
        ('fully_dispensed', 'Fully Dispensed'),
        ('cancelled', 'Cancelled'),
    ]

    id = models.AutoField(primary_key=True)
    prescription_number = models.CharField(max_length=50, unique=True, db_index=True)
    customer = models.ForeignKey('customers.Customer', on_delete=models.CASCADE, related_name='prescriptions')
    doctor_name = models.CharField(max_length=255)
    clinic_name = models.CharField(max_length=255, blank=True, default='')
    
    prescription_date = models.DateField(db_index=True)
    expiry_date = models.DateField(null=True, blank=True)
    
    status = models.CharField(max_length=25, choices=STATUS_CHOICES, default='pending')
    notes = models.TextField(blank=True, default='')
    
    dispensed_by = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, null=True, blank=True, related_name='dispensed_prescriptions')
    dispensed_date = models.DateTimeField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'prescriptions'
        ordering = ['-prescription_date', '-created_at']

    def __str__(self):
        return f"RX-{self.prescription_number} ({self.customer.name})"


class PrescriptionItem(models.Model):
    """Medicines prescribed within a prescription."""
    id = models.AutoField(primary_key=True)
    prescription = models.ForeignKey(Prescription, on_delete=models.CASCADE, related_name='items')
    medicine = models.ForeignKey('medicines.Medicine', on_delete=models.PROTECT, related_name='prescription_items')
    
    dosage_instructions = models.CharField(max_length=255, blank=True, default='')
    frequency = models.CharField(max_length=100, blank=True, default='')
    duration = models.CharField(max_length=100, blank=True, default='')
    
    quantity_prescribed = models.PositiveIntegerField()
    quantity_dispensed = models.PositiveIntegerField(default=0)
    
    notes = models.TextField(blank=True, default='')

    class Meta:
        db_table = 'prescription_items'
        ordering = ['id']

    def __str__(self):
        return f"{self.medicine.name} for RX-{self.prescription.prescription_number}"
