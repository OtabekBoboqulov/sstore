from django.db import models
from markets.models import Market


class Category(models.Model):
    name = models.CharField(max_length=100)
    market_id = models.ForeignKey(Market, on_delete=models.CASCADE, related_name='categories')

    def __str__(self):
        return self.name


class Product(models.Model):
    QUANTITY_TYPES = (
        ('mass', 'Grammda'),
        ('numeric', 'Sonda'),
    )
    STATUS_CHOICES = (
        ('ended', 'Tugagan'),
        ('few', 'Kam qolgan'),
        ('available', 'Mavjud'),
    )
    category_id = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=250)
    quantity = models.IntegerField()
    quantity_type = models.CharField(max_length=10, choices=QUANTITY_TYPES, default='numeric')
    price_per_quantity = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='ended')

    def __str__(self):
        return self.name


class Barcode(models.Model):
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='barcodes')
    number = models.CharField(max_length=20)

    def __str__(self):
        return self.number
