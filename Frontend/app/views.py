from django.shortcuts import render
import requests

# Create your views here.

def home(request):
    hi = {
        'helou': 'hola'
    }
    hi.json() 
    context = {
        'title':hi
    }
    return render(request, 'index.html', context)