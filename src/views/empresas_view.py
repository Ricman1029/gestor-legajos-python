import flet
from src.controles.tablero_empresa import TableroEmpresa
from src.controles.formulario_empresa import FormularioEmpresa
from src.utils.persistencia import crear_empresa, obtener_lista_empresas
from src.controles.mi_text_button import MiTextButton
from src.state import global_state, State


class EmpresasView(flet.Column):
    def __init__(self):
        self.solo_empresas_activas = True
        super().__init__(
            controls=[
                flet.Row(
                    controls=[
                        flet.Container(
                            content=flet.Text(
                                value="Empresas",
                                style=flet.TextThemeStyle.HEADLINE_MEDIUM
                            ),
                            expand=True,
                            padding=flet.padding.only(top=15),
                        ),
                        flet.Container(
                            content=MiTextButton(
                                texto="Agregar Empresa",
                                on_click=self.agregar_empresa
                            ),
                            padding=flet.padding.only(right=50, top=15)
                        )
                    ]
                ),
                flet.Row(
                    controls=[
                        flet.TextField(
                            hint_text="Buscar todas las empresas",
                            autofocus=False,
                            content_padding=flet.padding.only(left=10),
                            width=200,
                            height=40,
                            text_size=12,
                            suffix_icon=flet.Icons.SEARCH
                        ),
                        flet.Container(
                            content=flet.Switch(
                                label="Solo empresas activas",
                                on_change=self.alternar_empresas_visibles
                            ),
                            padding=flet.padding.only(right=50)
                        )
                    ],
                    alignment=flet.MainAxisAlignment.SPACE_BETWEEN
                ),
                flet.Row(
                    controls=[
                        flet.Text("No hay empresas para mostrar")
                    ]
                )
            ],
            expand=True,
        )

    def inicializar(self):
        lista_empresas = global_state.get_state_by_key("empresas").get_state()
        if len(lista_empresas) < 1:
            return

        self.controls[-1] = flet.Row(
            scroll=flet.ScrollMode.ALWAYS,
            wrap=True,
            height=470
        )
        for empresa in lista_empresas:
            if self.solo_empresas_activas:
                if empresa.activa:
                    tablero = TableroEmpresa(empresa=empresa)
                    self.controls[-1].controls.append(tablero)
            else:
                tablero = TableroEmpresa(empresa=empresa)
                self.controls[-1].controls.append(tablero)
        # self.update()

    def alternar_empresas_visibles(self, e):
        self.solo_empresas_activas = not self.solo_empresas_activas
        e.control.label = (
            "Solo empresas activas" if self.solo_empresas_activas else "Todas las empresas"
        )
        self.inicializar()
        self.page.update()

    def notificar_empresa_no_valida(self):
        alert_dialog = flet.AlertDialog(
            title=flet.Text("Empresa no válida"),
            content=flet.Text("La empresa ingresado no es válida\n"
                              "Por favor, intente de nuevo."),
            on_dismiss=self.agregar_empresa(self)
        )
        self.page.open(alert_dialog)

    def notificar_empresa_creada(self, empresa):
        notificacion = flet.SnackBar(
            content=flet.Text(f"La empresa {empresa.nombre_empresa} "
                              f"fue creada con éxito."),
            duration=3000
        )
        self.page.open(notificacion)

    def agregar_empresa(self, e):
        def cerrar_dialogo(f):
            if f.control.text == "Aceptar":
                if crear_empresa(view.empresa_creada()):
                    State(
                        key="empresas",
                        value=obtener_lista_empresas()
                    )
                    self.notificar_empresa_creada(view.empresa_creada())
                else:
                    self.notificar_empresa_no_valida()
            self.page.close(alert_dialog)
            self.inicializar()
            self.page.update()

        view = FormularioEmpresa()
        alert_dialog = flet.AlertDialog(
            modal=True,
            title=flet.Text("Agregar empresa"),
            content=view,
            actions=[
                flet.ElevatedButton(text="Aceptar", on_click=cerrar_dialogo),
                flet.ElevatedButton(text="Cancelar", on_click=cerrar_dialogo)
            ],
            actions_alignment=flet.MainAxisAlignment.CENTER
        )
        self.page.open(alert_dialog)
