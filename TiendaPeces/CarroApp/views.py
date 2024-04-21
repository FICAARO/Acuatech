from django.shortcuts import render, redirect
from .Carro import Carro as carro
from TiendaApp.models import Producto
def agregar(request,producto_id):
	mi_carro=carro(request)
	producto=Producto.objects.get(id=producto_id)
	mi_carro.agregar(producto)
	return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
def eliminar(request,producto_id):
	mi_carro=carro(request)
	producto=Producto.objects.get(id=producto_id)
	mi_carro.eliminar(producto)
	return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
def restar(request,producto_id):
	mi_carro=carro(request)
	producto=Producto.objects.get(id=producto_id)
	mi_carro.restar(producto)
	return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
def limpiar_carro(request,producto_id):
	mi_carro=carro(request)
	mi_carro.limpiar_carro()
	return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
def comprar(request,producto_id):
	mi_carro=carro(request)
	producto=Producto.objects.get(id=producto_id)
	mi_carro.agregar(producto)
	return redirect("/tienda/carro/")