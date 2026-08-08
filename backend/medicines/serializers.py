from rest_framework import serializers
from .models import Category, Manufacturer, Medicine

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class ManufacturerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Manufacturer
        fields = '__all__'

class MedicineListSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    manufacturer_name = serializers.CharField(source='manufacturer.name', read_only=True)
    total_stock = serializers.IntegerField(read_only=True)
    is_low_stock = serializers.BooleanField(read_only=True)
    is_out_of_stock = serializers.BooleanField(read_only=True)

    class Meta:
        model = Medicine
        fields = ['id', 'name', 'generic_name', 'sku', 'barcode', 'category', 'category_name',
                  'manufacturer', 'manufacturer_name', 'dosage_form', 'strength', 'unit',
                  'selling_price', 'status', 'total_stock', 'is_low_stock', 'is_out_of_stock']

class MedicineDetailSerializer(serializers.ModelSerializer):
    category_details = CategorySerializer(source='category', read_only=True)
    manufacturer_details = ManufacturerSerializer(source='manufacturer', read_only=True)
    total_stock = serializers.IntegerField(read_only=True)
    is_low_stock = serializers.BooleanField(read_only=True)
    is_out_of_stock = serializers.BooleanField(read_only=True)

    class Meta:
        model = Medicine
        fields = '__all__'
