import xml.etree.ElementTree as ET
import re
from clases import Empresa,Mensaje,Servicio
class Analizador():
    def __init__(self):
        self.palabraspositivas = []
        self.palabrasnegativas = []
        self.Fechas = []
        self.Empresas = []
        self.EmpresasAnalisis = []
        
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
                            palabra =subsubelement.text.strip()
                            palabra = palabra.replace('á','a')
                            palabra = palabra.replace('é','e')
                            palabra = palabra.replace('í','i')
                            palabra = palabra.replace('ó','o')
                            palabra = palabra.replace('ú','u')
                            print('Palabra: ' + str(palabra))
                            palabra = palabra.lower().lstrip().rstrip()
                            self.palabraspositivas.append(palabra)
                    elif subelement.tag == "sentimientos_negativos":
                        print('=====================NEGATIVOS=====================')
                        for subsubelement in subelement:
                            palabra =subsubelement.text.lstrip().rstrip()
                            palabra = palabra.replace('á','a')
                            palabra = palabra.replace('é','e')
                            palabra = palabra.replace('í','i')
                            palabra = palabra.replace('ó','o')
                            palabra = palabra.replace('ú','u')
                            print('Palabra: ' + str(palabra))
                            palabra = palabra.lower()
                            self.palabrasnegativas.append(palabra)
                    elif subelement.tag == "empresas_analizar":
                        print('=====================EMPRESAS A ANALIZAR=====================')
                        for subsubelement in subelement:
                            if subsubelement.tag == 'empresa':
                                print('=====================EMPRESA=====================')
                                for empresa in subsubelement:
                                    if empresa.tag == "nombre":
                                        print('Nombre: ' + str(empresa.text))
                                        nombre = empresa.text.lstrip().rstrip()
                                        nombres.append(nombre)
                                        empresan = empresa.text.lower().lstrip().rstrip()
                                        self.EmpresasAnalisis.append(empresan)
                                    elif empresa.tag == "servicio":
                                        print('     =================SERVICIO==================')
                                        print('Nombre: ' + str(empresa.attrib.get('nombre')))
                                        for alias in empresa:
                                            print('Alias: ' + str(alias.text))
            elif element.tag == "lista_mensajes":
                print('=====================LISTA DE MENSAJES=====================')
                for mensaje in element:
                    print('Mensaje: ')
                    texto = mensaje.text.lstrip().rstrip()
                    self.AnalizarMensaje(texto, nombres)

    def AnalizarMensaje(self, mensaje, nombres):
        mensaje = mensaje.lower()
        mensaje = mensaje.replace('á','a')
        mensaje = mensaje.replace('é','e')
        mensaje = mensaje.replace('í','i')
        mensaje = mensaje.replace('ó','o')
        mensaje = mensaje.replace('ú','u')
        mensaje = mensaje.replace('\n', ' ')
        mensaje = mensaje.replace('\t', ' ')
        palabras = mensaje.split()
        contador = 0
        mensaje = ''
        while(contador < len(palabras)):
            #VERIFICAR LUGAR Y FECHA
            if palabras[contador] == 'lugar' and palabras[contador+1] == 'y' and palabras[contador+2] == 'fecha:':
                contador += 4
                fecha = re.compile(r"\d\d\/\d\d\/\d\d\d\d")
                if re.match(fecha,palabras[contador]).group() == palabras[contador]:
                    print('Fecha: '+ str(re.match(fecha,palabras[contador]).group()))
                    hora = re.compile(r"(([01][0-9]|2[0-3])\:[0-5][0-9])")
                    if re.match(hora,palabras[contador+1]).group() == palabras[contador+1]:
                        print('Hora:' + str(re.match(hora,palabras[contador+1]).group()))
                        contador+=1
            elif palabras[contador] == 'lugar' and palabras[contador+1] == 'y' and palabras[contador+2] == 'fecha' and palabras[contador+3] == ':':
                contador += 5
                fecha = re.compile(r"\d\d\/\d\d\/\d\d\d\d")
                if re.match(fecha,palabras[contador]).group() == palabras[contador]:
                    print('Fecha: '+ str(re.match(fecha,palabras[contador]).group()))
                    hora = re.compile(r"(([01][0-9]|2[0-3])\:[0-5][0-9])")
                    if re.match(hora,palabras[contador+1]).group() == palabras[contador+1]:
                        print('Hora:' + str(re.match(hora,palabras[contador+1]).group()))
                        contador+=1

            #VERIFICAR USUARIO
            elif palabras[contador] == 'usuario:':
                contador +=1
                usuario = re.compile("([a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*)|([a-zA-Z0-9.!#$%&'\*\+/=?^_`{|}~-]+)")
                if re.match(usuario,palabras[contador]).group() == palabras[contador]:
                    print('Usuario: ' + str(re.match(usuario,palabras[contador]).group()))
            elif palabras[contador] == 'usuario' and palabras[contador+1] == ':':
                contador +=2
                usuario = re.compile("([a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*)|([a-zA-Z0-9.!#$%&'\*\+/=?^_`{|}~-]+)")
                if re.match(usuario,palabras[contador]).group() == palabras[contador]:
                    print('Usuario: ' + str(re.match(usuario,palabras[contador]).group()))

            #VERIFICAR RED SOCIAL
            elif palabras[contador] == 'red' and palabras[contador+1] == 'social:':
                contador += 2
                redsocial = re.compile("[a-zA-Z0-9.!#$%&'\*\+/=?^_`{|}~-]+")
                if re.match(redsocial,palabras[contador]).group() == palabras[contador]:
                    print('Red Social: ' + str(re.match(redsocial,palabras[contador]).group()))
            elif palabras[contador] == 'red' and palabras[contador+1] == 'social' and palabras[contador+2]:
                contador += 3
                redsocial = re.compile("[a-zA-Z0-9.!#$%&'\*\+/=?^_`{|}~-]+")
                if re.match(redsocial,palabras[contador]).group() == palabras[contador]:
                    print('Red Social: ' + str(re.match(redsocial,palabras[contador]).group()))

            #LEERA EL MENSAJE
            else:
                mensaje += palabras[contador] + ' '
            contador += 1
        
        print(mensaje)
        '''
        print('**************************************************************************')
        fechas = re.findall(r"(\d\d\/\d\d\/\d\d\d\d\ ([01][0-9]|2[0-3]):[0-5][0-9])",mensaje)
        print(fechas[0][0])
        fecha = re.findall(r"\d\d\/\d\d\/\d\d\d\d", fechas[0][0])
        self.AgregarFecha(fecha)
        print(fecha)
        
        for i in range(len(self.EmpresasAnalisis)):
            empresadetected =re.findall(self.EmpresasAnalisis[i], mensaje)
            print(empresadetected)
            if len(empresadetected)!= 0:
                print(nombres[i])
                self.AgregarEmpresa(fecha[0],nombres[i])

        self.MostrarLista()
        '''

    def AgregarFecha(self,fecha):
        if len(self.Fechas) == 0:
            self.Fechas.append(fecha)
        else:
            if fecha in self.Fechas:
                pass
            else:
                self.Fechas.append(fecha)

    def AgregarEmpresa(self,fecha, empresa):
        if len(self.Empresas) == 0:
            self.Empresas.append(Empresa(fecha,empresa,1))
        else:
            if self.VerificarEmpresa(fecha,empresa) == True:
                self.retornarEmpresa(fecha,empresa).cantidad += 1
            else:
                self.Empresas.append(Empresa(fecha,empresa,1))

    def VerificarEmpresa(self,fecha, empresa):
        encontrado = False
        for i in range(len(self.Empresas)):
            if empresa == self.Empresas[i].nombre and fecha == self.Empresas[i].fecha:
                encontrado = True
        return encontrado

    def retornarEmpresa(self,fecha,empresa):
        for i in range(len(self.Empresas)):
            if empresa == self.Empresas[i].nombre and fecha == self.Empresas[i].fecha:
                return self.Empresas[i]

    def MostrarLista(self):
        print('------------------EMPRESAS----------------')
        for i in range(len(self.Empresas)):
            print('Fecha: ' + str(self.Empresas[i].fecha))
            print('Nombre de la Empresa: ' + str(self.Empresas[i].nombre))
            print('Cantidad de Mensajes: ' + str(self.Empresas[i].cantidad))