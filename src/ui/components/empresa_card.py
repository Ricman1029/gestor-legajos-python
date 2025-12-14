import flet as ft
from src.data.models.empresa_model import Empresa

class EmpresaCard(ft.Container):
    def __init__(
            self,
            empresa: Empresa,
            on_edit: callable,
            on_delete: callable,
            on_ver_empleados: callable
            ):
        super().__init__()
        self.empresa = empresa
        self.on_edit = on_edit
        self.on_delete = on_delete
        self.on_ver_empleados = on_ver_empleados

        # --- CONFIGURACIÓN VISUAL ---
        self.width = 280
        self.height = 180
        self.border_raius = 15
        self.padding = 15
        self.bgcolor = ft.Colors.WHITE

        # Animación suave para todo el contenedor (Escala y Sombra)
        self.animate = ft.Animation(duration=300, curve=ft.AnimationCurve.EASE_OUT)
        self.animate_scale = ft.Animation(duration=300, curve=ft.AnimationCurve.EASE_OUT)

        # Sombre inicial
        self.shadow = ft.BoxShadow(
                blur_radius=5,
                spread_radius=1,
                color=ft.Colors.with_opacity(0.1, ft.Colors.BLACK),
                offset=ft.Offset(0, 2)
                )

        # --- CONTENIDO ---
        # 1. Icono y Título
        self.header = ft.Row(
                controls=[
                    ft.Container(
                        content=ft.Icon(ft.Icons.BUSINESS, color=ft.Colors.BLUE_600, size=30),
                        bgcolor=ft.Colors.BLUE_50,
                        padding=10,
                        border_radius=10
                        ),
                    ft.Column(
                        spacing=2,
                        controls=[
                            ft.Text(
                                value=empresa.razon_social,
                                weight=ft.FontWeight.BOLD,
                                size=16,
                                max_lines=1,
                                overflow=ft.TextOverflow.ELLIPSIS,
                                width=180,
                                color=ft.Colors.GREY_700,
                                ),
                            ft.Text(
                                value=f"CUIT: {empresa.cuit}",
                                size=12,
                                color=ft.Colors.GREY_600
                                )
                            ]
                        )
                    ]
                )

        # 2. Detalles (Ubicación)
        self.details = ft.Row(
                controls=[
                    ft.Icon(ft.Icons.LOCATION_ON, size=14, color=ft.Colors.GREY_500),
                    ft.Text(
                        value=f"{empresa.localidad}, {empresa.provincia}",
                        size=12,
                        color=ft.Colors.GREY_500,
                        max_lines=1,
                        overflow=ft.TextOverflow.ELLIPSIS
                        )
                    ],
                alignment=ft.MainAxisAlignment.START
                )

        # 3. Barra de Acciones (Oculta inicialmente)
        self.actions = ft.Row(
                alignment=ft.MainAxisAlignment.END,
                opacity=0,
                animate_opacity=ft.Animation(200, ft.AnimationCurve.EASE_IN),
                offset=ft.Offset(0, 0.5),
                animate_offset=ft.Animation(200, ft.AnimationCurve.EASE_IN),
                controls=[
                    ft.IconButton(
                        icon=ft.Icons.EDIT_OUTLINED,
                        icon_color=ft.Colors.BLUE,
                        tooltip="Editar Empresa",
                        on_click=self._editar_click
                        ),
                    ft.IconButton(
                        icon=ft.Icons.DELETE_OUTLINE,
                        icon_color=ft.Colors.RED,
                        tooltip="Eliminar Empresa",
                        on_click=self._borrar_click
                        ),
                    ft.IconButton(
                        icon=ft.Icons.PEOPLE,
                        icon_color=ft.Colors.INDIGO,
                        tooltip="Ver Empleados",
                        on_click=self._ver_empleados_click
                        ),
                    ]
                )

        # Ensamblaje
        self.content = ft.Column(
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                controls=[
                    self.header,
                    self.details,
                    ft.Divider(),
                    self.actions
                    ]
                )

        # Eventos
        self.on_hover = self.animar_tarjeta

    async def _editar_click(self, e):
        await self.on_edit(self.empresa.id)

    async def _borrar_click(self, e):
        await self.on_delete(self.empresa.id)

    async def _ver_empleados_click(self, e):
        await self.on_ver_empleados(self.empresa)

    def animar_tarjeta(self, e):
        """
        Maneja la lógica visual al pasar el mouse.
        """
        is_hovered = e.data == "true"

        if is_hovered:
            # Elevación visual
            self.shadow.blur_radius = 20
            self.shadow.spread_radius = 2
            self.shadow.offset = ft.Offset(0, 10)
            self.shadow.color = ft.Colors.with_opacity(0.2, ft.Colors.BLACK)
            self.scale = 1.02

            # Mostrar acciones (suben y aparecen)
            self.actions.opacity = 1
            self.actions.offset = ft.Offset(0, 0)

        else:
            # Estado normal
            self.shadow.blur_radius = 5
            self.shadow.spread_radius = 1
            self.shadow.offset = ft.Offset(0, 2)
            self.shadow.color = ft.Colors.with_opacity(0.1, ft.Colors.BLACK)
            self.scale = 1.0

            # Ocultar acciones
            self.actions.opacity = 0
            self.actions.offset = ft.Offset(0, 0.5)

        self.update()
