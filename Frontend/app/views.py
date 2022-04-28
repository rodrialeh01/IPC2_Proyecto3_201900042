import re
from django.shortcuts import render
from app.forms import FileForm
import requests
import json

# Create your views here.
endpoint = 'http://localhost:3000/'
def home(request):
    return render(request, template_name='Inicio.html')

contexto = {
        'content': '',
        'binario': '',
        'response': ''
    }

def carga(request):
    if request.method == 'POST':
        form = FileForm(request.POST,request.FILES)
        if form.is_valid():
            f = request.FILES['file']
            xml_binary = f.read()
            xml = xml_binary.decode('utf-8')
            print(xml)
            contexto['content'] = xml
            contexto['binario'] = xml_binary
        else:
            contexto['content'] = ''
    else:
        return render(request, 'Carga.html')
    return render(request, 'Carga.html',contexto)

def EnviarArchivo(request):
    if request.method == 'POST':
        if contexto['content'] != '':
            respuesta = requests.post(endpoint + 'ConsultarDatos', data=contexto['binario'])
            mensaje = json.loads(respuesta.content.decode('utf-8'))
            contexto['response'] = mensaje['contenido']
    return render(request, 'Carga.html', contexto)