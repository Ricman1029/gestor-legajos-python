import flet as ft
from pydantic import ValidationError
from src.core.database import get_db
from src.data.repositories.empresa_repository import EmpresaRepository
from src.data.repositories.parametricos_repository import ArtRepository, ConvenioRepository
from src.domain.schemas.empresa_schema import EmpresaCreate, EmpresaUpdate
from src.ui.components.empresa_card import EmpresaCard

class EmpresasPage(ft.Column):
    def __init__(self, on_seleccionar_empresa: callable):
        super().__init__()
        self.on_seleccionar_empresa = on_seleccionar_empresa
        self.expand = True
        self.id_empresa_editar = None

        # --- INPUTS ---
        self.txt_razon_social = ft.TextField(label="Razón Social", expand=True)
        self.txt_cuit = ft.TextField(label="CUIT (sólo números)",max_length=11, expand=True)
        self.txt_ieric = ft.TextField(label="Número de IERIC (solo empresas constructoras)", expand=True)

        self.lv_convenios = ft.Column(scroll=ft.ScrollMode.AUTO, height=150)
        self.text_error_convenio = ft.Text("", color=ft.Colors.ERROR, size=12, visible=False)
        self.borde_convenios = ft.Container(
                content=self.lv_convenios,
                border=ft.border.all(1, ft.Colors.GREY_400),
                border_radius=5,
                padding=5,
                )
        self.container_convenios = ft.Container(
                content=ft.Column([
                    ft.Text("Convenios y Sindicatos:", weight=ft.FontWeight.BOLD),
                    self.borde_convenios,
                    self.text_error_convenio
                    ])
                )

        self.dd_art = ft.Dropdown(label="A.R.T.", expand=True)

        # Ubicación
        self.txt_calle = ft.TextField(label="Calle", expand=True)
        self.txt_numero = ft.TextField(label="Altura", width=100)
        self.txt_piso = ft.TextField(label="Piso", expand=True)
        self.txt_depto = ft.TextField(label="Depto.", expand=True)
        self.txt_localidad = ft.TextField(label="Localidad", expand=True)
        self.txt_provincia = ft.TextField(label="Provincia", expand=True)
        self.txt_codigo_postal = ft.TextField(label="Código Postal", width=100)

        # Contacto
        self.txt_telefono = ft.TextField(label="Teléfono", expand=True)
        self.txt_mail = ft.TextField(label="Email", expand=True)

        # --- EL DIÁLOGO ---
        self.dialogo_borrar = ft.AlertDialog(
                title=ft.Text("Confirmar eliminación"),
                content=ft.Text("¿Estás seguro de que deseas eliminar esta empresa? Esta acción no se puede deshacer."),
                actions=[
                    ft.TextButton("Cancelar", on_click=self.cerrar_dialogo_borrar),
                    ft.TextButton("Eliminar", on_click=self.confirmar_borrado, style=ft.ButtonStyle(color=ft.Colors.RED)),
                    ],
                actions_alignment=ft.MainAxisAlignment.END
                )
        self.id_a_borrar = None

        self.dialogo = ft.AlertDialog(
                title=ft.Text("Nueva Empresa"),
                content=ft.Column(
                    width=600,
                    tight=True,
                    scroll=ft.ScrollMode.AUTO,
                    controls=[
                        ft.Text("Datos Fiscales", weight=ft.FontWeight.BOLD),
                        ft.Row([self.txt_razon_social, self.txt_cuit]),
                        ft.Row([self.dd_art, self.txt_ieric]),
                        ft.Divider(),
                        self.container_convenios,
                        ft.Divider(),
                        ft.Text("Ubicación", weight=ft.FontWeight.BOLD),
                        ft.Row([self.txt_calle, self.txt_numero]),
                        ft.Row([self.txt_piso, self.txt_depto, self.txt_codigo_postal]),
                        ft.Row([self.txt_localidad, self.txt_provincia]),
                        ft.Divider(),
                        ft.Text("Contacto", weight=ft.FontWeight.BOLD),
                        ft.Row([self.txt_telefono, self.txt_mail]),
                        ]
                    ),
                actions=[
                    ft.TextButton("Cancelar", on_click=self.cerrar_dialogo),
                    ft.ElevatedButton(
                        "Guardar", 
                        on_click=self.guardar_empresa, 
                        bgcolor=ft.Colors.BLUE, 
                        color=ft.Colors.WHITE
                        )
                    ],
                actions_alignment=ft.MainAxisAlignment.END,
                )

        # --- 3. UI PRINCIPAL ---
        self.header = ft.Row(
                controls=[
                    ft.Text("Listado de Empresas", size=24, weight=ft.FontWeight.BOLD),
                    ft.Container(expand=True),
                    ft.FloatingActionButton(
                        icon=ft.Icons.ADD,
                        text="Nueva Empresa",
                        on_click=self.abrir_dialogo_crear
                        )
                    ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                )

        self.grid = ft.GridView(
                expand=True,
                runs_count=5,
                max_extent=300,
                child_aspect_ratio=1.4,
                spacing=20,
                run_spacing=20,
                padding=20,
                )

        self.loading = ft.ProgressBar(visible=False)

        # Si no hay empresas, mostramos un mensaje
        self.empty_state = ft.Container(
                visible=False,
                alignment=ft.alignment.center,
                content=ft.Column(
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        ft.Icon(ft.Icons.BUSINESS_OUTLINED, size=60, color=ft.Colors.GREY_300),
                        ft.Text("No hay empresas todavía", color=ft.Colors.GREY_500)
                        ]
                    )
                )

        self.controls = [
                self.header,
                ft.Divider(),
                self.loading,
                self.empty_state,
                self.grid
                ]

    def did_mount(self):
        self.page.run_task(self.cargar_datos)

    async def cargar_datos(self):
        self.grid.controls.clear()
        self.loading.visible = True
        self.empty_state.visible = False
        self.update()

        try: 
            async for session in get_db():
                repositorio = EmpresaRepository(session)
                empresas = await repositorio.get_all()

                self.empty_state.visible = not empresas
                # Generamos una carta por cada empresa
                for empresa in empresas:
                    card = EmpresaCard(
                            empresa=empresa,
                            on_edit=self.editar_empresa,
                            on_delete=self.borrar_empresa,
                            on_ver_empleados=self.navegar_a_empleados,
                            )
                    self.grid.controls.append(card)
        except Exception as e:
            self._mostrar_mensaje(f"Error cargando datos: {e}", ft.Colors.RED)
        finally:
            self.loading.visible = False
            self.update()

    async def _cargar_parametricos(self):
        self.dd_art.options.clear()
        self.lv_convenios.controls.clear()

        async for session in get_db():
            repositorio_art = ArtRepository(session)
            arts = await repositorio_art.get_all()
            for art in arts:
                self.dd_art.options.append(ft.dropdown.Option(str(art.id), art.nombre))

            repositorio_convenio = ConvenioRepository(session)
            convenios = await repositorio_convenio.get_all_con_sindicato()
            for convenio in convenios:
                nombre_sindicato = convenio.sindicato_rel.nombre if convenio.sindicato_rel else "Sin Sindicato"
                label_texto = f"{nombre_sindicato} - {convenio.nombre}"

                checkbox = ft.Checkbox(label=label_texto, value=False, data=convenio.id)
                self.lv_convenios.controls.append(checkbox)


    # --- LÓGICA DEL FORMULARIO ---
    async def abrir_dialogo_crear(self, e):
        self.id_empresa_editar = None
        self.dialogo.title = ft.Text("Nueva Empresa")
        self._limpiar_controles_dialogo()

        await self._cargar_parametricos()

        # 3. Abrir diálogo
        self.page.open(self.dialogo)
        self.page.update()

    async def cerrar_dialogo(self, e):
        self.page.close(self.dialogo)
        self.page.update()

    async def guardar_empresa(self, e):
        self._quitar_errores_controles_dialogo()
        self.dialogo.update()

        ids_convenios = [convenio.data for convenio in self.lv_convenios.controls if convenio.value]

        try:
            datos = {
                    "razon_social": self.txt_razon_social.value,
                    "cuit": self.txt_cuit.value,
                    "art_id": int(self.dd_art.value) if self.dd_art.value else 0,
                    "convenios_ids": ids_convenios,
                    "numero_ieric": self.txt_ieric.value,
                    "calle": self.txt_calle.value,
                    "numero": self.txt_numero.value,
                    "piso": self.txt_piso.value,
                    "depto": self.txt_depto.value,
                    "localidad": self.txt_localidad.value,
                    "provincia": self.txt_provincia.value,
                    "codigo_postal": self.txt_codigo_postal.value,
                    "telefono": self.txt_telefono.value,
                    "mail": self.txt_mail.value,
                    }

            async for session in get_db():
                repositorio = EmpresaRepository(session)
                if self.id_empresa_editar:
                    await repositorio.update(self.id_empresa_editar, EmpresaUpdate(**datos))
                else:
                    await repositorio.create(EmpresaCreate(**datos))

            # Cerramos el diálogo
            self.page.close(self.dialogo)
            self._mostrar_mensaje("Empresa creada con éxito", ft.Colors.GREEN)
            await self.cargar_datos()

        except ValidationError as ve:
            self._mapear_errores(ve)

        except Exception as ex:
            self._mostrar_error_db(ex)

    async def editar_empresa(self, id_empresa):
        self.loading.visible = True
        self.update()
        try:
            async for session in get_db():
                repositorio = EmpresaRepository(session)
                empresa = await repositorio.get_para_edicion(id_empresa)

                if not empresa:
                    self._mostrar_mensaje("No se encontró las empresa", ft.Colors.RED)
                    return

                await self._cargar_parametricos()

                # Llenamos los inputs con los datos de la DB
                self.id_empresa_editar = id_empresa
                self.dialogo.title = ft.Text("Editar Empresa")

                self.txt_razon_social.value = empresa.razon_social
                self.txt_cuit.value = empresa.cuit
                self.txt_ieric.value = empresa.numero_ieric
                self.dd_art.value = str(empresa.art_rel.id)
                self.txt_calle.value = empresa.calle
                self.txt_numero.value = empresa.numero
                self.txt_piso.value = empresa.piso
                self.txt_depto.value = empresa.depto
                self.txt_localidad.value = empresa.localidad
                self.txt_provincia.value = empresa.provincia
                self.txt_codigo_postal.value = empresa.codigo_postal
                self.txt_telefono.value = empresa.telefono
                self.txt_mail.value = empresa.mail

                ids_actuales = [convenio.id for convenio in empresa.convenios]
                for checkbox in self.lv_convenios.controls:
                    checkbox.value = checkbox.data in ids_actuales


                self._quitar_errores_controles_dialogo()
                self.page.open(self.dialogo)
                
        except Exception as e:
            self._mostrar_mensaje(f"Error al cargar edición: {e}", ft.Colors.RED)
        finally:
            self.loading.visible = False
            self.update()

    async def borrar_empresa(self, id_empresa):
        self.id_a_borrar = id_empresa
        self.page.open(self.dialogo_borrar)

    async def cerrar_dialogo_borrar(self, e):
        self.id_a_borrar = None
        self.page.close(self.dialogo_borrar)

    async def confirmar_borrado(self, e):
        if not self.id_a_borrar: return

        try:
            self.page.close(self.dialogo_borrar)
            self.loading.visible = True
            self.update()

            async for session in get_db():
                repositorio = EmpresaRepository(session)
                await repositorio.delete(self.id_a_borrar)

            self._mostrar_mensaje("Empresa eliminada", ft.Colors.GREEN)
            await self.cargar_datos()

        except Exception as ex:
            self._mostrar_mensaje(f"Error al borrar: {ex}", ft.Colors.RED)
        finally:
            self.id_a_borrar = None
            self.loading.visible = False
            self.update()

    async def navegar_a_empleados(self, empresa_obj):
        if self.on_seleccionar_empresa:
            await self.on_seleccionar_empresa(empresa_obj)

    def _mapear_errores(self, ve):
            mapa_errores = {
                    "razon_social": self.txt_razon_social,
                    "cuit": self.txt_cuit,
                    "art_id": self.dd_art,
                    "numero_ieric": self.txt_ieric,
                    "calle": self.txt_calle,
                    "numero": self.txt_numero,
                    "piso": self.txt_piso,
                    "depto": self.txt_depto,
                    "localidad": self.txt_localidad,
                    "provincia": self.txt_provincia,
                    "codigo_postal": self.txt_codigo_postal,
                    "telefono": self.txt_telefono,
                    "mail": self.txt_mail,
                    }

            errores = ve.errors()
            for error in errores:
                nombre_campo = error["loc"][0]
                mensaje = error["msg"]

                # Buscamos el input que tiene error y lo pintamos
                if nombre_campo in mapa_errores:
                    input_flet = mapa_errores[nombre_campo]
                    input_flet.error_text = mensaje
                    input_flet.update()

                elif nombre_campo == "convenios_ids":
                    self.borde_convenios.border = ft.border.all(1, ft.Colors.ERROR)
                    self.borde_convenios.update()

                    self.text_error_convenio.value = "Debe seleccionar al menos un convenio"
                    self.text_error_convenio.visible = True
                    self.text_error_convenio.update()

    def _mostrar_error_db(self, ex):
        error_str = str(ex).lower()

        if "unique constraint" in error_str:
            if ".cuit" in error_str:
                self.txt_cuit.error_text = "Este CUIT ya está registrado"
                self.txt_cuit.update()
            elif ".razon_social" in error_str:
                self.txt_razon_social.error_text = "Esta Razón Social ya existe"
                self.txt_razon_social.update()
            else:
                self._mostrar_mensaje("Error de duplicado en la base de datos.", ft.Colors.RED)
        else:   
            self._mostrar_mensaje(f"Error inesperado al guardar: {ex}", ft.Colors.RED)

    def _mostrar_mensaje(self, mensaje, color):
        self.page.open(ft.SnackBar(ft.Text(mensaje), bgcolor=color))
    
    def _limpiar_controles_dialogo(self):
        # 1. Limpiar campos anteriores
        todos_los_inputs = [
            self.txt_razon_social, self.txt_cuit, self.dd_art,
            self.txt_ieric, self.txt_calle, self.txt_numero, self.txt_piso,
            self.txt_depto, self.txt_localidad, self.txt_provincia,
            self.txt_codigo_postal, self.txt_telefono, self.txt_mail,
            ]

        # 2. Reseteamos errores visuales
        for control in todos_los_inputs:
            control.value = ""
            control.error_text = None

    def _quitar_errores_controles_dialogo(self):
        # 1. Limpiar campos anteriores
        todos_los_inputs = [
            self.txt_razon_social, self.txt_cuit, self.dd_art,
            self.txt_ieric, self.txt_calle, self.txt_numero, self.txt_piso,
            self.txt_depto, self.txt_localidad, self.txt_provincia,
            self.txt_codigo_postal, self.txt_telefono, self.txt_mail,
            ]

        # 2. Reseteamos errores visuales
        for control in todos_los_inputs:
            control.error_text = None

        self.borde_convenios.border = ft.border.all(1, ft.Colors.GREY_400)
        # self.borde_convenios.update()

        self.text_error_convenio.value = ""
        self.text_error_convenio.visible = False
        # self.text_error_convenio.update()
