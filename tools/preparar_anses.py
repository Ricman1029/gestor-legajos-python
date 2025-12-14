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

    llenar_campo(page, "apellido", "empleado_nombre_completo", x=-20, y=-10)
    llenar_campo(page, "fecha de nacimiento", "empleado_dia_nacimiento", x=-82, y=-10)
    llenar_campo(page, "fecha de nacimiento", "empleado_mes_nacimiento", x=-50, y=-10)
    llenar_campo(page, "fecha de nacimiento", "empleado_año_nacimiento", x=-25, y=-10)
    llenar_campo(page, "nacionalidad", "empleado_nacionalidad", x=-50, y=-10)

    llenar_campo(page, "CUIL", "empleado_cuil", x=-10, y=-13)
    llenar_campo(page, "tipo y", "empleado_tipo_y_dni", x=-10, y=-13)
    llenar_campo(page, "sexo", "empleado_sexo", x=-10, y=-10)
    llenar_campo(page, "estado civil", "empleado_estado_civil", x=-30, y=-13)

    llenar_campo(page, "domicilio - calle - número", "empleado_calle_numero", x=20)

    llenar_campo(page, "piso", "empleado_piso", x=-10, y=-8)
    llenar_campo(page, "depto", "empleado_depto", x=-30, y=-8)
    llenar_campo(page, "código postal", "empleado_codigo_postal", x=-50, y=-8)
    llenar_campo(page, "localidad", "empleado_localidad", x=-30, y=-8)
    llenar_campo(page, "provincia", "empleado_provincia", x=-30, y=-8)

    llenar_campo(page, "dirección de correo electrónico", "empleado_mail", x=-120, y=-10)
    llenar_campo(page, "teléfono", "empleado_telefono", x=-30, y=-10)

    llenar_campo(page, "razón social", "empresa_razon_social", x=-50, y=-10)
    llenar_campo(page, "CUIT", "empresa_cuit", x=-20, y=-11)

    llenar_campo(page, "domicilio - calle - número", "empresa_calle_numero", coincidencia=1, x=20)

    llenar_campo(page, "piso", "empresa_piso", 1, x=-10, y=-8)
    llenar_campo(page, "depto", "empresa_depto", 1, x=-30, y=-8)
    llenar_campo(page, "código postal", "empresa_codigo_postal", 1, x=-50, y=-8)
    llenar_campo(page, "localidad", "empresa_localidad", 1, x=-30, y=-8)
    llenar_campo(page, "provincia", "empresa_provincia", 1, x=-30, y=-8)

    llenar_campo(page, "dirección de correo electrónico", "empresa_mail", 1, x=-120, y=-10)
    llenar_campo(page, "teléfono", "empresa_telefono", 1, x=-30, y=-10)

    llenar_campo(page, "Lugar", "documento_lugar", x=58, y=15)
    llenar_campo(page, "Lugar", "documento_dia", x=240, y=15)
    llenar_campo(page, "Lugar", "documento_mes", x=295, y=15)
    llenar_campo(page, "Lugar", "documento_año", x=390, y=15)

    doc.save(output_path)

generar_formulario_anses()
