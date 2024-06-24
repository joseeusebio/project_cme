from django.contrib import admin
from .models import Product, ProductTotalStock, ProductBatchStock, ProductBatchStage, ProductBatchStageHistory, ProcessBatchStage

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
    list_display = ['stage_number', 'batch_stock', 'stage_status', 'washing_status', 'sterilization_status', 'discard_status', 'distribution_status', 'creation_date', 'completion_date']
    list_filter = ['stage_status', 'washing_status', 'sterilization_status', 'discard_status', 'distribution_status', 'creation_date', 'completion_date']
    search_fields = ['stage_number', 'batch_stock__batch_number']
    readonly_fields = ['creation_date', 'created_by']

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)

@admin.register(ProcessBatchStage)
class ProcessBatchStageAdmin(admin.ModelAdmin):
    list_display = ('number_batch_stage', 'stage', 'processed_by', 'process_date')
    search_fields = ('number_batch_stage__stage_number', 'stage', 'processed_by__username')