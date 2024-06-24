from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from products.models import Product, ProductTotalStock, ProductBatchStock, ProductBatchStage, ProcessBatchStage
from products.serializers import ProductSerializer, ProductTotalStockSerializer, ProductBatchStockSerializer, ProductBatchStageSerializer, ProcessBatchStageSerializer
from django.shortcuts import get_object_or_404

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

    def delete(self, request, sku, *args, **kwargs):
        try:
            product = Product.objects.get(sku=sku)
            if ProductTotalStock.objects.filter(product=product).exists():
                return Response({"error": "Não é possível deletar produtos com saldo."}, status=status.HTTP_400_BAD_REQUEST)
            product.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Product.DoesNotExist:
            return Response({"error": "Produto não encontrado."}, status=status.HTTP_404_NOT_FOUND)

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
    
class ProductBatchStockCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = ProductBatchStockSerializer(data=request.data)
        if serializer.is_valid():
            batch_stock = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProductBatchStockDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk, *args, **kwargs):
        try:
            batch_stock = ProductBatchStock.objects.get(pk=pk)
            batch_stock.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ProductBatchStock.DoesNotExist:
            return Response({"error": "Lote não encontrado."}, status=status.HTTP_404_NOT_FOUND)
        
class ProductBatchStageCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = ProductBatchStageSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProductBatchStageListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        stages = ProductBatchStage.objects.all()
        serializer = ProductBatchStageSerializer(stages, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class ProductBatchStageDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, stage_number, *args, **kwargs):
        stage = get_object_or_404(ProductBatchStage, stage_number=stage_number)
        stage.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class ProductBatchStageUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, stage_number, *args, **kwargs):
        stage = get_object_or_404(ProductBatchStage, stage_number=stage_number)
        serializer = ProductBatchStageSerializer(stage, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class ProcessBatchStageCreateView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = ProcessBatchStageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(processed_by=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProcessBatchStageListView(APIView):
    def get(self, request, *args, **kwargs):
        processes = ProcessBatchStage.objects.all()
        serializer = ProcessBatchStageSerializer(processes, many=True)
        return Response(serializer.data)

class ProcessBatchStageDeleteView(APIView):
    def delete(self, request, pk, *args, **kwargs):
        process = get_object_or_404(ProcessBatchStage, pk=pk)
        process.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

class UserDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        data = {
            'name': user.get_full_name() or user.username,
            'email': user.email,
        }
        return Response(data)