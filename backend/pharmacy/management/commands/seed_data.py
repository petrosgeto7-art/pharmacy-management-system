from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta
import random

from accounts.models import Role, DEFAULT_ROLE_PERMISSIONS
from medicines.models import Category, Manufacturer, Medicine
from suppliers.models import Supplier
from inventory.models import Batch, StockMovement
from customers.models import Customer
from purchases.models import Purchase, PurchaseItem
from sales.models import Sale, SaleItem
from pharmacy.models import Pharmacy
from expenses.models import Expense

User = get_user_model()

class Command(BaseCommand):
    help = 'Seeds the database with realistic initial data'

    def handle(self, *args, **kwargs):
        self.stdout.write("Starting database seed...")

        # 1. Pharmacy
        pharmacy, _ = Pharmacy.objects.get_or_create(
            name="CarePlus Pharmacy",
            defaults={
                'address': '123 Health Ave, Medical District',
                'phone': '+1 (555) 123-4567',
                'email': 'contact@carepluspharmacy.com',
                'license_number': 'PHARM-2023-9876',
            }
        )
        self.stdout.write("Created Pharmacy settings.")

        # 2. Roles
        roles = {}
        for role_name, display_name in Role.ROLE_CHOICES:
            role, _ = Role.objects.get_or_create(
                name=role_name,
                defaults={
                    'display_name': display_name,
                    'permissions': DEFAULT_ROLE_PERMISSIONS.get(role_name, []),
                }
            )
            roles[role_name] = role
        self.stdout.write("Created Roles.")

        # 3. Users
        users_data = [
            {'username': 'admin', 'email': 'admin@careplus.com', 'role': roles[Role.SUPER_ADMIN], 'first': 'Super', 'last': 'Admin'},
            {'username': 'manager', 'email': 'manager@careplus.com', 'role': roles[Role.PHARMACY_MANAGER], 'first': 'John', 'last': 'Doe'},
            {'username': 'pharmacist', 'email': 'pharmacist@careplus.com', 'role': roles[Role.PHARMACIST], 'first': 'Jane', 'last': 'Smith'},
            {'username': 'cashier', 'email': 'cashier@careplus.com', 'role': roles[Role.CASHIER], 'first': 'Mike', 'last': 'Johnson'},
            {'username': 'inventory', 'email': 'inventory@careplus.com', 'role': roles[Role.INVENTORY_MANAGER], 'first': 'Sarah', 'last': 'Williams'},
        ]
        
        created_users = {}
        for u_data in users_data:
            user, created = User.objects.get_or_create(
                username=u_data['username'],
                defaults={
                    'email': u_data['email'],
                    'first_name': u_data['first'],
                    'last_name': u_data['last'],
                    'role': u_data['role'],
                    'pharmacy': pharmacy,
                    'is_staff': True,
                    'is_superuser': u_data['username'] == 'admin'
                }
            )
            if created:
                user.set_password('password123')
                user.save()
            created_users[u_data['username']] = user
        self.stdout.write("Created Users.")

        # 4. Categories
        categories = ['Antibiotics', 'Painkillers', 'Vitamins', 'Cardiovascular', 'Antacids', 'Antihistamines', 'Supplements', 'First Aid']
        cat_objs = []
        for cat in categories:
            obj, _ = Category.objects.get_or_create(name=cat)
            cat_objs.append(obj)
        self.stdout.write("Created Categories.")

        # 5. Manufacturers
        manufacturers = ['Pfizer', 'Novartis', 'Roche', 'Merck', 'GSK', 'Bayer', 'Local Pharma Ltd']
        mfg_objs = []
        for mfg in manufacturers:
            obj, _ = Manufacturer.objects.get_or_create(name=mfg, defaults={'country': 'USA'})
            mfg_objs.append(obj)
        self.stdout.write("Created Manufacturers.")

        # 6. Suppliers
        suppliers = ['MedSupply Co', 'Global Pharma Distributors', 'HealthCare Wholesale']
        sup_objs = []
        for sup in suppliers:
            obj, _ = Supplier.objects.get_or_create(
                name=sup, 
                defaults={
                    'contact_person': f"{sup} Rep",
                    'phone': '555-000-1111',
                    'email': f'sales@{sup.lower().replace(" ", "")}.com'
                }
            )
            sup_objs.append(obj)
        self.stdout.write("Created Suppliers.")

        # 7. Medicines & Batches
        medicines_data = [
            ('Amoxicillin', 'Amoxicillin', cat_objs[0], mfg_objs[0], 15.00, 'capsule', '500mg'),
            ('Paracetamol', 'Acetaminophen', cat_objs[1], mfg_objs[4], 5.00, 'tablet', '500mg'),
            ('Ibuprofen', 'Ibuprofen', cat_objs[1], mfg_objs[5], 8.00, 'tablet', '400mg'),
            ('Vitamin C', 'Ascorbic Acid', cat_objs[2], mfg_objs[6], 12.00, 'tablet', '1000mg'),
            ('Lisinopril', 'Lisinopril', cat_objs[3], mfg_objs[1], 25.00, 'tablet', '10mg'),
            ('Omeprazole', 'Omeprazole', cat_objs[4], mfg_objs[3], 18.00, 'capsule', '20mg'),
            ('Cetirizine', 'Cetirizine', cat_objs[5], mfg_objs[2], 10.00, 'tablet', '10mg'),
        ]

        today = timezone.now().date()
        admin_user = created_users['admin']
        
        for name, generic, cat, mfg, price, form, strength in medicines_data:
            med, _ = Medicine.objects.get_or_create(
                name=name,
                defaults={
                    'generic_name': generic,
                    'category': cat,
                    'manufacturer': mfg,
                    'selling_price': price,
                    'dosage_form': form,
                    'strength': strength,
                    'requires_prescription': name in ['Amoxicillin', 'Lisinopril'],
                    'min_stock_level': 50,
                    'reorder_level': 100,
                }
            )
            
            # Create 2 batches for each medicine
            for i in range(2):
                qty = random.randint(50, 200)
                purchase_price = float(price) * 0.6  # 40% margin
                
                # One batch expires in 3 months, one in 12 months
                exp_days = 90 if i == 0 else 365
                
                batch, batch_created = Batch.objects.get_or_create(
                    batch_number=f"B-{med.id}-{i+1}",
                    medicine=med,
                    defaults={
                        'supplier': random.choice(sup_objs),
                        'purchase_date': today - timedelta(days=30),
                        'expiry_date': today + timedelta(days=exp_days),
                        'purchase_price': purchase_price,
                        'selling_price': price,
                        'qty_received': qty,
                        'current_qty': qty,
                    }
                )
                
                if batch_created:
                    StockMovement.objects.create(
                        batch=batch,
                        movement_type='purchase',
                        quantity=qty,
                        notes='Initial Seed Stock',
                        created_by=admin_user
                    )
                    
        self.stdout.write("Created Medicines and Batches.")

        # 8. Customers
        for i in range(5):
            Customer.objects.get_or_create(
                customer_number=f"CUST-{i+1}",
                defaults={
                    'name': f"Customer {i+1}",
                    'phone': f"555-123-456{i}",
                }
            )
        self.stdout.write("Created Customers.")
        
        self.stdout.write(self.style.SUCCESS('Successfully seeded database! Login with admin / password123'))
