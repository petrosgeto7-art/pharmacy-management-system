from django.db import transaction
from django.utils import timezone
from .models import Sale, SaleItem
from inventory.models import Batch, StockMovement
from audit.models import AuditLog

class SaleService:
    @staticmethod
    @transaction.atomic
    def process_sale(sale_data, items_data, user):
        """
        Process a POS sale with FEFO batch selection.
        """
        # Create sale record
        sale = Sale.objects.create(
            sale_number=sale_data.get('sale_number'),
            customer=sale_data.get('customer'),
            prescription=sale_data.get('prescription'),
            subtotal=sale_data.get('subtotal', 0),
            tax=sale_data.get('tax', 0),
            discount=sale_data.get('discount', 0),
            total=sale_data.get('total', 0),
            payment_method=sale_data.get('payment_method', 'cash'),
            payment_status=sale_data.get('payment_status', 'paid'),
            amount_paid=sale_data.get('amount_paid', 0),
            change_due=sale_data.get('change_due', 0),
            notes=sale_data.get('notes', ''),
            processed_by=user
        )

        for item in items_data:
            medicine = item['medicine']
            requested_qty = item['quantity']
            unit_price = item['unit_price']
            
            # FEFO Logic: Find batches for this medicine, ordered by expiry date
            # Exclude expired batches and those with 0 current quantity
            available_batches = Batch.objects.filter(
                medicine=medicine,
                status='active',
                current_qty__gt=0,
                expiry_date__gt=timezone.now().date()
            ).order_by('expiry_date')
            
            qty_to_fulfill = requested_qty
            
            for batch in available_batches:
                if qty_to_fulfill <= 0:
                    break
                    
                qty_from_batch = min(qty_to_fulfill, batch.current_qty)
                
                # Create sale item
                SaleItem.objects.create(
                    sale=sale,
                    medicine=medicine,
                    batch=batch,
                    quantity=qty_from_batch,
                    unit_price=unit_price,
                    cost_price=batch.purchase_price,
                    total=qty_from_batch * unit_price
                )
                
                # Deduct stock
                batch.current_qty -= qty_from_batch
                if batch.current_qty == 0:
                    batch.status = 'empty'
                batch.save()
                
                # Create stock movement
                StockMovement.objects.create(
                    batch=batch,
                    movement_type='sale',
                    quantity=-qty_from_batch,
                    reference_type='sale',
                    reference_id=sale.id,
                    notes=f"Sale {sale.sale_number}",
                    created_by=user
                )
                
                qty_to_fulfill -= qty_from_batch
                
            if qty_to_fulfill > 0:
                raise ValueError(f"Insufficient stock for {medicine.name}. Short by {qty_to_fulfill}.")

        # Update customer balance if unpaid
        if sale.payment_status != 'paid' and sale.customer:
            unpaid_amount = sale.total - sale.amount_paid
            if unpaid_amount > 0:
                sale.customer.outstanding_balance += unpaid_amount
                sale.customer.save()

        # Log Audit
        AuditLog.objects.create(
            user=user,
            action='create',
            entity_type='Sale',
            entity_id=str(sale.id),
            description=f"Processed sale {sale.sale_number}"
        )
        
        return sale
