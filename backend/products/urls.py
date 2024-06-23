from django.urls import re_path
from .views import ProductCreateView, ProductListView, ProductDetailView, ProductUpdateView, ProductDeleteView, ProductTotalStockView, ProductBatchStockView
from .views import ProductBatchStockCreateView

urlpatterns = [
    re_path(r'^products/create/$', ProductCreateView.as_view(), name='product-create'),
    re_path(r'^products/$', ProductListView.as_view(), name='product-list'),
    re_path(r'^products/(?P<sku>[\w-]+)/$', ProductDetailView.as_view(), name='product-detail'),
    re_path(r'^products/(?P<sku>[\w-]+)/update/$', ProductUpdateView.as_view(), name='product-update'),
    re_path(r'^products/(?P<sku>[\w-]+)/delete/$', ProductDeleteView.as_view(), name='product-delete'),
    re_path(r'^total-stock/$', ProductTotalStockView.as_view(), name='total-stock'),
    re_path(r'^batch-stock/$', ProductBatchStockView.as_view(), name='batch-stock'),
    re_path(r'^batch-stocks/create/$', ProductBatchStockCreateView.as_view(), name='batch-stock-create'),
]
