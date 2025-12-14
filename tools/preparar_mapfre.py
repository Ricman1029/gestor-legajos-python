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
        llenar_campo(page, "nombre y apellido", "empleado_nombre_completo", y=1)
        llenar_campo(page, "ahorro", "empleado_cuil", y=1)
        llenar_campo(page, "documento tipo", "empleado_dni_tipo", y=1)
        llenar_campo(page, "documento tipo", "empleado_dni_numero", x=100, y=1)
        llenar_campo(page, "expedido por", "expedido_por", y=1)
        llenar_campo(page, "capital asegurado", "empleado_sueldo", y=1)
        llenar_campo(page, "ficha, etc.", "empleado_legajo", y=1)
        llenar_campo(page, "calle", "empleado_calle", y=1)
        # probando el numero de calle
        llenar_campo(page, "calle", "empleado_numero", x=175, y=1)
        llenar_campo(page, "piso", "empleado_piso", y=1)
        llenar_campo(page, "dpto.", "empleado_depto", y=1)
        llenar_campo(page, "cp", "empleado_codigo_postal", y=1)
        llenar_campo(page, "localidad", "empleado_localidad", y=1)
        llenar_campo(page, "pcia.", "empleado_provincia", y=1)

        llenar_campo(page, "fecha de nacimiento", "empleado_dia_nacimiento", x=14, y=1)
        llenar_campo(page, "fecha de nacimiento", "empleado_mes_nacimiento", x=40, y=1)
        llenar_campo(page, "fecha de nacimiento", "empleado_año_nacimiento", x=65, y=1)

        llenar_campo(page, "fecha del ingreso al empleo", "empleado_dia_ingreso", x=17, y=1)
        llenar_campo(page, "fecha del ingreso al empleo", "empleado_mes_ingreso", x=43, y=1)
        llenar_campo(page, "fecha del ingreso al empleo", "empleado_año_ingreso", x=68, y=1)

        # Empleador
        llenar_campo(page, "empleador", "empresa_razon_social", 2 if page.number == 0 else 1, y=1)
        llenar_campo(page, "calle", "empresa_calle", 1, y=1)
        llenar_campo(page, "calle", "empresa_numero", 1, x=175, y=1)
        llenar_campo(page, "piso", "empresa_piso", 1, y=1)
        llenar_campo(page, "dpto", "empresa_depto", 1, y=1)
        llenar_campo(page, "cp", "empresa_codigo_postal", 1, y=1)
        llenar_campo(page, "localidad", "empresa_localidad", 1, y=1)
        llenar_campo(page, "pcia.", "empresa_provincia", 1, y=1)

        llenar_campo(page, "lugar y fecha", "documento_lugar_y_fecha", y=1)

    doc.save(output_path)

generar_formulario_andina()
