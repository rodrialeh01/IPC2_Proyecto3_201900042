import xml.etree.ElementTree as ET
from clases import Empresa,Mensaje,Servicio
class Analizador():
    def __init__(self):
        self.palabraspositivas = []
        self.palabrasnegativas = []
        
    def analizarData(self, contenido):
        print(contenido)
        raiz = ET.XML(contenido)
        nombres = []
        for element in raiz:
            if element.tag == "diccionario":
                print('=====================DICCIONARIO=====================')
                for subelement in element:
                    if subelement.tag == "sentimientos_positivos":
                        print('=====================POSITIVOS=====================')
                        for subsubelement in subelement:
                            print('Palabra: ' + str(subsubelement.text))
                            self.palabraspositivas.append(str(subsubelement.text))
                    elif subelement.tag == "sentimientos_negativos":
                        print('=====================NEGATIVOS=====================')
                        for subsubelement in subelement:
                            print('Palabra: ' + str(subsubelement.text))
                            self.palabrasnegativas.append(str(subsubelement.text))
                    elif subelement.tag == "empresas_analizar":
                        print('=====================EMPRESAS A ANALIZAR=====================')
                        for subsubelement in subelement:
                            for empresa in subsubelement:
                                if empresa.tag == "nombre":
                                    print('Nombre: ' + str(empresa.text))
                                    nombres.append(empresa.text)
                                elif empresa.tag == "servicio":
                                    print('     =================SERVICIO==================')
                                    print('Nombre: ' + str(empresa.attrib.get('nombre')))
                                    for alias in empresa:
                                        print('Alias: ' + str(alias.text))
            elif element.tag == "lista_mensajes":
                print('=====================LISTA DE MENSAJES=====================')
                for mensaje in element:
                    print('Mensaje: ' + str(mensaje.text))

