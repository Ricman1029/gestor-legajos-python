import flet as ft
from src.core.database import get_db
from src.data.repositories.empleado_repository import EmpleadoRepository
from src.domain.services.gestor_service import GestorLegajosService

class EmpleadosPage(ft.Column):
    def __init__(self):
        super().__init__()
        self.expand = True

        # 1. Header Dinámico 
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

        # 2. La tabla
        self.tabla = ft.DataTable(
                columns=[
                    ft.DataColumn(ft.Text("Legajo")),
                    ft.DataColumn(ft.Text("Apellido y Nombre")),
                    ft.DataColumn(ft.Text("CUIL")),
                    ft.DataColumn(ft.Text("Categoría")),
                    ft.DataColumn(ft.Text("Ingreso")),
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
                    row = ft.DataRow(
                            cells=[
                                ft.DataCell(ft.Text(empleado.numero_legajo or "-")),
                                ft.DataCell(ft.Text(f"{empleado.apellido}, {empleado.nombre}", weight=ft.FontWeight.BOLD)),
                                ft.DataCell(ft.Text(empleado.cuil)),
                                ft.DataCell(ft.Text(empleado.categoria)),
                                ft.DataCell(ft.Text(empleado.fecha_ingreso.strftime("%d/%m/%Y"))),
                                ft.DataCell(
                                    ft.Row([
                                        ft.IconButton(
                                            ft.Icons.PICTURE_AS_PDF, 
                                            icon_color=ft.Colors.GREEN, 
                                            tooltip="Contrato",
                                            data=empleado.id,
                                            on_click=self.generar_contrato
                                            ),
                                        ft.IconButton(
                                            ft.Icons.EDIT, 
                                            icon_color=ft.Colors.BLUE, 
                                            tooltip="Editar",
                                            data=empleado.id,
                                            on_click=self.editar
                                            ),
                                        ft.IconButton(
                                            ft.Icons.DELETE, 
                                            icon_color=ft.Colors.RED, 
                                            tooltip="Baja",
                                            data=empleado.id,
                                            on_click=self.borrar
                                            ),
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
        print("Crear")
    
    async def editar(self, e):
        print(f"Editar")

    async def borrar(self, e):
        print(f"Borrar")
