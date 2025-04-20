from django.contrib import admin
from .models import Category, Product, Barcode, ProductUpdate

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Barcode)
admin.site.register(ProductUpdate)
