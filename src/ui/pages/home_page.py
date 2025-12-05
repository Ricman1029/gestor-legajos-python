import flet as ft

class HomePage(ft.Column):
    def __init__(self):
        super().__init__()
        self.controls = [
                ft.Text("Bienvenido al Gestor de Legajos", size=30, weight=ft.FontWeight.BOLD),
                ft.Text("Selecciona una opción del menú lateral para comenzar.", size=30, weight=ft.FontWeight.BOLD)
                ]
