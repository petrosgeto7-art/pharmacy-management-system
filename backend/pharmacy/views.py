from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from accounts.permissions import HasPermission
from .models import Pharmacy
from .serializers import PharmacySerializer

class PharmacyViewSet(viewsets.ModelViewSet):
    queryset = Pharmacy.objects.all()
    serializer_class = PharmacySerializer
    permission_prefix = 'settings'
    permission_classes = [IsAuthenticated, HasPermission()]
