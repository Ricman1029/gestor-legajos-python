import flet as ft
from src.data.db_initializer import create_tables
from src.ui.layout import MainLayout

async def main(page: ft.Page):
    page.title = "Gestion de Legajos"
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 0

    await create_tables()
    
    app_layout = MainLayout(page)

    page.add(app_layout)
    page.update()
