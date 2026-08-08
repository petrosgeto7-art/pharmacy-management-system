from django.db.models import Sum, Count, F
from django.utils import timezone
from datetime import timedelta
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from accounts.permissions import HasPermission
from sales.models import Sale
from purchases.models import Purchase
from inventory.models import Batch
from customers.models import Customer
from medicines.models import Medicine
from prescriptions.models import Prescription
from expenses.models import Expense

class DashboardSummaryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        today = timezone.now().date()
        thirty_days_ago = today - timedelta(days=30)
        
        # Today's Sales & Profit
        today_sales = Sale.objects.filter(date__date=today, status='completed')
        sales_revenue = today_sales.aggregate(total=Sum('total'))['total'] or 0
        
        # For simplified profit, we subtract total cost of items from total revenue
        # Better profit calculation would use SaleItem cost_price
        from sales.models import SaleItem
        today_sale_items = SaleItem.objects.filter(sale__in=today_sales)
        cogs = sum(item.quantity * item.cost_price for item in today_sale_items)
        profit = sales_revenue - cogs
        
        # Today's Purchases
        purchases = Purchase.objects.filter(date=today, status__in=['ordered', 'received'])
        purchases_total = purchases.aggregate(total=Sum('total'))['total'] or 0
        
        # Inventory Value
        inventory = Batch.objects.filter(status='active', current_qty__gt=0)
        inventory_value = sum(batch.current_qty * batch.purchase_price for batch in inventory)
        
        # Counts
        medicines_count = Medicine.objects.filter(status='active').count()
        customers_count = Customer.objects.filter(status='active').count()
        
        # Alerts
        # Low stock (this is an approximation, real logic is per medicine total)
        expiring_medicines_count = Batch.objects.filter(
            status='active', 
            expiry_date__lte=today + timedelta(days=30),
            expiry_date__gte=today,
            current_qty__gt=0
        ).count()
        
        expired_medicines_count = Batch.objects.filter(
            status='active',
            expiry_date__lt=today,
            current_qty__gt=0
        ).count()
        
        pending_prescriptions = Prescription.objects.filter(status='pending').count()
        
        # Charts Data - Last 7 Days Sales
        seven_days_ago = today - timedelta(days=6)
        sales_by_day = []
        for i in range(7):
            day = seven_days_ago + timedelta(days=i)
            day_sales = Sale.objects.filter(date__date=day, status='completed').aggregate(total=Sum('total'))['total'] or 0
            sales_by_day.append({'date': day.strftime('%Y-%m-%d'), 'total': day_sales})

        return Response({
            'today_revenue': sales_revenue,
            'today_profit': profit,
            'today_purchases': purchases_total,
            'inventory_value': inventory_value,
            'medicines_count': medicines_count,
            'customers_count': customers_count,
            'expiring_medicines_count': expiring_medicines_count,
            'expired_medicines_count': expired_medicines_count,
            'pending_prescriptions': pending_prescriptions,
            'sales_chart': sales_by_day,
        })
