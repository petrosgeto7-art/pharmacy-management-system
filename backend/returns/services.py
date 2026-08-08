from django.db import transaction
from .models import Return, ReturnItem
from inventory.models import StockMovement
from audit.models import AuditLog

class ReturnService:
    @staticmethod
    @transaction.atomic
    def process_return(return_id, user):
        """
        Process a return: Mark as approved, restock items if requested, and refund.
        """
        return_record = Return.objects.select_for_update().get(id=return_id)
        
        if return_record.status != 'pending':
            raise ValueError(f"Return is already {return_record.status}")
            
        for item in return_record.items.all():
            sale_item = item.sale_item
            batch = item.batch
            
            if item.quantity > sale_item.quantity:
                raise ValueError(f"Cannot return more than sold for {sale_item.medicine.name}")
                
            if item.restock:
                batch.current_qty += item.quantity
                if batch.current_qty > 0 and batch.status == 'empty':
                    batch.status = 'active'
                batch.save()
                
                # Create stock movement
                StockMovement.objects.create(
                    batch=batch,
                    movement_type='return_in',
                    quantity=item.quantity,
                    reference_type='return',
                    reference_id=return_record.id,
                    notes=f"Return {return_record.return_number} from Sale {return_record.sale.sale_number}",
                    created_by=user
                )

        # Update customer balance if applicable
        if return_record.customer:
            # If they had an outstanding balance, reduce it. Otherwise, it might be a cash refund.
            return_record.customer.outstanding_balance -= return_record.total_refund
            return_record.customer.save()
            
        return_record.status = 'completed'
        return_record.processed_by = user
        return_record.save()
        
        # Log Audit
        AuditLog.objects.create(
            user=user,
            action='process',
            entity_type='Return',
            entity_id=str(return_record.id),
            description=f"Processed return {return_record.return_number}"
        )
        
        return return_record
