import sys
from src.domain.services.form_filler_service import FormFillerService

def probar_inspeccion():

    service = FormFillerService()
    
    service.inspccionar_dibujos(sys.argv[1])

if __name__ == "__main__":
    probar_inspeccion()
