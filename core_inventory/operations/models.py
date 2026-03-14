from django.db import models
from products.models import Product
from inventory.models import Warehouse
from inventory.services import process_receipt, process_delivery, process_transfer, process_adjustment

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

    def save(self, *args, **kwargs):

        is_new = self.pk is None

        previous_status = None
        if not is_new:
            previous_status = Receipt.objects.get(pk=self.pk).status

        super().save(*args, **kwargs)

        if self.status == "DONE" and previous_status != "DONE":

            for item in self.items.all():

                process_receipt(
                    product=item.product,
                    warehouse=self.warehouse,
                    quantity=item.quantity,
                    reference=f"Receipt {self.id}"
                )

    def __str__(self):
        return f"Receipt {self.id} - {self.supplier}"

class ReceiptItem(models.Model):

    receipt = models.ForeignKey(Receipt, on_delete=models.CASCADE, related_name="items")

    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    quantity = models.IntegerField()

    def save(self, *args, **kwargs):
        from inventory.models import Stock, StockLedger

        super().save(*args, **kwargs)

        stock, created = Stock.objects.get_or_create(
            product=self.product,
            warehouse=self.receipt.warehouse
        )

        stock.quantity += self.quantity
        stock.save()

        StockLedger.objects.create(
            product=self.product,
            warehouse=self.receipt.warehouse,
            change=self.quantity,
            movement_type="RECEIPT",
            reference=f"Receipt #{self.receipt.id}"
        )
    
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

    def save(self, *args, **kwargs):

        is_new = self.pk is None

        previous_status = None
        if not is_new:
            previous_status = Delivery.objects.get(pk=self.pk).status

        super().save(*args, **kwargs)

        if self.status == "DONE" and previous_status != "DONE":

            for item in self.items.all():

                process_delivery(
                    product=item.product,
                    warehouse=self.warehouse,
                    quantity=item.quantity,
                    reference=f"Delivery {self.id}"
                )

    def __str__(self):
        return f"Delivery {self.id} - {self.customer}"

class DeliveryItem(models.Model):

    delivery = models.ForeignKey(Delivery, on_delete=models.CASCADE, related_name="items")

    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    quantity = models.IntegerField()

    def save(self, *args, **kwargs):
        from inventory.models import Stock, StockLedger

        super().save(*args, **kwargs)

        stock = Stock.objects.get(
            product=self.product,
            warehouse=self.delivery.warehouse
        )

        stock.quantity -= self.quantity
        stock.save()

        StockLedger.objects.create(
            product=self.product,
            warehouse=self.delivery.warehouse,
            change=-self.quantity,
            movement_type="DELIVERY",
            reference=f"Delivery #{self.delivery.id}"
        )

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

    def save(self, *args, **kwargs):

        is_new = self.pk is None

        super().save(*args, **kwargs)

        if is_new:

            process_transfer(
                product=self.product,
                from_warehouse=self.from_warehouse,
                to_warehouse=self.to_warehouse,
                quantity=self.quantity
            )

    def __str__(self):
        return f"Transfer {self.product} {self.quantity}"

class Adjustment(models.Model):

    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE)

    counted_quantity = models.IntegerField()

    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):

        is_new = self.pk is None

        super().save(*args, **kwargs)

        if is_new:

            process_adjustment(
                product=self.product,
                warehouse=self.warehouse,
                counted_quantity=self.counted_quantity
            )

    def __str__(self):
        return f"Adjustment {self.product}"