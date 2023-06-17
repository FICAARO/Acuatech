from django.contrib import messages
from django.shortcuts import redirect, render

from django.contrib.auth.decorators import login_required
from carro.carro import Carro

from pedidos.models import LineaPedido, Pedido

from django.template.loader import render_to_string

from django.utils.html import strip_tags

from django.core.mail import send_mail

from .models import Producto


# Create your views here.


@login_required(login_url='/autenticacion/logear')
def procesar_pedido(request):
    pedido=Pedido.objects.create(user=request.user) # damos de alta un pedido
    carro=Carro(request)  # cogemos el carro
    lineas_pedido=list()  # lista con los pedidos para recorrer los elementos del carro
    for key, value in carro.carro.items(): #recorremos el carro con sus items
        lineas_pedido.append(LineaPedido(
            producto_id=key,
            cantidad=value['cantidad'],
            user=request.user,
            pedido=pedido                 
            ))

    LineaPedido.objects.bulk_create(lineas_pedido) # crea registros en BBDD en paquete
    #enviamos mail al cliente
    enviar_mail(
        pedido=pedido,
        lineas_pedido=lineas_pedido,
        nombreusuario=request.user.username,
        email_usuario=request.user.email
        

    )
    #mensaje para el futuro
    messages.success(request, "El pedido se ha creado correctamente")
    
    return redirect('../tienda')
    #return redirect('listado_productos')
    #return render(request, "tienda/tienda.html",{"productos":productos})
    

def enviar_mail(**kwargs):
    asunto="Gracias por el pedido"
    mensaje=render_to_string("emails/pedido.html", {
        "pedido": kwargs.get("pedido"),
        "lineas_pedido": kwargs.get("lineas_pedido"),
        "nombreusuario":kwargs.get("nombreusuario") 
                       
        })

    mensaje_texto=strip_tags(mensaje)
    from_email="cursos@pildorasinformaticas.es"
    #to=kwargs.get("email_usuario")
    to="aquí la dirección del destinatario"
    send_mail(asunto,mensaje_texto,from_email,[to], html_message=mensaje)
    
