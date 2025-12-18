import datetime
from babel.dates import format_date
from sqlalchemy.ext.asyncio import AsyncSession
from src.data.models.empleado_model import Empleado
from src.data.models.empresa_model import Empresa
from src.data.repositories.empresa_repository import EmpresaRepository
from src.data.repositories.empleado_repository import EmpleadoRepository
from src.domain.services import PdfService

class GestorLegajosService:
    def __init__(self, session:AsyncSession):
        self.session = session
        self.pdf_service = PdfService()
        self.empresa_repositorio = EmpresaRepository(session)
        self.empleado_repositorio = EmpleadoRepository(session)

    async def generar_contrato_empleado(self, empleado_id: int) -> str | None:
        print("Generando contrato generar_contrato_empleado")
        rutas_generadas = []

        empleado = await self.empleado_repositorio.get_para_edicion(empleado_id)
        if not empleado: raise ValueError(f"Empleado no encontrado")

        empresa = await self.empresa_repositorio.get_para_edicion(empleado.empresa_id)
        if not empresa: raise ValueError("Empresa no encontrada")

        datos_typst = self._preparar_datos_typst(empleado, empresa)
        nombre_pdf = f"typst"
        ruta_typst = self.pdf_service.generar_contrato(datos_typst, nombre_pdf)
        if ruta_typst: rutas_generadas.append(ruta_typst)

        nombre_art = empresa.art_rel.nombre.lower().replace(" ", "_")
        formularios_a_llenar = [
                "formulario_anses.pdf",
                f"formulario_{nombre_art}.pdf",
                ]
        datos_formularios = self._preparar_datos_formularios(empleado, empresa)
        for formulario in formularios_a_llenar:
            ruta_formulario = self.pdf_service.rellenar_formulario(datos_formularios, formulario)
            if ruta_formulario: rutas_generadas.append(ruta_formulario)

        nombre_completo = empleado.apellido + "_" + empleado.nombre.replace(".", "").replace(" ", "_")
        ruta_contrato = self.pdf_service._unir_pdfs(rutas_generadas, nombre_completo)

        return ruta_contrato

    def _preparar_datos_typst(self, empleado, empresa) -> dict:
        """
        Convierte los objetos de DB en un diccionario listo para documentos.
        """
        return {
                "empresa": {
                    "razon_social": empresa.razon_social,
                    "cuit": empresa.cuit,
                    "convenio": empleado.categoria_rel.convenio.nombre,
                    "contacto": {
                        "telefono": empresa.telefono,
                        "mail": empresa.mail
                        },
                    "direccion": {
                        "calle": empresa.calle,
                        "numero": empresa.numero,
                        "piso": empresa.piso,
                        "depto": empresa.depto,
                        "codigo_postal": empresa.codigo_postal,
                        "localidad": empresa.localidad,
                        "provincia": empresa.provincia
                        },
                    "art": {
                        "nombre": empresa.art_rel.nombre,
                        "telefono_emergencias": empresa.art_rel.telefono
                        },
                    "display": {
                        "direccion_completa": self.formatear_direccion_completa(empresa.calle, empresa.numero, empresa.piso, empresa.depto),
                        "cuit": self.formatear_cuit_cuil(empresa.cuit)
                        }
                    },
                "empleado": {
                    "legajo": empleado.numero_legajo,

                    "identificacion": {
                        "nombre": empleado.nombre,
                        "apellido": empleado.apellido,
                        "dni": empleado.dni,
                        "cuil": empleado.cuil,
                        "fecha_nacimiento": self.formatear_fecha(empleado.fecha_nacimiento),
                        "sexo": empleado.sexo
                        },
                    "direccion": {
                        "calle": empleado.calle,
                        "numero": empleado.numero,
                        "piso": empleado.piso,
                        "depto": empleado.depto,
                        "codigo_postal": empleado.codigo_postal,
                        "localidad": empleado.localidad,
                        "provincia": empleado.provincia
                        },
                    "contacto": {
                        "telefono": empleado.telefono,
                        "mail": empleado.mail
                        },
                    "laborales": {
                        "fecha_ingreso": self.formatear_fecha(empleado.fecha_ingreso),
                        "obra_social": empleado.obra_social_rel.nombre,
                        "sindicato": empleado.categoria_rel.convenio.sindicato_rel.nombre,
                        "categoria": empleado.categoria_rel.nombre,
                        "sueldo_neto": empleado.sueldo
                        },
                    "display": {
                        "nombre_completo": self.formatear_dos_campos(empleado.apellido, empleado.nombre),
                        "dni": self.formatear_dni(empleado.dni),
                        "cuil": self.formatear_cuit_cuil(empleado.cuil),
                        "string_sueldo": self.formatear_moneda(empleado.sueldo),
                        "direccion_completa": self.formatear_direccion_completa(empleado.calle, empleado.numero, empleado.piso, empleado.depto)
                        }
                    }
                }

    def _preparar_datos_formularios(self, empleado: Empleado, empresa: Empresa):
        return {
                # --- Documento ---
                "documento_año": empleado.fecha_ingreso.year,
                "documento_mes": format_date(empleado.fecha_ingreso, "MMMM", locale="es"),
                "documento_dia": empleado.fecha_ingreso.day,
                "documento_lugar": empresa.localidad,
                "documento_lugar_y_fecha": self.formatear_dos_campos(empresa.localidad, self.formatear_fecha(empleado.fecha_ingreso)),

                # --- Empleado ---
                # Personales
                "empleado_nombre_completo": self.formatear_dos_campos(empleado.apellido, empleado.nombre),
                "empleado_cuil": self.formatear_cuit_cuil(empleado.cuil),
                "empleado_dni_tipo": "DU",
                "empleado_dni_numero": self.formatear_dni(empleado.dni),
                "empleado_estado_civil": "",
                "empleado_nacionalidad": empleado.nacionalidad,
                "empleado_sexo": empleado.sexo,
                "empleado_tipo_y_dni": "DU " + self.formatear_dni(empleado.dni),

                # Fechas Personales
                "empleado_fecha_nacimiento": self.formatear_fecha(empleado.fecha_nacimiento),
                "empleado_dia_nacimiento": empleado.fecha_nacimiento.day,
                "empleado_mes_nacimiento": empleado.fecha_nacimiento.month,
                "empleado_año_nacimiento": empleado.fecha_nacimiento.year,

                # Fechas laborales
                "empleado_fecha_ingreso": self.formatear_fecha(empleado.fecha_ingreso),
                "empleado_dia_ingreso": empleado.fecha_ingreso.day,
                "empleado_mes_ingreso": empleado.fecha_ingreso.month,
                "empleado_año_ingreso": empleado.fecha_ingreso.year,

                # Domicilio Empleado
                "empleado_calle": empleado.calle,
                "empleado_numero": empleado.numero,
                "empleado_piso": empleado.piso,
                "empleado_depto": empleado.depto,
                "empleado_localidad": empleado.localidad,
                "empleado_provincia": empleado.provincia,
                "empleado_codigo_postal": empleado.codigo_postal,
                "empleado_calle_numero": self.formatear_dos_campos(empleado.calle, empleado.numero),
                "empleado_piso_depto": self.formatear_dos_campos(empleado.piso if empleado.piso else "", empleado.depto if empleado.depto else ""),
                
                # Laborales
                "empleado_legajo": empleado.numero_legajo,
                "empleado_sueldo": self.formatear_moneda(empleado.sueldo),

                # Contacto
                "empleado_mail": empleado.mail,
                "empleado_telefono": empleado.telefono,
                
                # --- Empresa ---
                "empresa_razon_social": empresa.razon_social,
                "empresa_cuit": empresa.cuit,

                # Domicilio Empresa
                "empresa_calle": empresa.calle,
                "empresa_numero": empresa.numero,
                "empresa_piso": empresa.piso,
                "empresa_depto": empresa.depto,
                "empresa_localidad": empresa.localidad,
                "empresa_provincia": empresa.provincia,
                "empresa_codigo_postal": empresa.codigo_postal,
                "empresa_calle_numero": self.formatear_dos_campos(empresa.calle, empresa.numero),
                "empresa_piso_depto": self.formatear_dos_campos(empresa.piso if empresa.piso else "", empresa.depto if empresa.depto else ""),

                # Contacto
                "empresa_mail": empresa.mail,
                "empresa_telefono": empresa.telefono,

                # --- Otros ---
                "expedido_por": "RENAPER",
                }

    def formatear_fecha(self, fecha: datetime.date):
        return str(fecha.strftime("%d/%m/%Y"))

    def formatear_dos_campos(self, primero: str, segundo: str):
        return f"{primero} {segundo}" 

    def formatear_moneda(self, valor: float):
        return f"$ {valor:,.2f}" if valor else ""

    def formatear_cuit_cuil(self, cuit: str):
        return cuit[0:2] + "-" + cuit[2:10] + "-" + cuit[10] if cuit else ""

    def formatear_dni(self, dni: str):
        if len(dni) == 8:
            return dni[0:2] + "." + dni[2:5] + "." + dni[5:]
        return dni[0] + "." + dni[1:4] + "." + dni[4:]

    def formatear_direccion_completa(self, calle: str, numero: str, piso: str, depto: str):
        return f"{calle} {numero} - Piso {piso}  Depto. {depto}"
