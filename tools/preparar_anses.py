import pymupdf
from tests.utilidades import llenar_campo, llenar_fecha
from src.core.config import FORMS_TEMPLATES_DIR, OUTPUT_DIR

def generar_formulario_anses():
    print("Generando formulario de anses...")

    input_path = FORMS_TEMPLATES_DIR / "formulario_anses.pdf"
    output_path = OUTPUT_DIR / "formulario_anses.pdf"

    if not input_path.exists():
        print(f"No se encontró el archivo {input_path}")
        return

    doc = pymupdf.Document(input_path)
    page = doc[0]

    # Empleado
    llenar_campo(page, "apellido", "empleado_nombre_completo", ancho=250, x=-30, y=13)
    llenar_campo(page, "tipo y", "empleado_tipo_y_dni", ancho=110, x=-10, y=13)
    llenar_campo(page, "CUIL", "empleado_cuil", ancho=130, x=-10, y=13)
    llenar_campo(page, "sexo", "empleado_sexo", ancho=50, x=-10, y=13)
    llenar_campo(page, "nacionalidad", "empleado_nacionalidad", ancho=60, x=-50, y=13)
    llenar_campo(page, "estado civil", "empleado_estado_civil", ancho=60, x=-30, y=13)
    # probando el numero de calle
    llenar_domicilio(page, "domicilio - calle - número", "empleado_calle_numero", ancho=300)
    llenar_campo(page, "piso", "empleado_piso", ancho=40, x=-10, y=13)
    llenar_campo(page, "depto", "empleado_depto", ancho=40, x=-30, y=13)
    llenar_campo(page, "código postal", "empleado_codigo_postal", ancho=65, x=-50, y=13)
    llenar_campo(page, "localidad", "empleado_localidad", ancho=110, x=-30, y=13)
    llenar_campo(page, "provincia", "empleado_provincia", ancho=80, x=-30, y=13)
    llenar_campo(page, "dirección de correo electrónico", "empleado_mail", ancho=200, x=-120, y=13)
    llenar_campo(page, "teléfono", "empleado_telefono", ancho=200, x=-30, y=13)

    llenar_fecha(page, "fecha de nacimiento", "nacimiento", x=-82, y=13, ancho=23)

    # Empleador
    llenar_campo(page, "razón social", "empresa_razon_social", ancho=200, x=-50, y=13)
    llenar_campo(page, "CUIT", "empresa_cuit", ancho=200, x=-20, y=13)
    # agregar domicilio del empleador (se puede hacer para que funcione con numero de calle de empleado)
    llenar_domicilio(page, "domicilio - calle - número", "empresa_calle_numero", coincidencia=1, ancho=300)
    llenar_campo(page, "piso", "empresa_piso", 1, ancho=40, x=-10, y=13)
    llenar_campo(page, "depto", "empresa_depto", 1, ancho=40, x=-30, y=13)
    llenar_campo(page, "código postal", "empresa_codigo_postal", 1, ancho=65, x=-50, y=13)
    llenar_campo(page, "localidad", "empresa_localidad", 1, ancho=110, x=-30, y=13)
    llenar_campo(page, "provincia", "empresa_provincia", 1, ancho=80, x=-30, y=13)
    llenar_campo(page, "dirección de correo electrónico", "empresa_mail", 1, ancho=200, x=-120, y=13)
    llenar_campo(page, "teléfono", "empresa_telefono", 1, ancho=200, x=-30, y=13)

    llenar_lugar_y_fecha(page, "Lugar")

    doc.save(output_path)

def llenar_domicilio(pagina: pymupdf.Page, campo_buscado: str, nombre_widget, coincidencia: int=0, ancho: int=200):
    print(f"Buscando campo '{campo_buscado}'...")
    areas = pagina.search_for(campo_buscado)

    if areas:
        print("Encontrado! Creando Widget...")

        rectangulo = areas[coincidencia]
        x0 = rectangulo.x1 + 22
        x1 = x0 + ancho
        y0 = rectangulo.y0 - 2
        y1 = rectangulo.y1

        widget = pymupdf.Widget()
        widget.rect = pymupdf.Rect(x0, y0, x1, y1)
        widget.field_name = nombre_widget
        widget.field_type = 7
        widget.text_fontsize = 10
        # widget.field_value = campo_buscado
        # widget.border_color = [1,0,0]
        # widget.border_width = 1
        pagina.add_widget(widget)


def llenar_lugar_y_fecha(pagina: pymupdf.Page, campo_buscado: str):
    print(f"Buscando campo '{campo_buscado}'...")
    areas = pagina.search_for(campo_buscado)

    if areas:
        print("Encontrado! Creando Widget...")

        rectangulo = areas[0]
        x0 = rectangulo.x1 + 50
        x1 = x0 + 150
        y0 = rectangulo.y0 - 12
        y1 = rectangulo.y1 - 12

        widget = pymupdf.Widget()
        widget.rect = pymupdf.Rect(x0, y0, x1, y1)
        widget.field_name = "documento_lugar"
        widget.field_type = 7
        widget.text_fontsize = 10
        # widget.field_value = campo_buscado
        # widget.border_color = [1,0,0]
        # widget.border_width = 1
        pagina.add_widget(widget)

        x0 = x1 + 30
        x1 = x0 + 30
        widget = pymupdf.Widget()
        widget.rect = pymupdf.Rect(x0, y0, x1, y1)
        widget.field_name = "documento_dia"
        widget.field_type = 7
        widget.text_fontsize = 10
        # widget.field_value = campo_buscado
        # widget.border_color = [1,0,0]
        # widget.border_width = 1
        pagina.add_widget(widget)

        x0 = x1 + 30
        x1 = x0 + 70
        widget = pymupdf.Widget()
        widget.rect = pymupdf.Rect(x0, y0, x1, y1)
        widget.field_name = "documento_mes"
        widget.field_type = 7
        widget.text_fontsize = 10
        # widget.field_value = campo_buscado
        # widget.border_color = [1,0,0]
        # widget.border_width = 1
        pagina.add_widget(widget)

        x0 = x1 + 30
        x1 = x0 + 50
        widget = pymupdf.Widget()
        widget.rect = pymupdf.Rect(x0, y0, x1, y1)
        widget.field_name = "documento_año"
        widget.field_type = 7
        widget.text_fontsize = 10
        # widget.field_value = campo_buscado
        # widget.border_color = [1,0,0]
        # widget.border_width = 1
        pagina.add_widget(widget)

    else:
        print(f"No se encontró el campo {campo_buscado}")

generar_formulario_anses()
