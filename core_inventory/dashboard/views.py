from django.shortcuts import render

from products.models import Product
from inventory.models import Stock, Warehouse, StockLedger
from operations.models import Receipt, Delivery


def dashboard_page(request):

    context = {
        "products": Product.objects.count(),
        "warehouses": Warehouse.objects.count(),
        "receipts": Receipt.objects.count(),
        "deliveries": Delivery.objects.count(),
    }

    return render(request,"dashboard.html",context)


def products_page(request):

    products = Product.objects.all()

    return render(request,"products.html",{"products":products})


def stock_page(request):

    stock = Stock.objects.select_related("product","warehouse")

    return render(request,"stock.html",{"stock":stock})


def activity_page(request):

    activity = StockLedger.objects.order_by("-timestamp")[:20]

    return render(request,"activity.html",{"activity":activity})