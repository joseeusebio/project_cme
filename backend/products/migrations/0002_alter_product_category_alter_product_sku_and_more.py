# Generated by Django 5.0.6 on 2024-06-22 22:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='product',
            name='sku',
            field=models.CharField(blank=True, editable=False, max_length=50, unique=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='unit',
            field=models.CharField(max_length=10),
        ),
    ]
