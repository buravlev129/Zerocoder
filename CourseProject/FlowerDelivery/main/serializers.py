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

    month_name = serializers.SerializerMethodField()
    year = serializers.SerializerMethodField()
    
    def get_month_name(self, obj):
        month_num = obj['month'].month
        months = {
            1: 'Январь', 2: 'Февраль', 3: 'Март', 
            4: 'Апрель', 5: 'Май', 6: 'Июнь',
            7: 'Июль', 8: 'Август', 9: 'Сентябрь',
            10: 'Октябрь', 11: 'Ноябрь', 12: 'Декабрь'
        }
        return months.get(month_num, '')
    
    def get_year(self, obj):
        return obj['month'].year


class PopularGoodsReportSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    product_name = serializers.CharField()
    total_quantity = serializers.IntegerField()
