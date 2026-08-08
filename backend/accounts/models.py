from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid


class Role(models.Model):
    """User roles for RBAC."""
    SUPER_ADMIN = 'super_admin'
    PHARMACY_MANAGER = 'pharmacy_manager'
    PHARMACIST = 'pharmacist'
    CASHIER = 'cashier'
    INVENTORY_MANAGER = 'inventory_manager'

    ROLE_CHOICES = [
        (SUPER_ADMIN, 'Super Admin'),
        (PHARMACY_MANAGER, 'Pharmacy Manager'),
        (PHARMACIST, 'Pharmacist'),
        (CASHIER, 'Cashier'),
        (INVENTORY_MANAGER, 'Inventory Manager'),
    ]

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, unique=True, choices=ROLE_CHOICES)
    display_name = models.CharField(max_length=100)
    description = models.TextField(blank=True, default='')
    permissions = models.JSONField(default=list, blank=True,
        help_text='List of permission strings')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'roles'
        ordering = ['name']

    def __str__(self):
        return self.display_name

    def has_permission(self, permission):
        """Check if role has a specific permission."""
        return permission in self.permissions


# All available permissions
PERMISSIONS = [
    # Medicines
    'medicines.view', 'medicines.create', 'medicines.edit', 'medicines.delete',
    'categories.view', 'categories.create', 'categories.edit', 'categories.delete',
    # Inventory
    'inventory.view', 'inventory.adjust', 'inventory.manage',
    'batches.view', 'batches.create', 'batches.edit', 'batches.delete',
    # Suppliers
    'suppliers.view', 'suppliers.create', 'suppliers.edit', 'suppliers.delete',
    # Purchases
    'purchases.view', 'purchases.create', 'purchases.edit', 'purchases.delete',
    # Sales
    'sales.view', 'sales.create', 'sales.process_payment',
    # Prescriptions
    'prescriptions.view', 'prescriptions.create', 'prescriptions.edit', 'prescriptions.dispense',
    # Customers
    'customers.view', 'customers.create', 'customers.edit', 'customers.delete',
    # Returns
    'returns.view', 'returns.create', 'returns.approve',
    # Expenses
    'expenses.view', 'expenses.create', 'expenses.edit', 'expenses.delete',
    # Reports
    'reports.sales', 'reports.inventory', 'reports.financial', 'reports.export',
    # Admin
    'users.view', 'users.create', 'users.edit', 'users.delete',
    'roles.view', 'roles.manage',
    'audit.view',
    'settings.view', 'settings.manage',
    'notifications.view',
]

# Default permissions per role
DEFAULT_ROLE_PERMISSIONS = {
    Role.SUPER_ADMIN: PERMISSIONS,  # All permissions
    Role.PHARMACY_MANAGER: [
        'medicines.view', 'medicines.create', 'medicines.edit', 'medicines.delete',
        'categories.view', 'categories.create', 'categories.edit', 'categories.delete',
        'inventory.view', 'inventory.adjust', 'inventory.manage',
        'batches.view', 'batches.create', 'batches.edit', 'batches.delete',
        'suppliers.view', 'suppliers.create', 'suppliers.edit', 'suppliers.delete',
        'purchases.view', 'purchases.create', 'purchases.edit', 'purchases.delete',
        'sales.view', 'sales.create', 'sales.process_payment',
        'prescriptions.view', 'prescriptions.create', 'prescriptions.edit', 'prescriptions.dispense',
        'customers.view', 'customers.create', 'customers.edit', 'customers.delete',
        'returns.view', 'returns.create', 'returns.approve',
        'expenses.view', 'expenses.create', 'expenses.edit', 'expenses.delete',
        'reports.sales', 'reports.inventory', 'reports.financial', 'reports.export',
        'users.view', 'users.create', 'users.edit',
        'notifications.view',
    ],
    Role.PHARMACIST: [
        'medicines.view',
        'categories.view',
        'inventory.view',
        'batches.view',
        'suppliers.view',
        'sales.view', 'sales.create', 'sales.process_payment',
        'prescriptions.view', 'prescriptions.create', 'prescriptions.edit', 'prescriptions.dispense',
        'customers.view', 'customers.create', 'customers.edit',
        'returns.view', 'returns.create',
        'notifications.view',
    ],
    Role.CASHIER: [
        'medicines.view',
        'categories.view',
        'inventory.view',
        'batches.view',
        'sales.view', 'sales.create', 'sales.process_payment',
        'customers.view', 'customers.create',
        'returns.view', 'returns.create',
        'notifications.view',
    ],
    Role.INVENTORY_MANAGER: [
        'medicines.view', 'medicines.create', 'medicines.edit',
        'categories.view', 'categories.create', 'categories.edit',
        'inventory.view', 'inventory.adjust', 'inventory.manage',
        'batches.view', 'batches.create', 'batches.edit', 'batches.delete',
        'suppliers.view', 'suppliers.create', 'suppliers.edit',
        'purchases.view', 'purchases.create', 'purchases.edit',
        'reports.inventory',
        'notifications.view',
    ],
}


class User(AbstractUser):
    """Custom user model with role-based access."""
    id = models.AutoField(primary_key=True)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True, default='')
    role = models.ForeignKey(Role, on_delete=models.PROTECT, null=True, blank=True,
                             related_name='users')
    pharmacy = models.ForeignKey('pharmacy.Pharmacy', on_delete=models.SET_NULL,
                                 null=True, blank=True, related_name='users')
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    is_active = models.BooleanField(default=True)
    last_login_ip = models.GenericIPAddressField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    class Meta:
        db_table = 'users'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.get_full_name() or self.username}"

    def has_perm_custom(self, permission):
        """Check if user has a specific permission through their role."""
        if not self.role:
            return False
        if self.role.name == Role.SUPER_ADMIN:
            return True
        return self.role.has_permission(permission)

    @property
    def role_name(self):
        return self.role.name if self.role else None

    @property
    def is_admin(self):
        return self.role and self.role.name == Role.SUPER_ADMIN
