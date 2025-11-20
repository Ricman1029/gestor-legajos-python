from src.entidades.domicilio import Domicilio


class Persona:
    def __init__(self,
                 nombre: str,
                 apellido: str,
                 fecha_nacimiento: str,
                 nacionalidad: str,
                 cuil: str,
                 domicilio: Domicilio,
                 obra_social: str,
                 sexo="Masculino",
                 estado_civil="Soltero",
                 telefono="",
                 correo_electronico=""):
        self.nombre = nombre
        self.apellido = apellido
        self.fecha_nacimiento = fecha_nacimiento
        self.nacionalidad = nacionalidad
        self.cuil = cuil
        self.sexo = sexo
        self.estado_civil = estado_civil
        self.domicilio = domicilio
        self.obra_social = obra_social
        self.telefono = telefono
        self.correo_electronico = correo_electronico

    def dni(self):
        return self.cuil[3:11]

    def dia_nacimiento(self):
        return self.fecha_nacimiento[0:2]

    def mes_nacimiento(self):
        return self.fecha_nacimiento[3:5]

    def año_nacimiento(self):
        return self.fecha_nacimiento[6:10]
