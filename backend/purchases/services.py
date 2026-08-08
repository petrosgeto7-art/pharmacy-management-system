from django.db import transaction
from .models import Purchase
from inventory.models import Batch, StockMovement
from audit.models import AuditLog

class PurchaseService:
    @staticmethod
    @transaction.atomic
    def complete_purchase(purchase_id, user):
        """
        Completes a purchase order:
        1. Changes status to 'received'
        2. Creates/updates Batches
        3. Creates StockMovements
        4. Updates Supplier balance
        5. Logs audit
        """
        purchase = Purchase.objects.select_for_update().get(id=purchase_id)
        
        if purchase.status == 'received':
            raise ValueError("Purchase is already received.")
            
        purchase.status = 'received'
        purchase.save()
        
        supplier = purchase.supplier
        
        for item in purchase.items.all():
            if item.quantity <= 0:
                continue
                
            # Create a new batch for this purchase item
            batch = Batch.objects.create(
                batch_number=item.batch_number or f"PO{purchase.purchase_number}-{item.id}",
                medicine=item.medicine,
                supplier=supplier,
                purchase_date=purchase.date,
                manufacturing_date=item.manufacturing_date,
                expiry_date=item.expiry_date,
                purchase_price=item.unit_price,
                selling_price=item.medicine.selling_price, # Default to medicine selling price
                qty_received=item.quantity,
                current_qty=item.quantity,
            )
            
            # Link item to batch
            item.batch = batch
            item.save()
            
            # Create stock movement
            StockMovement.objects.create(
                batch=batch,
                movement_type='purchase',
                quantity=item.quantity,
                reference_type='purchase',
                reference_id=purchase.id,
                notes=f"Received via PO {purchase.purchase_number}",
                created_by=user
            )
            
        # Update supplier balance
        supplier.outstanding_balance += purchase.total
        supplier.save()
        
        # Log Audit
        AuditLog.objects.create(
            user=user,
            action='process',
            entity_type='Purchase',
            entity_id=str(purchase.id),
            description=f"Completed purchase {purchase.purchase_number}"
        )
        
        return purchase
