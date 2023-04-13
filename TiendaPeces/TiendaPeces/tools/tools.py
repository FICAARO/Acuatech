from django.template import Template, Context

def render_template(str:fpath,**html_vars=dict()):
	file=open(fpath)
	plt=Template(file.read())
	file.close()
	context=Context(html_vars)
	doc=plt.render(context)
	return HttpResponse(doc)