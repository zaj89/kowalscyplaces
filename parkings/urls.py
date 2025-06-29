from django.urls import path
from . import views

urlpatterns = [
    path('mapa/', views.parking_map, name='parking_map'),
    path('mapa/add/', views.add_parking, name='add_parking'),
]
