from django.db import models

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
    condition = models.CharField(
        max_length=50,
        choices=[
            ('new', 'New'),
            ('used', 'Used'),
            ('damaged', 'Damaged'),
        ],
        default='new'
    )
    needs_washing = models.BooleanField(default=True)
    needs_sterilization = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Saldo por Lote'
        verbose_name_plural = 'Saldos por Lote'

    def save(self, *args, **kwargs):
        if not self.batch_number:
            last_batch = ProductBatchStock.objects.order_by('-id').first()
            if last_batch:
                new_batch_number = str(int(last_batch.batch_number) + 1).zfill(6)
            else:
                new_batch_number = '000001'
            self.batch_number = new_batch_number
        super(ProductBatchStock, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.product.name} - Batch: {self.batch_number} - {self.quantity} items"

class ProductBatchStage(models.Model):
    batch_stock = models.ForeignKey(ProductBatchStock, on_delete=models.CASCADE, related_name='stages',to_field='batch_number')
    stage = models.CharField(
        max_length=50,
        choices=[
            ('recebimento', 'Recebimento'),
            ('lavagem', 'Lavagem'),
            ('esterilizacao', 'Esterilização'),
            ('distribuicao', 'Distribuição'),
        ],
        default='recebimento'
    )
    stage_quantity = models.PositiveIntegerField()
    stage_status = models.CharField(
        max_length=20,
        choices=[
            ('in_process', 'In Process'),
            ('completed', 'Completed'),
        ]
    )
    stage_date = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name = 'Fase Por Lote'
        verbose_name_plural = 'Fase Por Lote'

    def __str__(self):
        return f"{self.batch_stock.product.name} - Batch: {self.batch_stock.batch_number} - Stage: {self.stage} - {self.stage_quantity} items ({self.stage_status})"

class ProductBatchStageHistory(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='stage_history', to_field='sku')
    batch_stock = models.ForeignKey('ProductBatchStock', on_delete=models.CASCADE, related_name='stage_history', to_field='batch_number')
    stage = models.CharField(max_length=50)
    quantity = models.PositiveIntegerField()
    status = models.CharField(max_length=20)
    timestamp = models.DateTimeField(auto_now_add=True)
    performed_by = models.CharField(max_length=255)

    class Meta:
        verbose_name = 'Historico do Lote'
        verbose_name_plural = 'Historico do Lote'

    def __str__(self):
        return f"{self.batch_stock.product.name} - Batch: {self.batch_stock.batch_number} - Stage: {self.stage} - {self.quantity} items ({self.status}) at {self.timestamp}"


