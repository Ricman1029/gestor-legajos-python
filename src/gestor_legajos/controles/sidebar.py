import flet
import time
from math import pi
from gestor_legajos.state import State, global_state

class SidebarDestination(flet.Container):
    def __init__(self, icon: flet.Icons, texto: str, ruta, on_click, on_tap_down=None):
        self.ruta = ruta
        super().__init__(
            key="",
            width=180,
            height=45,
            border_radius=10,
            on_hover=self.hover,
            on_tap_down=on_tap_down,
            on_click=on_click,
            bgcolor=flet.Colors.SURFACE,
            animate=flet.Animation(
                duration=200,
                curve=flet.AnimationCurve.DECELERATE
            ),
            content=flet.Row(
                controls=[
                    flet.IconButton(
                        icon=icon,
                        icon_size=18,
                        icon_color=flet.Colors.PRIMARY,
                        style=flet.ButtonStyle(
                            shape=flet.RoundedRectangleBorder(radius=7),
                            overlay_color=flet.Colors.TRANSPARENT,
                        ),
                    ),
                    flet.Text(
                        value=texto,
                        size=11,
                        opacity=1,
                        animate_opacity=200,
                        color=flet.Colors.ON_SURFACE,
                    )
                ]
            )
        )

    def hover(self, e):
        if self.key != "seleccionado":
            if e.data == "true":
                self.bgcolor = flet.Colors.SURFACE_CONTAINER_HIGHEST
                self.content.controls[0].icon_color = flet.Colors.ON_PRIMARY_CONTAINER
                self.content.controls[1].color = flet.Colors.ON_PRIMARY_CONTAINER
            else:
                self.bgcolor = None
                self.content.controls[0].icon_color = flet.Colors.PRIMARY
                self.content.controls[1].color = flet.Colors.ON_SURFACE
            self.update()


class Sidebar(flet.Container):
    def __init__(self):
        # self.app = app
        self.destinations = [
            SidebarDestination(
                icon=flet.Icons.BUSINESS,
                texto="Empresas",
                on_click=self.seleccionar,
                ruta="/empresas"
            ),
            SidebarDestination(
                icon=flet.Icons.PEOPLE,
                texto="Ver empleados",
                on_click=self.seleccionar,
                ruta="/lista_empleados"
            ),
            SidebarDestination(
                icon=flet.Icons.PERSON_ADD,
                texto="Agregar Empleado",
                on_click=self.seleccionar,
                ruta="/agregar_empleados"
            ),
            SidebarDestination(
                icon=flet.Icons.CATEGORY,
                texto="Otros",
                on_click=self.seleccionar,
                ruta="/otros"
            ),
        ]
        super().__init__(
            width=200,
            bgcolor=flet.Colors.SURFACE,
            alignment=flet.alignment.center,
            padding=flet.Padding(top=15, left=10, right=10, bottom=0),
            animate=flet.Animation(
                duration=200,
                curve=flet.AnimationCurve.DECELERATE
            ),
            content=flet.Column(
                horizontal_alignment=flet.CrossAxisAlignment.CENTER,
                controls=[
                    self.datos_usuarios(
                        iniciales="...",
                        nombre="Seleccionar Empresa",
                        descripcion="..."
                    ),
                    flet.IconButton(
                        icon=flet.Icons.ARROW_BACK_IOS_ROUNDED,
                        on_click=self.animar_sidebar,
                        rotate=flet.Rotate(0, alignment=flet.alignment.center),
                        animate_rotation=flet.Animation(300, flet.AnimationCurve.DECELERATE),
                    ),
                    flet.Divider(
                        height=5,
                        color=flet.Colors.TRANSPARENT,
                    ),
                    *self.destinations,
                ]
            )
        )

    def inicializar(self):
        # Le damos el color al elemento seleccionado
        self.destinations[0].key = "seleccionado"
        self.destinations[0].bgcolor = flet.Colors.SECONDARY_CONTAINER
        self.destinations[0].content.controls[0].icon_color = flet.Colors.ON_SECONDARY_CONTAINER
        self.destinations[0].content.controls[1].color = flet.Colors.ON_SECONDARY_CONTAINER

    def notificar_seleccion_empresa(self):
        notificacion = flet.SnackBar(
            content=flet.Text(f"Primero debe seleccionar una empresa."),
            duration=3000
        )
        self.page.open(notificacion)

    def seleccionar(self, e):
        if e.control.key == "seleccionado":
            return

        empresa_seleccionada = global_state.get_state_by_key("empresa_seleccionada").get_state()
        if empresa_seleccionada:
            # Le quitamos el color a todos
            for destination in self.destinations:
                destination.key = ""
                destination.bgcolor = None
                destination.content.controls[0].icon_color = flet.Colors.PRIMARY
                destination.content.controls[1].color = flet.Colors.ON_SURFACE

            # Le damos el color al elemento seleccionado
            e.control.key = "seleccionado"
            e.control.bgcolor = flet.Colors.SECONDARY_CONTAINER
            e.control.content.controls[0].icon_color = flet.Colors.ON_SECONDARY_CONTAINER
            e.control.content.controls[1].color = flet.Colors.ON_SECONDARY_CONTAINER

            # Nos movemos entre views
            self.page.go(e.control.ruta)
        else:
            self.notificar_seleccion_empresa()
        self.update()

    def datos_usuarios(self, iniciales, nombre, descripcion):
        return flet.Container(
            content=flet.Row(
                controls=[
                    flet.Container(
                        width=44,
                        height=44,
                        bgcolor=flet.Colors.INVERSE_SURFACE,
                        alignment=flet.alignment.center,
                        border_radius=8,
                        content=flet.Text(
                            value=iniciales,
                            font_family="Consolas",
                            size=24,
                            weight=flet.FontWeight.BOLD,
                            color=flet.Colors.ON_INVERSE_SURFACE,
                        )
                    ),
                    flet.Column(
                        spacing=1,
                        alignment=flet.MainAxisAlignment.CENTER,
                        controls=[
                            flet.Text(
                                value=nombre,
                                size=11,
                                weight=flet.FontWeight.BOLD,
                                opacity=1,
                                animate_opacity=200,
                                width=130,
                                max_lines=2,
                                overflow=flet.TextOverflow.ELLIPSIS
                            ),
                            flet.Text(
                                value=descripcion,
                                size=9,
                                weight=flet.FontWeight.W_400,
                                opacity=1,
                                animate_opacity=200,
                                width=130,
                                max_lines=2,
                                overflow=flet.TextOverflow.ELLIPSIS
                            ),
                        ]
                    )
                ]
            )
        )

    def animar_sidebar(self, e):
        items_titulo = self.content.controls[0].content.controls[1].controls
        if self.width != 62:
            for item in items_titulo:
                item.opacity = 0
            for item in self.destinations:
                if isinstance(item, flet.Container):
                    item.content.controls[1].opacity = 0
            e.control.rotate.angle += pi
            self.update()
            time.sleep(0.2)
            self.width = 62
            self.width = 62
        else:
            self.width = 200
            self.width = 200
            e.control.rotate.angle -= pi
            self.update()
            time.sleep(0.1)
            for item in items_titulo:
                item.opacity = 1
            for item in self.destinations:
                if isinstance(item, flet.Container):
                    item.content.controls[1].opacity = 1
        self.update()

    def actualizar_sidebar(self):
        empresa = global_state.get_state_by_key("empresa_seleccionada").get_state()
        self.content.controls[0] = self.datos_usuarios(
            iniciales=empresa.siglas,
            nombre=empresa.nombre_empresa,
            descripcion=empresa.convenio,
        )
        self.update()
