from flask import Flask, request
from flask_cors import CORS
from flask.json import jsonify
from datetime import datetime, timedelta

from Analizador import Analizador

#CREANDO LA API DE FLASK
app = Flask(__name__)
cors = CORS(app)

#RUTA DE INICIO DEL BACKEND
@app.route('/')
def index():
    return '<h1>Backend en funcionamiento :D</h1>'

#CREANDO UNA VARIABLE GLOBAL LA CUAL LLAMA A NUESTRO ANALIZADOR DE MENSAJES
data = Analizador()

#FUNCION PARA LEER EL ARCHIVO XML Y GENERAR SUS ESTADISTICAS (POST) Y PARA RETORNAR EL ARCHIVO DE SALIDA (GET)
@app.route('/ConsultarDatos', methods=['POST','GET'])
def ProcesarXML():
    if request.method == 'POST':
        try:
            #print(request.data)
            archivo = request.data.decode('utf-8')
            data.analizarData(archivo)
            archivo = open("Database\Respuestas.xml", 'r', encoding='utf-8')
            contenido = archivo.read()
            archivo.close()
            return jsonify({
                'message':'Archivo analizado correctamente',
                'contenido': contenido
            }), 200
        except:
            return jsonify({
                'message':'Hubo un error al procesar el archivo',
                'contenido': ""
            }), 500
    
#FUNCION PARA ANALIZAR MENSAJES DE PRUEBA Y GENERAR SUS ESTADISTICAS (POST) Y RETORNAR SU ARCHIVO DE SALIDA (GET)
@app.route('/ProcesarMensaje', methods=['POST'])
def ProcesarXMLMensaje():
    if request.method == 'POST':
        try:
            mensaje = request.data.decode('utf-8')
            data.AnalizarMensajePrueba(mensaje)
            archivo = open("Database\Respuesta.xml", 'r', encoding='utf-8')
            contenido = archivo.read()
            archivo.close()
            return jsonify({
                'message':'Mensaje analizado correctamente',
                'contenido': contenido
            }), 200
        except:
            return jsonify({
                'message':'Hubo un error al procesar el archivo',
                'contenido': ''
            }), 500


@app.route('/Fechas', methods=['GET'])
def Fechas():
    F=[]
    for d in data.MensajesF:
        objeto ={
            'date':d.fecha 
        }
        F.append(objeto)
    return jsonify(F)

@app.route('/Empresas', methods=['GET'])
def Empresas():
    E=[]
    for e in data.Nombres:
        objeto ={
            'business': e
        }
        E.append(objeto)
    return jsonify(E)

#FUNCION PARA RETORNAR LAS ESTADISTICAS POR FECHA O POR NOMBRE DE EMPRESA Y FECHA SOLICITADA
@app.route('/ConsultaFecha', methods=['POST'])
def FitrarFecha():
    try:
        fecha = None
        nombre = None
        try:
            fecha = request.json['fecha']
        except:
            fecha = None
        try:
            nombre = request.json['empresa']
        except:
            nombre = None
        
        if fecha != None and nombre == None or nombre == "":
            empresas = []
            for empresa in data.Empresas:
                if fecha == empresa.fecha:
                    objeto = {
                        'nombre': empresa.nombre,
                        'mensajes_totales': empresa.cantidad,
                        'mensajes_positivos': empresa.positivos,
                        'mensajes_negativos': empresa.negativos,
                        'mensajes_neutros': empresa.neutros
                    }
                    empresas.append(objeto)
            return jsonify(empresas),200
        elif fecha != None and nombre != None:
            for empresa in data.Empresas:
                if str(empresa.fecha) == str(fecha) and str(empresa.nombre) == str(nombre):
                    return jsonify({
                        'nombre': empresa.nombre,
                        'mensajes_totales': empresa.cantidad,
                        'mensajes_positivos': empresa.positivos,
                        'mensajes_negativos': empresa.negativos,
                        'mensajes_neutros': empresa.neutros
                    }),200
            return jsonify({
                'message':'No se encontro nada en la base de datos'
            }),400
        else:
            return jsonify({
                'message':'No se selecccionó ninguna fecha o empresa'
            }),400
    except:
        return jsonify({
            'message':'Hubo un error en la peticion'
        }), 500

@app.route('/reset', methods=['DELETE'])
def reset():
    archivo=open("Database/Respuestas.xml", 'w', encoding='utf-8')
    archivo.write('')
    archivo.close()
    archivo2=open('Database/Respuesta.xml', 'w', encoding='utf-8')
    archivo2.write('')
    archivo.close()
    data = Analizador()
    return jsonify({
        'message':  'Se eliminaron los datos'
    })

@app.route('/ConsultaRangoFechas', methods=['POST'])
def FiltrarRango():
    try:
        empresa = None 
        fecha_inicio = request.json['fecha_inicio']
        fecha_final = request.json['fecha_final']
        try:
            empresa = request.json['empresa']
        except:
            empresa = None
        
        if empresa != None:
            if fecha_inicio == fecha_final:
                for e in data.Empresas:
                    if str(e.fecha) == str(fecha_inicio) and str(e.nombre) == str(empresa):
                        return jsonify({
                            'nombre': e.nombre,
                            'fecha': e.fecha,
                            'mensajes_totales': e.cantidad,
                            'mensajes_positivos': e.positivos,
                            'mensajes_negativos': e.negativos,
                            'mensajes_neutros': e.neutros
                        }),200
            else:
                fecha_i = datetime.strptime(fecha_inicio, '%d/%m/%Y')
                fecha_f = datetime.strptime(fecha_final, '%d/%m/%Y')

                lista_fecha = [(fecha_i + timedelta(days=d)).strftime('%d/%m/%Y') for d in range((fecha_f - fecha_i).days + 1)]
                L = []
                for f in lista_fecha:
                    for e in data.Empresas:
                        if str(f) == str(e.fecha) and str(empresa) == str(e.nombre):
                            objeto = {
                                'nombre': e.nombre,
                                'fecha': e.fecha,
                                'mensajes_totales': e.cantidad,
                                'mensajes_positivos': e.positivos,
                                'mensajes_negativos': e.negativos,
                                'mensajes_neutros': e.neutros
                            }
                            L.append(objeto)
                return (jsonify(L))
        else:
            fecha_i = datetime.strptime(fecha_inicio, '%d/%m/%Y')
            fecha_f = datetime.strptime(fecha_final, '%d/%m/%Y')

            lista_fecha = [(fecha_i + timedelta(days=d)).strftime('%d/%m/%Y') for d in range((fecha_f - fecha_i).days + 1)]
            L = []
            for f in lista_fecha:
                for e in data.Empresas:
                    if f == e.fecha:
                        objeto = {
                            'nombre': e.nombre,
                            'fecha': e.fecha,
                            'mensajes_totales': e.cantidad,
                            'mensajes_positivos': e.positivos,
                            'mensajes_negativos': e.negativos,
                            'mensajes_neutros': e.neutros
                        }
                        L.append(objeto)
            return (jsonify(L))
    except:
        return jsonify({
            'message':'Hubo un error en la peticion'
        }), 500

@app.route('/Totales', methods=['POST'])
def MostrarMensajesTotales():
    try:
        fecha_inicio = request.json['fecha_inicio']
        fecha_final = request.json['fecha_final']
        fecha_i = datetime.strptime(fecha_inicio, '%d/%m/%Y')
        fecha_f = datetime.strptime(fecha_final, '%d/%m/%Y')
        lista_fecha = [(fecha_i + timedelta(days=d)).strftime('%d/%m/%Y') for d in range((fecha_f - fecha_i).days + 1)]
        L = []
        for f in lista_fecha:
            for e in data.MensajesF:
                if f == e.fecha:
                    objeto = {
                        'fecha': e.fecha,
                        'mensajes_totales': e.totales,
                        'mensajes_positivos': e.positivos,
                        'mensajes_negativos': e.negativos,
                        'mensajes_neutros': e.neutros
                    }
                    L.append(objeto)
        return (jsonify(L))
    except:
        return jsonify({
            'message':'Hubo un error en la peticion'
        }), 500

@app.route('/Fecha', methods=['POST'])
def MostrarMensajesxFecha():
    try:
        fecha = request.json['fecha']
        for f in data.MensajesF:
            if fecha == f.fecha:
                return jsonify({
                    'fecha':f.fecha,
                    'mensajes_totales': f.totales,
                    'mensajes_positivos': f.positivos,
                    'mensajes_negativos': f.negativos,
                    'mensajes_neutros': f.neutros
                })
    except:
        return jsonify({
            'message':'Hubo un error en la peticion'
        }), 500

#LLAMANDO LA EJECUCION DE LA API EN EL MAIN
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000, debug=True)