from rest_framework import serializers
from .models import Product, ProductTotalStock, ProductBatchStock, ProductBatchStage, ProcessBatchStage, DistributionBalance, ProductRequest

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
    created_by = serializers.StringRelatedField(read_only=True)
    batch_stock = serializers.SlugRelatedField(slug_field='batch_number', queryset=ProductBatchStock.objects.all())

    class Meta:
        model = ProductBatchStage
        fields = [
            'id', 'batch_stock', 'stage_number', 'stage_status',
            'estimated_time_to_complete', 'completion_date', 'created_by',
            'washing_status', 'sterilization_status', 'discard_status', 'distribution_status',
            'creation_date'
        ]
        read_only_fields = ['id', 'stage_number', 'created_by', 'creation_date']

    def create(self, validated_data):
        batch_stock = validated_data.pop('batch_stock')
        validated_data['batch_stock'] = batch_stock
        return super().create(validated_data)

class ProcessBatchStageSerializer(serializers.ModelSerializer):
    user_name = serializers.SerializerMethodField()
    number_batch_stage = serializers.SlugRelatedField(
        slug_field='stage_number',
        queryset=ProductBatchStage.objects.all()
    )

    class Meta:
        model = ProcessBatchStage
        fields = [
            'id', 'number_batch_stage', 'stage', 
            'processed_by', 'process_date', 'user_name'
        ]
        read_only_fields = ['id', 'processed_by', 'process_date']

    def get_user_name(self, obj):
        if obj.processed_by:
            return obj.processed_by.get_full_name() or obj.processed_by.username
        return None

class DistributionBalanceSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    product_sku = serializers.CharField(source='product.sku', read_only=True)

    class Meta:
        model = DistributionBalance
        fields = ['product_name', 'product_sku', 'total_quantity']
        read_only_fields = ['product_name', 'product_sku', 'total_quantity']


class ProductRequestSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    requested_by_name = serializers.CharField(source='requested_by.username', read_only=True)

    class Meta:
        model = ProductRequest
        fields = [
            'id', 'product', 'product_name', 'quantity', 'department',
            'status', 'requested_by', 'requested_by_name', 'request_date'
        ]
        read_only_fields = ['id', 'request_date', 'requested_by']