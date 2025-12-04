import flet
from gestor_legajos.entidades.empresa import Empresa, Domicilio
from gestor_legajos.controles.mi_textfield import MiTextField
from gestor_legajos.state import State, global_state
from gestor_legajos.utils.persistencia import leer_convenios, leer_sindicatos


class FormularioEmpresa(flet.Column):
    def __init__(self):
        self.actualizar_estado()
        lista_convenios = global_state.get_state_by_key("convenios").get_state()
        lista_sindicatos = global_state.get_state_by_key("sindicatos").get_state()
        self.nombre_empresa = MiTextField(
            width=300,
            label="Nombre empresa",
            autofocus=True,
        )
        self.siglas = MiTextField(
            width=90,
            label="Siglas",
            max_length=3,
        )
        self.cuit_empresa = MiTextField(
            width=200,
            label="C.U.I.T.",
        )
        self.numero_ieric = MiTextField(
            label="Número de IERIC",
        )
        self.telefono = MiTextField(
            label="Teléfono",
            error_text=False,
            requerido=False,
        )
        self.correo_electronico = MiTextField(
            label="Correo electrónico",
            width=610,
            error_text=False,
            requerido=False,
        )
        self.nombre_dueño = MiTextField(
            label="Nombre",
            width=200,
        )
        self.apellido_dueño = MiTextField(
            label="Apellido",
            width=200,
        )
        self.dni_dueño = MiTextField(
            label="D.N.I.",
            width=190,
        )
        self.calle = MiTextField(
            label="Calle",
            width=330,
        )
        self.numero = MiTextField(
            label="Número",
            width=100,
        )
        self.piso = MiTextField(
            label="Piso",
            width=70,
            error_text=False,
            requerido=False,
        )
        self.departamento = MiTextField(
            label="Depto.",
            width=80,
            error_text=False,
            requerido=False,
        )
        self.codigo_postal = MiTextField(
            label="Código Postal",
            value="8400",
            width=140,
            error_text=False
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
            width=250,
            error_text=False,
        )
        self.convenio = flet.Dropdown(
            width=300,
            label="Convenio",
            error_text="Requerido",
            filled=True,
            dense=True,
            border=flet.InputBorder.UNDERLINE,
            on_change=self.campo_requerido,
            options=[
                flet.dropdown.Option(convenio.nombre) for convenio in lista_convenios
            ],
        )
        self.sindicato = flet.Dropdown(
            width=300,
            label="Sindicato",
            error_text="Requerido",
            filled=True,
            dense=True,
            border=flet.InputBorder.UNDERLINE,
            on_change=self.campo_requerido,
            options=[
                flet.dropdown.Option(sindicato["siglas"]) for sindicato in lista_sindicatos
            ],
        )
        super().__init__(
            width=620,
            scroll=flet.ScrollMode.ALWAYS,
            controls=[
                self.divider("Empresa"),
                flet.Row(
                    vertical_alignment=flet.CrossAxisAlignment.START,
                    height=63,
                    controls=[
                        self.nombre_empresa,
                        self.siglas,
                        self.cuit_empresa,
                    ],
                ),
                flet.Row(
                    vertical_alignment=flet.CrossAxisAlignment.START,
                    height=63,
                    controls=[
                        self.numero_ieric,
                        self.convenio,
                    ],
                ),
                flet.Row(
                    vertical_alignment=flet.CrossAxisAlignment.START,
                    height=63,
                    controls=[
                        self.sindicato,
                        self.telefono,
                    ],
                ),
                flet.Row(
                    vertical_alignment=flet.CrossAxisAlignment.START,
                    height=63,
                    controls=[
                        self.correo_electronico,
                    ],
                ),
                self.divider("Dueño"),
                flet.Row(
                    vertical_alignment=flet.CrossAxisAlignment.START,
                    height=63,
                    controls=[
                        self.nombre_dueño,
                        self.apellido_dueño,
                        self.dni_dueño,
                    ]
                ),
                self.divider("Domicilio Empresa"),
                flet.Row(
                    vertical_alignment=flet.CrossAxisAlignment.START,
                    height=63,
                    controls=[
                        self.calle,
                        self.numero,
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
                        self.provincia
                    ]
                )
            ],
        )

    def build(self):
        self.height = self.page.window.height - 200

    def actualizar_estado(self):
        State(
            key="convenios",
            value=leer_convenios()
        )
        State(
            key="sindicatos",
            value=leer_sindicatos()
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

    def campo_requerido(self, e):
        if e.control.value == "":
            e.control.error_text = "Requerido"
        else:
            e.control.error_text = None
        self.update()

    def llenar_formulario(self, empresa):
        self.siglas.value = empresa.siglas
        self.siglas.error_text = None
        self.nombre_empresa.value = empresa.nombre_empresa
        self.nombre_empresa.error_text = None
        self.cuit_empresa.value = empresa.cuit_empresa
        self.cuit_empresa.error_text = None
        self.numero_ieric.value = empresa.numero_ieric
        self.numero_ieric.error_text = None
        self.convenio.value = empresa.convenio
        self.convenio.error_text = None
        self.sindicato.value = empresa.sindicato
        self.sindicato.error_text = None
        self.telefono.value = empresa.telefono
        self.telefono.error_text = None
        self.correo_electronico.value = empresa.correo_electronico
        self.correo_electronico.error_text = None
        self.nombre_dueño.value = empresa.nombre_dueño
        self.nombre_dueño.error_text = None
        self.apellido_dueño.value = empresa.apellido_dueño
        self.apellido_dueño.error_text = None
        self.dni_dueño.value = empresa.dni_dueño
        self.dni_dueño.error_text = None
        self.calle.value = empresa.domicilio.calle
        self.calle.error_text = None
        self.numero.value = empresa.domicilio.numero
        self.numero.error_text = None
        self.piso.value = empresa.domicilio.piso
        self.piso.error_text = None
        self.departamento.value = empresa.domicilio.departamento
        self.departamento.error_text = None
        self.codigo_postal.value = empresa.domicilio.codigo_postal
        self.codigo_postal.error_text = None
        self.localidad.value = empresa.domicilio.localidad
        self.localidad.error_text = None
        self.provincia.value = empresa.domicilio.provincia
        self.provincia.error_text = None

    def empresa_creada(self):
        return Empresa(
            siglas=self.siglas.value,
            nombre_empresa=self.nombre_empresa.value,
            cuit_empresa=self.cuit_empresa.value,
            numero_ieric=self.numero_ieric.value,
            nombre_dueño=self.nombre_dueño.value,
            apellido_dueño=self.apellido_dueño.value,
            dni_dueño=self.dni_dueño.value,
            telefono=self.telefono.value,
            correo_electronico=self.correo_electronico.value,
            domicilio=Domicilio(
                calle=self.calle.value,
                numero=self.numero.value,
                piso=self.piso.value,
                departamento=self.departamento.value,
                codigo_postal=self.codigo_postal.value,
                localidad=self.localidad.value,
                provincia=self.provincia.value,
            ),
            convenio=self.convenio.value,
            sindicato=self.sindicato.value
        )


