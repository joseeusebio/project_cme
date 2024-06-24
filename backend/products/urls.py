from django.urls import re_path
from .views import ProductCreateView, ProductListView, ProductDetailView, ProductUpdateView, ProductDeleteView, ProductTotalStockView
from .views import ProductBatchStockView, ProductBatchStockCreateView, ProductBatchStockDeleteView, ProductBatchStageCreateView, ProductBatchStageListView
from .views import ProductBatchStageDeleteView, ProductBatchStageUpdateView, ProcessBatchStageCreateView, ProcessBatchStageListView 
from .views import ProcessBatchStageDeleteView, UserDetailView
from django.urls import path

urlpatterns = [
    re_path(r'^products/create/$', ProductCreateView.as_view(), name='product-create'),
    re_path(r'^products/$', ProductListView.as_view(), name='product-list'),
    re_path(r'^products/(?P<sku>[\w-]+)/$', ProductDetailView.as_view(), name='product-detail'),
    re_path(r'^products/(?P<sku>[\w-]+)/update/$', ProductUpdateView.as_view(), name='product-update'),
    re_path(r'^products/(?P<sku>[\w-]+)/delete/$', ProductDeleteView.as_view(), name='product-delete'),
    re_path(r'^total-stock/$', ProductTotalStockView.as_view(), name='total-stock'),
    re_path(r'^batch-stock/$', ProductBatchStockView.as_view(), name='batch-stock'),
    re_path(r'^batch-stocks/create/$', ProductBatchStockCreateView.as_view(), name='batch-stock-create'),
    re_path(r'^batch-stocks/(?P<pk>\d+)/delete/$', ProductBatchStockDeleteView.as_view(), name='batch-stock-delete'),
    re_path(r'^batch-stages/create/$', ProductBatchStageCreateView.as_view(), name='batch-stage-create'),
    re_path(r'^batch-stages/$', ProductBatchStageListView.as_view(), name='batch-stage-list'),
    re_path(r'^batch-stages/(?P<stage_number>\d+)/delete/$', ProductBatchStageDeleteView.as_view(), name='batch-stage-delete'),
    re_path(r'^batch-stages/(?P<stage_number>\d+)/update/$', ProductBatchStageUpdateView.as_view(), name='batch-stage-update'),
    re_path(r'^process-batch-stages/create/$', ProcessBatchStageCreateView.as_view(), name='process-batch-stage-create'),
    re_path(r'^process-batch-stages/$', ProcessBatchStageListView.as_view(), name='process-batch-stage-list'),
    re_path(r'^process-batch-stages/(?P<pk>\d+)/delete/$', ProcessBatchStageDeleteView.as_view(), name='process-batch-stage-delete'),
    path('api/user/', UserDetailView.as_view(), name='user-detail')
]
