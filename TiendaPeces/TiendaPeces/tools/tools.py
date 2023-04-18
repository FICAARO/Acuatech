from django.template import Template, Context

def render_template(fpath:str,**html_vars):
	file=open(fpath)
	plt=Template(file.read())
	file.close()
	context=Context(html_vars)
	doc=plt.render(context)
	return HttpResponse(doc)