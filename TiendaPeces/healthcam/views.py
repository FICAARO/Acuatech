from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import healthcam
  
def healthcamIndex(request):
    print("healthcam")
    if request.method == 'POST':
        form = healthcam(request.POST, request.FILES)
        print("form",form.is_valid())
        if form.is_valid():
            print("sve")
            form.save()
            return redirect('success')
    else:
        form = healthcam()
    return render(request, 'healthcam.html', {'form': form})
 
 
def success(request):
    return HttpResponse('successfully uploaded')

def diagnosis(request, image_name):
    #load model, get asnwer and send again
    return render(request, 'diagnosis.html', {'image_name': image_name})