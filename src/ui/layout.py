import flet as ft
from src.ui.pages import HomePage, EmpresasPage, EmpleadosPage

class MainLayout(ft.Row):
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page
        self.expand = True

        # 1. Instanciamos las páginas UNA SOLA VEZ
        # Esto guarda el estado (si escribimos algo en algún input, no se borra al cambiar de página)
        self.empresas_page = EmpresasPage(on_seleccionar_empresa=self.ir_a_empleados)
        self.empleados_page = EmpleadosPage()

        self.pages = [
                HomePage(),
                self.empresas_page,
                self.empleados_page,
                ]

        # 2. El área de Contenido
        # Empezamos mostrando la HomePage()
        self.content_area = ft.Container(
                content=self.pages[0],
                expand=True,
                padding=20
                )

        # 3. El NavigationRail
        self.rail = ft.NavigationRail(
                selected_index=0,
                label_type=ft.NavigationRailLabelType.ALL,
                min_width=100,
                min_extended_width=200,
                group_alignment=-0.9,
                destinations=[
                    ft.NavigationRailDestination(
                        icon=ft.Icons.HOME_OUTLINED,
                        selected_icon=ft.Icons.HOME,
                        label="Inicio"
                        ),
                    ft.NavigationRailDestination(
                        icon=ft.Icons.BUSINESS_OUTLINED,
                        selected_icon=ft.Icons.BUSINESS,
                        label="Empresas"
                        ),
                    ft.NavigationRailDestination(
                        icon=ft.Icons.PEOPLE_OUTLINE,
                        selected_icon=ft.Icons.PEOPLE,
                        label="Empleados"
                        ),
                    ],
                on_change=self.on_nav_change
                )

        # 4. Agregamos las partes al Layout
        self.controls = [
                self.rail,
                ft.VerticalDivider(width=1),
                self.content_area
                ]

    def on_nav_change(self, e):
        self.cambiar_pagina(e.control.selected_index)

    def cambiar_pagina(self, index):
        self.rail.selected_index = index
        self.content_area.content = self.pages[index]
        self.page.update()

        if index == 2:
            self.page.run_task(self.empleados_page.cargar_datos)

    async def ir_a_empleados(self, empresa):
        self.page.session.set("empresa_seleccionada_id", empresa.id)
        self.page.session.set("empresa_seleccionada_nombre", empresa.razon_social)
        self.cambiar_pagina(2)
