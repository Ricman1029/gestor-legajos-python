import re
import datetime
import locale
from src.entidades.persona import Persona

# Para que las fechas se escriban siempre en español
locale.setlocale(locale.LC_TIME, "es_ES.UTF-8")


class Empleado:
    def __init__(self,
                 numero_legajo: str,
                 persona: Persona,
                 fecha_ingreso: str,
                 antiguedad: str,
                 sueldo: str,
                 categoria: str,
                 ):
        self.numero_legajo = numero_legajo
        self.persona = persona
        self.fecha_ingreso = fecha_ingreso
        self.antiguedad = antiguedad
        self.sueldo = sueldo
        self.categoria = categoria
        self.activo = True

    def escribir_fecha_ingreso(self):
        numeros = re.findall(r"\d+", self.fecha_ingreso)
        numeros = list(map(int, numeros))
        fecha = datetime.datetime(numeros[2], numeros[1], numeros[0])

        fecha_texto = fecha.strftime("%d de %B de %Y")
        return str(fecha_texto)

    def dia_ingreso(self):
        return self.fecha_ingreso[0:2]

    def mes_ingreso(self):
        return self.fecha_ingreso[3:5]

    def año_ingreso(self):
        return self.fecha_ingreso[6:10]

    def dar_baja(self):
        self.activo = False

    def dar_alta(self):
        self.activo = True

    def editar_empleado(self, empleado):
        self.numero_legajo = empleado.numero_legajo
        self.persona = empleado.persona
        self.fecha_ingreso = empleado.fecha_ingreso
        self.antiguedad = empleado.antiguedad
        self.sueldo = empleado.sueldo
        self.categoria = empleado.categoria
