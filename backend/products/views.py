from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from products.models import Product, ProductTotalStock, ProductBatchStock
from products.serializers import ProductSerializer, ProductTotalStockSerializer, ProductBatchStockSerializer
from django.db.models import F
class ProductCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        data = request.data.copy()
        serializer = ProductSerializer(data=data)
        if serializer.is_valid():
            serializer.save() 
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProductListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

class ProductDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, sku, format=None):
        try:
            product = Product.objects.get(sku=sku)
            serializer = ProductSerializer(product)
            return Response(serializer.data)
        except Product.DoesNotExist:
            return Response({"error": "Produto não encontrado."}, status=status.HTTP_404_NOT_FOUND)

class ProductUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, sku, format=None):
        try:
            product = Product.objects.get(sku=sku)
        except Product.DoesNotExist:
            return Response({"error": "Produto não encontrado."}, status=status.HTTP_404_NOT_FOUND)

        data = request.data.copy()
        serializer = ProductSerializer(product, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProductDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, sku, format=None):
        try:
            product = Product.objects.get(sku=sku)
            if ProductTotalStock.objects.filter(product=product, total_quantity__gt=0).exists():
                return Response({"error": "Não é possível deletar produtos com saldo."}, status=status.HTTP_400_BAD_REQUEST)
            product.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Product.DoesNotExist:
            return Response({"error": "Produto não encontrado."}, status=status.HTTP_404_NOT_FOUND)
        except ProductTotalStock.DoesNotExist:
            product.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)


class ProductTotalStockView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        total_stocks = ProductTotalStock.objects.all()
        serializer = ProductTotalStockSerializer(total_stocks, many=True)
        return Response(serializer.data)
    

class ProductBatchStockView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        batch_stocks = ProductBatchStock.objects.all()
        serializer = ProductBatchStockSerializer(batch_stocks, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = ProductBatchStockSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class ProductBatchStockCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = ProductBatchStockSerializer(data=request.data)
        if serializer.is_valid():
            batch_stock = serializer.save()
            try:
                total_stock = ProductTotalStock.objects.get(product=batch_stock.product)
                total_stock.total_quantity = F('total_quantity') + batch_stock.quantity
                total_stock.save()
            except ProductTotalStock.DoesNotExist:
                ProductTotalStock.objects.create(product=batch_stock.product, total_quantity=batch_stock.quantity)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

