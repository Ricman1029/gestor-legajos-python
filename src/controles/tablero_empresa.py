import flet
from src.utils.persistencia import guardar_empresa, crear_empresa, obtener_lista_empresas
from src.utils.helpers import devolver_coincidencia
from src.controles.formulario_empresa import FormularioEmpresa
from src.controles.mi_carta_animada import CartaAnimada, BotonCarta
from src.state import State, global_state


class TableroEmpresa(flet.Container):
    def __init__(self, empresa):
        self.empresa = empresa
        self.botones = [
            BotonCarta(
                icon=flet.Icons.BLOCK,
                tooltip="Dar de baja",
                on_click=self.confirmar_dar_baja,
            ),
            BotonCarta(
                icon=flet.Icons.DONE_OUTLINE_ROUNDED,
                tooltip="Dar de alta",
                on_click=self.dar_alta_empresa,
            ),
            BotonCarta(
                icon=flet.Icons.EDIT_SQUARE,
                tooltip="Editar",
                on_click=self.editar_empresa,
            )
        ]
        self.tablero = CartaAnimada(
            botones=self.botones,
            cuerpo=[
                flet.Container(
                    padding=20,
                    alignment=flet.alignment.bottom_center,
                    content=flet.Text(
                        value=empresa.nombre_empresa,
                        text_align=flet.TextAlign.CENTER,
                        color=flet.Colors.ON_PRIMARY_CONTAINER,
                        size=26,
                        weight=flet.FontWeight.W_800,
                    )
                ),
                flet.Container(
                    margin=flet.Margin(top=0, left=20, right=20, bottom=20),
                    width=80,
                    border_radius=3,
                    alignment=flet.alignment.bottom_center,
                    bgcolor=flet.Colors.SECONDARY,
                    content=flet.Text(
                        value="Activa" if empresa.activa else "Inactiva",
                        color=flet.Colors.ON_SECONDARY,
                        size=14,
                        weight=flet.FontWeight.W_800,
                    )
                ),
                flet.Text(
                    value=f"Total empleados: {empresa.total_empleados()}\n"
                          f"Empleados activos: {empresa.empleados_activos}",
                    text_align=flet.TextAlign.CENTER,
                    weight=flet.FontWeight.W_500,
                    color=flet.Colors.ON_PRIMARY_CONTAINER
                ),
            ],
            on_click=self.tablero_click,
        )
        super().__init__(
            content=self.tablero
        )

    def notificar_empresa_no_valida(self):
        alert_dialog = flet.AlertDialog(
            title=flet.Text("Empresa no válida"),
            content=flet.Text("La empresa ingresado no es válida\n"
                              "Por favor, intente de nuevo."),
            on_dismiss=self.editar_empresa(self)
        )
        self.page.open(alert_dialog)

    def editar_empresa(self, e):
        def cerrar_dialogo(f):
            if f.control.text == "Aceptar":
                if crear_empresa(view.empresa_creada()):
                    State(
                        key="empresas",
                        value=obtener_lista_empresas()
                    )
                else:
                    self.notificar_empresa_no_valida()
            self.page.close(alert_dialog)

        view = FormularioEmpresa()
        view.llenar_formulario(self.empresa)
        alert_dialog = flet.AlertDialog(
            modal=True,
            title=flet.Text("Editar empresa"),
            content=view,
            actions=[
                flet.ElevatedButton(text="Aceptar", on_click=cerrar_dialogo),
                flet.ElevatedButton(text="Cancelar", on_click=cerrar_dialogo)
            ],
            actions_alignment=flet.MainAxisAlignment.CENTER
        )
        self.page.open(alert_dialog)

    def dar_alta_empresa(self, e):
        self.empresa.dar_alta()
        guardar_empresa(self.empresa)
        self.page.update()

    def confirmar_dar_baja(self, e):
        def cerrar_alerta(e):
            self.page.close(alert_dialog)
            if e.control.text == "Sí":
                self.dar_baja_empresa()

        alert_dialog = flet.AlertDialog(
            modal=True,
            title=flet.Text("Advertencia"),
            content=flet.Text("Está seguro de que quiere dar de baja a la empresa?"),
            actions=[
                flet.TextButton("Sí", on_click=cerrar_alerta),
                flet.TextButton("No", on_click=cerrar_alerta)
            ]
        )
        self.page.open(alert_dialog)

    def dar_baja_empresa(self):
        self.empresa.dar_de_baja()
        guardar_empresa(self.empresa)
        self.parent.parent.inicializar()
        self.page.update()

    def tablero_click(self, e):
        # Empresa seleccionada
        empresa_seleccionada = State(
            key="empresa_seleccionada",
            value=self.empresa
        )
        # Lista convenios
        lista_convenios = global_state.get_state_by_key("convenios").get_state()
        # Convenio seleccionado
        State(
            key="convenio_seleccionado",
            value=devolver_coincidencia(
                lista=lista_convenios,
                valor=empresa_seleccionada.get_state().convenio,
                por_atributo=lambda convenio: convenio.nombre
            )
        )
        self.parent.parent.parent.parent.sidebar.actualizar_sidebar()
        self.page.update()
