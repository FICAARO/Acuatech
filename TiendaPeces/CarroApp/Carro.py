class Carro:
	def __init__(self,request):
		self.request=request
		self.session=request.session
		carro=self.session.get("carro")
		if not carro:
			carro=self.session["carro"]={}
		else:
			self.carro=carro
	def guardar_carro(self):
		self.session["carro"]=self.carro
		self.session.modifier=True
	def agregar(self,producto):
		if str(producto.id) not in self.carro.keys():
			self.carro[producto.id]={
				"producto_id":producto.id
				"nombre":producto.nombre,
				"precio":producto.precio,
				"imagen":producto.imagen.url,
				"catidad":1,
			}
		else:
			self.carro[producto.id]["catidad"]+=1
		self.guardar_carro()
	def eliminar(self,producto):
		if str(producto.id) in self.carro.keys():
			del self.carro[producto.id]
			self.guardar_carro()
	def restar(self,producto):
		if str(producto.id) in self.carro.keys():
			if self.carro[producto.id]["catidad"]>1:
				self.carro[producto.id]["catidad"]-=1
				self.guardar_carro()
			else if self.carro[producto.id]["catidad"]==1:
				self.eliminar(producto)
	def limpiar_carro():
		carro=self.session["carro"]={}
		self.guardar_carro()
#if self.carro[producto.id]["catidad"]>1: