from rest_framework import serializers

from .models import Product


class ProductSerializer(serializers.ModelSerializer):
    """
    Serializing all the Products
    """
    class Meta:
        model = Product
        fields = ('id', 'name', 'type', 'price', 'description', 'image')
