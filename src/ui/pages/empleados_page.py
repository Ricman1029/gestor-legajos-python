import flet as ft

class EmpleadosPage(ft.Column):
    def __init__(self):
        super().__init__()
        self.controls = [
                ft.Text("Gestión de Empleados", size=35, weight=ft.FontWeight.BOLD),
                ft.Divider(),
                ft.Text("Acá va a ir la tabla de empleados")
                ]
