# Generated by Django 5.2 on 2025-06-15 10:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('markets', '0006_alter_market_profile_picture'),
        ('reports', '0004_alter_expanse_type'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Expanse',
            new_name='Expense',
        ),
    ]
