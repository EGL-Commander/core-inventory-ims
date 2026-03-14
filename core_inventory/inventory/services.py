from .models import Stock, StockLedger
from products.models import Product
from inventory.models import Warehouse


def get_or_create_stock(product, warehouse):

    stock, created = Stock.objects.get_or_create(
        product=product,
        warehouse=warehouse,
        defaults={'quantity': 0}
    )

    return stock

def process_receipt(product, warehouse, quantity, reference="Receipt"):

    stock = get_or_create_stock(product, warehouse)

    stock.quantity += quantity
    stock.save()

    StockLedger.objects.create(
        product=product,
        warehouse=warehouse,
        change=quantity,
        movement_type="RECEIPT",
        reference=reference
    )

def process_delivery(product, warehouse, quantity, reference="Delivery"):

    stock = get_or_create_stock(product, warehouse)

    if stock.quantity < quantity:
        raise ValueError("Not enough stock available")

    stock.quantity -= quantity
    stock.save()

    StockLedger.objects.create(
        product=product,
        warehouse=warehouse,
        change=-quantity,
        movement_type="DELIVERY",
        reference=reference
    )

def process_transfer(product, from_warehouse, to_warehouse, quantity):

    from_stock = get_or_create_stock(product, from_warehouse)
    to_stock = get_or_create_stock(product, to_warehouse)

    if from_stock.quantity < quantity:
        raise ValueError("Not enough stock to transfer")

    from_stock.quantity -= quantity
    from_stock.save()

    to_stock.quantity += quantity
    to_stock.save()

    StockLedger.objects.create(
        product=product,
        warehouse=from_warehouse,
        change=-quantity,
        movement_type="TRANSFER_OUT"
    )

    StockLedger.objects.create(
        product=product,
        warehouse=to_warehouse,
        change=quantity,
        movement_type="TRANSFER_IN"
    )

def process_adjustment(product, warehouse, counted_quantity):

    stock = get_or_create_stock(product, warehouse)

    difference = counted_quantity - stock.quantity

    stock.quantity = counted_quantity
    stock.save()

    StockLedger.objects.create(
        product=product,
        warehouse=warehouse,
        change=difference,
        movement_type="ADJUSTMENT"
    )