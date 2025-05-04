from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name="main"),
    path('about/', views.about, name="about"),
    path('login/', views.user_login, name="login"),
    path('register/', views.register, name="register"),
    path('logout/', views.custom_logout, name='logout')

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
