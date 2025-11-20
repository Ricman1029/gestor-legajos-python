from src.entidades.domicilio import Domicilio
from src.entidades.empleado import Empleado
from src.utils.helpers import agregar_en_orden


class Empresa:
    def __init__(
            self,
            siglas,
            nombre_empresa,
            cuit_empresa,
            numero_ieric,
            nombre_dueño,
            apellido_dueño,
            dni_dueño,
            sindicato,
            telefono,
            correo_electronico,
            domicilio: Domicilio,
            convenio
    ):
        self.siglas = siglas
        self.nombre_empresa = nombre_empresa.upper()
        self.cuit_empresa = cuit_empresa
        self.numero_ieric = numero_ieric
        self.nombre_dueño = nombre_dueño
        self.apellido_dueño = apellido_dueño
        self.dni_dueño = dni_dueño
        self.convenio = convenio
        self.sindicato = sindicato
        self.telefono = telefono
        self.correo_electronico = correo_electronico
        self.domicilio = domicilio
        self.convenio = convenio
        self.empleados = []
        self.empleados_activos = 0
        self.activa = True
        self.opciones_pdfs = [None, None, None, None, None]

    def agregar_empleado(self, empleado: Empleado):
        agregar_en_orden(
            lista=self.empleados,
            valor=int(empleado.numero_legajo),
            objeto=empleado,
            ordenar_por=lambda medio: int(self.empleados[medio].numero_legajo)
        )
        self.empleados_activos += 1

    def total_empleados(self):
        return len(self.empleados)

    def dar_alta(self):
        self.activa = True

    def dar_de_baja(self):
        for empleado in self.empleados:
            empleado.dar_baja()
            self.empleados_activos = 0 if self.empleados_activos - 1 < 0 else self.empleados_activos - 1
        self.activa = False

    def buscar_empleado(self, cuil):
        for empleado in self.empleados:
            if empleado.persona.cuil == cuil:
                return empleado

    def debe_elegir_opciones_pdfs(self):
        return any(opcion is None for opcion in self.opciones_pdfs)

    def elegir_opciones_pdfs(self, opciones: list):
        self.opciones_pdfs = opciones
