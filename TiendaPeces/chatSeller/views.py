from django.shortcuts import render
# Create your views here.
def chatSellerIndex(request):
	r=request.GET.get("message")
	print(r)
	return render(request,"chat.html",{"chatmsg":"tets"})