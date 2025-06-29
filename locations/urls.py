from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('search/', views.search_locations, name='search_locations'),
    path('locations/add/', views.add_location, name='add_location'),
    path('locations/<int:location_id>/', views.location_detail, name='location_detail'),
    path('locations/<int:location_id>/edit/', views.edit_location, name='edit_location'),
]