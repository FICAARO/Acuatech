from django.shortcuts import render
def index(request):
	return render(request,"index.html")#render_template("templates/index.html")

# Create your views here.
