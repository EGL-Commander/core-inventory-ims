from django.urls import path
from .views import product_list, stock_list, dashboard_stats, recent_activity, warehouse_list

urlpatterns = [
    path("products/", product_list),
    path("stock/", stock_list),
    path("dashboard/", dashboard_stats),
    path("activity/", recent_activity),
    path("warehouses/", warehouse_list),
]