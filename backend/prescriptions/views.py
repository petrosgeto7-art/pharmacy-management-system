from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from accounts.permissions import HasPermission
from .models import Prescription
from .serializers import PrescriptionSerializer
from django.utils import timezone

class PrescriptionViewSet(viewsets.ModelViewSet):
    queryset = Prescription.objects.all().select_related('customer', 'dispensed_by').prefetch_related('items__medicine')
    serializer_class = PrescriptionSerializer
    permission_prefix = 'prescriptions'
    permission_classes = [IsAuthenticated, HasPermission()]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'customer']
    search_fields = ['prescription_number', 'customer__name', 'doctor_name']
    ordering_fields = ['prescription_date', 'created_at']

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated, HasPermission('prescriptions.dispense')])
    def dispense(self, request, pk=None):
        """Mark prescription as fully dispensed"""
        prescription = self.get_object()
        
        if prescription.status == 'fully_dispensed':
            return Response({'error': 'Already dispensed'}, status=status.HTTP_400_BAD_REQUEST)
            
        prescription.status = 'fully_dispensed'
        prescription.dispensed_by = request.user
        prescription.dispensed_date = timezone.now()
        
        # In a complete workflow, this might also validate against the related sale
        # For now, we simply update the status and items
        for item in prescription.items.all():
            item.quantity_dispensed = item.quantity_prescribed
            item.save()
            
        prescription.save()
        serializer = self.get_serializer(prescription)
        return Response(serializer.data)
