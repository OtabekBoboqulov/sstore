from django.contrib import admin
from .models import Market


@admin.register(Market)
class NewUserAdmin(admin.ModelAdmin):
    list_display = ('market_username', 'market_name', 'phone_number', 'is_active')
    search_fields = ('market_username', 'market_name')
