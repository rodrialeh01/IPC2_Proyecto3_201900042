from django.shortcuts import render
import requests

# Create your views here.
endpoint = 'http://localhost:3000/'
def home(request):
    return render(request, template_name='Inicio.html')

def carga(request):
    return render(request, template_name='Carga.html')