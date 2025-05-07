from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name="main"),
    path('about/', views.about, name="about"),

    path('login/', views.user_login, name="login"),
    path('register/', views.register, name="register"),
    path('logout/', views.custom_logout, name='logout'),

    path('add_product/', views.add_product, name="add_product"),
    path('product_list/', views.product_list, name="product_list"),

    path('process_order/', views.process_order, name="process_order"),
    path('order_confirmation/<int:order_id>/', views.order_confirmation, name="order_confirmation"),
    path('order_history/', views.order_history, name="order_history"),
    path('order-details/<int:order_id>/', views.order_details, name="order_details"),
    path('repeat-order/<int:order_id>/', views.repeat_order, name='repeat_order'),
    path('order_list/', views.order_list, name="order_list"),
    path('order-in-work/<int:order_id>/', views.order_in_work, name='order_in_work'),

    path('api/rate-product/', views.RateProductView.as_view(), name='rate_product'),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
