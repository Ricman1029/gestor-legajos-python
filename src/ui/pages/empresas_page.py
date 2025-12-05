import flet as ft

class EmpresasPage(ft.Column):
    def __init__(self):
        super().__init__()
        self.controls = [
                ft.Text("Gestión de Empresas", size=25, weight=ft.FontWeight.BOLD),
                ft.Divider(),
                ft.Text("Acá va a ir la tabla de empresas...")
                ]
