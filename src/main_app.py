import flet as ft
from src.data.db_initializer import create_tables

async def main(page: ft.Page):
    page.title = "Gestion de Legajos"
    page.theme_mode = ft.ThemeMode.DARK

    await create_tables()
    msg = ft.Text("Base de datos inicializada y lista.")

    page.add(msg)
    page.update()

