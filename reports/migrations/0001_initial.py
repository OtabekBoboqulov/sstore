# Generated by Django 5.2 on 2025-04-20 16:50

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('markets', '0004_market_plan'),
    ]

    operations = [
        migrations.CreateModel(
            name='Expanse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('salary', 'Maosh'), ('rent', 'Ijara'), ('tax', 'Soliq'), ('add', 'Reklama'), ('other', 'Boshqa')], default='salary', max_length=10)),
                ('price', models.DecimalField(decimal_places=2, max_digits=11)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('market_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Expanses', to='markets.market')),
            ],
        ),
    ]
