from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from products.models import Product, ProductTotalStock, ProductBatchStock, ProductBatchStage, ProcessBatchStage, DistributionBalance, ProductRequest
from products.serializers import ProductSerializer, ProductTotalStockSerializer, ProductBatchStockSerializer, ProductBatchStageSerializer
from products.serializers import ProcessBatchStageSerializer, DistributionBalanceSerializer, ProductRequestSerializer
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import ValidationError

#Views Product
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
        product = get_object_or_404(Product, sku=sku)
        serializer = ProductSerializer(product)
        return Response(serializer.data)

class ProductUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, sku, format=None):
        product = get_object_or_404(Product, sku=sku)
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
        product = get_object_or_404(Product, sku=sku)
        if ProductTotalStock.objects.filter(product=product).exists():
            return Response({"error": "Não é possível deletar produtos com saldo."}, status=status.HTTP_400_BAD_REQUEST)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

#Views ProductTotalStock
class ProductTotalStockView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        total_stocks = ProductTotalStock.objects.all()
        serializer = ProductTotalStockSerializer(total_stocks, many=True)
        return Response(serializer.data)

#Views ProductBatchStock
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
        batch_stock = get_object_or_404(ProductBatchStock, pk=pk)
        
        if ProductBatchStage.objects.filter(batch_stock=batch_stock).exists():
            return Response({"detail": "Não é possível deletar um lote com ordens de tratamento associadas."}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            batch_stock.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ValidationError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

#Views ProductBatchStage
class ProductBatchStageCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = ProductBatchStageSerializer(data=request.data)
        if serializer.is_valid():
            batch_stock = serializer.validated_data['batch_stock']
            if ProductBatchStage.objects.filter(batch_stock=batch_stock).exists():
                return Response({"detail": "Já existe uma ordem de tratamento associada a este lote."}, status=status.HTTP_400_BAD_REQUEST)
            serializer.save(created_by=request.user)
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
        if stage.processes.exists():
            raise ValidationError("Não é possível deletar uma ordem de tratamento com processos vinculados.")
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

#Views ProcessBatchStage
class ProcessBatchStageCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = ProcessBatchStageSerializer(data=request.data)
        if serializer.is_valid():
            product_batch_stage = get_object_or_404(ProductBatchStage, stage_number=request.data['number_batch_stage'])
            if product_batch_stage.stage_status == 'completed':
                raise ValidationError("Não é possível adicionar processos a uma ordem de tratamento concluída.")
            process_batch_stage = serializer.save(processed_by=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class ProcessBatchStageListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        processes = ProcessBatchStage.objects.all()
        serializer = ProcessBatchStageSerializer(processes, many=True)
        return Response(serializer.data)
    
class ProcessBatchStageByOrderView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, order_id, *args, **kwargs):
        processes = ProcessBatchStage.objects.filter(number_batch_stage__id=order_id)
        serializer = ProcessBatchStageSerializer(processes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class ProcessBatchStageDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk, *args, **kwargs):
        process = get_object_or_404(ProcessBatchStage, pk=pk)
        product_batch_stage = process.number_batch_stage

        if product_batch_stage.stage_status == 'completed':
            return Response({"detail": "Não é possível excluir processos de uma ordem de tratamento concluída."}, status=status.HTTP_400_BAD_REQUEST)

        process.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


#Views User
class UserDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        data = {
            'name': user.get_full_name() or user.username,
            'email': user.email,
            'id': user.id
        }
        return Response(data)

#Views Distribuition Balance
class DistributionBalanceListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        distribution_balances = DistributionBalance.objects.all()
        serializer = DistributionBalanceSerializer(distribution_balances, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
#Views ProductRequest

class ProductRequestListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        requests = ProductRequest.objects.all()
        serializer = ProductRequestSerializer(requests, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class ProductRequestCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        data = request.data.copy()
        data['requested_by'] = request.user.id
        serializer = ProductRequestSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProductRequestUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, pk, *args, **kwargs):
        product_request = get_object_or_404(ProductRequest, pk=pk)
        serializer = ProductRequestSerializer(product_request, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class ProductRequestDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk, *args, **kwargs):
        product_request = get_object_or_404(ProductRequest, pk=pk)
        product_request.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class ProductRequestDistributeView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, pk, *args, **kwargs):
        product_request = get_object_or_404(ProductRequest, pk=pk)
        if product_request.status == 'completed':
            return Response({"detail": "Requisição já está finalizada."}, status=status.HTTP_400_BAD_REQUEST)
        
        distribution_balance = DistributionBalance.objects.get(product=product_request.product)
        if distribution_balance.total_quantity < product_request.quantity:
            return Response({"detail": "Saldo insuficiente para atender a requisição."}, status=status.HTTP_400_BAD_REQUEST)
        
        distribution_balance.total_quantity -= product_request.quantity
        distribution_balance.save()
        
        product_request.status = 'completed'
        product_request.save()
        
        return Response(status=status.HTTP_200_OK)