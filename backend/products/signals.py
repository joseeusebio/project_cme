from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import ProductBatchStock, ProductTotalStock, ProductBatchStage
from django.db import models
from django.db.models import F
from django.db import transaction
from datetime import datetime, date

@receiver(post_save, sender=ProductBatchStock)
def update_total_stock(sender, instance, **kwargs):
    total_quantity = ProductBatchStock.objects.filter(product=instance.product).aggregate(total=models.Sum('quantity'))['total']
    if total_quantity is None:
        total_quantity = 0

    total_stock, created = ProductTotalStock.objects.get_or_create(product=instance.product, defaults={'total_quantity': total_quantity})
    if not created:
        total_stock.total_quantity = total_quantity
        total_stock.save()

@receiver(post_delete, sender=ProductBatchStock)
@transaction.atomic
def update_total_stock_on_delete(sender, instance, **kwargs):
    product = instance.product
    quantity = instance.quantity

    try:
        total_stock = ProductTotalStock.objects.select_for_update().get(product=product)
        total_stock.total_quantity = F('total_quantity') - quantity
        total_stock.save()
        total_stock.refresh_from_db()
        if total_stock.total_quantity < 0:
            total_stock.total_quantity = 0
            total_stock.save()
    except ProductTotalStock.DoesNotExist:
        pass

@receiver(post_save, sender=ProductBatchStage)
def update_stage_status(sender, instance, created, **kwargs):
    if not created:
        all_stages_completed = (
            (instance.washing_status == 'completed' or instance.washing_status == 'not_needed') and
            (instance.sterilization_status == 'completed' or instance.sterilization_status == 'not_needed') and
            (instance.discard_status == 'completed' or instance.discard_status == 'not_needed') and
            (instance.distribution_status == 'completed' or instance.distribution_status == 'not_needed')
        )

        if all_stages_completed:
            instance.stage_status = 'completed'
            if not instance.completion_date:
                instance.completion_date = date.today()
        elif (
            instance.washing_status == 'pending' or
            instance.sterilization_status == 'pending' or
            instance.discard_status == 'pending' or
            instance.distribution_status == 'pending'
        ):
            instance.stage_status = 'in_process'
        else:
            instance.stage_status = 'not_started'

        ProductBatchStage.objects.filter(pk=instance.pk).update(stage_status=instance.stage_status, completion_date=instance.completion_date)
