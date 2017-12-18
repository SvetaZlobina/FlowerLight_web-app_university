from django.contrib import admin
from .models import Client
from .models import Product, ProductTag
from .models import Order

# Register your models here.


@admin.register(Client)
class ClientsAdmin(admin.ModelAdmin):
    list_display = ['login', 'email', 'name']


@admin.register(Product)
class ProductsAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'type']
    list_filter = ('type', 'price')


@admin.register(Order)
class OrdersAdmin(admin.ModelAdmin):
    list_display = ['client', 'product', 'amount', 'order_date', 'delivery_date']
    list_filter = ('product', 'amount', 'order_date', 'delivery_date')


@admin.register(ProductTag)
class ProductTagsAdmin(admin.ModelAdmin):
    pass
