# Generated by Django 5.2 on 2025-04-18 18:50

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('markets', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomToken',
            fields=[
                ('key', models.CharField(max_length=40, primary_key=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('market', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='custom_tokens', to='markets.market')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='custom_tokens', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
