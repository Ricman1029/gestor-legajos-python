import flet as ft
from pydantic import ValidationError
from src.core.database import get_db
from src.data.repositories.empresa_repository import EmpresaRepository
from src.domain.schemas.empresa_schema import EmpresaCreate
from src.ui.components.empresa_card import EmpresaCard

class EmpresasPage(ft.Column):
    def __init__(self):
        super().__init__()
        self.expand = True

        # --- 1. REFERENCIAS A INPUTS ---
        self.txt_razon_social = ft.TextField(label="Razón Social", expand=True)
        self.txt_cuit = ft.TextField(label="CUIT (sólo números)",max_length=11, expand=True)
        self.txt_convenio = ft.TextField(label="Convenio", expand=True)

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

        # --- 2. EL DIÁLOGO ---
        self.dialogo = ft.AlertDialog(
                title=ft.Text("Nueva Empresa"),
                content=ft.Column(
                    width=600,
                    tight=True,
                    scroll=ft.ScrollMode.AUTO,
                    controls=[
                        ft.Text("Datos Fiscales", weight=ft.FontWeight.BOLD),
                        ft.Row([self.txt_razon_social, self.txt_cuit]),
                        self.txt_convenio,
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

                if not empresas:
                    self.empty_state.visible = True
                else:
                    # Generamos una carta por cada empresa
                    for empresa in empresas:
                        card = EmpresaCard(
                                empresa=empresa,
                                on_edit=self.editar_empresa,
                                on_delete=self.borrar_empresa
                                )
                        self.grid.controls.append(card)
        except Exception as e:
            self.mostrar_error(f"Error cargando datos: {e}")
        finally:
            self.loading.visible = False
            self.update()

    # --- LÓGICA DEL FORMULARIO ---
    async def abrir_dialogo_crear(self, e):
        # Limpiamos los controles del diálogo
        self._limpiar_controles_dialogo()

        # 3. Abrir diálogo
        self.page.open(self.dialogo)
        self.page.update()

    async def cerrar_dialogo(self, e):
        self.page.close(self.dialogo)
        self.page.update()

    async def guardar_empresa(self, e):
        self._quitar_errores_controles_dialogo()
        self.dialogo.update()

        try:
            # Creamos un DTO (Data Transfer Object)
            # Pydantic va a validar longitudes, CUIT válido, etc.
            nueva_empresa_schema = EmpresaCreate(
                    razon_social=self.txt_razon_social.value,
                    cuit=self.txt_cuit.value,
                    convenio=self.txt_convenio.value,
                    calle=self.txt_calle.value,
                    numero=self.txt_numero.value,
                    piso=self.txt_piso.value,
                    depto=self.txt_depto.value,
                    localidad=self.txt_localidad.value,
                    provincia=self.txt_provincia.value,
                    codigo_postal=self.txt_codigo_postal.value,
                    telefono=self.txt_telefono.value,
                    mail=self.txt_mail.value,
                    )

            async for session in get_db():
                repositorio = EmpresaRepository(session)
                await repositorio.create(nueva_empresa_schema)

            # Cerramos el diálogo
            self.page.close(self.dialogo)
            self.update()

            # Recargamos la Grid
            self.page.open(ft.SnackBar(ft.Text("Empresa creada con éxito"), bgcolor=ft.Colors.GREEN))
            await self.cargar_datos()

        except ValidationError as ve:
            # --- MAPEAMOS LOS ERRORES PARA ACTUALIZAR LOS INPUTS ---
            mapa_errores = {
                    "razon_social": self.txt_razon_social,
                    "cuit": self.txt_cuit,
                    "convenio": self.txt_convenio,
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

        except Exception as ex:
            error_str = str(ex).lower()

            if "unique constraint" in error_str:
                if ".cuit" in error_str:
                    self.txt_cuit.error_text = "Este CUIT ya está registrado"
                    self.txt_cuit.update()
                elif ".razon_social" in error_str:
                    self.txt_razon_social.error_text = "Esta Razón Social ya existe"
                    self.txt_razon_social.update()
                else:
                    self.mostrar_error("Error de duplicado en la base de datos.")
            else:   
                self.mostrar_error(f"Error inesperado al guardar: {ex}")

    async def editar_empresa(self, id_empresa):
        print(f"Editando empresa {id_empresa}")

    async def borrar_empresa(self, id_empresa):
        print(f"Borrando empresa {id_empresa}")

    def mostrar_error(self, mensaje):
        self.page.open(ft.SnackBar(ft.Text(mensaje), bgcolor=ft.Colors.RED))
    
    def _limpiar_controles_dialogo(self):
        # 1. Limpiar campos anteriores
        todos_los_inputs = [
            self.txt_razon_social, self.txt_cuit, self.txt_convenio,
            self.txt_calle, self.txt_numero, self.txt_piso,
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
            self.txt_razon_social, self.txt_cuit, self.txt_convenio,
            self.txt_calle, self.txt_numero, self.txt_piso,
            self.txt_depto, self.txt_localidad, self.txt_provincia,
            self.txt_codigo_postal, self.txt_telefono, self.txt_mail,
            ]

        # 2. Reseteamos errores visuales
        for control in todos_los_inputs:
            control.error_text = None
