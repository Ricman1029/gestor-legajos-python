import flet
from gestor_legajos.controles.tablero_obras_sociales import TableroObraSocial
from gestor_legajos.controles.tablero_convenios import TableroConvenios
from gestor_legajos.controles.tablero_sindicatos import TableroSindicatos


class OtrosView(flet.Column):
    def __init__(self):
        super().__init__()

    def inicializar(self):
        self.controls = [
            flet.Container(
                content=flet.Text(
                    value="Generales",
                    style=flet.TextThemeStyle.HEADLINE_MEDIUM),
                padding=flet.padding.only(top=15),
            ),
            flet.Row(
                controls=[
                    TableroObraSocial(),
                    TableroConvenios(),
                    TableroSindicatos()
                ],
            )
        ]
