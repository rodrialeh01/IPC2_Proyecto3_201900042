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

data = Analizador()

@app.route('/datos', methods=['POST'])
def ProcesarXML():
    try:
        print(request.data)
        archivo = request.data.decode('utf-8')
        data.analizarData(archivo)
        return jsonify({
            'message':'Archivo procesado correctamente'
        })
    except:
        return jsonify({
            'message':'Hubo un error al procesar el archivo'
        })
    

#LLAMANDO LA EJECUCION DE LA API EN EL MAIN
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000, debug=True)