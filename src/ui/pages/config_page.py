import flet as ft
from sqlalchemy.exc import IntegrityError
from src.core.database import get_db
from src.domain.schemas.parametricos_schema import ArtCreate, CategoriaCreate, ConvenioCreate, SindicatoCreate, ObraSocialCreate
from src.data.repositories.parametricos_repository import (
        SindicatoRepository, ConvenioRepository, CategoriaRepository, ArtRepository, ObraSocialRepository, 
        )

class ConfigPage(ft.Column):
    def __init__(self):
        super().__init__()
        self.expand = True

        self.sindicato_seleccionado_id = None
        self.convenio_seleccionado_id = None

        self.txt_sindicato = ft.TextField(label="Nuevo Sindicato", expand=True, height=40)
        self.lista_sindicatos = ft.ListView(expand=True, spacing=5, padding=5)
        self.columna_sindicatos = self._build_column(
                "1. Sindicatos", 
                self.txt_sindicato, 
                self.agregar_sindicato,
                self.lista_sindicatos, 
                )

        self.txt_convenio = ft.TextField(label="Nuevo Convenio", expand=True, height=40, disabled=True)
        self.lista_convenios = ft.ListView(expand=True, spacing=10)
        self.columna_convenios = self._build_column(
                "2. Convenios", 
                self.txt_convenio, 
                self.agregar_convenio,
                self.lista_convenios, 
                )

        self.txt_categoria = ft.TextField(label="Nueva Categoría", disabled=True, expand=True)
        self.lista_categorias = ft.ListView(expand=True, spacing=10)
        self.columna_categorias = self._build_column(
                "3. Categorías", 
                self.txt_categoria, 
                self.agregar_categoria,
                self.lista_categorias, 
                )

        self.txt_art_nombre = ft.TextField(label="Nombre ART", expand=True)
        self.txt_art_telefono = ft.TextField(label="Teléfono ART", expand=True)
        self.lista_arts = ft.ListView(expand=True, spacing=5, padding=5)

        self.panel_art = ft.Container(
                expand=True,
                padding=20, 
                content=ft.Column([
                    ft.Text("Gestión de Aseguradoras de Riesgos del Trabajo (ART)", size=20, weight=ft.FontWeight.BOLD),
                    ft.Row([
                        self.txt_art_nombre,
                        self.txt_art_telefono,
                        ft.IconButton(icon=ft.Icons.ADD_CIRCLE, icon_color=ft.Colors.GREEN, icon_size=40, on_click=self.agregar_art)
                        ]),
                    ft.Divider(),
                    ft.Container(
                        content=self.lista_arts,
                        border=ft.border.all(1, ft.Colors.GREY_300),
                        border_radius=8,
                        expand=True
                        )
                    ])
                )

        self.txt_obra_social_nombre = ft.TextField(label="Nombre Obra Social", expand=True)
        self.txt_obra_social_codigo = ft.TextField(label="Código Obra Social", expand=True)
        self.lista_obras_sociales = ft.ListView(expand=True, spacing=5, padding=5)

        self.panel_obra_social = ft.Container(
                expand=True,
                padding=20, 
                content=ft.Column([
                    ft.Text("Gestión de Obras Sociales (OS)", size=20, weight=ft.FontWeight.BOLD),
                    ft.Row([
                        self.txt_obra_social_nombre,
                        self.txt_obra_social_codigo,
                        ft.IconButton(icon=ft.Icons.ADD_CIRCLE, icon_color=ft.Colors.GREEN, icon_size=40, on_click=self.agregar_obra_social)
                        ]),
                    ft.Divider(),
                    ft.Container(
                        content=self.lista_obras_sociales,
                        border=ft.border.all(1, ft.Colors.GREY_300),
                        border_radius=8,
                        expand=True
                        )
                    ])
                )

        self.tabs = ft.Tabs(
                selected_index=0,
                animation_duration=300,
                tabs=[
                    ft.Tab(
                        text="Estructura Laboral",
                        icon=ft.Icons.ACCOUNT_TREE,
                        content=ft.Container(
                            padding=10,
                            content=ft.Row([
                                self.columna_sindicatos,
                                ft.VerticalDivider(width=1, color=ft.Colors.GREY_300),
                                self.columna_convenios,
                                ft.VerticalDivider(width=1, color=ft.Colors.GREY_300),
                                self.columna_categorias,
                                ], expand=True)
                            )
                        ),
                    ft.Tab(
                        text="Aseguradoras (ART)",
                        icon=ft.Icons.MEDICAL_SERVICES,
                        content=ft.Container(
                            padding=10,
                            content=ft.Row([
                                self.panel_obra_social,
                                ft.VerticalDivider(width=1, color=ft.Colors.GREY_300),
                                self.panel_art
                                ], expand=True)
                            )
                        ),
                    ],
                expand=True
                )

        self.controls = [self.tabs]

    def _build_column(self, titulo, input_field, on_add, list_view):
        return ft.Container(
                expand=True,
                padding=10,
                content=ft.Column([
                    ft.Text(titulo, weight=ft.FontWeight.BOLD, size=16),
                    ft.Row([
                        input_field,
                        ft.IconButton(icon=ft.Icons.ADD, icon_color=ft.Colors.GREEN, on_click=on_add)
                        ]),
                    ft.Container(
                        content=list_view,
                        border=ft.border.all(1, ft.Colors.GREY_300),
                        border_radius=5,
                        expand=True
                        )
                    ])
                )

    def did_mount(self):
        self.page.run_task(self.cargar_sindicatos)
        self.page.run_task(self.cargar_arts)
        self.page.run_task(self.cargar_obras_sociales)

    async def cargar_sindicatos(self):
        self.lista_sindicatos.controls.clear()

        async for session in get_db():
            repositorio = SindicatoRepository(session)
            sindicatos = await repositorio.get_all()

            for sindicato in sindicatos:
                es_seleccionado = sindicato.id == self.sindicato_seleccionado_id
                self.lista_sindicatos.controls.append(
                        self._crear_item_lista(
                            sindicato.id,
                            sindicato.nombre,
                            es_seleccionado,
                            self.seleccionar_sindicato,
                            self.borrar_sindicato
                            )
                        )
        self.update()

    async def cargar_convenios(self):
        self.lista_convenios.controls.clear()
        self.lista_categorias.controls.clear()

        if not self.sindicato_seleccionado_id: return

        async for session in get_db():
            repositorio = ConvenioRepository(session)
            todos = await repositorio.get_all()
            filtrados = [convenio for convenio in todos if convenio.sindicato_id == self.sindicato_seleccionado_id]

            for convenio in filtrados:
                es_seleccionado = convenio.id == self.convenio_seleccionado_id
                self.lista_convenios.controls.append(
                        self._crear_item_lista(
                            convenio.id,
                            convenio.nombre,
                            es_seleccionado,
                            self.seleccionar_convenio,
                            self.borrar_convenio
                            )
                        )
        self.update()

    async def cargar_categorias(self):
        self.lista_categorias.controls.clear()
        if not self.convenio_seleccionado_id: return

        async for session in get_db():
            repositorio = CategoriaRepository(session)
            categorias = await repositorio.get_by_convenio(int(self.convenio_seleccionado_id))
            for categoria in categorias:
                self.lista_categorias.controls.append(
                        self._crear_item_lista(
                            categoria.id,
                            categoria.nombre,
                            False,
                            None,
                            self.borrar_categoria
                            )
                        )
        self.update()

    async def cargar_arts(self):
        self.lista_arts.controls.clear()

        async for session in get_db():
            repositorio = ArtRepository(session)
            arts = await repositorio.get_all()

            for art in arts:
                self.lista_arts.controls.append(
                        ft.ListTile(
                            title=ft.Text(art.nombre, weight=ft.FontWeight.BOLD),
                            subtitle=ft.Text(f"Tel: {art.telefono}"),
                            leading=ft.Icon(ft.Icons.LOCAL_HOSPITAL, color=ft.Colors.RED),
                            trailing=ft.IconButton(
                                icon=ft.Icons.DELETE,
                                icon_color=ft.Colors.RED,
                                data=art.id,
                                on_click=self.borrar_art
                                )
                            )
                        )
        self.update()

    async def cargar_obras_sociales(self):
        self.lista_obras_sociales.controls.clear()

        async for session in get_db():
            repositorio = ObraSocialRepository(session)
            obras_sociales = await repositorio.get_all()

            for obra_social in obras_sociales:
                self.lista_obras_sociales.controls.append(
                        ft.ListTile(
                            title=ft.Text(obra_social.nombre, weight=ft.FontWeight.BOLD),
                            subtitle=ft.Text(f"Código: {obra_social.codigo}"),
                            leading=ft.Icon(ft.Icons.LOCAL_HOSPITAL, color=ft.Colors.RED),
                            trailing=ft.IconButton(
                                icon=ft.Icons.DELETE,
                                icon_color=ft.Colors.RED,
                                data=obra_social.id,
                                on_click=self.borrar_obra_social
                                )
                            )
                        )
        self.update()

    async def seleccionar_sindicato(self, e):
        self.sindicato_seleccionado_id = e.control.data
        self.convenio_seleccionado_id = None

        self.txt_convenio.disabled = False
        self.txt_convenio.label = f"Convenio de {e.control.tooltip}"

        self.txt_categoria.disabled = True

        await self.cargar_sindicatos()
        await self.cargar_convenios()

    async def seleccionar_convenio(self, e):
        self.convenio_seleccionado_id = e.control.data

        self.txt_categoria.disabled = False

        await self.cargar_convenios()
        await self.cargar_categorias()

    async def agregar_sindicato(self, e):
        if not self.txt_sindicato.value: return
        try:
            async for session in get_db():
                repositorio = SindicatoRepository(session)

                sindicato = SindicatoCreate(nombre=self.txt_sindicato.value)

                await repositorio.create(sindicato)

            self.txt_sindicato.value = ""
            await self.cargar_sindicatos()
            self._mostrar_mensaje("Sindicato agregado", ft.Colors.GREEN)

        except Exception as ex:
            self._mostrar_mensaje(f"Error: {ex}", ft.Colors.RED)

    async def agregar_convenio(self, e):
        if not self.txt_convenio.value: return
        try:
            async for session in get_db():
                repositorio = ConvenioRepository(session)

                convenio = ConvenioCreate(
                        nombre=self.txt_convenio.value,
                        sindicato_id=self.sindicato_seleccionado_id
                        )
                await repositorio.create(convenio)

            self.txt_convenio.value = ""
            await self.cargar_convenios()
            self._mostrar_mensaje("Convenio agregado", ft.Colors.GREEN)

        except IntegrityError:
            self._mostrar_mensaje("Error: Ya existe ese convenio", ft.Colors.RED)
        except Exception as ex:
            self._mostrar_mensaje(f"Error: {ex}", ft.Colors.RED)

    async def agregar_categoria(self, e):
        if not self.convenio_seleccionado_id: return
        if not self.txt_categoria.value: return
        
        try:
            async for session in get_db():
                repositorio = CategoriaRepository(session)
                categoria = CategoriaCreate(
                        nombre=self.txt_categoria.value,
                        convenio_id=self.convenio_seleccionado_id
                        )
                await repositorio.create(categoria)
            
            self.txt_categoria.value = ""
            await self.cargar_categorias()
            self._mostrar_mensaje(f"Categoría creada", ft.Colors.GREEN)

        except IntegrityError:
            self._mostrar_mensaje(f"Error Ya existe esa categoría", ft.Colors.RED)
        except Exception as ex:
            self._mostrar_mensaje(f"Error: {ex}", ft.Colors.RED)

    async def agregar_art(self, e):
        if not self.txt_art_nombre.value: return
        if not self.txt_art_telefono.value: return

        try:
            async for session in get_db():
                repositorio = ArtRepository(session)
                art = ArtCreate(
                        nombre=self.txt_art_nombre.value,
                        telefono=self.txt_art_telefono.value
                        )
                await repositorio.create(art)

            self.txt_art_nombre.value = ""
            self.txt_art_telefono.value = ""
            await self.cargar_arts()
            self._mostrar_mensaje("Art agregada", ft.Colors.GREEN)
            
        except Exception as ex:
            self._mostrar_mensaje(f"Error: {ex}", ft.Colors.RED)

    async def agregar_obra_social(self, e):
        if not self.txt_obra_social_nombre.value: return
        if not self.txt_obra_social_codigo.value: return

        try:
            async for session in get_db():
                repositorio = ObraSocialRepository(session)
                obra_social = ObraSocialCreate(
                        nombre=self.txt_obra_social_nombre.value,
                        codigo=int(self.txt_obra_social_codigo.value)
                        )
                await repositorio.create(obra_social)

            self.txt_obra_social_nombre.value = ""
            self.txt_obra_social_codigo.value = ""
            await self.cargar_obras_sociales()
            self._mostrar_mensaje("Obra Social agregada", ft.Colors.GREEN)
            
        except Exception as ex:
            self._mostrar_mensaje(f"Error: {ex}", ft.Colors.RED)

    async def borrar_sindicato(self, e):
        await self._borrar_generico(
                e.control.data,
                SindicatoRepository,
                self.cargar_sindicatos
                )
        self.sindicato_seleccionado_id = None
        self.convenio_seleccionado_id = None
        self.lista_convenios.controls.clear()
        self.lista_categorias.controls.clear()

    async def borrar_convenio(self, e):
        await self._borrar_generico(
                e.control.data,
                ConvenioRepository,
                self.cargar_convenios
                )
        self.convenio_seleccionado_id = None
        self.lista_categorias.controls.clear()

    async def borrar_categoria(self, e):
        await self._borrar_generico(
                e.control.data,
                CategoriaRepository,
                self.cargar_categorias
                )

    async def borrar_art(self, e):
        await self._borrar_generico(
                e.control.data,
                ArtRepository,
                self.cargar_arts
                )

    async def borrar_obra_social(self, e):
        await self._borrar_generico(
                e.control.data,
                ObraSocialRepository,
                self.cargar_obras_sociales
                )

    async def _borrar_generico(self, id_borrar, RepositorioClase, funcion_cargar):
        try:
            async for session in get_db():
                repositorio = RepositorioClase(session)
                await repositorio.delete(id_borrar)
            await funcion_cargar()
            self._mostrar_mensaje(f"Registro borrado", ft.Colors.ORANGE)

        except IntegrityError:
            self._mostrar_mensaje("No se puede borrar: Este convenio está en uso por Empresas o tiene Categorías", ft.Colors.RED)
        except Exception as ex:
            self._mostrar_mensaje(f"Error {ex}", ft.Colors.RED)

    def _crear_item_lista(self, id, texto, es_seleccionado, on_click, on_delete):
        return ft.Container(
                content=ft.Row([
                    ft.Text(texto, weight=ft.FontWeight.BOLD if es_seleccionado else ft.FontWeight.NORMAL, expand=True),
                    ft.IconButton(
                        icon=ft.Icons.DELETE,
                        icon_size=18,
                        icon_color=ft.Colors.RED,
                        data=id,
                        on_click=on_delete
                        )
                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                padding=5,
                bgcolor=ft.Colors.BLUE_50 if es_seleccionado else ft.Colors.TRANSPARENT,
                border_radius=5,
                data=id,
                tooltip=texto,
                on_click=on_click if on_click else None,
                ink=True
                )

    def _mostrar_mensaje(self, texto, color):
        self.page.open(ft.SnackBar(ft.Text(texto), bgcolor=color))
