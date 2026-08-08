from django.db import models


class Category(models.Model):
    """Medicine categories."""
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, default='')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'categories'
        ordering = ['name']
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name


class Manufacturer(models.Model):
    """Medicine manufacturers."""
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200, unique=True)
    country = models.CharField(max_length=100, blank=True, default='')
    contact_email = models.EmailField(blank=True, default='')
    contact_phone = models.CharField(max_length=20, blank=True, default='')
    website = models.URLField(blank=True, default='')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'manufacturers'
        ordering = ['name']

    def __str__(self):
        return self.name


class Medicine(models.Model):
    """Medicine / product model."""

    DOSAGE_FORMS = [
        ('tablet', 'Tablet'),
        ('capsule', 'Capsule'),
        ('syrup', 'Syrup'),
        ('injection', 'Injection'),
        ('cream', 'Cream'),
        ('ointment', 'Ointment'),
        ('drops', 'Drops'),
        ('inhaler', 'Inhaler'),
        ('suppository', 'Suppository'),
        ('powder', 'Powder'),
        ('gel', 'Gel'),
        ('solution', 'Solution'),
        ('suspension', 'Suspension'),
        ('spray', 'Spray'),
        ('patch', 'Patch'),
        ('other', 'Other'),
    ]

    UNIT_CHOICES = [
        ('pcs', 'Pieces'),
        ('box', 'Box'),
        ('strip', 'Strip'),
        ('bottle', 'Bottle'),
        ('tube', 'Tube'),
        ('vial', 'Vial'),
        ('ampoule', 'Ampoule'),
        ('sachet', 'Sachet'),
        ('pack', 'Pack'),
        ('other', 'Other'),
    ]

    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('discontinued', 'Discontinued'),
    ]

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=300, db_index=True)
    generic_name = models.CharField(max_length=300, blank=True, default='')
    brand_name = models.CharField(max_length=300, blank=True, default='')
    sku = models.CharField(max_length=50, unique=True, blank=True, null=True)
    barcode = models.CharField(max_length=100, unique=True, blank=True, null=True,
                                db_index=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT,
                                  related_name='medicines', null=True, blank=True)
    dosage_form = models.CharField(max_length=20, choices=DOSAGE_FORMS,
                                    default='tablet')
    strength = models.CharField(max_length=100, blank=True, default='',
                                 help_text='e.g., 500mg, 10ml')
    unit = models.CharField(max_length=20, choices=UNIT_CHOICES, default='pcs')
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.SET_NULL,
                                      related_name='medicines', null=True, blank=True)
    description = models.TextField(blank=True, default='')
    requires_prescription = models.BooleanField(default=False)
    min_stock_level = models.PositiveIntegerField(default=10)
    reorder_level = models.PositiveIntegerField(default=20)
    selling_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    tax_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0,
                                    help_text='Tax percentage')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    image = models.ImageField(upload_to='medicines/', null=True, blank=True)
    notes = models.TextField(blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'medicines'
        ordering = ['name']
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['generic_name']),
            models.Index(fields=['barcode']),
            models.Index(fields=['status']),
        ]

    def __str__(self):
        strength_str = f" {self.strength}" if self.strength else ""
        return f"{self.name}{strength_str}"

    @property
    def total_stock(self):
        """Get total current stock across all active batches."""
        from inventory.models import Batch
        return self.batches.filter(
            status='active',
            expiry_date__gt=models.functions.Now()
        ).aggregate(total=models.Sum('current_qty'))['total'] or 0

    @property
    def is_low_stock(self):
        return self.total_stock <= self.min_stock_level

    @property
    def is_out_of_stock(self):
        return self.total_stock == 0
