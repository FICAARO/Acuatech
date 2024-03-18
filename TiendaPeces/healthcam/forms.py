from django import forms
from .models import UploadedFile
 
 
class healthcam(forms.ModelForm):
 
    class Meta:
        model = UploadedFile
        fields = ['file']
