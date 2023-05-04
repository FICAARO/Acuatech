from django.shortcuts import render, redirect
from .Carro import carro
from tienda.models import Producto
def agregar(request,prodocto_id):
	mi_carro=carro(request)
	prodocto=Producto.objects.get(id=prodocto_id)
	mi_carro.agregar(producto)
	return rendirect("tienda")
def eliminar(request,prodocto_id):
	mi_carro=carro(request)
	prodocto=Producto.objects.get(id=prodocto_id)
	mi_carro.eliminar(producto)
	return rendirect("tienda")
def restar(request,prodocto_id):
	mi_carro=carro(request)
	prodocto=Producto.objects.get(id=prodocto_id)
	mi_carro.restar(producto)
	return rendirect("tienda")
def limpiar_carro(request,prodocto_id):
	mi_carro=carro(request)
	mi_carro.limpiar_carro()
	return rendirect("tienda")