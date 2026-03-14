from django.contrib import admin
from .models import Receipt, ReceiptItem, Delivery, DeliveryItem, Transfer, Adjustment

# Register your models here.

class ReceiptItemInline(admin.TabularInline):
    model = ReceiptItem
    extra = 1

class ReceiptAdmin(admin.ModelAdmin):
    inlines = [ReceiptItemInline]

class DeliveryItemInline(admin.TabularInline):
    model = DeliveryItem
    extra = 1

class DeliveryAdmin(admin.ModelAdmin):
    inlines = [DeliveryItemInline]


admin.site.register(Receipt, ReceiptAdmin)
admin.site.register(Delivery, DeliveryAdmin)
admin.site.register(Transfer)
admin.site.register(Adjustment)