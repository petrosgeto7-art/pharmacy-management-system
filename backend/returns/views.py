from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from accounts.permissions import HasPermission
from .models import Return
from .serializers import ReturnSerializer
from .services import ReturnService

class ReturnViewSet(viewsets.ModelViewSet):
    queryset = Return.objects.all().select_related('sale', 'customer', 'processed_by').prefetch_related('items__sale_item__medicine')
    serializer_class = ReturnSerializer
    permission_prefix = 'returns'
    permission_classes = [IsAuthenticated, HasPermission()]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'customer', 'sale']
    search_fields = ['return_number', 'customer__name', 'sale__sale_number']
    ordering_fields = ['date', 'total_refund', 'created_at']

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated, HasPermission('returns.approve')])
    def process(self, request, pk=None):
        """Endpoint to mark return as completed and update inventory/finance"""
        try:
            return_record = ReturnService.process_return(pk, request.user)
            serializer = self.get_serializer(return_record)
            return Response(serializer.data)
        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': 'An unexpected error occurred.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
