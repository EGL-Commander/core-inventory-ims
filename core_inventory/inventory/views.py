from django.shortcuts import render
from django.http import JsonResponse
from products.models import Product
from inventory.models import Stock, Warehouse, StockLedger
from operations.models import Receipt, Delivery

# Create your views here.

def product_list(request):

    products = Product.objects.all()

    data = []

    for p in products:
        data.append({
            "id": p.id,
            "name": p.name,
            "sku": p.sku
        })

    return JsonResponse(data, safe=False)

def stock_list(request):

    stocks = Stock.objects.select_related("product","warehouse")

    data = []

    for s in stocks:
        data.append({
            "product": s.product.name,
            "warehouse": s.warehouse.name,
            "quantity": s.quantity
        })

    return JsonResponse(data, safe=False)

def dashboard_stats(request):

    total_products = Product.objects.count()
    total_warehouses = Warehouse.objects.count()
    total_receipts = Receipt.objects.count()
    total_deliveries = Delivery.objects.count()

    data = {
        "products": total_products,
        "warehouses": total_warehouses,
        "receipts": total_receipts,
        "deliveries": total_deliveries
    }

    return JsonResponse(data)

def recent_activity(request):

    entries = StockLedger.objects.select_related("product","warehouse").order_by("-timestamp")[:10]

    data = []

    for e in entries:
        data.append({
            "product": e.product.name,
            "warehouse": e.warehouse.name,
            "change": e.change,
            "type": e.movement_type,
            "time": e.timestamp
        })

    return JsonResponse(data, safe=False)

def warehouse_list(request):

    warehouses = Warehouse.objects.all()

    data = []

    for w in warehouses:
        data.append({
            "id": w.id,
            "name": w.name,
            "location": w.location
        })

    return JsonResponse(data, safe=False)