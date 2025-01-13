from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="main"),
    path('about', views.about, name="about"),
    path('contacts', views.contacts, name="contacts"),
    path('services', views.services, name="services"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

