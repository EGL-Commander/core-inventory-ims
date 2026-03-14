from django.contrib import admin
from .models import Receipt, ReceiptItem, Delivery, DeliveryItem, Transfer, Adjustment

# Register your models here.

admin.site.register(Receipt)
admin.site.register(ReceiptItem)
admin.site.register(Delivery)
admin.site.register(DeliveryItem)
admin.site.register(Transfer)
admin.site.register(Adjustment)