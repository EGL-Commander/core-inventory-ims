from django.shortcuts import render
from django.db.models import Sum
from products.models import Product
from inventory.models import Stock, Warehouse, StockLedger
from operations.models import Receipt, Delivery


def dashboard_page(request):

    total_stock = Stock.objects.aggregate(total=Sum("quantity"))["total"] or 0

    recent = StockLedger.objects.order_by("-timestamp")[:5]

    context = {
        "products": Product.objects.count(),
        "warehouses": Warehouse.objects.count(),
        "receipts": Receipt.objects.count(),
        "deliveries": Delivery.objects.count(),
        "stock": total_stock,
        "recent": recent,
    }

    return render(request,"dashboard.html",context)


def products_page(request):

    if request.method == "POST":

        name = request.POST.get("name")
        sku = request.POST.get("sku")

        Product.objects.create(
            name=name,
            sku=sku
        )

    products = Product.objects.all()

    return render(request,"products.html",{"products":products})


def stock_page(request):

    stock = Stock.objects.select_related("product","warehouse")

    return render(request,"stock.html",{"stock":stock})


def activity_page(request):

    activity = StockLedger.objects.order_by("-timestamp")[:20]

    return render(request,"activity.html",{"activity":activity})