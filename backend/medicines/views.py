from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from accounts.permissions import HasPermission
from .models import Category, Manufacturer, Medicine
from .serializers import (
    CategorySerializer, ManufacturerSerializer, 
    MedicineListSerializer, MedicineDetailSerializer
)

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_prefix = 'categories'
    permission_classes = [IsAuthenticated, HasPermission()]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'created_at']

class ManufacturerViewSet(viewsets.ModelViewSet):
    queryset = Manufacturer.objects.all()
    serializer_class = ManufacturerSerializer
    # Reusing medicines permission prefix for manufacturers for simplicity
    permission_prefix = 'medicines' 
    permission_classes = [IsAuthenticated, HasPermission()]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'country']
    ordering_fields = ['name']

class MedicineViewSet(viewsets.ModelViewSet):
    queryset = Medicine.objects.all().select_related('category', 'manufacturer')
    permission_prefix = 'medicines'
    permission_classes = [IsAuthenticated, HasPermission()]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'manufacturer', 'status', 'requires_prescription', 'dosage_form']
    search_fields = ['name', 'generic_name', 'brand_name', 'barcode', 'sku']
    ordering_fields = ['name', 'selling_price', 'created_at']

    def get_serializer_class(self):
        if self.action == 'list':
            return MedicineListSerializer
        return MedicineDetailSerializer
