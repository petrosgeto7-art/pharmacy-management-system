from rest_framework import serializers
from .models import Return, ReturnItem

class ReturnItemSerializer(serializers.ModelSerializer):
    medicine_name = serializers.CharField(source='sale_item.medicine.name', read_only=True)
    batch_number = serializers.CharField(source='batch.batch_number', read_only=True)

    class Meta:
        model = ReturnItem
        fields = '__all__'
        read_only_fields = ['return_record']

class ReturnSerializer(serializers.ModelSerializer):
    items = ReturnItemSerializer(many=True)
    customer_name = serializers.CharField(source='customer.name', read_only=True)
    sale_number = serializers.CharField(source='sale.sale_number', read_only=True)
    processed_by_name = serializers.CharField(source='processed_by.get_full_name', read_only=True)

    class Meta:
        model = Return
        fields = '__all__'
        read_only_fields = ['processed_by', 'status']

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        return_record = Return.objects.create(**validated_data)
        
        for item_data in items_data:
            ReturnItem.objects.create(return_record=return_record, **item_data)
            
        return return_record
