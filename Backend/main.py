from flask import Flask, request
from flask_cors import CORS
from flask.json import jsonify

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
@app.route('/ProcesarMensaje', methods=['POST', 'GET'])
def ProcesarXMLMensaje():
    if request.method == 'POST':
        try:
            mensaje = request.data.decode('utf-8')
            data.AnalizarMensajePrueba(mensaje)
            return jsonify({
                'message':'Mensaje analizado correctamente'
            }), 200
        except:
            return jsonify({
                'message':'Hubo un error al procesar el archivo'
            }), 500
    elif request.method == 'GET':
        archivo = open("Database\Respuesta.xml", 'r', encoding='utf-8')
        contenido = archivo.read()
        archivo.close()
        return contenido

@app.route('/Fechas', methods=['GET'])
def Fechas():
    F=[]
    for d in data.Fechas:
        objeto ={
            'date':d 
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

#LLAMANDO LA EJECUCION DE LA API EN EL MAIN
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000, debug=True)