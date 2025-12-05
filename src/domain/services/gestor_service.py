from datetime import date
from sqlalchemy.ext.asyncio import AsyncSession
from src.data.repositories.empresa_repository import EmpresaRepository
from src.data.repositories.empleado_repository import EmpleadoRepository
from src.domain.services.pdf_service import PdfService

class GestorLegajosService:
    def __init__(self, session:AsyncSession):
        self.session = session
        self.empresa_repositorio = EmpresaRepository(session)
        self.empleado_repositorio = EmpleadoRepository(session)

    async def generar_contrato_empleado(self, empleado_id: int) -> str | None:
        # 1. Obtener datos
        empleado = await self.empleado_repositorio.get_by_id(empleado_id)
        if not empleado:
            raise ValueError(f"Empleado {empleado_id} no encontrado")

        empresa = await self.empresa_repositorio.get_by_id(empleado.empresa_id)
        if not empresa:
            raise ValueError("Empresa no encontrada")

        # 2. Aramos un diccionario plano
        # Nota: convertimos todo a strings o tipo simples para el JSON
        datos_contrato = {
                "fecha_actual": date.today().strftime("%d/%m/%Y"),
                "empresa_razon": empresa.razon_social,
                "empresa_cuit": empresa.cuit,
                "empresa_domicilio": f"{empresa.calle} {empresa.numero}, {empresa.localidad}",

                "empleado_nombre": empleado.nombre,
                "empleado_apellido": empleado.apellido,
                "empleado_dni": empleado.dni,
                "empleado_categoria": empleado.categoria,
                "empleado_ingreso": empleado.fecha_ingreso.strftime("%d/%m/%Y"),
                "empleado_sueldo": f"{empleado.sueldo:,.2f}"
                }

        # 3. Llamamos al servicio PDF
        nombre_archivo = f"Legajo_{empleado.apellido}_{empleado.nombre}"
        return PdfService.generar_contrato(datos_contrato, nombre_archivo)
