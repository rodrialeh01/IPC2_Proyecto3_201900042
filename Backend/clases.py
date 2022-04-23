class Empresa():
    def __init__(self, fecha,nombre, cantidad):
        self.fecha = fecha
        self.nombre = nombre
        self.cantidad = cantidad
        self.positivos = 0
        self.negativos = 0
        self.neutros = 0
        self.servicios = []

class Servicio():
    def __init__(self, nombre,fecha, cantidad):
        self.nombre = nombre
        self.fecha = fecha
        self.cantidad = cantidad
        self.positivos = 0
        self.negativos = 0
        self.neutros = 0
