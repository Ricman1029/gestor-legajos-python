import flet as ft
from src.ui.pages import HomePage, EmpresasPage, EmpleadosPage

class MainLayout(ft.Row):
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page
        self.expand = True

        # 1. Instanciamos las páginas UNA SOLA VEZ
        # Esto guarda el estado (si escribimos algo en algún input, no se borra al cambiar de página)
        self.pages = [
                HomePage(),
                EmpresasPage(),
                EmpleadosPage(),
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
        """Manejador de evento: Cambia el contenido según el índice seleccionado"""
        selected_index = e.control.selected_index

        # Cambiamos el contenido del contenedor derecho
        self.content_area.content = self.pages[selected_index]
        self.content_area.update()
