# Generated by Django 5.2 on 2025-04-20 16:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_barcode_date_category_date_product_date_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='productupdate',
            name='quantity',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
