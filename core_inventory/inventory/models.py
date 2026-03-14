from django.db import models
from products.models import Product

# Create your models here.

class Warehouse(models.Model):
    name = models.CharField(max_length=200)
    location = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Stock(models.Model):

    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE)

    quantity = models.IntegerField(default=0)


    class Meta:
        unique_together = ('product', 'warehouse')


    def __str__(self):
        return f"{self.product.name} - {self.warehouse.name}: {self.quantity}"

class StockLedger(models.Model):

    MOVEMENT_TYPES = [

        ('RECEIPT', 'Receipt'),
        ('DELIVERY', 'Delivery'),
        ('TRANSFER_IN', 'Transfer In'),
        ('TRANSFER_OUT', 'Transfer Out'),
        ('ADJUSTMENT', 'Adjustment')

    ]

    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE)

    change = models.IntegerField()

    movement_type = models.CharField(max_length=20, choices=MOVEMENT_TYPES)

    reference = models.CharField(max_length=200, blank=True)

    timestamp = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"{self.product.name} {self.change} ({self.movement_type})"