from django.shortcuts import render

# Create your views here.
def fishtankviewer(request):
	return render(request,"fishtankviewer.html")