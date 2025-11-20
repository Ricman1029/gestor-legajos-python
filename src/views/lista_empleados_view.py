import flet
from src.pdfs.creacion_pdf import armar_pdf
from src.controles.formulario_empleado import FormularioEmpleado
from src.controles.formulario_opciones_pdfs import FormularioOpcionesPdfs
from src.controles.mi_tabla import MyScrollableDataTable
from src.utils.persistencia import guardar_empresa
from src.state import global_state


class ListaEmpleadosView(flet.Column):
    def __init__(self):
        self.empresa_seleccionada = global_state.get_state_by_key("empresa_seleccionada").get_state()
        super().__init__()

    def inicializar(self):
        tabla = MyScrollableDataTable(
            columns=[
                flet.DataColumn(flet.Text("Legajo")),
                flet.DataColumn(flet.Text("Nombre y Apellido")),
                flet.DataColumn(flet.Text("C.U.I.L.")),
                flet.DataColumn(flet.Text("Fecha Nacimiento")),
                flet.DataColumn(flet.Text("Domicilio")),
                flet.DataColumn(flet.Text("Fecha Ingreso")),
                flet.DataColumn(flet.Text("Categoría")),
                flet.DataColumn(flet.Text("Obra Social")),
            ],
            rows=[
                (flet.DataRow(
                    cells=[
                        flet.DataCell(flet.Text(value=empleado.numero_legajo)),
                        flet.DataCell(flet.Text(value=f"{empleado.persona.apellido} {empleado.persona.nombre}")),
                        flet.DataCell(flet.Text(value=empleado.persona.cuil)),
                        flet.DataCell(flet.Text(value=empleado.persona.fecha_nacimiento)),
                        flet.DataCell(flet.Text(value=empleado.persona.domicilio.direccion())),
                        flet.DataCell(flet.Text(value=empleado.fecha_ingreso)),
                        flet.DataCell(flet.Text(value=empleado.categoria)),
                        flet.DataCell(flet.Text(value=empleado.persona.obra_social)),
                    ],
                    on_select_changed=self.fila_seleccionada,
                    data=empleado
                )) for empleado in self.empresa_seleccionada.empleados
            ],
            column_spacing=15,
            vertical_lines=flet.BorderSide(1, flet.Colors.GREY_700),
            height=530,
        )
        self.controls = [
            flet.Row(
                width=1050,
                scroll=flet.ScrollMode.ALWAYS,
                controls=[tabla],
            )
        ]

    def generar_legajo(self, empleado, opciones):
        armar_pdf(empleado, self.empresa_seleccionada, opciones)

    def notificar_legajo_creado(self, empleado):
        notificacion = flet.SnackBar(
            content=flet.Text(f"El legajo de {empleado.persona.apellido} {empleado.persona.nombre} "
                              f"de la empresa {self.empresa_seleccionada.nombre_empresa} "
                              f"fue creado."),
            duration=3000
        )
        self.page.open(notificacion)

    def fila_seleccionada(self, e):
        def cerrar_alerta(e):
            self.page.close(alert_dialog)
            if e.control.text == "Editar Empleado":
                self.editar_empleado(empleado_seleccionado)
            elif e.control.text == "Imprimir Legajo":
                self.imprimir_legajo(empleado_seleccionado)

        empleado_seleccionado = e.control.data
        alert_dialog = flet.AlertDialog(
            title=flet.Text("Elija una opción."),
            actions=[
                flet.TextButton(
                    text="Editar Empleado",
                    icon=flet.Icons.EDIT,
                    on_click=cerrar_alerta,
                    style=flet.ButtonStyle(
                        shape={
                            flet.ControlState.DEFAULT: flet.RoundedRectangleBorder(radius=3)
                        },
                    ),
                ),
                flet.TextButton(
                    text="Imprimir Legajo",
                    icon=flet.Icons.PRINT,
                    on_click=cerrar_alerta,
                    style=flet.ButtonStyle(
                        shape={
                            flet.ControlState.DEFAULT: flet.RoundedRectangleBorder(radius=3)
                        },
                    ),
                ),
            ]
        )
        self.page.open(alert_dialog)

    def notificar_empleado_no_valido(self, empleado):
        alert_dialog = flet.AlertDialog(
            title=flet.Text("Empleado no válido"),
            content=flet.Text("El empleado ingresado no es válido\n"
                              "Por favor, intente de nuevo."),
            on_dismiss=self.editar_empleado(empleado)
        )
        self.page.open(alert_dialog)

    def editar_empleado(self, empleado):
        def cerrar_alerta(e):
            if e.control.text == "Aceptar":
                if formulario_empleado.editar_empleado(empleado):
                    self.page.close(alert_dialog)
                    self.inicializar()
                    self.update()
                else:
                    self.notificar_empleado_no_valido(empleado)
            else:
                self.page.close(alert_dialog)

        formulario_empleado = FormularioEmpleado()
        formulario_empleado.llenar_formulario(empleado)
        alert_dialog = flet.AlertDialog(
            modal=True,
            title=flet.Text("Editar Empleado"),
            content=formulario_empleado,
            actions=[
                flet.Container(
                    content=flet.Row(
                        controls=[
                            flet.ElevatedButton(text="Aceptar", on_click=cerrar_alerta),
                            flet.ElevatedButton(text="Cancelar", on_click=cerrar_alerta)
                        ],
                        alignment=flet.MainAxisAlignment.CENTER
                    ),
                    padding=5,
                )
            ]
        )
        self.page.open(alert_dialog)

    def notificar_opciones_no_validas(self, empleado):
        alert_dialog = flet.AlertDialog(
            title=flet.Text("Opciones no válidas"),
            content=flet.Text("Las opciones para los pdfs no son válidas.\n"
                              "Por favor, intente de nuevo."),
        )
        self.page.open(alert_dialog)

    def elegir_opciones_pdfs(self, empleado):
        def cerrar_alerta(f):
            if f.control.text == "Aceptar":
                opciones = [
                    formulario.constancia_entrega.value,
                    formulario.asignacion_familiar.value,
                    formulario.seguro_vida.value,
                    formulario.notificacion_art.value,
                    formulario.notificacion_obra_social.value,
                ]
                if any(opcion is None for opcion in opciones):
                    self.notificar_opciones_no_validas(empleado)
                else:
                    self.empresa_seleccionada.opciones_pdfs = [opcion.lower() for opcion in opciones]
                    guardar_empresa(self.empresa_seleccionada)
                    self.generar_legajo(empleado, self.empresa_seleccionada.opciones_pdfs)
                    self.notificar_legajo_creado(empleado)
                    self.inicializar()
            self.page.close(alert_dialog)

        formulario = FormularioOpcionesPdfs()
        alert_dialog = flet.AlertDialog(
            modal=True,
            title=flet.Text("Elegir las opciones de los pdfs"),
            content=formulario,
            actions=[
                flet.ElevatedButton(text="Aceptar", on_click=cerrar_alerta),
                flet.ElevatedButton(text="Cancelar", on_click=cerrar_alerta)
            ]
        )
        self.page.open(alert_dialog)

    def imprimir_legajo(self, empleado):
        def cerrar_alerta_si(f):
            self.page.close(alert_dialog)
            if self.empresa_seleccionada.debe_elegir_opciones_pdfs():
                self.elegir_opciones_pdfs(empleado)
            else:
                self.generar_legajo(empleado, self.empresa_seleccionada.opciones_pdfs)
                self.notificar_legajo_creado(empleado)

        def cerrar_alerta_no(f):
            self.page.close(alert_dialog)

        alert_dialog = flet.AlertDialog(
            modal=True,
            title=flet.Text("Imprimir Legajo"),
            content=flet.Text(f"Estas seguro de querer imprimir el legajo de "
                              f"{empleado.persona.apellido} {empleado.persona.nombre}"
                              f"de la empresa {self.empresa_seleccionada.nombre_empresa}"),
            actions=[
                flet.ElevatedButton(text="Sí", on_click=cerrar_alerta_si),
                flet.ElevatedButton(text="No", on_click=cerrar_alerta_no)
            ]
        )
        self.page.open(alert_dialog)
