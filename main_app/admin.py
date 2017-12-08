from django.contrib import admin
from .models import Client
from .models import Product
from .models import Order

# Register your models here.


@admin.register(Client)
class ClientsAdmin(admin.ModelAdmin):
    pass


@admin.register(Product)
class ProductsAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'image']


@admin.register(Order)
class OrdersAdmin(admin.ModelAdmin):
    pass
