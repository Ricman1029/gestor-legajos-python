import flet
from gestor_legajos.controles.mi_tabla import MyScrollableDataTable
from gestor_legajos.utils.persistencia import guardar_convenio
from gestor_legajos.utils.helpers import devolver_coincidencia
from gestor_legajos.entidades.convenio import Convenio
from gestor_legajos.controles.mi_carta_animada import CartaAnimada, BotonCarta
from gestor_legajos.state import global_state, State


class TableroConvenios(flet.Container):
    def __init__(self):
        super().__init__()
        self.inicializar()

    def inicializar(self):
        self.lista_convenios = global_state.get_state_by_key("convenios").get_state()
        self.empresa_seleccionada = global_state.get_state_by_key("empresa_seleccionada").get_state()
        self.convenio_seleccionado = global_state.get_state_by_key("convenio_seleccionado").get_state()
        self.tablero = CartaAnimada(
            width=400,
            height=300,
            botones=[
                BotonCarta(
                    icon=flet.Icons.ADD_CARD_ROUNDED,
                    tooltip="Agregar Convenio",
                    on_click=self.agregar_convenio
                ),
                BotonCarta(
                    icon=flet.Icons.PLAYLIST_ADD_ROUNDED,
                    tooltip="Agregar Categoría",
                    on_click=self.agregar_categoria
                )
            ],
            cuerpo=[
                flet.Dropdown(
                    value=self.convenio_seleccionado.nombre,
                    alignment=flet.alignment.center,
                    padding=10,
                    on_change=self.dropdown_change,
                    options=[
                        flet.dropdown.Option(convenio.nombre) for convenio in self.lista_convenios
                    ]
                ),
                MyScrollableDataTable(
                    columns=[
                        flet.DataColumn(flet.Text("Categorías")),
                    ],
                    rows=[
                        (flet.DataRow(
                            cells=[
                                flet.DataCell(flet.Text(categoria)),
                            ]
                        )) for categoria in self.convenio_seleccionado.categorias
                    ],
                    height=100,
                )
            ]
        )
        self.content = self.tablero

    def notificar_convenio_no_valido(self):
        alert_dialog = flet.AlertDialog(
            title=flet.Text("Convenio ingresado no válido"),
            content=flet.Text("El convenio ingresado no es válido.\nPor favor intente de nuevo"),
        )
        self.page.open(alert_dialog)

    def notificar_convenio_creado(self, convenio):
        notificacion = flet.SnackBar(
            content=flet.Text(f"El convenio {convenio} fue agregado con éxito."),
            duration=3000
        )
        self.page.open(notificacion)

    def guardar_convenio(self, convenio):
        if convenio.nombre == "":
            self.notificar_convenio_no_valido()
            return

        guardar_convenio(
            lista_convenios=self.lista_convenios,
            convenio=convenio
        )
        self.notificar_convenio_creado(convenio.nombre)

    def agregar_convenio(self, e):
        def cerrar_alerta(f):
            self.page.close(alert_dialog)
            if f.control.text == "Aceptar":
                self.guardar_convenio(Convenio(alert_dialog.content.controls[0].value))
                self.parent.parent.inicializar()

        alert_dialog = flet.AlertDialog(
            title=flet.Text("Agregar Convenio"),
            content=flet.Row(
                width=300,
                wrap=True,
                controls=[
                    flet.TextField(
                        label="Nombre",
                    ),
                ],
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

    def notificar_categoria_no_valida(self):
        alert_dialog = flet.AlertDialog(
            title=flet.Text("Categoría ingresada no válida"),
            content=flet.Text("La categoría ingresada no es válida.\nPor favor intente de nuevo"),
        )
        self.page.open(alert_dialog)

    def notificar_categoria_creada(self, categoria):
        notificacion = flet.SnackBar(
            content=flet.Text(f"La categoría {categoria} fue agregada con éxito."),
            duration=3000
        )
        self.page.open(notificacion)

    def guardar_categoria(self, categoria):
        if categoria == "":
            self.notificar_categoria_no_valida()
            return

        convenio_seleccionado = devolver_coincidencia(
            lista=self.lista_convenios,
            valor=self.empresa_seleccionada.convenio,
            por_atributo=lambda convenio: convenio.nombre,
            devolver_indice=True
        )
        self.lista_convenios[convenio_seleccionado].agregar_categoria(categoria)
        guardar_convenio(lista_convenios=self.lista_convenios)
        self.notificar_categoria_creada(categoria)
        self.parent.parent.inicializar()

    def agregar_categoria(self, e):
        def cerrar_alerta(f):
            self.page.close(alert_dialog)
            if f.control.text == "Aceptar":
                self.guardar_categoria(alert_dialog.content.controls[0].value)

        alert_dialog = flet.AlertDialog(
            title=flet.Text("Agregar Categoría"),
            content=flet.Row(
                width=300,
                wrap=True,
                controls=[
                    flet.TextField(
                        label="Nombre",
                    ),
                ],
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

    def dropdown_change(self, e):
        State(
            key="convenio_seleccionado",
            value=devolver_coincidencia(
                lista=self.lista_convenios,
                valor=e.control.value,
                por_atributo=lambda convenio: convenio.nombre
            )
        )
        self.tablero.cuerpo[1] = MyScrollableDataTable(
            columns=[
                flet.DataColumn(flet.Text("Categorías")),
            ],
            rows=[
                (flet.DataRow(
                    cells=[
                        flet.DataCell(flet.Text(categoria)),
                    ]
                )) for categoria in self.convenio_seleccionado.categorias
            ],
            height=100,
        )
        self.inicializar()
        self.update()
