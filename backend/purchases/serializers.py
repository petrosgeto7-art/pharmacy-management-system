from rest_framework import serializers
from .models import Purchase, PurchaseItem

class PurchaseItemSerializer(serializers.ModelSerializer):
    medicine_name = serializers.CharField(source='medicine.name', read_only=True)
    batch_display = serializers.CharField(source='batch.batch_number', read_only=True)

    class Meta:
        model = PurchaseItem
        fields = '__all__'
        read_only_fields = ['purchase', 'batch']

class PurchaseSerializer(serializers.ModelSerializer):
    items = PurchaseItemSerializer(many=True)
    supplier_name = serializers.CharField(source='supplier.name', read_only=True)
    created_by_name = serializers.CharField(source='created_by.get_full_name', read_only=True)

    class Meta:
        model = Purchase
        fields = '__all__'
        read_only_fields = ['created_by', 'status']

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        purchase = Purchase.objects.create(**validated_data)
        
        for item_data in items_data:
            PurchaseItem.objects.create(purchase=purchase, **item_data)
            
        return purchase

    def update(self, instance, validated_data):
        if instance.status == 'received':
            raise serializers.ValidationError("Cannot edit a received purchase.")
            
        items_data = validated_data.pop('items', None)
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        if items_data is not None:
            # Simple approach: delete existing items and recreate
            # In a real app, you might want to carefully sync them
            instance.items.all().delete()
            for item_data in items_data:
                PurchaseItem.objects.create(purchase=instance, **item_data)
                
        return instance
