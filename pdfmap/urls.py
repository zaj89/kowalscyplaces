from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='pdfparser_index'),
]
