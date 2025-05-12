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


class SalesReportSerializer(serializers.Serializer):
    month = serializers.DateField(format="%Y-%m")
    total_revenue = serializers.DecimalField(max_digits=10, decimal_places=2)
    average_check = serializers.DecimalField(max_digits=10, decimal_places=2)
    total_orders = serializers.IntegerField()


class PopularGoodsReportSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    product_name = serializers.CharField()
    total_quantity = serializers.IntegerField()

