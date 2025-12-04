import flet
from gestor_legajos.entidades.empleado import Empleado, Persona
from gestor_legajos.entidades.domicilio import Domicilio
from gestor_legajos.utils.persistencia import validar_empleado
from gestor_legajos.utils.persistencia import guardar_empresa
from gestor_legajos.controles.mi_text_button import MiTextButton
from gestor_legajos.controles.formulario_empleado import FormularioEmpleado
from gestor_legajos.state import global_state, State


class AgregarEmpleadoView(flet.Column):
    def __init__(self):
        self.empresa_seleccionada = global_state.get_state_by_key("empresa_seleccionada").get_state()
        self.boton_aceptar = MiTextButton(
            texto="Aceptar",
            on_click=self.agregar_empleado,
        )
        self.formulario_empleado = None
        super().__init__()

    def inicializar(self):
        self.formulario_empleado = FormularioEmpleado()
        self.controls = [
            flet.Row(
                controls=[
                    flet.Container(
                        content=flet.Text(
                            value="Agregar Empleado",
                            style=flet.TextThemeStyle.HEADLINE_MEDIUM
                        ),
                        expand=True,
                        padding=flet.padding.only(top=15),
                    ),
                    flet.Container(
                        content=self.boton_aceptar,
                        padding=flet.padding.only(right=50, top=15)
                    )
                ],
            ),
            self.formulario_empleado
        ]
        self.expand = True

    def notificar_empleado_no_valido(self):
        alert_dialog = flet.AlertDialog(
            title=flet.Text("Empleado ingresado no válido"),
            content=flet.Text("El empleado ingresado no es un empleado válido.\nPor favor intente de nuevo"),
        )
        self.page.open(alert_dialog)

    def notificar_empleado_agregado(self, empleado):
        notificacion = flet.SnackBar(
            content=flet.Text(f"El empleado {empleado.persona.apellido} {empleado.persona.nombre} "
                              f"fue agregado con éxito."),
            duration=3000
        )
        self.page.open(notificacion)

    def resetear_controles(self):
        self.formulario_empleado.numero_legajo.value = ""
        self.formulario_empleado.numero_legajo.error_text = None
        self.formulario_empleado.nombre.value = ""
        self.formulario_empleado.nombre.error_text = None
        self.formulario_empleado.apellido.value = ""
        self.formulario_empleado.apellido.error_text = None
        self.formulario_empleado.fecha_nacimiento.value = ""
        self.formulario_empleado.fecha_nacimiento.error_text = None
        self.formulario_empleado.nacionalidad.value = "Argentina"
        self.formulario_empleado.cuil.value = ""
        self.formulario_empleado.cuil.error_text = None
        self.formulario_empleado.sexo.value = "Masculino"
        self.formulario_empleado.estado_civil.value = "Soltero"
        self.formulario_empleado.fecha_ingreso.value = ""
        self.formulario_empleado.fecha_ingreso.error_text = None
        self.formulario_empleado.antiguedad.value = ""
        self.formulario_empleado.obra_social.value = ""
        self.formulario_empleado.obra_social.error_text = None
        self.formulario_empleado.categoria.value = ""
        self.formulario_empleado.categoria.error_text = None
        self.formulario_empleado.sueldo.value = ""
        self.formulario_empleado.sueldo.error_text = None
        self.formulario_empleado.calle.value = ""
        self.formulario_empleado.calle.error_text = None
        self.formulario_empleado.numero_calle.value = ""
        self.formulario_empleado.numero_calle.error_text = None
        self.formulario_empleado.piso.value = ""
        self.formulario_empleado.departamento.value = ""
        self.formulario_empleado.codigo_postal.value = "8400"
        self.formulario_empleado.localidad.value = "Bariloche"
        self.formulario_empleado.provincia.value = "Río Negro"
        self.formulario_empleado.telefono.value = ""
        self.formulario_empleado.correo_electronico.value = ""

    def agregar_empleado(self, e):
        empleado = Empleado(
            numero_legajo=self.formulario_empleado.numero_legajo.value,
            persona=Persona(
                nombre=self.formulario_empleado.nombre.value,
                apellido=self.formulario_empleado.apellido.value,
                fecha_nacimiento=self.formulario_empleado.fecha_nacimiento.value,
                nacionalidad=self.formulario_empleado.nacionalidad.value,
                cuil=self.formulario_empleado.cuil.value,
                domicilio=Domicilio(
                    calle=self.formulario_empleado.calle.value,
                    numero=self.formulario_empleado.numero_calle.value,
                    piso=self.formulario_empleado.piso.value,
                    departamento=self.formulario_empleado.departamento.value,
                    codigo_postal=self.formulario_empleado.codigo_postal.value,
                    localidad=self.formulario_empleado.localidad.value,
                    provincia=self.formulario_empleado.provincia.value,
                ),
                obra_social=self.formulario_empleado.obra_social.value,
                sexo=self.formulario_empleado.sexo.value,
                estado_civil=self.formulario_empleado.estado_civil.value,
                telefono=self.formulario_empleado.telefono.value,
                correo_electronico=self.formulario_empleado.correo_electronico.value,
            ),
            fecha_ingreso=self.formulario_empleado.fecha_ingreso.value,
            antiguedad=self.formulario_empleado.antiguedad.value,
            sueldo=self.formulario_empleado.sueldo.value,
            categoria=self.formulario_empleado.categoria.value,
        )

        if validar_empleado(empleado):
            self.empresa_seleccionada.agregar_empleado(empleado)
            guardar_empresa(self.empresa_seleccionada)
            self.notificar_empleado_agregado(empleado)
            self.resetear_controles()
            self.page.update()
        else:
            self.notificar_empleado_no_valido()
