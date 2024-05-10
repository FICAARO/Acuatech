from django.urls import re_path, path

from dashboard.views import dashboard, data, generate

urlpatterns = [
    path('', dashboard, name="dashboard"),
    path('data/', data, name='data'),
    path('generate/', generate, name='generate')
]