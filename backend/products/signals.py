from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import ProductBatchStock, ProductTotalStock
from django.db import models

@receiver(post_save, sender=ProductBatchStock)
def update_total_stock(sender, instance, **kwargs):
    total_stock, created = ProductTotalStock.objects.get_or_create(product=instance.product)
    total_stock.total_quantity = ProductBatchStock.objects.filter(product=instance.product).aggregate(total=models.Sum('quantity'))['total']
    total_stock.save()