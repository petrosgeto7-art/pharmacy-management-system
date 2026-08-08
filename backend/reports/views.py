from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from accounts.permissions import HasPermission
from sales.models import Sale, SaleItem
from purchases.models import Purchase
from expenses.models import Expense
from django.db.models import Sum, Q
import csv
from django.http import HttpResponse

class SalesReportView(APIView):
    permission_classes = [IsAuthenticated, HasPermission('reports.sales')]

    def get(self, request):
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        
        sales = Sale.objects.filter(status='completed')
        if start_date:
            sales = sales.filter(date__date__gte=start_date)
        if end_date:
            sales = sales.filter(date__date__lte=end_date)
            
        total_revenue = sales.aggregate(total=Sum('total'))['total'] or 0
        total_tax = sales.aggregate(total=Sum('tax'))['total'] or 0
        total_discount = sales.aggregate(total=Sum('discount'))['total'] or 0
        
        # Group by payment method
        payment_methods = list(sales.values('payment_method').annotate(total=Sum('total')))
        
        return Response({
            'total_revenue': total_revenue,
            'total_tax': total_tax,
            'total_discount': total_discount,
            'sales_count': sales.count(),
            'by_payment_method': payment_methods,
        })


class FinancialReportView(APIView):
    permission_classes = [IsAuthenticated, HasPermission('reports.financial')]

    def get(self, request):
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        
        sales = Sale.objects.filter(status='completed')
        expenses = Expense.objects.all()
        purchases = Purchase.objects.filter(status__in=['ordered', 'received'])
        
        if start_date:
            sales = sales.filter(date__date__gte=start_date)
            expenses = expenses.filter(date__gte=start_date)
            purchases = purchases.filter(date__gte=start_date)
        if end_date:
            sales = sales.filter(date__date__lte=end_date)
            expenses = expenses.filter(date__lte=end_date)
            purchases = purchases.filter(date__lte=end_date)
            
        revenue = sales.aggregate(total=Sum('total'))['total'] or 0
        
        sale_items = SaleItem.objects.filter(sale__in=sales)
        cogs = sum(item.quantity * item.cost_price for item in sale_items)
        
        gross_profit = revenue - cogs
        
        total_expenses = expenses.aggregate(total=Sum('amount'))['total'] or 0
        
        net_profit = gross_profit - total_expenses
        
        return Response({
            'revenue': revenue,
            'cogs': cogs,
            'gross_profit': gross_profit,
            'expenses': total_expenses,
            'net_profit': net_profit,
        })
