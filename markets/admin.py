from django.contrib import admin
from .models import Market, CustomToken

admin.site.register(CustomToken)

@admin.register(Market)
class NewUserAdmin(admin.ModelAdmin):
    list_display = ('phone_number', 'market_name', 'plan', 'is_active')
    search_fields = ('phone_number', 'market_name')
