def total_carro(request):
	total=0
	for key,value in request.session["carro"].items():
		total+=float(value["precio"]*value["cantidad"])
	return {"total_carro":total}