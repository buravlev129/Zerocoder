from django.contrib import admin
from .models import UserProfile, Product, OrderStatus, Order, OrderDetail, OrderReview, ProductRating, SalesReport

admin.site.register(UserProfile)

admin.site.register(Product)
admin.site.register(ProductRating)

admin.site.register(OrderStatus)
admin.site.register(Order)
admin.site.register(OrderDetail)
admin.site.register(OrderReview)

admin.site.register(SalesReport)

