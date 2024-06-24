# Generated by Django 5.0.6 on 2024-06-24 12:55

import datetime
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('sku', models.CharField(blank=True, editable=False, max_length=50, unique=True)),
                ('category', models.CharField(max_length=50)),
                ('manufacturer', models.CharField(max_length=255)),
                ('unit', models.CharField(max_length=10)),
            ],
            options={
                'verbose_name': 'Produto',
                'verbose_name_plural': 'Produtos',
            },
        ),
        migrations.CreateModel(
            name='ProductBatchStage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stage_number', models.CharField(blank=True, max_length=100, unique=True)),
                ('stage_status', models.CharField(choices=[('not_started', 'Not Started'), ('in_process', 'In Process'), ('completed', 'Completed')], default='not_started', max_length=20)),
                ('estimated_time_to_complete', models.DurationField(blank=True, null=True)),
                ('completion_date', models.DateField(blank=True, null=True)),
                ('creation_date', models.DateField(default=datetime.date.today)),
                ('washing_status', models.CharField(choices=[('pending', 'Pending'), ('completed', 'Completed'), ('not_needed', 'Not Needed')], default='not_needed', max_length=20)),
                ('sterilization_status', models.CharField(choices=[('pending', 'Pending'), ('completed', 'Completed'), ('not_needed', 'Not Needed')], default='not_needed', max_length=20)),
                ('discard_status', models.CharField(choices=[('pending', 'Pending'), ('completed', 'Completed'), ('not_needed', 'Not Needed')], default='not_needed', max_length=20)),
                ('distribution_status', models.CharField(choices=[('pending', 'Pending'), ('completed', 'Completed'), ('not_needed', 'Not Needed')], default='not_needed', max_length=20)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Estágio do Lote',
                'verbose_name_plural': 'Estágios do Lote',
            },
        ),
        migrations.CreateModel(
            name='ProcessBatchStage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stage', models.CharField(choices=[('lavagem', 'Lavagem'), ('esterilizacao', 'Esterilização'), ('distribuicao', 'Distribuição'), ('descarte', 'Descarte')], max_length=50)),
                ('quantity_processed', models.PositiveIntegerField()),
                ('process_date', models.DateField(auto_now_add=True)),
                ('processed_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('number_batch_stage', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='processes', to='products.productbatchstage', to_field='stage_number')),
            ],
            options={
                'verbose_name': 'Processo de Estágio do Lote',
                'verbose_name_plural': 'Processos de Estágios do Lote',
            },
        ),
        migrations.CreateModel(
            name='ProductBatchStock',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('batch_number', models.CharField(blank=True, max_length=100, unique=True)),
                ('quantity', models.PositiveIntegerField()),
                ('expiration_date', models.DateField(blank=True, null=True)),
                ('entry_date', models.DateField(auto_now_add=True)),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('condition', models.CharField(choices=[('new', 'New'), ('used', 'Used'), ('damaged', 'Damaged')], default='new', max_length=50)),
                ('needs_washing', models.BooleanField(default=True)),
                ('needs_sterilization', models.BooleanField(default=True)),
                ('needs_discard', models.BooleanField(default=False)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='batch_stocks', to='products.product', to_field='sku')),
            ],
            options={
                'verbose_name': 'Recebimento de Material',
                'verbose_name_plural': 'Recebimentos de Material',
            },
        ),
        migrations.CreateModel(
            name='ProductBatchStageHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stage', models.CharField(max_length=50)),
                ('quantity', models.PositiveIntegerField()),
                ('status', models.CharField(max_length=20)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('performed_by', models.CharField(max_length=255)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='stage_history', to='products.product', to_field='sku')),
                ('batch_stock', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='stage_history', to='products.productbatchstock', to_field='batch_number')),
            ],
        ),
        migrations.AddField(
            model_name='productbatchstage',
            name='batch_stock',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='stages', to='products.productbatchstock', to_field='batch_number'),
        ),
        migrations.CreateModel(
            name='ProductTotalStock',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_quantity', models.PositiveIntegerField()),
                ('product', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='total_stock', to='products.product', to_field='sku')),
            ],
            options={
                'verbose_name': 'Saldo Total do Produto',
                'verbose_name_plural': 'Saldo Total do Produto',
            },
        ),
    ]