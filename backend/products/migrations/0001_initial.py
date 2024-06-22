# Generated by Django 5.0.6 on 2024-06-21 23:01

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('sku', models.CharField(max_length=50, unique=True)),
                ('category', models.CharField(choices=[('surgical', 'Surgical - Instrumentos Cirúrgicos'), ('imaging', 'Imaging - Equipamentos de Visualização'), ('anesthesia', 'Anesthesia - Dispositivos de Anestesia'), ('catheterization', 'Catheterization - Material de Cateterização e Drenagem'), ('dental', 'Dental - Instrumental Odontológico'), ('containers', 'Containers - Recipientes e Acessórios'), ('obstetric', 'Obstetric - Instrumental para Parto'), ('ppe', 'PPE - Equipamento de Proteção Individual (Personal Protective Equipment)')], max_length=50)),
                ('manufacturer', models.CharField(max_length=255)),
                ('unit', models.CharField(choices=[('pc', 'Peça'), ('set', 'Conjunto'), ('unit', 'Unidade'), ('pk', 'Pacote'), ('box', 'Caixa')], max_length=10)),
            ],
            options={
                'verbose_name': 'Produto',
                'verbose_name_plural': 'Produtos',
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
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='batch_stocks', to='products.product', to_field='sku')),
            ],
            options={
                'verbose_name': 'Saldo Por Lote',
                'verbose_name_plural': 'Saldo Por Lote',
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
            options={
                'verbose_name': 'Historico do Lote',
                'verbose_name_plural': 'Historico do Lote',
            },
        ),
        migrations.CreateModel(
            name='ProductBatchStage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stage', models.CharField(choices=[('recebimento', 'Recebimento'), ('lavagem', 'Lavagem'), ('esterilizacao', 'Esterilização'), ('distribuicao', 'Distribuição')], default='recebimento', max_length=50)),
                ('stage_quantity', models.PositiveIntegerField()),
                ('stage_status', models.CharField(choices=[('in_process', 'In Process'), ('completed', 'Completed')], max_length=20)),
                ('stage_date', models.DateField(auto_now_add=True)),
                ('batch_stock', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='stages', to='products.productbatchstock', to_field='batch_number')),
            ],
            options={
                'verbose_name': 'Fase Por Lote',
                'verbose_name_plural': 'Fase Por Lote',
            },
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
