from django.urls import path
from .views import dashboard_page, products_page, stock_page, activity_page

urlpatterns = [

path("", dashboard_page),

path("products/", products_page),

path("stock/", stock_page),

path("activity/", activity_page),

]