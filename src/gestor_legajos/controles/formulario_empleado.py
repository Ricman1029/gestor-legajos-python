import flet
import datetime
from gestor_legajos.entidades.empleado import Empleado, Persona
from gestor_legajos.entidades.domicilio import Domicilio
from gestor_legajos.utils.helpers import devolver_coincidencia
from gestor_legajos.controles.mi_textfield import MiTextField
from gestor_legajos.state import State, global_state
from gestor_legajos.utils.persistencia import (guardar_convenio,
                                                        guardar_empresa,
                                                        validar_empleado,
                                                        guardar_obra_social)


class FormularioEmpleado(flet.Column):
    def __init__(self):
        # Cargamos la información que necesitamos
        self.lista_convenios = global_state.get_state_by_key("convenios").get_state()
        self.lista_obras_sociales = global_state.get_state_by_key("obras_sociales").get_state()
        self.empresa_seleccionada = global_state.get_state_by_key("empresa_seleccionada").get_state()

        self.convenio_empresa_seleccionada = devolver_coincidencia(
            lista=self.lista_convenios,
            valor=self.empresa_seleccionada.convenio,
            por_atributo=lambda convenio: convenio.nombre
        )
        self.numero_legajo = MiTextField(
            label="Número de legajo",
            width=160,
        )
        self.nombre = MiTextField(
            label="Nombre",
        )
        self.apellido = MiTextField(
            label="Apellido",
        )
        self.nacionalidad = MiTextField(
            label="Nacionalidad",
            value="Argentina",
            width=140,
            error_text=False,
        )
        self.cuil = MiTextField(
            label="C.U.I.L.",
            width=180,
        )
        self.sexo = MiTextField(
            label="Sexo",
            value="Masculino",
            width=120,
            error_text=False,
        )
        self.estado_civil = MiTextField(
            label="Estado civil",
            value="Soltero",
            width=120,
            error_text=False,
        )
        self.antiguedad = MiTextField(
            label="Antigüedad",
            error_text=False,
            requerido=False,
        )
        self.sueldo = MiTextField(
            label="Sueldo",
            width=200,
        )
        self.calle = MiTextField(
            label="Calle",
        )
        self.numero_calle = MiTextField(
            label="Número",
            width=100,
        )
        self.piso = MiTextField(
            label="Piso",
            width=100,
            error_text=False,
            requerido=False,
        )
        self.departamento = MiTextField(
            label="Depto.",
            width=100,
            error_text=False,
            requerido=False,
        )
        self.codigo_postal = MiTextField(
            label="Código Postal",
            value="8400",
            width=120,
            error_text=False,
        )
        self.localidad = MiTextField(
            label="Localidad",
            value="Bariloche",
            width=200,
            error_text=False,
        )
        self.provincia = MiTextField(
            label="Provincia",
            value="Río Negro",
            width=200,
            error_text=False,
        )
        self.telefono = MiTextField(
            label="Teléfono",
            width=200,
            requerido=False,
            error_text=False,
        )
        self.correo_electronico = MiTextField(
            label="Correo electrónico",
            requerido=False,
            error_text=False,
        )
        self.fecha_nacimiento = MiTextField(
            label="Fecha de nacimiento",
            width=160,
            error_text=True,
            on_submit=self.elegir_fecha,
            hint_text="'ENTER' abre el selector de fecha",
        )
        self.fecha_ingreso = MiTextField(
            label="Fecha de ingreso",
            width=160,
            error_text=True,
            on_submit=self.elegir_fecha,
            hint_text="'ENTER' abre el selector de fecha",
        )
        opciones_obra_social = [
            flet.dropdown.Option(obra_social["siglas"])
            for obra_social in self.lista_obras_sociales
        ]
        opciones_obra_social.append(flet.dropdown.Option("--Agregar Obra Social--"))
        self.obra_social = flet.Dropdown(
            label="Obra Social",
            error_text="Requerido",
            border=flet.InputBorder.UNDERLINE,
            dense=True,
            filled=True,
            max_menu_height=200,
            on_change=self.campo_requerido,
            options=opciones_obra_social,
        )
        opciones_categoria = [
            flet.dropdown.Option(categoria)
            for categoria in self.convenio_empresa_seleccionada.categorias
        ]
        opciones_categoria.append(flet.dropdown.Option("--Agregar Categoría--"))
        self.categoria = flet.Dropdown(
            label="Categoría",
            error_text="Requerido",
            border=flet.InputBorder.UNDERLINE,
            dense=True,
            filled=True,
            width=500,
            max_menu_height=200,
            on_change=self.campo_requerido,
            options=opciones_categoria,
        )
        super().__init__(
            scroll=flet.ScrollMode.ALWAYS,
            controls=[
                self.divider("Datos Personales"),
                flet.Row(
                    vertical_alignment=flet.CrossAxisAlignment.START,
                    height=63,
                    controls=[
                        self.numero_legajo,
                        self.nombre,
                        self.apellido,
                    ]
                ),
                flet.Row(
                    vertical_alignment=flet.CrossAxisAlignment.START,
                    height=63,
                    controls=[
                        self.fecha_nacimiento,
                        self.nacionalidad,
                        self.cuil,
                        self.sexo,
                        self.estado_civil
                    ]
                ),
                self.divider("Datos para la empresa"),
                flet.Row(
                    vertical_alignment=flet.CrossAxisAlignment.START,
                    height=63,
                    controls=[
                        self.fecha_ingreso,
                        self.antiguedad,
                        self.obra_social
                    ]
                ),
                flet.Row(
                    vertical_alignment=flet.CrossAxisAlignment.START,
                    height=63,
                    controls=[
                        self.categoria,
                        self.sueldo,
                    ]
                ),
                self.divider("Domicilio"),
                flet.Row(
                    vertical_alignment=flet.CrossAxisAlignment.START,
                    height=63,
                    controls=[
                        self.calle,
                        self.numero_calle,
                        self.piso,
                        self.departamento
                    ]
                ),
                flet.Row(
                    vertical_alignment=flet.CrossAxisAlignment.START,
                    height=63,
                    controls=[
                        self.codigo_postal,
                        self.localidad,
                        self.provincia,
                    ]
                ),
                self.divider("Contacto"),
                flet.Row(
                    vertical_alignment=flet.CrossAxisAlignment.START,
                    height=63,
                    controls=[
                        self.telefono,
                        self.correo_electronico
                    ]
                ),
            ],
        )

    def divider(self, value):
        return flet.Container(
            bgcolor=flet.Colors.PRIMARY_CONTAINER,
            border_radius=flet.border_radius.all(30),
            height=20,
            padding=flet.padding.only(left=20),
            alignment=flet.alignment.center,
            width=780,
            content=flet.Text(
                value=value,
                color=flet.Colors.ON_PRIMARY_CONTAINER,
                weight=flet.FontWeight.W_500,
            ),
        )

    def cuadro_texto(
            self,
            label,
            error_text=True,
            width=300,
            value=None,
            on_submit=None,
            hint_text=None,
    ):
        return flet.TextField(
            width=width,
            label=label,
            value=value,
            hint_text=hint_text,
            border=flet.InputBorder.UNDERLINE,
            filled=True,
            dense=True,
            error_text="Requerido" if error_text else None,
            on_change=self.campo_requerido if error_text else None,
            on_submit=on_submit,
        )

    def build(self):
        self.height = self.page.window.height - 200

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

    def agregar_categoria(self, e):
        def cerrar_alerta(f):
            self.page.close(alert_dialog)
            if f.control.text == "Aceptar":
                self.guardar_categoria(alert_dialog.content.controls[0].value)
                e.control.options.insert(-1, flet.dropdown.Option(alert_dialog.content.controls[0].value))
                e.control.update()

        alert_dialog = flet.AlertDialog(
            title=flet.Text("Agregar Categoría"),
            content=flet.Row(
                controls=[
                    flet.TextField(
                        label="Nombre",
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
        alert_dialog.content.controls[0].focus()

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

    def crear_obra_social(self, e):
        def cerrar_alerta(f):
            self.page.close(alert_dialog)
            if f.control.text == "Aceptar":
                self.agregar_obra_social(alert_dialog)
                e.control.options.insert(-1, flet.dropdown.Option(alert_dialog.content.controls[0].value))
                e.control.update()

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

    def campo_requerido(self, e):
        if e.control.value == "--Agregar Categoría--":
            self.agregar_categoria(e)
            return

        if e.control.value == "--Agregar Obra Social--":
            self.crear_obra_social(e)
            return

        if e.control.value == "":
            e.control.error_text = "Requerido"
        else:
            e.control.error_text = None
        self.update()

    def elegir_fecha(self, e):
        def escribir_fecha(f):
            if e.control.label == "Fecha de nacimiento":
                self.nacionalidad.focus()
            elif e.control.label == "Fecha de ingreso":
                self.antiguedad.focus()
            e.control.value = f.control.value.strftime("%d/%m/%Y")
            e.control.error_text = None
            self.page.update()

        selector_fecha = flet.DatePicker(
            first_date=datetime.datetime(year=1950, month=1, day=1),
            last_date=datetime.date.today(),
            on_change=escribir_fecha,
            date_picker_mode=flet.DatePickerMode.YEAR,
            date_picker_entry_mode=flet.DatePickerEntryMode.CALENDAR,
            value=datetime.datetime(year=1990, month=1, day=1)
        )
        self.page.open(selector_fecha)

    def llenar_formulario(self, empleado):
        self.numero_legajo.value = empleado.numero_legajo
        self.numero_legajo.error_text = None
        self.nombre.value = empleado.persona.nombre
        self.nombre.error_text = None
        self.apellido.value = empleado.persona.apellido
        self.apellido.error_text = None
        self.fecha_nacimiento.value = empleado.persona.fecha_nacimiento
        self.fecha_nacimiento.error_text = None
        self.nacionalidad.value = empleado.persona.nacionalidad
        self.cuil.value = empleado.persona.cuil
        self.cuil.error_text = None
        self.sexo.value = empleado.persona.sexo
        self.estado_civil.value = empleado.persona.estado_civil
        self.calle.value = empleado.persona.domicilio.calle
        self.calle.error_text = None
        self.numero_calle.value = empleado.persona.domicilio.numero
        self.numero_calle.error_text = None
        self.piso.value = empleado.persona.domicilio.piso
        self.departamento.value = empleado.persona.domicilio.departamento
        self.codigo_postal.value = empleado.persona.domicilio.codigo_postal
        self.localidad.value = empleado.persona.domicilio.localidad
        self.provincia.value = empleado.persona.domicilio.provincia
        self.obra_social.value = empleado.persona.obra_social
        self.obra_social.error_text = None
        self.telefono.value = empleado.persona.telefono
        self.correo_electronico.value = empleado.persona.correo_electronico
        self.fecha_ingreso.value = empleado.fecha_ingreso
        self.fecha_ingreso.error_text = None
        self.antiguedad.value = empleado.antiguedad
        self.sueldo.value = empleado.sueldo
        self.sueldo.error_text = None
        self.categoria.value = empleado.categoria
        self.categoria.error_text = None

    def notificar_empleado_editado(self, empleado):
        notificacion = flet.SnackBar(
            content=flet.Text(f"El empleado {empleado.persona.apellido} {empleado.persona.nombre} "
                              f"fue editado con éxito."),
            duration=3000
        )
        self.page.open(notificacion)

    def editar_empleado(self, empleado):
        edicion = Empleado(
            numero_legajo=self.numero_legajo.value,
            persona=Persona(
                nombre=self.nombre.value,
                apellido=self.apellido.value,
                fecha_nacimiento=self.fecha_nacimiento.value,
                nacionalidad=self.nacionalidad.value,
                cuil=self.cuil.value,
                domicilio=Domicilio(
                    calle=self.calle.value,
                    numero=self.numero_calle.value,
                    piso=self.piso.value,
                    departamento=self.departamento.value,
                    codigo_postal=self.codigo_postal.value,
                    localidad=self.localidad.value,
                    provincia=self.provincia.value,
                ),
                obra_social=self.obra_social.value,
                sexo=self.sexo.value,
                estado_civil=self.estado_civil.value,
                telefono=self.telefono.value,
                correo_electronico=self.correo_electronico.value,
            ),
            fecha_ingreso=self.fecha_ingreso.value,
            antiguedad=self.antiguedad.value,
            sueldo=self.sueldo.value,
            categoria=self.categoria.value,
        )

        if validar_empleado(edicion):
            (self.empresa_seleccionada.buscar_empleado(empleado.persona.cuil)).editar_empleado(edicion)
            guardar_empresa(self.empresa_seleccionada)
            self.notificar_empleado_editado(empleado)
            return 1
