from django.shortcuts import render
from .models import Producto
def peces(request):
	productosall=Producto.objects.filter(categorias="1")
	return render(request,"productos.html",{"productos":productosall})
def productos(request):
	return render(request,"productos.html",{"productos":Producto.objects.all()})
def productos_search(request,busqueda):
	if "-" in busqueda:
		cat,subcat=busqueda.split("-")
		productos=Producto.objects.filter(categorias=cat,subCategoria=subcat)
	else:
		productos=Producto.objects.filter(categorias=busqueda)
	return render(request,"productos.html",{"productos":productos})
def index(request):
	return render(request,"tiendaindex.html")
def carro(request):
	return render(request,"carro.html")

