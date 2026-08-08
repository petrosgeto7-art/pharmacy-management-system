from rest_framework import serializers
from .models import Batch, StockMovement

class BatchSerializer(serializers.ModelSerializer):
    medicine_name = serializers.CharField(source='medicine.name', read_only=True)
    supplier_name = serializers.CharField(source='supplier.name', read_only=True)
    available_qty = serializers.IntegerField(read_only=True)

    class Meta:
        model = Batch
        fields = '__all__'

class StockMovementSerializer(serializers.ModelSerializer):
    batch_number = serializers.CharField(source='batch.batch_number', read_only=True)
    medicine_name = serializers.CharField(source='batch.medicine.name', read_only=True)
    created_by_name = serializers.CharField(source='created_by.get_full_name', read_only=True)

    class Meta:
        model = StockMovement
        fields = '__all__'
