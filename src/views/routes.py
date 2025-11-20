from src.views.router import Router
from src.views.empresas_view import EmpresasView
from src.views.lista_empleados_view import ListaEmpleadosView
from src.views.agregar_empleado_view import AgregarEmpleadoView
from src.views.otros_view import OtrosView

router = Router()

router.routes = {
    "/empresas": EmpresasView,
    "/lista_empleados": ListaEmpleadosView,
    "/agregar_empleados": AgregarEmpleadoView,
    "/otros": OtrosView,
}
