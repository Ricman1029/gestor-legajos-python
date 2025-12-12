import pymupdf
from src.core.config import FORMS_TEMPLATES_DIR, OUTPUT_DIR

class FormFillerService:
    def rellenar_formulario(self):
        ruta_formulario = FORMS_TEMPLATES_DIR / "formulario_andina.pdf"
        formulario = pymupdf.Document(ruta_formulario)
