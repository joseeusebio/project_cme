from django.contrib import admin
from .models import Product, ProductTotalStock, ProductBatchStock, ProductBatchStage, ProductBatchStageHistory

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'sku', 'category', 'manufacturer', 'unit')
    list_filter = ('category', 'manufacturer', 'unit')
    search_fields = ('name', 'sku', 'manufacturer')
    ordering = ('name',)
    readonly_fields = ('sku',)
    fields = ('name', 'description', 'category', 'manufacturer', 'unit')

@admin.register(ProductTotalStock)
class ProductTotalStockAdmin(admin.ModelAdmin):
    list_display = ('product', 'total_quantity')
    search_fields = ('product__name', 'product__sku')
    ordering = ('product',)

@admin.register(ProductBatchStock)
class ProductBatchStockAdmin(admin.ModelAdmin):
    list_display = ('product', 'batch_number', 'quantity', 'expiration_date', 'entry_date', 'last_updated', 'condition', 'needs_washing', 'needs_sterilization')
    list_filter = ('condition', 'needs_washing', 'needs_sterilization', 'entry_date', 'expiration_date')
    search_fields = ('product__name', 'product__sku', 'batch_number')
    ordering = ('product', 'batch_number')
    readonly_fields = ('entry_date', 'last_updated')

@admin.register(ProductBatchStage)
class ProductBatchStageAdmin(admin.ModelAdmin):
    list_display = ('batch_stock', 'stage', 'stage_quantity', 'stage_status', 'stage_date')
    list_filter = ('stage', 'stage_status', 'stage_date')
    search_fields = ('batch_stock__product__name', 'batch_stock__product__sku', 'batch_stock__batch_number', 'stage')
    ordering = ('batch_stock', 'stage_date')
    readonly_fields = ('stage_date',)

@admin.register(ProductBatchStageHistory)
class ProductBatchStageHistoryAdmin(admin.ModelAdmin):
    list_display = ('product', 'batch_stock', 'stage', 'quantity', 'status', 'timestamp', 'performed_by')
    list_filter = ('stage', 'status', 'timestamp', 'performed_by')
    search_fields = ('product__sku', 'batch_stock__batch_number', 'stage', 'status', 'performed_by')
    date_hierarchy = 'timestamp'
    ordering = ('-timestamp',)
    readonly_fields = ('timestamp',)

    def product(self, obj):
        return obj.product.sku

    def batch_stock(self, obj):
        return obj.batch_stock.batch_number

    product.short_description = 'Product SKU'
    batch_stock.short_description = 'Batch Number'
