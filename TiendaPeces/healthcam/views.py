from django.shortcuts import render
# Create your views here.
def healthcamIndex(request):
	return render(request,"healthcam.html")