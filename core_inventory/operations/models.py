from django.db import models
from products.models import Product
from inventory.models import Warehouse
from inventory.services import process_receipt, process_delivery

# Create your models here.

class Receipt(models.Model):

    supplier = models.CharField(max_length=200)

    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)

    status = models.CharField(
        max_length=20,
        choices=[
            ('DRAFT','Draft'),
            ('DONE','Done')
        ],
        default='DRAFT'
    )

    def __str__(self):
        return f"Receipt {self.id} - {self.supplier}"

class ReceiptItem(models.Model):

    receipt = models.ForeignKey(Receipt, on_delete=models.CASCADE, related_name="items")

    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    quantity = models.IntegerField()
    
class Delivery(models.Model):

    customer = models.CharField(max_length=200)

    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)

    status = models.CharField(
        max_length=20,
        choices=[
            ('DRAFT','Draft'),
            ('DONE','Done')
        ],
        default='DRAFT'
    )

    def __str__(self):
        return f"Delivery {self.id} - {self.customer}"

class DeliveryItem(models.Model):

    delivery = models.ForeignKey(Delivery, on_delete=models.CASCADE, related_name="items")

    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    quantity = models.IntegerField()

class Transfer(models.Model):

    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    from_warehouse = models.ForeignKey(
        Warehouse,
        related_name="transfer_from",
        on_delete=models.CASCADE
    )

    to_warehouse = models.ForeignKey(
        Warehouse,
        related_name="transfer_to",
        on_delete=models.CASCADE
    )

    quantity = models.IntegerField()

    created_at = models.DateTimeField(auto_now_add=True)

class Adjustment(models.Model):

    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE)

    counted_quantity = models.IntegerField()

    created_at = models.DateTimeField(auto_now_add=True)