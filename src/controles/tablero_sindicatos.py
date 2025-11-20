import flet
from src.utils.persistencia import guardar_sindicato
from src.controles.mi_tabla import MyScrollableDataTable
from src.controles.mi_carta_animada import CartaAnimada, BotonCarta
from src.state import global_state


class TableroSindicatos(flet.Container):
    def __init__(self):
        self.lista_sindicatos = global_state.get_state_by_key("sindicatos").get_state()
        self.tablero = CartaAnimada(
            width=250,
            height=300,
            botones=[
                BotonCarta(
                    icon=flet.Icons.PLAYLIST_ADD_ROUNDED,
                    tooltip="Agregar Sindicato",
                    on_click=self.crear_sindicato
                )
            ],
            cuerpo=[
                MyScrollableDataTable(
                    columns=[
                        flet.DataColumn(flet.Text("Sindicatos")),
                    ],
                    rows=[
                        (flet.DataRow(
                            cells=[
                                flet.DataCell(flet.Text(sindicato["siglas"])),
                            ]
                        )) for sindicato in self.lista_sindicatos
                    ],
                    height=160,
                )
            ]
        )
        super().__init__(
            content=self.tablero
        )

    def notificar_sindicato_no_valido(self):
        alert_dialog = flet.AlertDialog(
            title=flet.Text("Sindicato ingresado no válido"),
            content=flet.Text("El sindicato ingresado no es válido.\nPor favor intente de nuevo"),
        )
        self.page.open(alert_dialog)

    def notificar_sindicato_creado(self, sindicato):
        notificacion = flet.SnackBar(
            content=flet.Text(f"El sindicato {sindicato} fue agregado con éxito."),
            duration=3000
        )
        self.page.open(notificacion)

    def agregar_sindicato(self, alerta):
        nombre = alerta.content.controls[0].value
        siglas = alerta.content.controls[1].value

        if nombre == "" or siglas == "":
            self.notificar_sindicato_no_valido()
            return

        sindicato = {
            "nombre": nombre,
            "siglas": siglas
        }
        guardar_sindicato(self.lista_sindicatos, sindicato)
        self.notificar_sindicato_creado(nombre)
        self.parent.parent.inicializar()

    def crear_sindicato(self, e):
        def cerrar_alerta(f):
            self.page.close(alert_dialog)
            if f.control.text == "Aceptar":
                self.agregar_sindicato(alert_dialog)

        alert_dialog = flet.AlertDialog(
            title=flet.Text("Agregar Sindicato"),
            content=flet.Row(
                controls=[
                    flet.TextField(
                        label="Nombre",
                        width=145,
                    ),
                    flet.TextField(
                        label="Siglas",
                        width=145,
                    ),
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
