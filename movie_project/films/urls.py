from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

urlpatterns = [
    path('', views.films, name="film_list"),
    path('add_film', views.add_film, name="add_film"),
    path('film_detail/<int:film_id>/', views.film_detail, name='film_detail'),
    path('film_detail/<int:film_id>/delete/', views.delete_film, name='delete_film'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

