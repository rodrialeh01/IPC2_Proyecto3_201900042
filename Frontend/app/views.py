from datetime import date
import re
from urllib import response
from django.http import FileResponse
from django.shortcuts import render
from app.forms import FileForm, DeleteForm, AddForm
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import requests
import json
import io

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
    try:
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
    except:
        return render(request, '404.html')

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
c = {
    'content':'',
    'response':''
}
def MensajePrueba(request):
    print(request.method)
    if request.method == 'POST':
        form = AddForm(request.POST)
        if form.is_valid():
            json_data = form.cleaned_data
            contenido = json_data['mensaje']
            c['content'] = contenido
            mensaje = str(contenido).encode('utf-8')
            response = requests.post(endpoint + 'ProcesarMensaje',data=mensaje)
            respuesta = json.loads(response.content.decode('utf-8'))
            c['response'] = respuesta['contenido']
    else:
        return render(request, 'Prueba.html', c)
    return render(request, 'Prueba.html',c)

def Documentacion(request):
    return render(request,'Documentacion.html')

def Informacion(request):
    return render(request, 'Informacion.html')

def GenerarReporte1(request):
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter, bottomup=0)
    datos = requests.get(endpoint + 'pdf1')
    fecha = requests.get(endpoint + 'pdff1')
    f = fecha.json()
    d = datos.json()
    
    text_object = p.beginText(40,50)
    text_object.setFont('Helvetica', 20)
    text_object.textLine('FECHA: ' + f['fecha'])
    text_object.setFont('Helvetica', 14)
    text_object.textLine('Cantidad total de mensajes recibidos: ' + str(f['mensajes_totales']))
    text_object.textLine('Cantidad total de mensajes positivos: ' + str(f['mensajes_positivos']))
    text_object.textLine('Cantidad total de mensajes negativos: ' + str(f['mensajes_negativos']))
    text_object.textLine('Cantidad total de mensajes neutros: ' + str(f['mensajes_neutros']))
    text_object.textLine('')
    for data in d:
        text_object.setFont('Helvetica', 20)
        text_object.textLine(data['nombre'])
        text_object.setFont('Helvetica', 14)
        text_object.textLine('Número total de mensajes que mencionan a ' + str(data['nombre'] + ': ' + str(data['mensajes_totales'])))
        text_object.textLine('Mensajes positivos: ' + str(data['mensajes_positivos']))
        text_object.textLine('Mensajes negativos: ' + str(data['mensajes_negativos']))
        text_object.textLine('Mensajes neutros: ' + str(data['mensajes_neutros']))
        text_object.textLine('')

    p.drawText(text_object)
    p.showPage()
    p.save()
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename='Reporte_Resumen_' + str(f['fecha']) + str('.pdf'))

def GenerarReporte2(request):
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter, bottomup=0)
    datos = requests.get(endpoint + 'pdf2')
    data = datos.json()

    text_object = p.beginText(40,50)
    text_object.setFont('Helvetica', 25)
    text_object.textLine('RANGO DE FECHAS: ' + str(data['fecha_inicio']) + str(' - ') + str(data['fecha_final']))
    text_object.textLine('')
    for datas in data['dataresponse']:
        text_object.setFont('Helvetica', 20)
        text_object.textLine(datas['fecha'])
        text_object.textLine(datas['nombre'])
        text_object.setFont('Helvetica', 14)
        text_object.textLine('Número total de mensajes que mencionan a ' + str(datas['nombre'] + ': ' + str(datas['mensajes_totales'])))
        text_object.textLine('Mensajes positivos: ' + str(datas['mensajes_positivos']))
        text_object.textLine('Mensajes negativos: ' + str(datas['mensajes_negativos']))
        text_object.textLine('Mensajes neutros: ' + str(datas['mensajes_neutros']))
        text_object.textLine('')

    p.drawText(text_object)
    p.showPage()
    p.save()
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename='Reporte_Resumen_del_Rango_' + str(data['fecha_inicio']) +'__'+ str(data['fecha_final']) + str('.pdf'))