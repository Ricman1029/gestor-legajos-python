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
    llenar_campo(page, "apellido y nombre", "empleado_nombre_completo", x=4, y=1)
    llenar_campo(page, "n°", "empleado_dni_numero", x=4, y=1)
    llenar_campo(page, "expedido por", "expedido_por", x=4, y=1)
    llenar_campo(page, "ahorro", "empleado_cuil", x=4, y=1)
    llenar_campo(page, "ficha, etc.", "empleado_legajo", x=4, y=1)
    llenar_campo(page, "cap. asegurado", "empleado_sueldo", x=4, y=1)
    llenar_campo(page, "calle", "empleado_calle", x=4, y=1)
    # probando el numero de calle
    llenar_campo(page, "n°", "empleado_numero", 2, x=4, y=1)
    llenar_campo(page, "piso/dto", "empleado_piso_depto", x=4, y=1)
    llenar_campo(page, "c.p.", "empleado_codigo_postal", x=4, y=1)
    llenar_campo(page, "localidad", "empleado_localidad", x=4, y=1)
    llenar_campo(page, "provincia", "empleado_provincia", x=4, y=1)

    llenar_campo(page, "nacimiento", "empleado_dia_nacimiento", x=16, y=1)
    llenar_campo(page, "nacimiento", "empleado_mes_nacimiento", x=46, y=1)
    llenar_campo(page, "nacimiento", "empleado_año_nacimiento", x=68, y=1)

    llenar_campo(page, "al empleo", "empleado_dia_ingreso", x=28, y=1)
    llenar_campo(page, "al empleo", "empleado_mes_ingreso", x=58, y=1)
    llenar_campo(page, "al empleo", "empleado_año_ingreso", x=80, y=1)

    # Empleador
    llenar_campo(page, "razon social", "empresa_razon_social", x=4, y=1)
    llenar_campo(page, "calle", "empresa_calle", 1, x=4, y=1)
    llenar_campo(page, "n°", "empresa_numero", 3, x=4, y=1)
    llenar_campo(page, "piso/dto", "empresa_piso_depto", 1, x=4, y=1)
    llenar_campo(page, "c.p.", "empresa_codigo_postal", 1, x=4, y=1)
    llenar_campo(page, "localidad", "empresa_localidad", 1, x=4, y=1)
    llenar_campo(page, "provincia", "empresa_provincia", 1, x=4, y=1)

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
