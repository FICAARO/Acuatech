from django.db import models

# Create your models here.
class CategoriaProducto(models.Model):
	nombre=models.CharField(max_length=50)
	created=models.DateTimeField(auto_now_add=True)
	updated=models.DateTimeField(auto_now_add=True)
	class Meta:
		verbose_name="categoriaProd"
		verbose_name_plural="categoriasProd"
	def __str__(self):
		return self.nombre

class SubCategoriaProducto(models.Model):
	nombre=models.CharField(max_length=50)
	categorias=models.ForeignKey(CategoriaProducto,on_delete=models.CASCADE)
	created=models.DateTimeField(auto_now_add=True)
	updated=models.DateTimeField(auto_now_add=True)
	class Meta:
		verbose_name="subcategoriaProd"
		verbose_name_plural="subcategoriasProd"
	def __str__(self):
		return self.nombre


class Producto(models.Model):
	nombre=models.CharField(max_length=50)
	descripcion=models.CharField(max_length=250,null=True)
	categorias=models.ForeignKey(CategoriaProducto,on_delete=models.CASCADE)
	subCategoria=models.ForeignKey(SubCategoriaProducto,on_delete=models.CASCADE)
	imagen=models.ImageField(upload_to="tienda",null=True,blank=True)
	precio=models.FloatField()
	disponibilidad=models.BooleanField(default=True)
	created=models.DateTimeField(auto_now_add=True)
	updated=models.DateTimeField(auto_now_add=True)
	class Meta:
		verbose_name="Producto"
		verbose_name_plural="Productos"
	def __str__(self):
		return self.nombre
