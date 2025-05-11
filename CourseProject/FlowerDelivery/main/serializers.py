from rest_framework import serializers
from .models import ProductRating, Order

class ProductRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductRating
        fields = ['product', 'rating']


class OrderSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'user', 'username', 'delivery_address', 'phone_number', 'status', 'created_at', 'total_price']


