import sys
from tests.utilidades import inspeccionar_widgets

def probar_inspeccion():
    
    inspeccionar_widgets(sys.argv[1])

if __name__ == "__main__":
    probar_inspeccion()
