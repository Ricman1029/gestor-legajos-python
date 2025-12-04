import pickle
import sys
from pathlib import Path

root_path = Path(__file__).parent.parent
sys.path.append(str(root_path))

from gestor_legajos.entidades.convenio import Convenio
from gestor_legajos.utils.persistencia import guardar_convenio, obtener_ruta_defaults


def generar_conveio():
    convenio = Convenio("0445/06 - CONSTRUCCIÓN")
    convenio.agregar_categoria("OPERADOR ESPECIALIZADO DE BOMBA - NIVEL D")
    convenio.agregar_categoria("OPERADOR OFICIAL INICIAL DE BOMBA - NIVEL C")

    with open(obtener_ruta_defaults("convenios.dat"), "wb") as archivo:
        pickle.dump(convenio, archivo)


if __name__ == "__main__":
    generar_conveio()
