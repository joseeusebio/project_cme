from rest_framework import serializers
from .models import Product, ProductTotalStock, ProductBatchStock, ProductBatchStage, ProcessBatchStage

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'sku', 'category', 'manufacturer', 'unit']
        read_only_fields = ['id', 'sku']

    def create(self, validated_data):
        product = Product.objects.create(**validated_data)
        return product

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.category = validated_data.get('category', instance.category)
        instance.manufacturer = validated_data.get('manufacturer', instance.manufacturer)
        instance.unit = validated_data.get('unit', instance.unit)
        instance.save()
        return instance


class ProductTotalStockSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_name = serializers.CharField(source='product.name', read_only=True)
    product_sku = serializers.CharField(source='product.sku', read_only=True)

    class Meta:
        model = ProductTotalStock
        fields = ['product','product_name', 'product_sku', 'total_quantity']



class ProductBatchStockSerializer(serializers.ModelSerializer):
    product_sku = serializers.CharField(source='product.sku', read_only=True)
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(), write_only=True)

    class Meta:
        model = ProductBatchStock
        fields = [
            'id', 'product', 'product_sku', 'batch_number', 'quantity', 
            'expiration_date', 'entry_date', 'last_updated', 'condition', 
            'needs_washing', 'needs_sterilization', 'needs_discard'
        ]
        read_only_fields = ['id', 'batch_number', 'entry_date', 'last_updated']

    def create(self, validated_data):
        product = validated_data.pop('product')
        batch_stock = ProductBatchStock.objects.create(product=product, **validated_data)
        return batch_stock

    def update(self, instance, validated_data):
        if 'product' in validated_data:
            instance.product = validated_data.pop('product')
        instance.quantity = validated_data.get('quantity', instance.quantity)
        instance.expiration_date = validated_data.get('expiration_date', instance.expiration_date)
        instance.condition = validated_data.get('condition', instance.condition)
        instance.needs_washing = validated_data.get('needs_washing', instance.needs_washing)
        instance.needs_sterilization = validated_data.get('needs_sterilization', instance.needs_sterilization)
        instance.needs_discard = validated_data.get('needs_discard', instance.needs_discard)
        instance.save()
        return instance


class ProductBatchStageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductBatchStage
        fields = [
            'id', 'batch_stock', 'stage_number', 'stage_status',
            'estimated_time_to_complete', 'completion_date', 'created_by',
            'washing_status', 'sterilization_status', 'discard_status', 'distribution_status',
            'creation_date'
        ]
        read_only_fields = ['id', 'stage_number', 'created_by', 'creation_date', 'completion_date']

class ProcessBatchStageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProcessBatchStage
        fields = [
            'id', 'number_batch_stage', 'stage', 'quantity_processed', 
            'processed_by', 'process_date'
        ]
        read_only_fields = ['id', 'processed_by', 'process_date']





