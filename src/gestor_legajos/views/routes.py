from gestor_legajos.views.router import Router
from gestor_legajos.views.empresas_view import EmpresasView
from gestor_legajos.views.lista_empleados_view import ListaEmpleadosView
from gestor_legajos.views.agregar_empleado_view import AgregarEmpleadoView
from gestor_legajos.views.otros_view import OtrosView

router = Router()

router.routes = {
    "/empresas": EmpresasView,
    "/lista_empleados": ListaEmpleadosView,
    "/agregar_empleados": AgregarEmpleadoView,
    "/otros": OtrosView,
}
