from src.utils.helpers import agregar_en_orden


class Convenio:
    def __init__(self, nombre):
        self.nombre = nombre
        self.categorias = []

    def agregar_categoria(self, nombre_categoria):
        agregar_en_orden(
            self.categorias,
            nombre_categoria,
        )
