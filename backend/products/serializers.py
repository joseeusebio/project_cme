from rest_framework import serializers
from .models import Product, ProductTotalStock, ProductBatchStock

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

    class Meta:
        model = ProductTotalStock
        fields = ['product', 'total_quantity']


class ProductBatchStockSerializer(serializers.ModelSerializer):
    product = serializers.CharField(source='product.sku')

    class Meta:
        model = ProductBatchStock
        fields = ['id', 'product', 'batch_number', 'quantity', 'expiration_date', 'entry_date', 'last_updated', 'condition', 'needs_washing', 'needs_sterilization']
        read_only_fields = ['id', 'batch_number', 'entry_date', 'last_updated']

    def create(self, validated_data):
        product_sku = validated_data.pop('product')['sku']
        try:
            product = Product.objects.get(sku=product_sku)
        except Product.DoesNotExist:
            raise serializers.ValidationError(f"Produto com SKU {product_sku} não encontrado")

        batch_stock = ProductBatchStock.objects.create(
            product=product,
            **validated_data
        )

        return batch_stock

    def update(self, instance, validated_data):
        instance.quantity = validated_data.get('quantity', instance.quantity)
        instance.expiration_date = validated_data.get('expiration_date', instance.expiration_date)
        instance.condition = validated_data.get('condition', instance.condition)
        instance.needs_washing = validated_data.get('needs_washing', instance.needs_washing)
        instance.needs_sterilization = validated_data.get('needs_sterilization', instance.needs_sterilization)
        instance.save()
        return instance




