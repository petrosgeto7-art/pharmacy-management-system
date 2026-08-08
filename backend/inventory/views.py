from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from accounts.permissions import HasPermission
from .models import Batch, StockMovement
from .serializers import BatchSerializer, StockMovementSerializer
from django.utils import timezone
from datetime import timedelta
from django.db.models import Sum

class BatchViewSet(viewsets.ModelViewSet):
    queryset = Batch.objects.all().select_related('medicine', 'supplier')
    serializer_class = BatchSerializer
    permission_prefix = 'batches'
    permission_classes = [IsAuthenticated, HasPermission()]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'medicine', 'supplier']
    search_fields = ['batch_number', 'medicine__name']
    ordering_fields = ['expiry_date', 'current_qty', 'created_at']

    @action(detail=False, methods=['get'])
    def expiring_soon(self, request):
        """Get batches expiring within the next 30 days"""
        thirty_days = timezone.now().date() + timedelta(days=30)
        batches = self.get_queryset().filter(
            status='active',
            expiry_date__lte=thirty_days,
            expiry_date__gte=timezone.now().date()
        ).order_by('expiry_date')
        serializer = self.get_serializer(batches, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def expired(self, request):
        """Get already expired batches"""
        batches = self.get_queryset().filter(
            status='active',
            expiry_date__lt=timezone.now().date()
        ).order_by('-expiry_date')
        serializer = self.get_serializer(batches, many=True)
        return Response(serializer.data)


class StockMovementViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = StockMovement.objects.all().select_related('batch__medicine', 'created_by')
    serializer_class = StockMovementSerializer
    permission_prefix = 'inventory'
    permission_classes = [IsAuthenticated, HasPermission('inventory.view')]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['movement_type', 'batch', 'reference_type', 'reference_id']
    search_fields = ['batch__batch_number', 'batch__medicine__name']
    ordering_fields = ['timestamp', 'quantity']
