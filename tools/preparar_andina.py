import pymupdf
from tests.utilidades import llenar_campo, llenar_fecha
from src.core.config import FORMS_TEMPLATES_DIR, OUTPUT_DIR

def generar_formulario_andina():
    print("Generando formulario de andina...")

    input_path = FORMS_TEMPLATES_DIR / "formulario_andina.pdf"
    output_path = OUTPUT_DIR / "formulario_andina.pdf"

    if not input_path.exists():
        print(f"No se encontró el archivo {input_path}")
        return

    doc = pymupdf.Document(input_path)
    page = doc[0]

    # Empleado
    llenar_campo(page, "apellido y nombre", "empleado_nombre_completo", x=4)
    llenar_campo(page, "n°", "empleado_dni_numero", ancho=110, x=4)
    llenar_campo(page, "expedido por", "expedido_por", ancho=110, x=4)
    llenar_campo(page, "ahorro", "empleado_cuil", ancho=150, x=4)
    llenar_campo(page, "ficha, etc.", "empleado_legajo", ancho=70, x=4)
    llenar_campo(page, "cap. asegurado", "empleado_sueldo", ancho=70, x=4)
    llenar_campo(page, "calle", "empleado_calle", ancho=110, x=4)
    # probando el numero de calle
    llenar_campo(page, "n°", "empleado_numero", 2, ancho=40, x=4)
    llenar_campo(page, "piso/dto", "empleado_piso_depto", ancho=40, x=4)
    llenar_campo(page, "c.p.", "empleado_codigo_postal", ancho=45, x=4)
    llenar_campo(page, "localidad", "empleado_localidad", ancho=50, x=4)
    llenar_campo(page, "provincia", "empleado_provincia", ancho=56, x=4)

    llenar_fecha(page, "fecha de nacimiento", "nacimiento", x=12, ancho=23)
    llenar_fecha(page, "fecha ingreso al empleo", "ingreso", x=23, ancho=23)

    # Empleador
    llenar_campo(page, "razon social", "empresa_razon_social", x=4)
    # agregar domicilio del empleador (se puede hacer para que funcione con numero de calle de empleado)
    llenar_campo(page, "calle", "empresa_calle", 1, ancho=110, x=4)
    llenar_campo(page, "n°", "empresa_numero", 3, ancho=40, x=4)
    llenar_campo(page, "piso/dto", "empresa_piso_depto", 1, ancho=40, x=4)
    llenar_campo(page, "c.p.", "empresa_codigo_postal", 1, ancho=45, x=4)
    llenar_campo(page, "localidad", "empresa_localidad", 1, ancho=50, x=4)
    llenar_campo(page, "provincia", "empresa_provincia", 1, ancho=56, x=4)

    llenar_fecha_firma(page, "fecha (dia/mes/", "empleado_fecha_ingreso")

    doc.save(output_path)

def llenar_fecha_firma(pagina: pymupdf.Page, campo_buscado: str, nombre_widget: str):
    print(f"Buscando campo '{campo_buscado}'...")
    areas = pagina.search_for(campo_buscado)

    if areas:
        print("Encontrado! Creando Widget...")

        rectangulo = areas[0]
        x0 = rectangulo.x1 + 50
        x1 = x0 + 300
        y0 = rectangulo.y0 - 25
        y1 = rectangulo.y1

        widget = pymupdf.Widget()
        widget.rect = pymupdf.Rect(x0, y0, x1, y1)
        widget.field_name = nombre_widget
        widget.field_type = 7
        widget.text_fontsize = 10
        # widget.field_value = campo_buscado
        pagina.add_widget(widget)
    else:
        print(f"No se encontró el campo {campo_buscado}")

generar_formulario_andina()
