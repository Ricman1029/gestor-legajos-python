import pymupdf
from tests.utilidades import llenar_campo, llenar_fecha
from src.core.config import FORMS_TEMPLATES_DIR, OUTPUT_DIR

def generar_formulario_andina():
    print("Generando formulario de andina...")

    input_path = FORMS_TEMPLATES_DIR / "formulario_mapfre.pdf"
    output_path = OUTPUT_DIR / "formulario_mapfre.pdf"

    if not input_path.exists():
        print(f"No se encontró el archivo {input_path}")
        return

    doc = pymupdf.Document(input_path)
    pages = [doc[0], doc[2], doc[4]]

    for page in pages:
        # Empleado
        llenar_campo(page, "nombre y apellido", "empleado_nombre_completo", ancho=220)
        llenar_campo(page, "ahorro", "empleado_cuil", ancho=120)
        llenar_campo(page, "documento tipo", "empleado_dni_tipo", ancho=60)
        llenar_campo(page, "documento tipo", "empleado_dni_numero", ancho=110, x=100)
        llenar_campo(page, "expedido por", "expedido_por", ancho=110)
        llenar_campo(page, "capital asegurado", "empleado_sueldo", ancho=120)
        llenar_campo(page, "ficha, etc.", "empleado_legajo", ancho=70)
        llenar_campo(page, "calle", "empleado_calle", ancho=130)
        # probando el numero de calle
        llenar_campo(page, "calle", "empleado_numero", ancho=35, x=175)
        llenar_campo(page, "piso", "empleado_piso", ancho=35)
        llenar_campo(page, "dpto.", "empleado_depto", ancho=35)
        llenar_campo(page, "cp", "empleado_codigo_postal", ancho=65)
        llenar_campo(page, "localidad", "empleado_localidad", ancho=190)
        llenar_campo(page, "pcia.", "empleado_provincia", ancho=190)

        llenar_fecha(page, "fecha de nacimiento", "nacimiento", x=8, ancho=23)
        llenar_fecha(page, "fecha del ingreso al empleo", "ingreso")

        # Empleador
        llenar_campo(page, "empleador", "empresa_razon_social", 2 if page.number == 0 else 1)
        # agregar domicilio del empleador (se puede hacer para que funcione con numero de calle de empleado)
        llenar_campo(page, "calle", "empresa_calle", 1, ancho=130)
        llenar_campo(page, "calle", "empresa_numero", 1, ancho=35, x=175)
        llenar_campo(page, "piso", "empresa_piso", 1, ancho=35)
        llenar_campo(page, "dpto", "empresa_depto", 1, ancho=35)
        llenar_campo(page, "cp", "empresa_codigo_postal", 1, ancho=65)
        llenar_campo(page, "localidad", "empresa_localidad", 1, ancho=190)
        llenar_campo(page, "pcia.", "empresa_provincia", 1, ancho=190)

        llenar_campo(page, "lugar y fecha", "documento_lugar_y_fecha", ancho=200)

    doc.save(output_path)

generar_formulario_andina()
