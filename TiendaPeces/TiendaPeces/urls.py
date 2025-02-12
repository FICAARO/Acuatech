"""
URL configuration for TiendaPeces project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
#from TiendaPeces.views import *
#import TiendaPecesWebApp.views 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('TiendaPecesWebApp.urls')),# TiendaPecesWebApp.views.site.index,name="index"),
    path('tienda/',include('TiendaApp.urls')),
    path('carro/',include('CarroApp.urls')),
    path('autenticacion/',include('autenticacion.urls')),
    path('pedidos/',include('pedidos.urls')),
    path('fishtank3d/',include('fishtank3d.urls')),
    path('chatSupport/',include('chatSeller.urls')),
    path('healthcam/',include('healthcam.urls')),
    path('fishtanks_map/',include('map_fishtanks.urls')),
    path('dashboard/', include('dashboard.urls')),
    #path('index/', TiendaPecesWebApp.views.site.index,name="index")
]

urlpatterns +=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)