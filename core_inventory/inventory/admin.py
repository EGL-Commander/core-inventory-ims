from django.contrib import admin
from . models import Stock, StockLedger, Warehouse

# Register your models here.

admin.site.register(Warehouse)
admin.site.register(Stock)
admin.site.register(StockLedger)