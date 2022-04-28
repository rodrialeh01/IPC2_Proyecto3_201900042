from django.shortcuts import render
from app.forms import FileForm
import requests

# Create your views here.
endpoint = 'http://localhost:3000/'
def home(request):
    return render(request, template_name='Inicio.html')

contexto = {
        'content': '',
        'response': ''
    }

def carga(request):
    print(request.method)
    if request.method == 'POST':
        form = FileForm(request.POST,request.FILES)
        print(form)
        if form.is_valid():
            f = request.FILES['file']
            xml_binary = f.read()
            xml = xml_binary.decode('utf-8')
            contexto['content'] = xml
        else:
            contexto['content'] = ''
    else:
        return render(request, 'Carga.html')
    return render(request, 'Carga.html',contexto)