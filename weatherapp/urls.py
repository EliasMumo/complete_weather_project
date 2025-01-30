from django.urls import path
from . import views

urlpatterns = [
    path('', views.weather_view, name='weather'),
    path('add_favorite/', views.add_favorite, name='add_favorite'),
    path('favorites/', views.favorites_view, name='favorites'),
]

