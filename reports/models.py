from django.db import models
from markets.models import Market


class Expanse(models.Model):
    EXPANSE_TYPES = (
        ('salary', 'Maosh'),
        ('rent', 'Ijara'),
        ('tax', 'Soliq'),
        ('add', 'Reklama'),
        ('other', 'Boshqa'),
    )
    market_id = models.ForeignKey(Market, on_delete=models.CASCADE, related_name='Expanses')
    type = models.CharField(max_length=10, choices=EXPANSE_TYPES, default='salary')
    price = models.DecimalField(max_digits=11, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.market_id}-{self.type}'


class Debtor(models.Model):
    market_id = models.ForeignKey(Market, on_delete=models.CASCADE, related_name='Debtors')
    name = models.CharField(max_length=250)
    phone = models.CharField(max_length=20)
    price = models.DecimalField(max_digits=11, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.market_id}-{self.name}: {self.price}'
