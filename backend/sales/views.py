from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from accounts.permissions import HasPermission
from .models import Sale
from .serializers import SaleSerializer, SaleCreateSerializer
from .services import SaleService

class SaleViewSet(viewsets.ModelViewSet):
    queryset = Sale.objects.all().select_related('customer', 'processed_by').prefetch_related('items__medicine', 'items__batch')
    serializer_class = SaleSerializer
    permission_prefix = 'sales'
    permission_classes = [IsAuthenticated, HasPermission()]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'payment_status', 'payment_method', 'customer']
    search_fields = ['sale_number', 'customer__name']
    ordering_fields = ['date', 'total']

    def create(self, request, *args, **kwargs):
        """Custom endpoint for processing a POS sale"""
        serializer = SaleCreateSerializer(data=request.data)
        if serializer.is_valid():
            try:
                sale_data = serializer.validated_data
                items_data = sale_data.pop('items')
                
                sale = SaleService.process_sale(sale_data, items_data, request.user)
                
                response_serializer = SaleSerializer(sale)
                return Response(response_serializer.data, status=status.HTTP_201_CREATED)
            except ValueError as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
