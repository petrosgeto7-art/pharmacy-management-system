from rest_framework import serializers
from .models import Sale, SaleItem
from medicines.models import Medicine
from customers.models import Customer
from prescriptions.models import Prescription
import uuid

class SaleItemSerializer(serializers.ModelSerializer):
    medicine_name = serializers.CharField(source='medicine.name', read_only=True)
    batch_display = serializers.CharField(source='batch.batch_number', read_only=True)

    class Meta:
        model = SaleItem
        fields = '__all__'
        read_only_fields = ['sale', 'batch', 'cost_price']

class SaleSerializer(serializers.ModelSerializer):
    items = SaleItemSerializer(many=True, read_only=True)
    customer_name = serializers.CharField(source='customer.name', read_only=True)
    processed_by_name = serializers.CharField(source='processed_by.get_full_name', read_only=True)

    class Meta:
        model = Sale
        fields = '__all__'
        read_only_fields = ['processed_by', 'status']

class SaleCreateItemSerializer(serializers.Serializer):
    medicine = serializers.PrimaryKeyRelatedField(queryset=Medicine.objects.all())
    quantity = serializers.IntegerField(min_value=1)
    unit_price = serializers.DecimalField(max_digits=10, decimal_places=2)

class SaleCreateSerializer(serializers.Serializer):
    sale_number = serializers.CharField(required=False, allow_blank=True)
    customer = serializers.PrimaryKeyRelatedField(queryset=Customer.objects.all(), required=False, allow_null=True)
    prescription = serializers.PrimaryKeyRelatedField(queryset=Prescription.objects.all(), required=False, allow_null=True)
    
    subtotal = serializers.DecimalField(max_digits=12, decimal_places=2)
    tax = serializers.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    discount = serializers.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    total = serializers.DecimalField(max_digits=12, decimal_places=2)
    
    payment_method = serializers.ChoiceField(choices=Sale.PAYMENT_METHOD_CHOICES, default='cash')
    payment_status = serializers.ChoiceField(choices=Sale.PAYMENT_STATUS_CHOICES, default='paid')
    amount_paid = serializers.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    change_due = serializers.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    
    notes = serializers.CharField(required=False, allow_blank=True)
    items = SaleCreateItemSerializer(many=True, min_length=1)

    def validate(self, attrs):
        if not attrs.get('sale_number'):
            import time
            attrs['sale_number'] = f"SL-{int(time.time())}"
            
        # Ensure total is correct
        calc_total = attrs['subtotal'] + attrs['tax'] - attrs['discount']
        if abs(calc_total - attrs['total']) > 0.05:
            raise serializers.ValidationError("Total does not match subtotal + tax - discount")
            
        return attrs
