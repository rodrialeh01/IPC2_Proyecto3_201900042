import xml.etree.ElementTree as ET
import re
from clases import Empresa,Servicio
class Serviciotemp():
    def __init__(self,empresa, nombre):
        self.empresa = empresa
        self.nombre = nombre
        self.alias = []

class FechaTemp():
    def __init__(self, fecha, cantidad):
        self.fecha = fecha
        self.totales = cantidad
        self.positivos = 0
        self.negativos = 0
        self.neutros = 0

class Analizador():
    def __init__(self):
        self.palabraspositivas = []
        self.palabrasnegativas = []
        self.Empresas = []
        self.EmpresasAnalisis = []
        self.Servicios = []
        self.Nombres = []
        self.MensajesF = []
        self.palabraspositivasT = []
        self.palabrasnegativasT = []
        self.EmpresasT = []
        self.EmpresasAnalisisT = []
        self.ServiciosT = []
        self.NombresT = []
        self.MensajesFT = []
        
    def analizarArchivo(self, contenido):
        #print(contenido)
        raiz = ET.XML(contenido)
        self.palabraspositivasT = []
        self.palabrasnegativasT = []
        self.EmpresasT = []
        self.EmpresasAnalisisT = []
        self.ServiciosT = []
        self.NombresT = []
        self.MensajesFT = []
        empre =''
        for element in raiz:
            if element.tag == "diccionario":
                #print('=====================DICCIONARIO=====================')
                for subelement in element:
                    if subelement.tag == "sentimientos_positivos":
                        #print('=====================POSITIVOS=====================')
                        for subsubelement in subelement:                            
                            palabra =subsubelement.text.strip()
                            palabra = palabra.replace('á','a')
                            palabra = palabra.replace('é','e')
                            palabra = palabra.replace('í','i')
                            palabra = palabra.replace('ó','o')
                            palabra = palabra.replace('ú','u')
                            #print('Palabra: ' + str(palabra))
                            palabra = palabra.lower().lstrip().rstrip()
                            self.palabraspositivasT.append(palabra)
                    elif subelement.tag == "sentimientos_negativos":
                        #print('=====================NEGATIVOS=====================')
                        for subsubelement in subelement:
                            palabra =subsubelement.text.lstrip().rstrip()
                            palabra = palabra.replace('á','a')
                            palabra = palabra.replace('é','e')
                            palabra = palabra.replace('í','i')
                            palabra = palabra.replace('ó','o')
                            palabra = palabra.replace('ú','u')
                            #print('Palabra: ' + str(palabra))
                            palabra = palabra.lower()
                            self.palabrasnegativasT.append(palabra)
                    elif subelement.tag == "empresas_analizar":
                        #print('=====================EMPRESAS A ANALIZAR=====================')
                        for subsubelement in subelement:
                            if subsubelement.tag == 'empresa':
                                #print('=====================EMPRESA=====================')
                                for empresa in subsubelement:
                                    if empresa.tag == "nombre":
                                        #print('Nombre: ' + str(empresa.text))
                                        nombre = empresa.text.lstrip().rstrip()
                                        empre = nombre
                                        self.NombresT.append(nombre)
                                        empresan = empresa.text.lower().lstrip().rstrip()
                                        empresan = empresan.replace('á','a')
                                        empresan = empresan.replace('é','e')
                                        empresan = empresan.replace('í','i')
                                        empresan = empresan.replace('ó','o')
                                        empresan = empresan.replace('ú','u')
                                        empresan = empresan.replace('\n', ' ')
                                        empresan = empresan.replace('\t', ' ')
                                        self.EmpresasAnalisisT.append(empresan)
                                    elif empresa.tag == "servicio":
                                        #print('     =================SERVICIO==================')
                                        #print('Nombre: ' + str(empresa.attrib.get('nombre')))
                                        nombre = empresa.attrib.get('nombre').lstrip().rstrip()
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
                                            #print('Alias: ' + str(alias.text))
                                            nombre2 = alias.text.lstrip().rstrip()
                                            nombre2 = nombre2.lower()
                                            nombre2 = nombre2.replace('á','a')
                                            nombre2 = nombre2.replace('é','e')
                                            nombre2 = nombre2.replace('í','i')
                                            nombre2 = nombre2.replace('ó','o')
                                            nombre2 = nombre2.replace('ú','u')
                                            nombre2 = nombre2.replace('\n', ' ')
                                            nombre2 = nombre2.replace('\t', ' ')
                                            a.append(nombre2)
                                        #print(empre)
                                        nuevo = Serviciotemp(empre,nombre)
                                        nuevo.alias = a 
                                        self.ServiciosT.append(nuevo)
            elif element.tag == "lista_mensajes":
                #print('=====================LISTA DE MENSAJES=====================')
                for mensaje in element:
                    #print('Mensaje: ')
                    texto = mensaje.text.lstrip().rstrip()
                    self.AnalizarMensajeT(texto)
    
    def AnalizarMensajeT(self, mensaje):
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
        positivo = 0
        negativo = 0
        empresasrep ={}
        for i in range(len(palabras)):
            palabras[i] = palabras[i].replace(' ', '')
            #print(palabras[i])
        while(contador < len(palabras)):
            #VERIFICAR LUGAR Y FECHA
            if palabras[contador] == 'lugar' and palabras[contador+1] == 'y' and palabras[contador+2] == 'fecha:':
                contador += 4
                fecha = re.compile(r"\d\d\/\d\d\/\d\d\d\d")
                if re.match(fecha,palabras[contador]).group() == palabras[contador]:
                    #print('Fecha: '+ str(re.match(fecha,palabras[contador]).group()))
                    date = str(re.match(fecha,palabras[contador]).group())
                    hora = re.compile(r"(([01][0-9]|2[0-3])\:[0-5][0-9])")
                    if re.match(hora,palabras[contador+1]).group() == palabras[contador+1]:
                        #print('Hora:' + str(re.match(hora,palabras[contador+1]).group()))
                        self.AgregarMensajeFT(date)
                        contador+=1
            elif palabras[contador] == 'lugar' and palabras[contador+1] == 'y' and palabras[contador+2] == 'fecha' and palabras[contador+3] == ':':
                contador += 5
                fecha = re.compile(r"\d\d\/\d\d\/\d\d\d\d")
                if re.match(fecha,palabras[contador]).group() == palabras[contador]:
                    #print('Fecha: '+ str(re.match(fecha,palabras[contador]).group()))
                    date = str(re.match(fecha,palabras[contador]).group())
                    hora = re.compile(r"(([01][0-9]|2[0-3])\:[0-5][0-9])")
                    if re.match(hora,palabras[contador+1]).group() == palabras[contador+1]:
                        #print('Hora:' + str(re.match(hora,palabras[contador+1]).group()))
                        self.AgregarMensajeFT(date)
                        contador+=1

            #VERIFICAR USUARIO
            elif palabras[contador] == 'usuario:':
                contador +=1
                usuario = re.compile("([a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*)|([a-zA-Z0-9.!#$%&'\*\+/=?^_`{|}~-]+)")
                if re.match(usuario,palabras[contador]).group() == palabras[contador]:
                    #print('Usuario: ' + str(re.match(usuario,palabras[contador]).group()))
                    pass
            elif palabras[contador] == 'usuario' and palabras[contador+1] == ':':
                contador +=2
                usuario = re.compile("([a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*)|([a-zA-Z0-9.!#$%&'\*\+/=?^_`{|}~-]+)")
                if re.match(usuario,palabras[contador]).group() == palabras[contador]:
                    #print('Usuario: ' + str(re.match(usuario,palabras[contador]).group()))
                    pass

            #VERIFICAR RED SOCIAL
            elif palabras[contador] == 'red' and palabras[contador+1] == 'social:':
                contador += 2
                redsocial = re.compile("[a-zA-Z0-9.!#$%&'\*\+/=?^_`{|}~-]+")
                if re.match(redsocial,palabras[contador]).group() == palabras[contador]:
                    #print('Red Social: ' + str(re.match(redsocial,palabras[contador]).group()))
                    pass
            elif palabras[contador] == 'red' and palabras[contador+1] == 'social' and palabras[contador+2] == ':':
                contador += 3
                redsocial = re.compile("[a-zA-Z0-9.!#$%&'\*\+/=?^_`{|}~-]+")
                if re.match(redsocial,palabras[contador]).group() == palabras[contador]:
                    #print('Red Social: ' + str(re.match(redsocial,palabras[contador]).group()))
                    pass

            #LEERA EL MENSAJE
            else:
                mensaje += palabras[contador] + ' '
                palabras[contador] = palabras[contador].replace(',', '')
                palabras[contador] = palabras[contador].replace('.', '')
                palabras[contador] = palabras[contador].replace('!', '')
                palabras[contador] = palabras[contador].replace('?', '')
                #LEE LA EMPRESA
                for i in range(len(self.EmpresasAnalisisT)):
                    if palabras[contador] == self.EmpresasAnalisisT[i]:
                        empresa = self.NombresT[i]
                        if empresa in empresasrep:
                            empresasrep[empresa] +=1
                        else:
                            empresasrep[empresa] = 1
                #LEE LAS PALABRAS POSITIVAS
                for j in range(len(self.palabraspositivasT)):
                    if palabras[contador] == self.palabraspositivasT[j]:
                        positivo += 1
                #LEE LAS PALABRAS NEGATIVAS
                for j in range(len(self.palabrasnegativasT)):
                    if palabras[contador] == self.palabrasnegativasT[j]:
                        negativo += 1
            contador += 1

        #AGREGANDO AL TOTAL DE MENSAJES
        if positivo == negativo:
            self.retornarMensajeFT(date).neutros += 1
        elif positivo > negativo:
            self.retornarMensajeFT(date).positivos += 1
        elif negativo > positivo:
            self.retornarMensajeFT(date).negativos += 1

        for e in empresasrep:
            self.AgregarEmpresaT(date,e)
            if positivo == negativo:
                if self.retornarEmpresaT(date,e) != None:
                    self.retornarEmpresaT(date,e).neutros += 1
                    self.mensajesneutros = 1
                #print('NEU: ' + str(self.retornarEmpresa(date,e).neutros))
            elif positivo > negativo:
                if self.retornarEmpresaT(date,e) != None:
                    self.retornarEmpresaT(date,e).positivos += 1
                    #print('POS: ' + str(self.retornarEmpresa(date,e).positivos))
            elif negativo > positivo:
                if self.retornarEmpresaT(date,e) != None:
                    self.retornarEmpresaT(date,e).negativos += 1
                    #print('NEG: ' + str(self.retornarEmpresa(date,e).negativos))
        #VUELVE A ANALIZAR EL MENSAJE PARA CORRESPONDER LOS SERVICIOS
        pal = mensaje.split() 
        c = 0
        servicio = ''
        serviciosrep = {}
        while(c < len(pal)):
            pal[c] = pal[c].replace(',', '')
            pal[c] = pal[c].replace('.', '')
            pal[c] = pal[c].replace('!', '')
            pal[c] = pal[c].replace('?', '')
            j = 0
            while(j <len(self.ServiciosT)):
                if len(self.ServiciosT[j].alias) == 0:
                    if pal[c] == self.ServiciosT[j].nombre:
                        servicio = self.ServiciosT[j].nombre
                        #print(servicio)
                        if servicio in serviciosrep:
                            serviciosrep[servicio] +=1
                        else:
                            serviciosrep[servicio] = 1
                else:
                    k = 0
                    while(k <len(self.ServiciosT[j].alias)):
                        if pal[c] == self.ServiciosT[j].nombre or pal[c] == self.ServiciosT[j].alias[k]:
                            servicio = self.ServiciosT[j].nombre
                            #print(servicio)
                            if servicio in serviciosrep:
                                serviciosrep[servicio] +=1
                            else:
                                serviciosrep[servicio] = 1
                        k+=1
                j+=1
            c+=1
        #print(serviciosrep)
        
        #AGREGA LAS ESTADISTICAS DE LOS SERVICIOS EN EL MENSAJE
        for s in serviciosrep:
            for e in empresasrep:
                for i in range(len(self.ServiciosT)):
                    if self.retornarEmpresaT(date,e) != None:
                        if self.retornarEmpresaT(date,e).nombre == self.ServiciosT[i].empresa and s == self.ServiciosT[i].nombre:
                            self.AgregarServicioT(date,e,s)
                            if self.retornarServicioT(e,date,s)!= None:
                                if positivo == negativo:
                                    self.retornarServicioT(e,date,s).neutros += 1
                                elif positivo > negativo:
                                    self.retornarServicioT(e,date,s).positivos +=1
                                elif negativo > positivo:
                                    self.retornarServicioT(e,date,s).negativos += 1
        #print(mensaje)
        self.MostrarXMLT()
    
    def analizarData(self, contenido):
        #print(contenido)
        raiz = ET.XML(contenido)
        empre =''
        for element in raiz:
            if element.tag == "diccionario":
                #print('=====================DICCIONARIO=====================')
                for subelement in element:
                    if subelement.tag == "sentimientos_positivos":
                        #print('=====================POSITIVOS=====================')
                        for subsubelement in subelement:                            
                            palabra =subsubelement.text.strip()
                            palabra = palabra.replace('á','a')
                            palabra = palabra.replace('é','e')
                            palabra = palabra.replace('í','i')
                            palabra = palabra.replace('ó','o')
                            palabra = palabra.replace('ú','u')
                            #print('Palabra: ' + str(palabra))
                            palabra = palabra.lower().lstrip().rstrip()
                            self.palabraspositivas.append(palabra)
                    elif subelement.tag == "sentimientos_negativos":
                        #print('=====================NEGATIVOS=====================')
                        for subsubelement in subelement:
                            palabra =subsubelement.text.lstrip().rstrip()
                            palabra = palabra.replace('á','a')
                            palabra = palabra.replace('é','e')
                            palabra = palabra.replace('í','i')
                            palabra = palabra.replace('ó','o')
                            palabra = palabra.replace('ú','u')
                            #print('Palabra: ' + str(palabra))
                            palabra = palabra.lower()
                            self.palabrasnegativas.append(palabra)
                    elif subelement.tag == "empresas_analizar":
                        #print('=====================EMPRESAS A ANALIZAR=====================')
                        for subsubelement in subelement:
                            if subsubelement.tag == 'empresa':
                                #print('=====================EMPRESA=====================')
                                for empresa in subsubelement:
                                    if empresa.tag == "nombre":
                                        #print('Nombre: ' + str(empresa.text))
                                        nombre = empresa.text.lstrip().rstrip()
                                        empre = nombre
                                        self.Nombres.append(nombre)
                                        empresan = empresa.text.lower().lstrip().rstrip()
                                        empresan = empresan.replace('á','a')
                                        empresan = empresan.replace('é','e')
                                        empresan = empresan.replace('í','i')
                                        empresan = empresan.replace('ó','o')
                                        empresan = empresan.replace('ú','u')
                                        empresan = empresan.replace('\n', ' ')
                                        empresan = empresan.replace('\t', ' ')
                                        self.EmpresasAnalisis.append(empresan)
                                    elif empresa.tag == "servicio":
                                        #print('     =================SERVICIO==================')
                                        #print('Nombre: ' + str(empresa.attrib.get('nombre')))
                                        nombre = empresa.attrib.get('nombre').lstrip().rstrip()
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
                                            #print('Alias: ' + str(alias.text))
                                            nombre2 = alias.text.lstrip().rstrip()
                                            nombre2 = nombre2.lower()
                                            nombre2 = nombre2.replace('á','a')
                                            nombre2 = nombre2.replace('é','e')
                                            nombre2 = nombre2.replace('í','i')
                                            nombre2 = nombre2.replace('ó','o')
                                            nombre2 = nombre2.replace('ú','u')
                                            nombre2 = nombre2.replace('\n', ' ')
                                            nombre2 = nombre2.replace('\t', ' ')
                                            a.append(nombre2)
                                        #print(empre)
                                        nuevo = Serviciotemp(empre,nombre)
                                        nuevo.alias = a 
                                        self.Servicios.append(nuevo)
            elif element.tag == "lista_mensajes":
                #print('=====================LISTA DE MENSAJES=====================')
                for mensaje in element:
                    #print('Mensaje: ')
                    texto = mensaje.text.lstrip().rstrip()
                    self.AnalizarMensaje(texto)
                    #print('____________________________________')

        
        #for i in range(len(self.Servicios)):
            #print(':::::::::::::::::::::::::::::::::::::::::::::::::::::')
            #print('Nombre: ' + str(self.Servicios[i].nombre))
            #print(':::::::::::ALIAS:::::::::::')
            #for j in range(len(self.Servicios[i].alias)):
                #print('Alias: ' + str(self.Servicios[i].alias[j]))

        #self.MostrarporFecha()
        self.MostrarXML()

    def AnalizarMensaje(self, mensaje):
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
        positivo = 0
        negativo = 0
        empresasrep ={}
        for i in range(len(palabras)):
            palabras[i] = palabras[i].replace(' ', '')
            #print(palabras[i])
        while(contador < len(palabras)):
            #VERIFICAR LUGAR Y FECHA
            if palabras[contador] == 'lugar' and palabras[contador+1] == 'y' and palabras[contador+2] == 'fecha:':
                contador += 4
                fecha = re.compile(r"\d\d\/\d\d\/\d\d\d\d")
                if re.match(fecha,palabras[contador]).group() == palabras[contador]:
                    #print('Fecha: '+ str(re.match(fecha,palabras[contador]).group()))
                    date = str(re.match(fecha,palabras[contador]).group())
                    hora = re.compile(r"(([01][0-9]|2[0-3])\:[0-5][0-9])")
                    if re.match(hora,palabras[contador+1]).group() == palabras[contador+1]:
                        #print('Hora:' + str(re.match(hora,palabras[contador+1]).group()))
                        self.AgregarMensajeF(date)
                        contador+=1
            elif palabras[contador] == 'lugar' and palabras[contador+1] == 'y' and palabras[contador+2] == 'fecha' and palabras[contador+3] == ':':
                contador += 5
                fecha = re.compile(r"\d\d\/\d\d\/\d\d\d\d")
                if re.match(fecha,palabras[contador]).group() == palabras[contador]:
                    #print('Fecha: '+ str(re.match(fecha,palabras[contador]).group()))
                    date = str(re.match(fecha,palabras[contador]).group())
                    hora = re.compile(r"(([01][0-9]|2[0-3])\:[0-5][0-9])")
                    if re.match(hora,palabras[contador+1]).group() == palabras[contador+1]:
                        #print('Hora:' + str(re.match(hora,palabras[contador+1]).group()))
                        self.AgregarMensajeF(date)
                        contador+=1

            #VERIFICAR USUARIO
            elif palabras[contador] == 'usuario:':
                contador +=1
                usuario = re.compile("([a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*)|([a-zA-Z0-9.!#$%&'\*\+/=?^_`{|}~-]+)")
                if re.match(usuario,palabras[contador]).group() == palabras[contador]:
                    #print('Usuario: ' + str(re.match(usuario,palabras[contador]).group()))
                    pass
            elif palabras[contador] == 'usuario' and palabras[contador+1] == ':':
                contador +=2
                usuario = re.compile("([a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*)|([a-zA-Z0-9.!#$%&'\*\+/=?^_`{|}~-]+)")
                if re.match(usuario,palabras[contador]).group() == palabras[contador]:
                    #print('Usuario: ' + str(re.match(usuario,palabras[contador]).group()))
                    pass

            #VERIFICAR RED SOCIAL
            elif palabras[contador] == 'red' and palabras[contador+1] == 'social:':
                contador += 2
                redsocial = re.compile("[a-zA-Z0-9.!#$%&'\*\+/=?^_`{|}~-]+")
                if re.match(redsocial,palabras[contador]).group() == palabras[contador]:
                    #print('Red Social: ' + str(re.match(redsocial,palabras[contador]).group()))
                    pass
            elif palabras[contador] == 'red' and palabras[contador+1] == 'social' and palabras[contador+2] == ':':
                contador += 3
                redsocial = re.compile("[a-zA-Z0-9.!#$%&'\*\+/=?^_`{|}~-]+")
                if re.match(redsocial,palabras[contador]).group() == palabras[contador]:
                    #print('Red Social: ' + str(re.match(redsocial,palabras[contador]).group()))
                    pass

            #LEERA EL MENSAJE
            else:
                mensaje += palabras[contador] + ' '
                palabras[contador] = palabras[contador].replace(',', '')
                palabras[contador] = palabras[contador].replace('.', '')
                palabras[contador] = palabras[contador].replace('!', '')
                palabras[contador] = palabras[contador].replace('?', '')
                #LEE LA EMPRESA
                for i in range(len(self.EmpresasAnalisis)):
                    if palabras[contador] == self.EmpresasAnalisis[i]:
                        empresa = self.Nombres[i]
                        if empresa in empresasrep:
                            empresasrep[empresa] +=1
                        else:
                            empresasrep[empresa] = 1
                #LEE LAS PALABRAS POSITIVAS
                for j in range(len(self.palabraspositivas)):
                    if palabras[contador] == self.palabraspositivas[j]:
                        positivo += 1
                #LEE LAS PALABRAS NEGATIVAS
                for j in range(len(self.palabrasnegativas)):
                    if palabras[contador] == self.palabrasnegativas[j]:
                        negativo += 1
            contador += 1

        #AGREGANDO AL TOTAL DE MENSAJES
        if positivo == negativo:
            self.retornarMensajeF(date).neutros += 1
        elif positivo > negativo:
            self.retornarMensajeF(date).positivos += 1
        elif negativo > positivo:
            self.retornarMensajeF(date).negativos += 1

        for e in empresasrep:
            self.AgregarEmpresa(date,e)
            if positivo == negativo:
                if self.retornarEmpresa(date,e) != None:
                    self.retornarEmpresa(date,e).neutros += 1
                    self.mensajesneutros = 1
                #print('NEU: ' + str(self.retornarEmpresa(date,e).neutros))
            elif positivo > negativo:
                if self.retornarEmpresa(date,e) != None:
                    self.retornarEmpresa(date,e).positivos += 1
                    #print('POS: ' + str(self.retornarEmpresa(date,e).positivos))
            elif negativo > positivo:
                if self.retornarEmpresa(date,e) != None:
                    self.retornarEmpresa(date,e).negativos += 1
                    #print('NEG: ' + str(self.retornarEmpresa(date,e).negativos))
        #VUELVE A ANALIZAR EL MENSAJE PARA CORRESPONDER LOS SERVICIOS
        pal = mensaje.split() 
        c = 0
        servicio = ''
        serviciosrep = {}
        while(c < len(pal)):
            pal[c] = pal[c].replace(',', '')
            pal[c] = pal[c].replace('.', '')
            pal[c] = pal[c].replace('!', '')
            pal[c] = pal[c].replace('?', '')
            j = 0
            while(j <len(self.Servicios)):
                if len(self.Servicios[j].alias) == 0:
                    if pal[c] == self.Servicios[j].nombre:
                        servicio = self.Servicios[j].nombre
                        #print(servicio)
                        if servicio in serviciosrep:
                            serviciosrep[servicio] +=1
                        else:
                            serviciosrep[servicio] = 1
                else:
                    k = 0
                    while(k <len(self.Servicios[j].alias)):
                        if pal[c] == self.Servicios[j].nombre or pal[c] == self.Servicios[j].alias[k]:
                            servicio = self.Servicios[j].nombre
                            #print(servicio)
                            if servicio in serviciosrep:
                                serviciosrep[servicio] +=1
                            else:
                                serviciosrep[servicio] = 1
                        k+=1
                j+=1
            c+=1
        #print(serviciosrep)
        
        #AGREGA LAS ESTADISTICAS DE LOS SERVICIOS EN EL MENSAJE
        for s in serviciosrep:
            for e in empresasrep:
                for i in range(len(self.Servicios)):
                    if self.retornarEmpresa(date,e) != None:
                        if self.retornarEmpresa(date,e).nombre == self.Servicios[i].empresa and s == self.Servicios[i].nombre:
                            self.AgregarServicio(date,e,s)
                            if self.retornarServicio(e,date,s)!= None:
                                if positivo == negativo:
                                    self.retornarServicio(e,date,s).neutros += 1
                                elif positivo > negativo:
                                    self.retornarServicio(e,date,s).positivos +=1
                                elif negativo > positivo:
                                    self.retornarServicio(e,date,s).negativos += 1
        #print(mensaje)

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

    def AgregarMensajeF(self, fecha):
        if len(self.MensajesF) == 0:
            self.MensajesF.append(FechaTemp(fecha, 1))
        else:
            if self.VerificarMensajeF(fecha) == True:
                self.retornarMensajeF(fecha).totales += 1
            else:
                self.MensajesF.append(FechaTemp(fecha,1))

    def VerificarMensajeF(self,fecha):
        encontrado = False
        for i in range(len(self.MensajesF)):
            if self.MensajesF[i].fecha == fecha:
                encontrado = True
        return encontrado

    def retornarMensajeF(self,fecha):
        for i in range(len(self.MensajesF)):
            if self.MensajesF[i].fecha == fecha:
                return self.MensajesF[i]


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
            print('FECHA: ' + str(self.Fechas[i]))
            cantidadp = 0
            cantidadn = 0
            cantidadne = 0
            for j in range(len(self.Empresas)):
                if self.Fechas[i] == self.Empresas[j].fecha:
                    cantidadp += self.Empresas[j].positivos
                    cantidadn += self.Empresas[j].negativos
                    cantidadne += self.Empresas[j].neutros
            total = cantidadp + cantidadn + cantidadne
            print('Cantidad total de mensajes recibidos: ' + str(total))
            print('Cantidad total de mensajes positivos: ' + str(cantidadp))
            print('Cantidad total de mensajes negativos: ' + str(cantidadn))
            print('Cantidad total de mensajes neutros: ' + str(cantidadne))
            for j in range(len(self.Empresas)):
                if self.Fechas[i] == self.Empresas[j].fecha:
                    print('     -----------------------------------')
                    print('         Nombre: ' + str(self.Empresas[j].nombre))
                    print('         **********************')
                    print('         Número total de mensajes que mencionan a Empresa: ' + str(self.Empresas[j].cantidad))
                    print('         Mensajes positivos: ' + str(self.Empresas[j].positivos))
                    print('         Mensajes negativos: ' + str(self.Empresas[j].negativos))
                    print('         Mensajes neutros: ' + str(self.Empresas[j].neutros))
                    for k in range(len(self.Empresas[j].servicios)):
                        if self.Fechas[i] == self.Empresas[j].servicios[k].fecha:
                            print('             _________________________________')
                            print('                 Nombre: ' + str(self.Empresas[j].servicios[k].nombre))
                            print('                 -_-_-_-_-_-_-_-_-_-_-_-_-_')
                            print('                 Número total de mensajes que mencionan al servicio: ' + str(self.Empresas[j].servicios[k].cantidad))
                            print('                 Mensajes positivos: ' + str(self.Empresas[j].servicios[k].positivos))
                            print('                 Mensajes negativos: ' + str(self.Empresas[j].servicios[k].negativos))
                            print('                 Mensajes neutros: ' + str(self.Empresas[j].servicios[k].neutros))
            print('$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')

    def MostrarXML(self):
        texto = ''
        texto += '''<?xml version="1.0"?> 
<lista_respuestas>'''
        for i in range(len(self.MensajesF)):
            texto+='''
    <respuesta>
        <fecha>''' + str(self.MensajesF[i].fecha) + '''</fecha>
            <mensajes> 
                <total> '''+str(self.MensajesF[i].totales)+''' </total> 
                <positivos> '''+str(self.MensajesF[i].positivos)+''' </positivos> 
                <negativos> '''+str(self.MensajesF[i].negativos)+''' </negativos> 
                <neutros> '''+str(self.MensajesF[i].neutros)+''' </neutros> 
            </mensajes> 
        <analisis>'''
            for j in range(len(self.Empresas)):
                if self.MensajesF[i].fecha == self.Empresas[j].fecha:
                    texto+='''
            <empresa nombre=\"'''+str(self.Empresas[j].nombre)+'''\">
                <mensajes> 
                    <total> '''+str(self.Empresas[j].cantidad)+''' </total> 
                    <positivos> '''+str(self.Empresas[j].positivos)+''' </positivos> 
                    <negativos> '''+str(self.Empresas[j].negativos)+''' </negativos> 
                    <neutros> '''+str(self.Empresas[j].neutros)+''' </neutros> 
                </mensajes>
                    <servicios>'''
                    for k in range(len(self.Empresas[j].servicios)):
                        if self.MensajesF[i].fecha == self.Empresas[j].servicios[k].fecha:
                            texto += '''
                        <servicio nombre=\"''' +str(self.Empresas[j].servicios[k].nombre)+ '''\"> 
                            <mensajes> 
                                <total> '''+str(self.Empresas[j].servicios[k].cantidad)+''' </total> 
                                <positivos> '''+str(self.Empresas[j].servicios[k].positivos)+''' </positivos> 
                                <negativos> '''+str(self.Empresas[j].servicios[k].negativos)+''' </negativos> 
                                <neutros> '''+str(self.Empresas[j].servicios[k].neutros)+''' </neutros> 
                            </mensajes> 
                        </servicio>'''
                    texto +='''
                    </servicios>
            </empresa>'''
            texto +='''
        </analisis>
    </respuesta>'''
        texto +='''
</lista_respuestas>'''

        #print(texto)
        self.crearArchivo(texto)

    def crearArchivo(self, texto):
        archivo=open("Database\Respuestas.xml", 'w', encoding='utf8')
        archivo.write(texto)
        archivo.close()

    def mostrarServicios(self):
        print('/////////////////////////////////////////////////')
        for i in range(len(self.Empresas)):
            print(';;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;')
            print('Empresa: ' + self.Empresas[i].nombre)
            print('-------------------SERVICIOS--------------')
            for j in range(len(self.Empresas[i].servicios)):
                print('Fecha: ' + str(self.Empresas[i].servicios[j].fecha))
                print('Nombre: ' + str(self.Empresas[i].servicios[j].nombre))
                print('Cantidad: ' + str(self.Empresas[i].servicios[j].cantidad))
                print('Positivos: ' + str(self.Empresas[i].servicios[j].positivos))
                print('Negativos: ' + str(self.Empresas[i].servicios[j].negativos))
                print('Neutros: ' + str(self.Empresas[i].servicios[j].neutros))

    def AnalizarMensajePrueba(self, contenido):
        raiz = ET.XML(contenido)
        #print(raiz.text)
        #print('----------------------------')
        #print(raiz.tag)
        message = raiz.text.lstrip().rstrip().lower()
        message = message.replace('á','a')
        message = message.replace('é','e')
        message = message.replace('í','i')
        message = message.replace('ó','o')
        message = message.replace('ú','u')
        message = message.replace('\n', ' ')
        message = message.replace('\t', ' ')
        palabras = message.split()
        #print(palabras)
        contador = 0
        date = ''
        red = ''
        user = ''
        empresasrep = {}
        positivo = 0
        negativo = 0
        empresas = []
        serviciosrep = {}
        while(contador < len(palabras)):
            #VERIFICAR LUGAR Y FECHA
            if palabras[contador] == 'lugar' and palabras[contador+1] == 'y' and palabras[contador+2] == 'fecha:':
                contador += 4
                fecha = re.compile(r"\d\d\/\d\d\/\d\d\d\d")
                if re.match(fecha,palabras[contador]).group() == palabras[contador]:
                    #print('Fecha: '+ str(re.match(fecha,palabras[contador]).group()))
                    date = str(re.match(fecha,palabras[contador]).group())
                    hora = re.compile(r"(([01][0-9]|2[0-3])\:[0-5][0-9])")
                    if re.match(hora,palabras[contador+1]).group() == palabras[contador+1]:
                        #print('Hora:' + str(re.match(hora,palabras[contador+1]).group()))
                        hour = str(re.match(hora,palabras[contador+1]).group())
                        contador+=1
            elif palabras[contador] == 'lugar' and palabras[contador+1] == 'y' and palabras[contador+2] == 'fecha' and palabras[contador+3] == ':':
                contador += 5
                fecha = re.compile(r"\d\d\/\d\d\/\d\d\d\d")
                if re.match(fecha,palabras[contador]).group() == palabras[contador]:
                    #print('Fecha: '+ str(re.match(fecha,palabras[contador]).group()))
                    date = str(re.match(fecha,palabras[contador]).group())
                    hora = re.compile(r"(([01][0-9]|2[0-3])\:[0-5][0-9])")
                    if re.match(hora,palabras[contador+1]).group() == palabras[contador+1]:
                        #print('Hora:' + str(re.match(hora,palabras[contador+1]).group()))
                        hour = str(re.match(hora,palabras[contador+1]).group())
                        contador+=1

            #VERIFICAR USUARIO
            elif palabras[contador] == 'usuario:':
                contador +=1
                usuario = re.compile("([a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*)|([a-zA-Z0-9.!#$%&'\*\+/=?^_`{|}~-]+)")
                if re.match(usuario,palabras[contador]).group() == palabras[contador]:
                    #print('Usuario: ' + str(re.match(usuario,palabras[contador]).group()))
                    user = str(re.match(usuario,palabras[contador]).group())
            elif palabras[contador] == 'usuario' and palabras[contador+1] == ':':
                contador +=2
                usuario = re.compile("([a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*)|([a-zA-Z0-9.!#$%&'\*\+/=?^_`{|}~-]+)")
                if re.match(usuario,palabras[contador]).group() == palabras[contador]:
                    #print('Usuario: ' + str(re.match(usuario,palabras[contador]).group()))
                    user = str(re.match(usuario,palabras[contador]).group())
            #VERIFICAR RED SOCIAL
            elif palabras[contador] == 'red' and palabras[contador+1] == 'social:':
                contador += 2
                redsocial = re.compile("[a-zA-Z0-9.!#$%&'\*\+/=?^_`{|}~-]+")
                if re.match(redsocial,palabras[contador]).group() == palabras[contador]:
                    #print('Red Social: ' + str(re.match(redsocial,palabras[contador]).group()))
                    red = str(re.match(redsocial,palabras[contador]).group())
            elif palabras[contador] == 'red' and palabras[contador+1] == 'social' and palabras[contador+2] == ':':
                contador += 3
                redsocial = re.compile("[a-zA-Z0-9.!#$%&'\*\+/=?^_`{|}~-]+")
                if re.match(redsocial,palabras[contador]).group() == palabras[contador]:
                    #print('Red Social: ' + str(re.match(redsocial,palabras[contador]).group()))
                    red = str(re.match(redsocial,palabras[contador]).group())

            #LEERA EL MENSAJE
            else:
                message += palabras[contador] + ' '
                palabras[contador] = palabras[contador].replace(',', '')
                palabras[contador] = palabras[contador].replace('.', '')
                palabras[contador] = palabras[contador].replace('!', '')
                palabras[contador] = palabras[contador].replace('?', '')
                #LEE LA EMPRESA
                for i in range(len(self.EmpresasAnalisis)):
                    if palabras[contador] == self.EmpresasAnalisis[i]:
                        empresa = self.Nombres[i]
                        if empresa in empresasrep:
                            empresasrep[empresa] +=1
                        else:
                            empresasrep[empresa] = 1
                #LEE LAS PALABRAS POSITIVAS
                for j in range(len(self.palabraspositivas)):
                    if palabras[contador] == self.palabraspositivas[j]:
                        positivo += 1
                #LEE LAS PALABRAS NEGATIVAS
                for j in range(len(self.palabrasnegativas)):
                    if palabras[contador] == self.palabrasnegativas[j]:
                        negativo += 1
            contador += 1

        for e in empresasrep:
            nuevo = Empresa(date,e,1)
            nuevo.positivos += positivo
            nuevo.negativos += negativo
            empresas.append(nuevo)
        
        #VUELVE A ANALIZAR EL MENSAJE PARA CORRESPONDER LOS SERVICIOS
        pal = message.split() 
        c = 0
        servicio = ''
        serviciosrep = {}
        while(c < len(pal)):
            pal[c] = pal[c].replace(',', '')
            pal[c] = pal[c].replace('.', '')
            pal[c] = pal[c].replace('!', '')
            pal[c] = pal[c].replace('?', '')
            j = 0
            while(j <len(self.Servicios)):
                if len(self.Servicios[j].alias) == 0:
                    if pal[c] == self.Servicios[j].nombre:
                        servicio = self.Servicios[j].nombre
                        #print(servicio)
                        if servicio in serviciosrep:
                            serviciosrep[servicio] +=1
                        else:
                            serviciosrep[servicio] = 1
                else:
                    k = 0
                    while(k <len(self.Servicios[j].alias)):
                        if pal[c] == self.Servicios[j].nombre or pal[c] == self.Servicios[j].alias[k]:
                            servicio = self.Servicios[j].nombre
                            #print(servicio)
                            if servicio in serviciosrep:
                                serviciosrep[servicio] +=1
                            else:
                                serviciosrep[servicio] = 1
                        k+=1
                j+=1
            c+=1
        #print(serviciosrep)
        
        #AGREGA LAS ESTADISTICAS DE LOS SERVICIOS EN EL MENSAJE
        for s in serviciosrep:
            for e in empresas:
                for i in range(len(self.Servicios)):
                    if e != None:
                        if e.nombre == self.Servicios[i].empresa and s == self.Servicios[i].nombre:
                            new = Servicio(s,date,1)
                            e.servicios.append(new)
        #print(message)
        self.MostrarXMLRespuesta(date,red,user,empresas)

    def MostrarXMLRespuesta(self,fecha,red,usuario,empresas):
        texto = ''
        texto += '''<respuesta>
    <fecha> '''+ str(fecha) + ''' </fecha>
    <red_social> ''' +str(red.capitalize()) + ''' </red_social>
    <usuario> ''' + str(usuario) + ''' </usuario>
    <empresas>'''
        for i in range(len(empresas)):
            texto+='''
        <empresa nombre=\"''' + str(empresas[i].nombre) + '''\">'''
            for j in range(len(empresas[i].servicios)):
                texto+='''
            <servicio> ''' + str(empresas[i].servicios[j].nombre) + '''</servicio>'''
            texto+='''
        </empresa>'''
        texto+='''
    </empresas>'''
        positivos = 0
        negativos = 0
        for i in range(len(empresas)):
            positivos += empresas[i].positivos
            negativos += empresas[i].negativos
        total = positivos + negativos
        try:
            porcentajepos = (positivos/total)*100
            porcentajepos = int(porcentajepos)
        except:
            porcentajepos = 0
        try:
            porcentajeneg = (negativos/total)*100
            porcentajeneg = int(porcentajeneg)
        except:
            porcentajeneg = 0
        texto +='''
    <palabras_positivas> ''' + str(positivos) + '''</palabras_positivas>
    <palabras_negativas>''' + str(negativos) + '''</palabras_negativas>
    <sentimiento_positivo> ''' + str(porcentajepos) + '''% </sentimiento_positivo>
    <sentimiento_negativo> ''' + str(porcentajeneg) + '''% </sentimiento_negativo>'''
        if positivos ==  negativos:
            texto+='''
    <sentimiento_analizado> neutro </sentimiento_analizado>'''
        elif positivos > negativos:
            texto+='''
    <sentimiento_analizado> positivo </sentimiento_analizado>'''
        elif positivos < negativos:
            texto+='''
    <sentimiento_analizado> negativo </sentimiento_analizado>'''
        texto += '''
</respuesta>'''
        self.crearArchivoRespuesta(texto)

    def crearArchivoRespuesta(self, texto):
        archivo=open("Database\Respuesta.xml", 'w', encoding='utf8')
        archivo.write(texto)
        archivo.close()

    def AgregarEmpresaT(self,fecha, empresa):
        if len(self.EmpresasT) == 0:
            self.EmpresasT.append(Empresa(fecha,empresa,1))
        else:
            if self.VerificarEmpresaT(fecha,empresa) == True:
                self.retornarEmpresaT(fecha,empresa).cantidad += 1
            else:
                self.EmpresasT.append(Empresa(fecha,empresa,1))

    def VerificarEmpresaT(self,fecha, empresa):
        encontrado = False
        for i in range(len(self.EmpresasT)):
            if empresa == self.EmpresasT[i].nombre and fecha == self.EmpresasT[i].fecha:
                encontrado = True
        return encontrado

    def retornarEmpresaT(self,fecha,empresa):
        for i in range(len(self.EmpresasT)):
            if empresa == self.EmpresasT[i].nombre and fecha == self.EmpresasT[i].fecha:
                return self.EmpresasT[i]

    def AgregarServicioT(self,fecha,empresa, servicio):
        nuevo = Servicio(servicio,fecha,1)
        for i in range(len(self.EmpresasT)):
            if self.EmpresasT[i].nombre == empresa:
                if len(self.EmpresasT[i].servicios) == 0:
                    self.EmpresasT[i].servicios.append(nuevo)
                else:
                    if self.VerificarServicioT(empresa,fecha,servicio) == True:
                        self.retornarServicioT(empresa,fecha,servicio).cantidad += 1
                    else:
                        self.EmpresasT[i].servicios.append(nuevo)

    def VerificarServicioT(self,empresa,fecha, servicio):
        encontrado = False
        for i in range(len(self.EmpresasT)):
            if self.EmpresasT[i].nombre == empresa:
                for j in range(len(self.EmpresasT[i].servicios)):
                    if self.EmpresasT[i].servicios[j].fecha == fecha and self.EmpresasT[i].servicios[j].nombre == servicio:
                        encontrado = True
        return encontrado

    def retornarServicioT(self,empresa,fecha,servicio):
        for i in range(len(self.EmpresasT)):
            if self.EmpresasT[i].nombre == empresa:
                for j in range(len(self.EmpresasT[i].servicios)):
                    if self.EmpresasT[i].servicios[j].fecha == fecha and self.EmpresasT[i].servicios[j].nombre == servicio:
                        return self.EmpresasT[i].servicios[j]

    def AgregarMensajeFT(self, fecha):
        if len(self.MensajesFT) == 0:
            self.MensajesFT.append(FechaTemp(fecha, 1))
        else:
            if self.VerificarMensajeFT(fecha) == True:
                self.retornarMensajeFT(fecha).totales += 1
            else:
                self.MensajesFT.append(FechaTemp(fecha,1))

    def VerificarMensajeFT(self,fecha):
        encontrado = False
        for i in range(len(self.MensajesFT)):
            if self.MensajesFT[i].fecha == fecha:
                encontrado = True
        return encontrado

    def retornarMensajeFT(self,fecha):
        for i in range(len(self.MensajesFT)):
            if self.MensajesFT[i].fecha == fecha:
                return self.MensajesFT[i]

    def MostrarXMLT(self):
        texto = ''
        texto += '''<?xml version="1.0"?> 
<lista_respuestas>'''
        for i in range(len(self.MensajesFT)):
            texto+='''
    <respuesta>
        <fecha>''' + str(self.MensajesFT[i].fecha) + '''</fecha>
            <mensajes> 
                <total> '''+str(self.MensajesFT[i].totales)+''' </total> 
                <positivos> '''+str(self.MensajesFT[i].positivos)+''' </positivos> 
                <negativos> '''+str(self.MensajesFT[i].negativos)+''' </negativos> 
                <neutros> '''+str(self.MensajesFT[i].neutros)+''' </neutros> 
            </mensajes> 
        <analisis>'''
            for j in range(len(self.EmpresasT)):
                if self.MensajesFT[i].fecha == self.EmpresasT[j].fecha:
                    texto+='''
            <empresa nombre=\"'''+str(self.EmpresasT[j].nombre)+'''\">
                <mensajes> 
                    <total> '''+str(self.EmpresasT[j].cantidad)+''' </total> 
                    <positivos> '''+str(self.EmpresasT[j].positivos)+''' </positivos> 
                    <negativos> '''+str(self.EmpresasT[j].negativos)+''' </negativos> 
                    <neutros> '''+str(self.EmpresasT[j].neutros)+''' </neutros> 
                </mensajes>
                    <servicios>'''
                    for k in range(len(self.EmpresasT[j].servicios)):
                        if self.MensajesFT[i].fecha == self.EmpresasT[j].servicios[k].fecha:
                            texto += '''
                        <servicio nombre=\"''' +str(self.EmpresasT[j].servicios[k].nombre)+ '''\"> 
                            <mensajes> 
                                <total> '''+str(self.EmpresasT[j].servicios[k].cantidad)+''' </total> 
                                <positivos> '''+str(self.EmpresasT[j].servicios[k].positivos)+''' </positivos> 
                                <negativos> '''+str(self.EmpresasT[j].servicios[k].negativos)+''' </negativos> 
                                <neutros> '''+str(self.EmpresasT[j].servicios[k].neutros)+''' </neutros> 
                            </mensajes> 
                        </servicio>'''
                    texto +='''
                    </servicios>
            </empresa>'''
            texto +='''
        </analisis>
    </respuesta>'''
        texto +='''
</lista_respuestas>'''

        #print(texto)
        self.crearArchivoT(texto)

    def crearArchivoT(self, texto):
        archivo=open("Database\RespuestaSalida.xml", 'w', encoding='utf8')
        archivo.write(texto)
        archivo.close()