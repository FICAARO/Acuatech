from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib.auth.models import User  
from django.contrib.auth import login, logout, authenticate 
from django.contrib import messages
from django.forms.forms import Form  
from django import forms  
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

class CustomAuthenticationForm(AuthenticationForm):
    def __init__(self, request=None, *args, **kwargs):
        super().__init__(request=None, *args, **kwargs)
        self.fields['username'].label = 'Nombre de usuario'
        self.fields['password'].label = 'Contraseña'

class CustomUserCreationForm(UserCreationForm):  
    username = forms.CharField(label='Nombre de usuario', min_length=5, max_length=150)  
    email = forms.EmailField(label='Email')  
    password1 = forms.CharField(label='Contraseña', widget=forms.PasswordInput)  
    password2 = forms.CharField(label='Confirme Contraseña', widget=forms.PasswordInput)  
  
    def username_clean(self):  
        username = self.cleaned_data['username'].lower()  
        new = User.objects.filter(username = username)  
        if new.count():  
            raise ValidationError("User Already Exist")  
        return username  
  
    def email_clean(self):  
        email = self.cleaned_data['email'].lower()  
        new = User.objects.filter(email=email)  
        if new.count():  
            raise ValidationError(" Email ya Existe")  
        return email  
  
    def clean_password2(self):  
        password1 = self.cleaned_data['password1']  
        password2 = self.cleaned_data['password2']  
  
        if password1 and password2 and password1 != password2:  
            raise ValidationError("La contraseña no concide")  
        return password2  
  
    def save(self, commit = True):  
        user = User.objects.create_user(  
            self.cleaned_data['username'],  
            self.cleaned_data['email'],  
            self.cleaned_data['password1']  
        )  
        return user  
class VRegistro(View):

    def get(self, request):
        form=CustomUserCreationForm()
        return render(request,"registro.html",{"form":form})

    def post(self, request):
        form=CustomUserCreationForm(request.POST)

        if form.is_valid():

            usuario=form.save()

            login(request, usuario)

            return redirect('/')

        else:
            for msg in form.error_messages:
                messages.error(request, form.error_messages[msg])

            return render(request,"registro.html",{"form":form})

def cerrar_sesion(request):
    logout(request)

    return redirect('Home')

def loginView(request):
    if request.method=="POST":
        form=CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            nombre_usuario=form.cleaned_data.get("username")
            contra=form.cleaned_data.get("password")
            usuario=authenticate(username=nombre_usuario, password=contra)
            if usuario is not None:
                login(request, usuario)
                return redirect('/')
            else:
                messages.error(request, "usuario no válido")
        else:
            messages.error(request, "información incorrecta")

    form=CustomAuthenticationForm()
    return render(request,"login.html",{"form":form})




    

        
