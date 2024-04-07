from django.urls import path
from . import views

urlpatterns = [
    path('', views.index_map, name='index_map'),
    path('map/', views.mapweb, name='map'),
    path('addData/', views.addData, name='addData'),
]
