from django.http import HttpResponse
from django.template import Template, Context
def index(request):
	file=open("AcuarioCalypso/templates/index.html")
	plt=Template(file.read())
	file.close()
	context=Context()
	doc=plt.render(context)
	return HttpResponse(doc)