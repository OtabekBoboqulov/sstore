from django.db import models
from markets.models import Market
from reports.models import Debtor
from cloudinary.models import CloudinaryField


class Category(models.Model):
    name = models.CharField(max_length=100)
    market_id = models.ForeignKey(Market, on_delete=models.CASCADE, related_name='categories')
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    QUANTITY_TYPES = (
        ('kg', 'KG'),
        ('dona', 'DONA'),
        ('metr', 'METR'),
        ('litr', 'LITR'),
    )
    STATUS_CHOICES = (
        ('ended', 'Tugagan'),
        ('few', 'Kam qolgan'),
        ('available', 'Mavjud'),
    )
    category_id = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=250)
    quantity = models.IntegerField()
    quantity_type = models.CharField(max_length=10, choices=QUANTITY_TYPES, default='dona')
    price_per_quantity = models.DecimalField(max_digits=10, decimal_places=2)
    image = CloudinaryField('product image', folder='sstore_products',
                            default='sstore_products/0c32b31941863a0f1fb8e97eaf55f595_lc10im', overwrite=True)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='ended')
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Barcode(models.Model):
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='barcodes')
    number = models.CharField(max_length=20)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.number


class ProductUpdate(models.Model):
    STATUS_TYPES = (
        ('added', 'Qo`shish'),
        ('subed', 'Sotildi'),
    )
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='updates')
    status = models.CharField(max_length=10, choices=STATUS_TYPES, default='subed')
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=11, decimal_places=2)
    debtor = models.ForeignKey(Debtor, on_delete=models.SET_NULL, null=True, blank=True, related_name='debts')
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.product_id}-{self.status}'
