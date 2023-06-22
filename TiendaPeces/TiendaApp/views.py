from django.shortcuts import render,redirect
from django.contrib import messages
from django.core.mail import send_mail
from pedidos.models import LineaPedido, Pedido
from CarroApp.Carro import Carro
from django.utils.html import strip_tags

from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
import datetime
from .models import Producto,CategoriaProducto,SubCategoriaProducto

def enviar_mail(**kwargs):
	asunto="Pedido tienda peces"
	mensaje=f"""Hola {kwargs.get("nombreusuario")}
	N° pedido {kwargs.get("pedido").id}
	Lineas pedido {kwargs.get("lineas_pedido")}
	Pago <img src="{kwargs.get("url_pago")}">
	"""
	from_email="jero98772@gmail.com"
	to=kwargs.get("email_usuario")
	to="jero98772@gmail.com"
	mensaje=strip_tags(mensaje)
	try:
		send_mail(asunto,mensaje,from_email,[to])
	except:
		pass
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
@login_required(login_url='/autenticacion/logear')
def pagar(request):
	msg=""
	if request.method == 'POST' :#and request.FILES['upload']:

		upload = request.FILES['upload']
		fss = FileSystemStorage()
		ext=upload.name.split(".")[1]
		name=str(request.user)+datetime.datetime.today().strftime("%m-%d-%Y,%H:%M")+"."+ext
		file = fss.save("pagos/"+name, upload)
		file_url = fss.url(file)

		pedido=Pedido.objects.create(user=request.user) # damos de alta un pedido
		mi_carro=Carro(request)  # cogemos el carro
		lineas_pedido=list()  # lista con los pedidos para recorrer los elementos del carro
		for key, value in mi_carro.carro.items(): #recorremos el carro con sus items
			lineas_pedido.append(LineaPedido(
				producto_id=key,
				cantidad=value['cantidad'],
				user=request.user,
				pedido=pedido                 
				))
		print(file_url)
		LineaPedido.objects.bulk_create(lineas_pedido) # crea registros en BBDD en paquete
		msg="El pedido se ha creado correctamente"
		enviar_mail(pedido=pedido,lineas_pedido=lineas_pedido,nombreusuario=request.user.username,email_usuario=request.user.email,url_pago=file_url)
		#return redirect("/") 
	return render(request,"pagar.html",{"msg":msg})

