# Generated by Django 5.0.6 on 2024-06-24 13:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='processbatchstage',
            name='quantity_processed',
        ),
        migrations.AlterField(
            model_name='processbatchstage',
            name='stage',
            field=models.CharField(max_length=50),
        ),
    ]