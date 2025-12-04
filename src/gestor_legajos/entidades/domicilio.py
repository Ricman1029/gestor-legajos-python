class Domicilio:
    def __init__(self,
                 calle: str,
                 numero: str,
                 piso="",
                 departamento="",
                 codigo_postal="8400",
                 localidad="Bariloche",
                 provincia="Río Negro"):
        self.calle = calle
        self.numero = numero
        self.piso = piso
        self.departamento = departamento
        self.codigo_postal = codigo_postal
        self.localidad = localidad
        self.provincia = provincia

    def direccion(self):
        if self.calle.strip() == "":
            return "."*40
        if self.piso != "" and self.departamento != "":
            return f"{self.calle} {self.numero} - Piso {self.piso} Depto. {self.departamento}"
        return f"{self.calle} {self.numero}"
