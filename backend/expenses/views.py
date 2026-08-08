from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from accounts.permissions import HasPermission
from .models import Expense
from .serializers import ExpenseSerializer

class ExpenseViewSet(viewsets.ModelViewSet):
    queryset = Expense.objects.all().select_related('created_by')
    serializer_class = ExpenseSerializer
    permission_prefix = 'expenses'
    permission_classes = [IsAuthenticated, HasPermission()]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'payment_method', 'date']
    search_fields = ['expense_number', 'description']
    ordering_fields = ['date', 'amount', 'created_at']
