from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import healthcam
  
def healthcamIndex(request):
 
    if request.method == 'POST':
        form = healthcam(request.POST, request.FILES)
 
        if form.is_valid():
            form.save()
            return redirect('success')
    else:
        form = healthcam()
    return render(request, 'healthcam.html', {'form': form})
 
 
def success(request):
    return HttpResponse('successfully uploaded')
