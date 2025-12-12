import sys
from src.domain.services.form_filler_service import FormFillerService

def probar_inspeccion():

    service = FormFillerService()
    
    service.inspeccionar_widgets(sys.argv[1])

if __name__ == "__main__":
    probar_inspeccion()
