# Generated by Django 5.2 on 2025-04-19 05:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('markets', '0002_customtoken'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='market',
            name='market_username',
        ),
        migrations.AlterField(
            model_name='market',
            name='phone_number',
            field=models.CharField(max_length=16, unique=True),
        ),
    ]
