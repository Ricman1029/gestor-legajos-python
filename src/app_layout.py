import flet
from src.views.routes import router
from src.controles.sidebar import Sidebar
from src.state import State
from src.utils.persistencia import (obtener_lista_empresas,
                                                        leer_convenios,
                                                        leer_sindicatos,
                                                        leer_obras_sociales,
                                                        leer_opciones_pdfs)


class AppLayout(flet.Row):
    def __init__(
            self,
            page: flet.Page,
            *args,
            **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.page = page

        self.sidebar = Sidebar()
        self.sidebar.inicializar()
        self.actualizar_estado_global()

        self.page.on_route_change = router.route_change

        self.controls = [
            self.sidebar,
            router.body,
        ]

    def actualizar_estado_global(self):
        # Lista de empresas
        State(key="empresas", value=obtener_lista_empresas())
        # Empresa seleccionada
        State(key="empresa_seleccionada", value=None)
        # Lista convenios
        State(key="convenios", value=leer_convenios())
        # Lista sindicatos
        State(key="sindicatos", value=leer_sindicatos())
        # Lista obras sociales
        State(key="obras_sociales", value=leer_obras_sociales())
        # Diccionario opcoines pdfs
        State(key="opciones_pdfs", value=leer_opciones_pdfs())
