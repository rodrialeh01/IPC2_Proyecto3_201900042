import xml.etree.ElementTree as ET
import re
from clases import Empresa,Servicio
class Serviciotemp():
    def __init__(self, nombre):
        self.nombre = nombre
        self.alias = []
class Analizador():
    def __init__(self):
        self.palabraspositivas = []
        self.palabrasnegativas = []
        self.Fechas = []
        self.Empresas = []
        self.EmpresasAnalisis = []
        self.Servicios = []
        
    def analizarData(self, contenido):
        print(contenido)
        raiz = ET.XML(contenido)
        self.palabraspositivas = []
        self.palabrasnegativas = []
        self.Fechas = []
        self.Empresas = []
        self.EmpresasAnalisis = []
        self.Servicios = []
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
                                        nombre = empresa.attrib.get('nombre')
                                        nombre = nombre.lower()
                                        nombre = nombre.replace('á','a')
                                        nombre = nombre.replace('é','e')
                                        nombre = nombre.replace('í','i')
                                        nombre = nombre.replace('ó','o')
                                        nombre = nombre.replace('ú','u')
                                        nombre = nombre.replace('\n', ' ')
                                        nombre = nombre.replace('\t', ' ')
                                        a = []
                                        for alias in empresa:
                                            print('Alias: ' + str(alias.text))
                                            a.append(alias.text)
                                        nuevo = Serviciotemp(nombre)
                                        nuevo.alias = a 
                                        self.Servicios.append(nuevo)
            elif element.tag == "lista_mensajes":
                print('=====================LISTA DE MENSAJES=====================')
                for mensaje in element:
                    print('Mensaje: ')
                    texto = mensaje.text.lstrip().rstrip()
                    self.AnalizarMensaje(texto, nombres)
                    print('____________________________________')

        self.MostrarLista()
        self.MostrarporFecha()

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
        date = ''
        empresa = ''
        positivo = 0
        negativo = 0
        for i in range(len(palabras)):
            palabras[i] = palabras[i].replace(' ', '')
            print(palabras[i])
        while(contador < len(palabras)):
            #VERIFICAR LUGAR Y FECHA
            if palabras[contador] == 'lugar' and palabras[contador+1] == 'y' and palabras[contador+2] == 'fecha:':
                contador += 4
                fecha = re.compile(r"\d\d\/\d\d\/\d\d\d\d")
                if re.match(fecha,palabras[contador]).group() == palabras[contador]:
                    print('Fecha: '+ str(re.match(fecha,palabras[contador]).group()))
                    date = str(re.match(fecha,palabras[contador]).group())
                    hora = re.compile(r"(([01][0-9]|2[0-3])\:[0-5][0-9])")
                    if re.match(hora,palabras[contador+1]).group() == palabras[contador+1]:
                        print('Hora:' + str(re.match(hora,palabras[contador+1]).group()))
                        self.AgregarFecha(date)
                        contador+=1
            elif palabras[contador] == 'lugar' and palabras[contador+1] == 'y' and palabras[contador+2] == 'fecha' and palabras[contador+3] == ':':
                contador += 5
                fecha = re.compile(r"\d\d\/\d\d\/\d\d\d\d")
                if re.match(fecha,palabras[contador]).group() == palabras[contador]:
                    print('Fecha: '+ str(re.match(fecha,palabras[contador]).group()))
                    date = str(re.match(fecha,palabras[contador]).group())
                    hora = re.compile(r"(([01][0-9]|2[0-3])\:[0-5][0-9])")
                    if re.match(hora,palabras[contador+1]).group() == palabras[contador+1]:
                        print('Hora:' + str(re.match(hora,palabras[contador+1]).group()))
                        self.AgregarFecha(date)
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
                #LEE LA EMPRESA
                for i in range(len(self.EmpresasAnalisis)):
                    if palabras[contador] == self.EmpresasAnalisis[i] or palabras[contador] == (self.EmpresasAnalisis[i] + ',') or palabras[contador] == (self.EmpresasAnalisis[i] + '.'):
                        empresa = nombres[i]
                        self.AgregarEmpresa(date,empresa)
                #LEE LAS PALABRAS POSITIVAS
                for j in range(len(self.palabraspositivas)):
                    if palabras[contador] == self.palabraspositivas[j] or palabras[contador] == (self.palabraspositivas[j] + ',') or palabras[contador] == (self.palabraspositivas[j] + '.'):
                        positivo += 1
                #LEE LAS PALABRAS NEGATIVAS
                for j in range(len(self.palabrasnegativas)):
                    if palabras[contador] == self.palabrasnegativas[j] or palabras[contador] == (self.palabrasnegativas[j] + ',') or palabras[contador] == (self.palabrasnegativas[j] + '.'):
                        negativo += 1
            contador += 1
        print('P: ' + str(positivo))
        print('N: ' + str(negativo))
        if positivo == negativo:
            self.retornarEmpresa(date,empresa).neutros += 1
        elif positivo > negativo:
            self.retornarEmpresa(date,empresa).positivos += 1
        elif negativo > positivo:
            self.retornarEmpresa(date,empresa).negativos += 1
        print(mensaje)

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

    def AgregarServicio(self,fecha,empresa, servicio):
        nuevo = Servicio(servicio,fecha,1)
        for i in range(len(self.Empresas)):
            if self.Empresas[i].nombre == empresa:
                if len(self.Empresas[i].servicios) == 0:
                    self.Empresas[i].servicios.append(nuevo)
                else:
                    if self.VerificarServicio(empresa,fecha,servicio) == True:
                        self.retornarServicio(empresa,fecha,servicio).cantidad += 1
                    else:
                        self.Empresas[i].servicios.append(nuevo)

    def VerificarServicio(self,empresa,fecha, servicio):
        encontrado = False
        for i in range(len(self.Empresas)):
            if self.Empresas[i].nombre == empresa:
                for j in range(len(self.Empresas[i].servicios)):
                    if self.Empresas[i].servicios[j].fecha == fecha and self.Empresas[i].servicios[j].nombre == servicio:
                        encontrado = True
        return encontrado

    def retornarServicio(self,empresa,fecha,servicio):
        for i in range(len(self.Empresas)):
            if self.Empresas[i].nombre == empresa:
                for j in range(len(self.Empresas[i].servicios)):
                    if self.Empresas[i].servicios[j].fecha == fecha and self.Empresas[i].servicios[j].nombre == servicio:
                        return self.Empresas[i].servicios[j]

    def MostrarLista(self):
        print('------------------EMPRESAS----------------')
        for i in range(len(self.Empresas)):
            print('Fecha: ' + str(self.Empresas[i].fecha))
            print('Nombre de la Empresa: ' + str(self.Empresas[i].nombre))
            print('Cantidad de Mensajes: ' + str(self.Empresas[i].cantidad))
            print('Positivos: ' + str(self.Empresas[i].positivos))
            print('Negativos: ' + str(self.Empresas[i].negativos))
            print('Neutro: ' + str(self.Empresas[i].neutros))

    def MostrarporFecha(self):
        print('.....................................................')
        for i in range(len(self.Fechas)):
            print('Fecha: ' + str(self.Fechas[i]))
            cantidadp = 0
            cantidadn = 0
            cantidadne = 0
            for j in range(len(self.Empresas)):
                if self.Fechas[i] == self.Empresas[j].fecha:
                    print('Empresa: ' + str(self.Empresas[j].nombre))
                    print('Cantidad: ' + str(self.Empresas[j].cantidad))
                    cantidadp += self.Empresas[j].positivos
                    cantidadn += self.Empresas[j].negativos
                    cantidadne += self.Empresas[j].neutros
            print('Cantidad total de positivos en este dia: ' + str(cantidadp))
            print('Cantidad total de negativos en este dia: ' + str(cantidadn))
            print('Cantidad total de neutros en este dia: ' + str(cantidadne))
            total = cantidadp + cantidadn + cantidadne
            print('Cantidad total de mensajes en este dia: ' + str(total))
            print('$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')

    def mostrarServicios(self):
        print('/////////////////////////////////////////////////')
        for i in range(len(self.Empresas)):
            print('Empresa: ' + self.Empresas[i].nombre)
            print('-------------------SERVICIOS--------------')
            for j in range(len(self.Empresas[i].servicios)):
                print('Fecha: ' + str(self.Empresas[i].servicios[j].fecha))
                print('Nombre: ' + str(self.Empresas[i].servicios[j].nombre))
                print('Cantidad: ' + str(self.Empresas[i].servicios[j].cantidad))
                print('Positivos: ' + str(self.Empresas[i].servicios[j].positivos))
                print('Negativos: ' + str(self.Empresas[i].servicios[j].negativos))
                print('Neutros: ' + str(self.Empresas[i].servicios[j].neutros))
