class Empresa():
    def __init__(self, fecha,nombre, cantidad):
        self.fecha = fecha
        self.nombre = nombre
        self.cantidad = cantidad
        self.mensajes = []
        self.servicios = []

class Mensaje():
    def __init__(self, total, positivos, negativos, neutros):
        self.total = total
        self.positivos = positivos
        self.negativos = negativos
        self.neutros = neutros

class Servicio():
    def __init__(self, nombre):
        self.nombre = nombre
        self.alias = []
        self.mensajes = []
