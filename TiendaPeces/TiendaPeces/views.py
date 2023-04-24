from django.http import HttpResponse
from django.shortcuts import render
#from TiendaPeces.tools.tools import *
class site:
	#done 0
	def shoppingCart(request):
		return render(request,"shoppingcart.html")
	def login(request):
		return render(request,"index.html")
	def register(request):
		return render(request,"index.html")
	def shop(request):
		return render(request,"index.html")
