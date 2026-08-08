from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from accounts.permissions import HasPermission
from .models import Purchase
from .serializers import PurchaseSerializer
from .services import PurchaseService

class PurchaseViewSet(viewsets.ModelViewSet):
    queryset = Purchase.objects.all().select_related('supplier', 'created_by').prefetch_related('items__medicine')
    serializer_class = PurchaseSerializer
    permission_prefix = 'purchases'
    permission_classes = [IsAuthenticated, HasPermission()]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'payment_status', 'supplier']
    search_fields = ['purchase_number', 'supplier__name']
    ordering_fields = ['date', 'total', 'created_at']

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated, HasPermission('purchases.edit')])
    def complete(self, request, pk=None):
        """Endpoint to mark purchase as received and update inventory"""
        try:
            purchase = PurchaseService.complete_purchase(pk, request.user)
            serializer = self.get_serializer(purchase)
            return Response(serializer.data)
        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': 'An unexpected error occurred.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
