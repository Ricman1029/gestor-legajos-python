from sqlalchemy.exc import IntegrityError
import flet as ft
from src.core.database import get_db
from src.data.models.parametricos_model import Convenio, Categoria
from src.data.repositories.parametricos_repository import ConvenioRepository, CategoriaRepository

class ConfigPage(ft.Column):
    def __init__(self):
        super().__init__()
        self.expand = True

        self.convenio_seleccionado_id = None
        self.convenio_seleccionado_nombre = ""

        self.txt_convenio = ft.TextField(label="Nuevo Convenio", expand=True)
        self.boton_agregar_convenio = ft.IconButton(ft.Icons.ADD, on_click=self.agregar_convenio)
        self.lista_convenios = ft.ListView(expand=True, spacing=10)

        self.label_categoria = ft.Text("Categorías", weight=ft.FontWeight.BOLD, size=16)
        self.txt_categoria = ft.TextField(
                label="Nueva Categoría",
                disabled=True,
                hint_text="Seleccione un convenio...",
                expand=True,
                )
        self.boton_agregar_categoria = ft.IconButton(
                icon=ft.Icons.ADD,
                icon_color=ft.Colors.GREEN,
                on_click=self.agregar_categoria,
                tooltip="Agregar",
                disabled=True,
                )
        self.lista_categorias = ft.ListView(expand=True, spacing=10)

        self.controls = [
                ft.Text("Configuración de Parámetros", size=24, weight=ft.FontWeight.BOLD),
                ft.Divider(),

                ft.Row([
                    ft.Container(
                        content=ft.Column([
                            ft.Text("1. Convenios", weight=ft.FontWeight.BOLD),
                            ft.Row([self.txt_convenio, self.boton_agregar_convenio]),
                            ft.Container(
                                content=self.lista_convenios, 
                                border=ft.border.all(1, ft.Colors.GREY), 
                                border_radius=5, 
                                expand=True
                                )
                            ]),
                        expand=True, padding=10
                        ),
                    ft.Container(
                        content=ft.Column([
                            ft.Text("2. Categorías", weight=ft.FontWeight.BOLD), 
                            ft.Row([self.txt_categoria, self.boton_agregar_categoria]),
                            ft.Container(
                                content=self.lista_categorias,
                                border=ft.border.all(1, ft.Colors.GREY),
                                border_radius=5,
                                expand=True
                                )
                            ]),
                        expand=True, padding=10
                        )
                    ], expand=True)
                ]

    def did_mount(self):
        self.page.run_task(self.cargar_convenios)

    async def cargar_convenios(self):
        self.lista_convenios.controls.clear()

        async for session in get_db():
            repositorio = ConvenioRepository(session)
            convenios = await repositorio.get_all()

            for convenio in convenios:
                es_seleccionado = convenio.id == self.convenio_seleccionado_id
                color_fondo = ft.Colors.BLUE_50 if es_seleccionado else ft.Colors.TRANSPARENT
                icono_color = ft.Colors.BLUE if es_seleccionado else ft.Colors.GREY
                border_side = ft.border.BorderSide(2, ft.Colors.BLUE) if es_seleccionado \
                        else ft.border.BorderSide(0, ft.Colors.TRANSPARENT)
                        
                item = ft.Container(
                        content=ft.Row([
                            ft.Text(
                                f"{convenio.nombre}", 
                                weight=ft.FontWeight.BOLD if es_seleccionado else ft.FontWeight.NORMAL,
                                expand=True,
                                ),
                            ft.IconButton(
                                icon=ft.Icons.DELETE,
                                icon_size=18,
                                icon_color=ft.Colors.RED,
                                tooltip="Eliminar",
                                data=convenio.id,
                                on_click=self.boton_eliminar_convenio_click
                                )
                            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                        padding=5,
                        border=ft.border.only(bottom=ft.border.BorderSide(1, ft.Colors.GREY_200)),
                        bgcolor=color_fondo,
                        border_radius=5,
                        data={"id": convenio.id, "nombre": convenio.nombre},
                        on_click=self.seleccionar_convenio_click,
                        ink=True
                        )
                self.lista_convenios.controls.append(item)

        self.update()

    async def seleccionar_convenio_click(self, e):
        data = e.control.data
        self.convenio_seleccionado_id = data["id"]
        self.convenio_seleccionado_nombre = data["nombre"]

        self.label_categoria.value = f"Categorías de: {self.convenio_seleccionado_nombre}"
        self.txt_categoria.disabled = False
        self.txt_categoria.hint_text = "Nombre de categoría"
        self.boton_agregar_categoria.disabled = False

        await self.cargar_convenios()
        await self.cargar_categorias()

    async def cargar_categorias(self, e=None):
        if not self.convenio_seleccionado_id: return

        self.lista_categorias.controls.clear()

        async for session in get_db():
            repositorio = CategoriaRepository(session)
            categorias = await repositorio.get_by_convenio(int(self.convenio_seleccionado_id))

            if not categorias:
                self.lista_categorias.controls.append(ft.Text("Sin categorías registradas", italic=True, color=ft.Colors.GREY))
            else:
                for categoria in categorias:
                    item = ft.Container(
                            content=ft.Row([
                                ft.Text(f"{categoria.nombre}", expand=True),
                                ft.IconButton(
                                    icon=ft.Icons.DELETE,
                                    icon_size=18,
                                    icon_color=ft.Colors.RED,
                                    tooltip="Eliminar",
                                    data=categoria.id,
                                    on_click=self.boton_eliminar_categoria_click
                                    )
                                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                            padding=5,
                            border=ft.border.only(bottom=ft.border.BorderSide(1, ft.Colors.GREY_200))
                            )
                    self.lista_categorias.controls.append(item)

        self.lista_categorias.update()

    async def agregar_convenio(self, e):
        if not self.txt_convenio.value: return
        try:
            async for session in get_db():
                convenio = Convenio(nombre=self.txt_convenio.value)
                session.add(convenio)
                await session.commit()

            self.txt_convenio.value = ""
            self.page.open(ft.SnackBar(ft.Text("Convenio agregado"), bgcolor=ft.Colors.GREEN))
            await self.cargar_convenios()
        except IntegrityError:
            self.page.open(ft.SnackBar(ft.Text("Error: Ya existe ese convenio"), bgcolor=ft.Colors.RED))
        except Exception as ex:
            self.page.open(ft.SnackBar(ft.Text(f"Error: {ex}"), bgcolor=ft.Colors.RED))

    async def agregar_categoria(self, e):
        if not self.convenio_seleccionado_id: return
        if not self.convenio_seleccionado_nombre: return
        if not self.txt_categoria.value: return
        
        try:
            async for session in get_db():
                categoria = Categoria(
                        nombre=self.txt_categoria.value,
                        convenio_id=self.convenio_seleccionado_id
                        )
                session.add(categoria)
                await session.commit()
            
            self.txt_categoria.value = ""
            self.page.open(ft.SnackBar(
                ft.Text(f"Categoría agregada al convenio {self.convenio_seleccionado_nombre}"), 
                bgcolor=ft.Colors.GREEN
                ))
            await self.cargar_categorias()
            self.txt_categoria.update()
        except IntegrityError:
            self.page.open(ft.SnackBar(
                ft.Text(f"Error Ya existe esa categoría para el convenio {self.convenio_seleccionado_nombre}"), 
                bgcolor=ft.Colors.RED
                ))
        except Exception as ex:
            self.page.open(ft.SnackBar(ft.Text(f"Error: {ex}"), bgcolor=ft.Colors.GREEN))

    async def boton_eliminar_convenio_click(self, e):
        id_borrar = e.control.data
        try:
            async for session in get_db():
                repositorio = ConvenioRepository(session)
                await repositorio.delete(id_borrar)

            if id_borrar == self.convenio_seleccionado_id:
                self.convenio_seleccionado_id = None
                self.txt_categoria.disabled = True
                self.boton_agregar_categoria.disabled = True
                self.label_categoria.value = "Categorías"
                self.lista_categorias.controls.clear()

            self.page.open(ft.SnackBar(ft.Text("Convenio eliminado"), bgcolor=ft.Colors.ORANGE))
            await self.cargar_convenios()
            
        except IntegrityError:
            self.page.open(ft.SnackBar(
                ft.Text("No se puede borrar: Este convenio está en uso por Empresas o tiene Categorías"),
                bgcolor=ft.Colors.RED
                ))
        except Exception as ex:
            self.page.open(ft.SnackBar(
                ft.Text(f"Error {ex}"),
                bgcolor=ft.Colors.RED
                ))

    async def boton_eliminar_categoria_click(self, e):
        id_borrar = e.control.data
        try:
            async for session in get_db():
                repositorio = CategoriaRepository(session)
                await repositorio.delete(id_borrar)

            self.page.open(ft.SnackBar(ft.Text("Categoria eliminada"), bgcolor=ft.Colors.ORANGE))
            await self.cargar_categorias()
            
        except IntegrityError:
            self.page.open(ft.SnackBar(
                ft.Text("No se puede borrar: Hay empleados con esta categoría"),
                bgcolor=ft.Colors.RED
                ))
        except Exception as ex:
            self.page.open(ft.SnackBar(
                ft.Text(f"Error {ex}"),
                bgcolor=ft.Colors.RED
                ))
