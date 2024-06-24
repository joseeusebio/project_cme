from django.db import models
from django.contrib.auth.models import User
from datetime import datetime, date
from django.core.exceptions import ValidationError

class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    sku = models.CharField(max_length=50, unique=True, null=False, blank=True, editable=False)
    category = models.CharField(max_length=50)
    manufacturer = models.CharField(max_length=255)
    unit = models.CharField(max_length=10)

    class Meta:
        verbose_name = 'Produto'
        verbose_name_plural = 'Produtos'

    def save(self, *args, **kwargs):
        if not self.sku:
            last_product = Product.objects.all().order_by('id').last()
            if not last_product:
                self.sku = '000001'
            else:
                last_sku = last_product.sku
                new_sku = int(last_sku) + 1
                self.sku = str(new_sku).zfill(6)
        super(Product, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

class ProductTotalStock(models.Model):
    product = models.OneToOneField('Product', on_delete=models.CASCADE, related_name='total_stock', to_field='sku')
    total_quantity = models.PositiveIntegerField()

    class Meta:
        verbose_name = 'Saldo Total do Produto'
        verbose_name_plural = 'Saldo Total do Produto'

    def __str__(self):
        return f"{self.product.name} - Total: {self.total_quantity} items"

class ProductBatchStock(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='batch_stocks', to_field='sku')
    batch_number = models.CharField(max_length=100, null=False, blank=True, unique=True)
    quantity = models.PositiveIntegerField()
    expiration_date = models.DateField(null=True, blank=True)
    entry_date = models.DateField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    condition = models.CharField(max_length=50,choices=[('new', 'New'),('used', 'Used'),('damaged', 'Damaged'),],default='new')
    needs_washing = models.BooleanField(default=True)
    needs_sterilization = models.BooleanField(default=True)
    needs_discard = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Recebimento de Material'
        verbose_name_plural = 'Recebimentos de Material'

    def save(self, *args, **kwargs):
        if not self.batch_number:
            last_batch = ProductBatchStock.objects.order_by('-id').first()
            if last_batch:
                new_batch_number = str(int(last_batch.batch_number) + 1).zfill(6)
            else:
                new_batch_number = '000001'
            self.batch_number = new_batch_number
        super(ProductBatchStock, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if ProductBatchStage.objects.filter(batch_stock=self).exists():
            raise ValidationError("Não é possível deletar um lote com ordens de tratamento associadas.")
        super(ProductBatchStock, self).delete(*args, **kwargs)

    def __str__(self):
        return f"{self.product.name} - Batch: {self.batch_number} - {self.quantity} items"

class ProductBatchStage(models.Model):
    batch_stock = models.ForeignKey('ProductBatchStock', on_delete=models.CASCADE, related_name='stages', to_field='batch_number')
    stage_number = models.CharField(max_length=100, unique=True, blank=True)
    stage_status = models.CharField(
        max_length=20,
        choices=[
            ('not_started', 'Not Started'),
            ('in_process', 'In Process'),
            ('completed', 'Completed'),
        ],
        default='not_started'
    )
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    estimated_time_to_complete = models.DurationField(null=True, blank=True)
    completion_date = models.DateField(null=True, blank=True)
    creation_date = models.DateField(default=date.today)
    washing_status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('completed', 'Completed'), ('not_needed', 'Not Needed')], default='not_needed')
    sterilization_status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('completed', 'Completed'), ('not_needed', 'Not Needed')], default='not_needed')
    discard_status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('completed', 'Completed'), ('not_needed', 'Not Needed')], default='not_needed')
    distribution_status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('completed', 'Completed'), ('not_needed', 'Not Needed')], default='not_needed')

    class Meta:
        verbose_name = 'Estágio do Lote'
        verbose_name_plural = 'Estágios do Lote'

    def save(self, *args, **kwargs):
        if not self.stage_number:
            last_stage = ProductBatchStage.objects.order_by('-id').first()
            if last_stage:
                new_stage_number = str(int(last_stage.stage_number) + 1).zfill(6)
            else:
                new_stage_number = '000001'
            self.stage_number = new_stage_number

        if self.batch_stock.needs_washing:
            self.washing_status = 'pending'
        else:
            self.washing_status = 'not_needed'

        if self.batch_stock.needs_sterilization:
            self.sterilization_status = 'pending'
        else:
            self.sterilization_status = 'not_needed'

        if self.batch_stock.needs_discard:
            self.discard_status = 'pending'
        else:
            self.discard_status = 'not_needed'

        if not self.batch_stock.needs_washing and not self.batch_stock.needs_sterilization and not self.batch_stock.needs_discard:
            self.distribution_status = 'pending'
        else:
            self.distribution_status = 'not_needed'

        if self.stage_status == 'completed' and not self.completion_date:
            self.completion_date = date.today()

        super(ProductBatchStage, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.stage_number} - {self.get_stage_status_display()}"

class ProductBatchStageHistory(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='stage_history', to_field='sku')
    batch_stock = models.ForeignKey('ProductBatchStock', on_delete=models.CASCADE, related_name='stage_history', to_field='batch_number')
    stage = models.CharField(max_length=50)
    quantity = models.PositiveIntegerField()
    status = models.CharField(max_length=20)
    timestamp = models.DateTimeField(auto_now_add=True)
    performed_by = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.batch_stock.product.name} - Batch: {self.batch_stock.batch_number} - Stage: {self.stage} - {self.quantity} items ({self.status}) at {self.timestamp}"


class ProcessBatchStage(models.Model):
    number_batch_stage = models.ForeignKey(ProductBatchStage, on_delete=models.CASCADE, related_name='processes', to_field='stage_number')
    stage = models.CharField(max_length=50)
    processed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    process_date = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name = 'Processo de Estágio do Lote'
        verbose_name_plural = 'Processos de Estágios do Lote'

    def __str__(self):
        return f"{self.number_batch_stage.stage_number} - {self.stage}"
    
class DistributionBalance(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='distribution_balances', to_field='sku')
    total_quantity = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = 'Saldo de Distribuição'
        verbose_name_plural = 'Saldos de Distribuição'

    def __str__(self):
        return f"{self.product.name} - Total a distribuir: {self.total_quantity}"
    

class ProductRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
    ]

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_requests')
    quantity = models.PositiveIntegerField()
    department = models.CharField(max_length=255)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    requested_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    request_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.product.name} - {self.department} - {self.quantity} - {self.status}"

    class Meta:
        verbose_name = 'Product Request'
        verbose_name_plural = 'Product Requests'