from django.shortcuts import render
def index(request):
	return render(request,"index.html")
def contact(request):
	return render(request,"contacto.html")
def servicios(request):
	return render(request,"servicios.html")


