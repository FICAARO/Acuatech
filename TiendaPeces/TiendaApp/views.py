from django.shortcuts import render
from .models import Producto,CategoriaProducto,SubCategoriaProducto
def peces(request):
	productosall=Producto.objects.filter(categorias="1")
	return render(request,"productos.html",{"productos":productosall})
def productos(request):
	return render(request,"productos.html",{"productos":Producto.objects.all()})
def productos_search(request,busqueda):
	if "-" in busqueda:
		cat,subcat=busqueda.split("-")
		categoria=CategoriaProducto.objects.get(nombre=cat).id
		subcategoria=SubCategoriaProducto.objects.get(nombre=subcat).id
		productos=Producto.objects.filter(categorias=categoria,subCategoria=subcategoria)
	else:
		categoria=CategoriaProducto.objects.get(nombre=busqueda).id
		productos=Producto.objects.filter(categorias=categoria)
	return render(request,"productos.html",{"productos":productos})
def index(request):
	return render(request,"tiendaindex.html")
def carro(request):
	return render(request,"carro.html")

