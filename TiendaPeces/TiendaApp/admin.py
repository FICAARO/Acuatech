from django.contrib import admin
from .models import CategoriaProducto,Producto,SubCategoriaProducto

class CategoriaProductoAdmin(admin.ModelAdmin):
	readonly_fields=("created","updated")
class SubCategoriaProductoAdmin(admin.ModelAdmin):
	readonly_fields=("created","updated")
class ProductoAdmin(admin.ModelAdmin):
	readonly_fields=("created","updated")
admin.site.register(CategoriaProducto,CategoriaProductoAdmin)
admin.site.register(SubCategoriaProducto,SubCategoriaProductoAdmin)
admin.site.register(Producto,ProductoAdmin)
# Register your models here.
