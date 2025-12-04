import flet
from gestor_legajos.state import global_state


class FormularioOpcionesPdfs(flet.Column):
    def __init__(self):
        self.opciones_pdfs = global_state.get_state_by_key("opciones_pdfs").get_state()[0]
        self.constancia_entrega = flet.Dropdown(
            label="Constancia de Entrega",
            border=flet.InputBorder.UNDERLINE,
            dense=True,
            filled=True,
            max_menu_height=200,
            options=[
                flet.dropdown.Option(opcion) for opcion in self.opciones_pdfs["constancia_entrega"]
            ],
        )
        self.asignacion_familiar = flet.Dropdown(
            label="Asignación Familiar",
            border=flet.InputBorder.UNDERLINE,
            dense=True,
            filled=True,
            max_menu_height=200,
            options=[
                flet.dropdown.Option(opcion) for opcion in self.opciones_pdfs["asignacion_familiar"]
            ],
        )
        self.seguro_vida = flet.Dropdown(
            label="Seguro de Vida",
            border=flet.InputBorder.UNDERLINE,
            dense=True,
            filled=True,
            max_menu_height=200,
            options=[
                flet.dropdown.Option(opcion) for opcion in self.opciones_pdfs["seguro_vida"]
            ],
        )
        self.notificacion_art = flet.Dropdown(
            label="Notificacion ART",
            border=flet.InputBorder.UNDERLINE,
            dense=True,
            filled=True,
            max_menu_height=200,
            options=[
                flet.dropdown.Option(opcion) for opcion in self.opciones_pdfs["notificacion_art"]
            ],
        )
        self.notificacion_obra_social = flet.Dropdown(
            label="Notificación Obra Social",
            border=flet.InputBorder.UNDERLINE,
            dense=True,
            filled=True,
            max_menu_height=200,
            options=[
                flet.dropdown.Option(opcion) for opcion in self.opciones_pdfs["notificacion_obra_social"]
            ],
        )
        super().__init__(
            controls=[
                self.constancia_entrega,
                self.asignacion_familiar,
                self.seguro_vida,
                self.notificacion_art,
                self.notificacion_obra_social
            ]
        )
