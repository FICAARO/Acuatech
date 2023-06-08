from django.shortcuts import render
from .models import Producto
def peces(request):
	return render(request,"peces.html")
def productos(request):
	productosall=Producto.objects.all()
	return render(request,"productos.html",{"productos":Producto.objects.all()})
def index(request):
	return render(request,"tiendaindex.html")
def carro(request):
	return render(request,"carro.html")

