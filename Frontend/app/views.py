from datetime import date
import re
from django.shortcuts import render
from app.forms import FileForm, DeleteForm
import requests
import json

# Create your views here.
endpoint = 'http://localhost:3000/'
def home(request):
    return render(request, template_name='Inicio.html')

contexto = {
        'content': '',
        'binario': '',
        'response': '',
        'contenidoar': '',
        'data': ''
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
        return render(request, 'Carga.html', contexto)
    return render(request, 'Carga.html',contexto)

def EnviarArchivo(request):
    if request.method == 'POST':
        if contexto['content'] != '':
            respuesta = requests.post(endpoint + 'ConsultarDatos', data=contexto['binario'])
            mensaje = json.loads(respuesta.content.decode('utf-8'))
            contexto['response'] = mensaje['contenido']
            contexto['contenidoar']= mensaje['contenido']
            contexto['data'] = mensaje['contenido']
    else:
        return render(request, 'Carga.html', contexto)
    return render(request, 'Carga.html', contexto)

def ResetearData(request):
    print(request.method)
    if request.method == 'POST':
        respuesta = requests.delete(endpoint + 'reset')
        mensaje = json.loads(respuesta.content.decode('utf-8'))
        print(mensaje)
        contexto['response'] = ''
        contexto['content'] = ''
        contexto['binario']=''
        contexto['contenidoar']=''
        contexto['data'] =''
        return render(request, 'Carga.html', contexto)
    return render(request, 'Carga.html', contexto)

def ConsultarDatos(request):
    return render(request, 'Datos.html', contexto)
ctx = {
        'fechas':[],
        'empresas':[]
    }
def FiltrarFecha(request):
    dates = requests.get(endpoint + 'Fechas')
    d = dates.json()
    empresas = requests.get(endpoint + 'Empresas')
    e = empresas.json()
    ctx['fechas'] = d
    ctx['empresas'] = e

    return render(request, 'ResumenFecha.html', ctx)

def FiltrarRango(request):
    dates = requests.get(endpoint + 'Fechas')
    d = dates.json()
    empresas = requests.get(endpoint + 'Empresas')
    e = empresas.json()
    ctx['fechas'] = d
    ctx['empresas'] = e
    return render(request, 'ResumenRango.html', ctx)