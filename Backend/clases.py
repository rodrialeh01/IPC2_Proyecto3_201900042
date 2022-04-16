class Empresa():
    def __init__(self, fecha,nombre, mensajes, servicios):
        self.fecha = fecha
        self.nombre = nombre
        self.mensajes = mensajes
        self.servicios = servicios

class Mensaje():
    def __init__(self, total, positivos, negativos, neutros):
        self.total = total
        self.positivos = positivos
        self.negativos = negativos
        self.neutros = neutros

class Servicio():
    def __init__(self, nombre, mensajes):
        self.nombre = nombre
        self.mensajes = mensajes