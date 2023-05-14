def importe_tota_carro(request):
	total=0
	if request.user.is_authenticated:
		for key,value in request.session["carro"].items():
			pass
	"""
				total+=float(value["precio"]*value["cantidad"])
	"""
	return {"importe_tota_carro":total}