from django.urls import path

from .import views

app_name="carro"

urlpatterns = [
    path("agregar/<int:producto_id>/", views.agregar, name="agregar"),
    path("comprar/<int:producto_id>/", views.comprar, name="comprar"),
    path("eliminar/<int:producto_id>/", views.eliminar, name="eliminar"),
    path("restar/<int:producto_id>/", views.restar, name="restar"),
    path("limpiar/", views.limpiar_carro, name="limpiar"),
]



