import flet
from gestor_legajos.controles.mi_tabla import MyScrollableDataTable
from gestor_legajos.utils.persistencia import guardar_obra_social
from gestor_legajos.controles.mi_carta_animada import CartaAnimada, BotonCarta
from gestor_legajos.state import global_state

class TableroObraSocial(flet.Container):
    def __init__(self):
        self.lista_obras_sociales = global_state.get_state_by_key("obras_sociales").get_state()
        self.tablero = CartaAnimada(
            width=250,
            height=300,
            botones=[
                BotonCarta(
                    icon=flet.Icons.PLAYLIST_ADD_ROUNDED,
                    tooltip="Agregar obra social",
                    on_click=self.crear_obra_social
                )
            ],
            cuerpo=[
                MyScrollableDataTable(
                    columns=[
                        flet.DataColumn(flet.Text("Codigo")),
                        flet.DataColumn(flet.Text("Obra Social"))
                    ],
                    rows=[
                        (flet.DataRow(
                            cells=[
                                flet.DataCell(flet.Text(obra_social["codigo"])),
                                flet.DataCell(flet.Text(obra_social["siglas"]))
                            ],
                        )) for obra_social in self.lista_obras_sociales
                    ],
                    height=160,
                )
            ]
        )
        super().__init__(
            content=self.tablero,
        )

    def notificar_obra_social_no_valida(self):
        alert_dialog = flet.AlertDialog(
            title=flet.Text("Obra social ingresada no válida"),
            content=flet.Text("La obra social ingresada no es válida.\nPor favor intente de nuevo"),
        )
        self.page.open(alert_dialog)

    def notificar_obra_social_creada(self, siglas):
        notificacion = flet.SnackBar(
            content=flet.Text(f"La obra social {siglas} fue agregada con éxito."),
            duration=3000
        )
        self.page.open(notificacion)

    def agregar_obra_social(self, alerta):
        codigo = alerta.content.controls[0].value
        siglas = alerta.content.controls[1].value
        nombre = alerta.content.controls[2].value

        if codigo == "" or siglas == "" or nombre == "":
            self.notificar_obra_social_no_valida()
            return

        obra_social = {
            "codigo": codigo,
            "nombre": nombre,
            "siglas": siglas
        }
        guardar_obra_social(self.lista_obras_sociales, obra_social)
        self.notificar_obra_social_creada(siglas)
        self.parent.parent.inicializar()
        self.page.update()

    def crear_obra_social(self, e):
        def cerrar_alerta(f):
            self.page.close(alert_dialog)
            if f.control.text == "Aceptar":
                self.agregar_obra_social(alert_dialog)

        alert_dialog = flet.AlertDialog(
            title=flet.Text("Agregar Obra Social"),
            content=flet.Row(
                controls=[
                    flet.TextField(
                        label="Código",
                        width=145
                    ),
                    flet.TextField(
                        label="Siglas",
                        width=145
                    ),
                    flet.TextField(
                        label="Nombre"
                    )
                ],
                width=300,
                wrap=True
            ),
            actions=[
                flet.ElevatedButton(
                    text="Aceptar",
                    on_click=cerrar_alerta
                ),
                flet.ElevatedButton(
                    text="Cancelar",
                    on_click=cerrar_alerta
                )
            ]
        )
        self.page.open(alert_dialog)
