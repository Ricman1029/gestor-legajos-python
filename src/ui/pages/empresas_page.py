import flet as ft
from src.core.database import get_db
from src.data.repositories.empresa_repository import EmpresaRepository
from src.ui.components.empresa_card import EmpresaCard

class EmpresasPage(ft.Column):
    def __init__(self):
        super().__init__()
        self.expand = True

        # 1. Creamos un header para la página
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

        # 2. Armamos una Grid para disponer las tarjetas de empresas
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
            self.page.open(
                    ft.SnackBar(ft.Text(f"Error: {e}"), bgcolor=ft.Colors.RED)
                    )
        finally:
            self.loading.visible = False
            self.update()

    async def abrir_dialogo_crear(self, e):
        print("Crear empresa")

    async def editar_empresa(self, id_empresa):
        print(f"Editando empresa {id_empresa}")

    async def borrar_empresa(self, id_empresa):
        print(f"Borrando empresa {id_empresa}")
