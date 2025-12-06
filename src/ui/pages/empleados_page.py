import flet as ft
from datetime import datetime
from pydantic import ValidationError
from src.core.database import get_db
from src.data.repositories.empleado_repository import EmpleadoRepository, EmpleadoCreate, EmpleadoUpdate
from src.domain.services.gestor_service import GestorLegajosService

class EmpleadosPage(ft.Column):
    def __init__(self):
        super().__init__()
        self.expand = True
        self.id_empleado_editar = None

        # --- 1. INPUTS DEL FORMULARIO ---
        # A. Contexto
        self.txt_empresa = ft.TextField(label="Empesa", read_only=True, expand=True)

        # B. Personales
        self.txt_nombre = ft.TextField(label="Nombre", expand=True)
        self.txt_apellido = ft.TextField(label="Apellido", expand=True)
        self.txt_cuil = ft.TextField(label="CUIL", expand=True)
        self.dd_sexo = ft.Dropdown(label="Sexo", options=[
            ft.dropdown.Option("Masculino"),
            ft.dropdown.Option("Femenino"),
            ft.dropdown.Option("X"),
            ], expand=True)
        self.txt_nacionalidad = ft.TextField(label="Nacionalidad", value="Argentina", expand=True)
        self.txt_nacimiento = ft.TextField(label="Fecha Nacimientod (DD/MM/AAAA)", expand=True)

        # C. Laborales
        self.txt_legajo = ft.TextField(label="Nro Legajo", expand=True)
        self.txt_ingreso = ft.TextField(label="Fecha Ingreso (DD/MM/AAAA)", expand=True)
        self.txt_sueldo = ft.TextField(label="Sueldo", prefix_text="$ ", expand=True)
        self.txt_categoria = ft.TextField(label="Categoría", expand=True)
        self.txt_obra_social = ft.TextField(label="Obra Social", expand=True)

        # D. Domicilio
        self.txt_calle = ft.TextField(label="Calle", expand=True)
        self.txt_numero = ft.TextField(label="Altura", expand=True)
        self.txt_piso = ft.TextField(label="Piso", expand=True)
        self.txt_depto = ft.TextField(label="Depto", expand=True)
        self.txt_localidad = ft.TextField(label="Localidad", expand=True)
        self.txt_provincia = ft.TextField(label="Provincia", expand=True)
        self.txt_codigo_postal = ft.TextField(label="Código Postal", expand=True)

        # E. Contacto
        self.txt_telefono = ft.TextField(label="Teléfono", expand=True)
        self.txt_mail = ft.TextField(label="Email", expand=True)

        # --- 2. EL DIÁLOGO CON TABS ---
        self.dialogo = ft.AlertDialog(
                title=ft.Text("Gestión de Legajo"),
                content=ft.Container(
                    width=700,
                    height=500,
                    content=ft.Tabs(
                        selected_index=0,
                        animation_duration=300,
                        tabs=[
                            ft.Tab(
                                text="General",
                                icon=ft.Icons.PERSON,
                                content=ft.Column([
                                    ft.Text("Filiación", weight=ft.FontWeight.BOLD),
                                    self.txt_empresa,
                                    ft.Row([self.txt_nombre, self.txt_apellido]),
                                    ft.Row([self.txt_cuil, self.dd_sexo]),
                                    ft.Row([self.txt_nacimiento, self.txt_nacionalidad]),
                                    ], scroll=ft.ScrollMode.AUTO, spacing=15)
                                ),
                            ft.Tab(
                                text="Laboral",
                                icon=ft.Icons.WORK,
                                content=ft.Column([
                                    ft.Text("Contratación", weight=ft.FontWeight.BOLD),
                                    ft.Row([self.txt_legajo, self.txt_ingreso]),
                                    ft.Row([self.txt_categoria, self.txt_sueldo]),
                                    self.txt_obra_social,
                                    ], scroll=ft.ScrollMode.AUTO, spacing=15)
                                ),
                            ft.Tab(
                                text="Domicilio",
                                icon=ft.Icons.HOME,
                                content=ft.Column([
                                    ft.Text("Ubicación y Contacto", weight=ft.FontWeight.BOLD),
                                    ft.Row([self.txt_calle, self.txt_numero]),
                                    ft.Row([self.txt_piso, self.txt_depto]),
                                    ft.Row([self.txt_localidad, self.txt_provincia]),
                                    ft.Row([self.txt_codigo_postal, self.txt_telefono]),
                                    self.txt_mail
                                    ], scroll=ft.ScrollMode.AUTO, spacing=15)
                                ),
                            ],
                        expand=True
                        )
                    ),
                actions=[
                    ft.TextButton("Cancelar", on_click=self.cerrar_dialogo),
                    ft.ElevatedButton(
                        "Guardar Legajo",
                        on_click=self.guardar_empleado,
                        bgcolor=ft.Colors.BLUE,
                        color=ft.Colors.WHITE
                        )
                    ],
                actions_alignment=ft.MainAxisAlignment.END
                )

        # --- 3. DIÁLOGO DE BAJA LÓGICA ---
        self.txt_fecha_baja = ft.TextField(label="Fecha de Egreso (DD/MM/AAAA)")
        self.id_empleado_baja = None

        self.dialogo_baja = ft.AlertDialog(
                title=ft.Text("Regsitrar Baja"),
                content=ft.Column([
                    ft.Text("Ingrese la fecha de egreso para dar de baja el empleado.\n\
                            El legajo quedará inactivo pero no se borrará."),
                    self.txt_fecha_baja
                    ], tight=True),
                actions=[
                    ft.TextButton("Cancelar", on_click=self.cerrar_dialogo_baja),
                    ft.ElevatedButton(
                        "Confirmar Baja",
                        on_click=self.confirmar_baja,
                        bgcolor=ft.Colors.RED,
                        color=ft.Colors.WHITE
                        )
                    ],
                actions_alignment=ft.MainAxisAlignment.END
                )

        # --- 4. DIALOGO DE REACTIVACIÓN ---
        self.dialogo_reactivar = ft.AlertDialog(
                title=ft.Text("Reactivar Legajo"),
                content=self.txt_ingreso,
                actions=[
                    ft.TextButton("Cancelar", on_click=self.cerrar_dialogo_reactivacion), 
                    ft.ElevatedButton(
                        "Confirmar Reactivación",
                        on_click=self.confirmar_reactivacion,
                        bgcolor=ft.Colors.GREEN,
                        color=ft.Colors.WHITE
                        )
                    ],
                actions_alignment=ft.MainAxisAlignment.END
                )

        self.titulo = ft.Text("Empleados", size=24, weight=ft.FontWeight.BOLD)
        self.subtitulo = ft.Text("Seleccione una empresa para ver sus empleados", color=ft.Colors.GREY)

        self.boton_agregar = ft.FloatingActionButton(
                icon=ft.Icons.ADD,
                text="Nuevo Legajo",
                on_click=self.abrir_crear,
                visible=False
                )

        self.header = ft.Row(
                controls=[
                    ft.Column([self.titulo, self.subtitulo], spacing=2),
                    ft.Container(expand=True),  
                    self.boton_agregar
                    ]
                )

        self.tabla = ft.DataTable(
                columns=[
                    ft.DataColumn(ft.Text("Legajo")),
                    ft.DataColumn(ft.Text("Apellido y Nombre")),
                    ft.DataColumn(ft.Text("CUIL")),
                    ft.DataColumn(ft.Text("Categoría")),
                    ft.DataColumn(ft.Text("Estado")),
                    ft.DataColumn(ft.Text("Acciones")),
                    ],
                rows=[],
                border=ft.border.all(1, ft.Colors.GREY_300),
                vertical_lines=ft.border.all(1, ft.Colors.GREY_100),
                heading_row_color=ft.Colors.GREY_100,
                expand=True
                )

        self.tabla_container = ft.Column(
                controls=[self.tabla],
                scroll=ft.ScrollMode.ADAPTIVE,
                expand=True
                )

        self.loading = ft.ProgressBar(visible=False)

        self.controls = [self.header, ft.Divider(), self.loading, self.tabla_container]

    def did_mount(self):
        self.page.run_task(self.cargar_datos)

    async def cargar_datos(self):
        self.loading.visible = True
        self.tabla.rows.clear()
        self.update()

        try:
            empresa_id = self.page.session.get("empresa_seleccionada_id")
            razon_social = self.page.session.get("empresa_seleccionada_nombre")

            if not empresa_id:
                self.subtitulo.value = "Seleccione una empresa desde el menú 'Empresas'"
                self.boton_agregar.visible = False
                self.update()
                return

            self.titulo.value = f"Nómina: {razon_social}"
            self.subtitulo.value = "Listado de personal activo"
            self.boton_agregar.visible = True

            async for session in get_db():
                repositorio = EmpleadoRepository(session)
                empleados = await repositorio.get_by_empresa(empresa_id)

                for empleado in empleados:
                    es_inactivo = empleado.fecha_egreso is not None
                    color_fila = ft.Colors.PINK_200 if es_inactivo else None

                    texto_estado = f"Baja: {empleado.fecha_egreso.strftime("%d/%m/%Y")}" if es_inactivo \
                            else f"Alta: {empleado.fecha_ingreso.strftime("%d/%m/%Y")}"

                    if es_inactivo:
                        boton_accion = ft.IconButton(
                                icon=ft.Icons.RESTORE_FROM_TRASH,
                                icon_color=ft.Colors.GREEN,
                                tooltip="Reactivar Legajo",
                                data=empleado.id,
                                on_click=self.boton_reactivar_click
                                )
                    else:
                        boton_accion = ft.IconButton(
                                icon=ft.Icons.DELETE,
                                icon_color=ft.Colors.RED,
                                tooltip="Registrar Baja",
                                data=empleado.id,
                                on_click=self.boton_borrar_click
                                )


                    row = ft.DataRow(
                            color=color_fila,
                            cells=[
                                ft.DataCell(ft.Text(empleado.numero_legajo or "-")),
                                ft.DataCell(ft.Text(f"{empleado.apellido}, {empleado.nombre}", weight=ft.FontWeight.BOLD)),
                                ft.DataCell(ft.Text(empleado.cuil)),
                                ft.DataCell(ft.Text(empleado.categoria)),
                                ft.DataCell(ft.Text(texto_estado, size=12)),
                                ft.DataCell(
                                    ft.Row([
                                        ft.IconButton(
                                            ft.Icons.PICTURE_AS_PDF, 
                                            icon_color=ft.Colors.GREEN, 
                                            tooltip="Contrato",
                                            data=empleado.id,
                                            on_click=self.boton_generar_contrato_click
                                            ),
                                        ft.IconButton(
                                            ft.Icons.EDIT, 
                                            icon_color=ft.Colors.BLUE, 
                                            tooltip="Editar",
                                            data=empleado.id,
                                            on_click=self.boton_editar_click
                                            ),
                                        boton_accion
                                        ])
                                    ),
                                ]
                            )
                    self.tabla.rows.append(row)

        except Exception as e:
            self.page.open(ft.SnackBar(ft.Text(f"Error: {e}"), bgcolor=ft.Colors.RED))
        finally:
            self.loading.visible = False
            self.update()


    async def generar_contrato(self, e):
        print("Genera contrato")
        pass

    async def abrir_crear(self, e):
        self.id_empleado_editar = None
        self.dialogo.title = ft.Text("Nuevo Legajo")
        self._limpiar_formulario()

        nombre_empresa = self.page.session.get("empresa_seleccionada_nombre")
        self.txt_empresa.value = nombre_empresa

        self.page.open(self.dialogo)
        self.page.update()

    async def cerrar_dialogo(self, e):
        self.page.close(self.dialogo)
    
    async def guardar_empleado(self, e):
        self._quitar_errores_formulario()

        try:
            empresa_id = self.page.session.get("empresa_seleccionada_id")
            if not empresa_id:
                self.page.open(ft.SnackBar(ft.Text("Error de sesión: No hay emprsa seleccinada"), bgcolor=ft.Colors.RED))
                return

            def parse_date(str_date):
                if not str_date: return None
                return datetime.strptime(str_date, "%d/%m/%Y").date()

            fecha_nacimiento = None
            fecha_ingreso = None

            try: 
                fecha_nacimiento = parse_date(self.txt_nacimiento.value)
                fecha_ingreso = parse_date(self.txt_ingreso.value)
            except ValueError:
                self.page.open(ft.SnackBar(ft.Text("Error en fechas: Use formato DD/MM/AAAA"), bgcolor=ft.Colors.RED))
                return

            datos_empleado = {
                    "nombre": self.txt_nombre.value,
                    "apellido": self.txt_apellido.value,
                    "dni": self.txt_cuil.value[3:11],
                    "cuil": self.txt_cuil.value,
                    "sexo": self.dd_sexo.value or "",
                    "nacionalidad": self.txt_nacionalidad.value,
                    "fecha_nacimiento": fecha_nacimiento,
                    "numero_legajo": self.txt_legajo.value,
                    "fecha_ingreso": fecha_ingreso,
                    "fecha_egreso": None,
                    "sueldo": float(self.txt_sueldo.value or 0),
                    "categoria": self.txt_categoria.value,
                    "obra_social": self.txt_obra_social.value,
                    "calle": self.txt_calle.value,
                    "numero": self.txt_numero.value,
                    "piso": self.txt_piso.value,
                    "depto": self.txt_depto.value,
                    "localidad": self.txt_localidad.value,
                    "provincia": self.txt_provincia.value,
                    "codigo_postal": self.txt_codigo_postal.value,
                    "telefono": self.txt_telefono.value
                    }

            async for session in get_db():
                repositorio = EmpleadoRepository(session)

                if self.id_empleado_editar:
                    update_schema = EmpleadoUpdate(**datos_empleado)
                    await repositorio.update(self.id_empleado_editar, update_schema)
                    mensaje = "Legajo Actualizado"
                else:
                    datos_empleado["empresa_id"] = empresa_id
                    create_schema = EmpleadoCreate(**datos_empleado)
                    await repositorio.create(create_schema)
                    mensaje = "Legajo Creado"

            self.page.close(self.dialogo)
            self.page.open(ft.SnackBar(ft.Text(mensaje), bgcolor=ft.Colors.GREEN))
            await self.cargar_datos()
        
        except ValidationError as ve:
            self.page.open(ft.SnackBar(ft.Text(f"Error validación: {ve}"), bgcolor=ft.Colors.RED))
        except Exception as ex:
            self.page.open(ft.SnackBar(ft.Text(f"Error: {ex}"), bgcolor=ft.Colors.RED))

    async def boton_generar_contrato_click(self, e):
        id_empleado = e.control.data
        self.page.open(ft.SnackBar(ft.Text(f"Generando contrato ID {id_empleado}..."), bgcolor=ft.Colors.BLUE))
        
    async def boton_editar_click(self, e):
        self.id_empleado_editar = e.control.data
        self.dialogo.title = ft.Text("Editar Legajo")
        self.txt_empresa.value = self.page.session.get("empresa_seleccionada_nombre")

        async for session in get_db():
            repositorio = EmpleadoRepository(session)
            empleado = await repositorio.get_by_id(self.id_empleado_editar)
            if empleado:
                    self.txt_nombre.value = empleado.nombre
                    self.txt_apellido.value = empleado.apellido
                    self.txt_cuil.value = empleado.cuil
                    self.dd_sexo.value = empleado.sexo
                    self.txt_nacionalidad.value = empleado.nacionalidad
                    self.txt_nacimiento.value = empleado.fecha_nacimiento.strftime("%d/%m/%Y") if empleado.fecha_nacimiento else ""

                    self.txt_legajo.value = empleado.numero_legajo
                    self.txt_ingreso.value = empleado.fecha_ingreso.strftime("%d/%m/%Y") if empleado.fecha_ingreso else ""
                    self.txt_sueldo.value = empleado.sueldo
                    self.txt_categoria.value = empleado.categoria
                    self.txt_obra_social.value = empleado.obra_social

                    self.txt_calle.value = empleado.calle
                    self.txt_numero.value = empleado.numero
                    self.txt_piso.value = empleado.piso or ""
                    self.txt_depto.value = empleado.depto or ""
                    self.txt_localidad.value = empleado.localidad
                    self.txt_provincia.value = empleado.provincia
                    self.txt_codigo_postal.value = empleado.codigo_postal
                    self.txt_telefono.value = empleado.telefono or ""

                    self.page.open(self.dialogo)
                    self.page.update()

    async def boton_borrar_click(self, e):
        self.id_empleado_baja = e.control.data
        self.txt_fecha_baja.value = datetime.today().strftime("%d/%m/%Y")
        self.page.open(self.dialogo_baja)
        self.page.update()

    async def cerrar_dialogo_baja(self, e):
        self.page.close(self.dialogo_baja)

    async def cerrar_dialogo_reactivacion(self, e):
        self.page.close(self.dialogo_reactivar)

    async def confirmar_baja(self, e):
        try:
            fecha_egreso = datetime.strptime(self.txt_fecha_baja.value, "%d/%m/%Y").date()

            async for session in get_db():
                repositorio = EmpleadoRepository(session)
                update_schema = EmpleadoUpdate(fecha_egreso=fecha_egreso)
                await repositorio.update(self.id_empleado_baja, update_schema)
                
            self.page.close(self.dialogo_baja)
            self.page.open(ft.SnackBar(ft.Text("Baja registrada con éxito"), bgcolor=ft.Colors.ORANGE))
            await self.cargar_datos()

        except ValueError:
            self.txt_fecha_baja.error_text = "Formato inválido (DD/MM/AAAA)"

    async def boton_reactivar_click(self, e):
        self.id_empleado_accion = e.control.data
        self.page.open(self.dialogo_reactivar)
        self.page.update()

    async def confirmar_reactivacion(self, e):
        try:
            fecha_ingreso = datetime.strptime(self.txt_ingreso.value, "%d/%m/%Y").date()
            async for session in get_db():
                repositorio = EmpleadoRepository(session)
                update_schema = EmpleadoUpdate(fecha_egreso=None, fecha_ingreso=fecha_ingreso)
                await repositorio.update(self.id_empleado_accion, update_schema)

            self.page.close(self.dialogo_reactivar)
            self.page.open(ft.SnackBar(ft.Text("Empleado reactivado con éxito"), bgcolor=ft.Colors.GREEN))
            await self.cargar_datos()

        except Exception as ex:
            self.page.open(ft.SnackBar(ft.Text(f"Error al reactivar {ex}"), bgcolor=ft.Colors.RED))

    def _limpiar_formulario(self):
        inputs = [
            self.txt_nombre, self.txt_apellido, self.txt_cuil, self.dd_sexo,
            self.txt_nacionalidad, self.txt_nacimiento, self.txt_legajo, self.txt_ingreso,
            self.txt_sueldo, self.txt_categoria, self.txt_obra_social, self.txt_calle,
            self.txt_numero, self.txt_piso, self.txt_depto, self.txt_localidad,
            self.txt_provincia, self.txt_codigo_postal, self.txt_telefono, self.txt_mail,
                ]
        for control in inputs:
            control.value = ""
            control.error_text = None

    def _quitar_errores_formulario(self):
        inputs = [
            self.txt_nombre, self.txt_apellido, self.txt_cuil, self.dd_sexo,
            self.txt_nacionalidad, self.txt_nacimiento, self.txt_legajo, self.txt_ingreso,
            self.txt_sueldo, self.txt_categoria, self.txt_obra_social, self.txt_calle,
            self.txt_numero, self.txt_piso, self.txt_depto, self.txt_localidad,
            self.txt_provincia, self.txt_codigo_postal, self.txt_telefono, self.txt_mail,
                ]
        for control in inputs:
            control.error_text = None
