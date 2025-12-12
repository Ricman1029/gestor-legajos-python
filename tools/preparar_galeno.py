import pymupdf
from src.core.config import FORMS_TEMPLATES_DIR, OUTPUT_DIR

def generar_formulario_galeno():
    print("Generando formulario de andina...")

    input_path = FORMS_TEMPLATES_DIR / "formulario_galeno.pdf"
    output_path = OUTPUT_DIR / "formulario_galeno.pdf"

    if not input_path.exists():
        print(f"No se encontró el archivo {input_path}")
        return

    doc = pymupdf.Document(input_path)
    page = doc[0]

    print("Calculando dibujos...")
    lista_rects = []
    for pagina in doc:
        for dibujo in pagina.get_drawings():
            if dibujo["color"] == (0.0, 0.33521997928619385, 0.589614987373352) and dibujo["rect"].x0 == dibujo["rect"].x1:
                lista_rects.append(dibujo["rect"])
   
    contador = 0
    for indice, rect in enumerate(lista_rects):
        print(f"{indice}: {rect}")
        # print(rect, end="")
        # contador += 1
        # if contador % 2 == 0:
        #     print()

    print(f"La lista de rectángulos tiene {len(lista_rects)} elementos")

    fields = [
            "empresa_razon_social", "empleado_localidad", "empresa_cuit", "empleado_nombre_completo", "empleado_cuil", "empleado_tipo_y_dni",
            "empleado_sueldo", "empleado_fecha_nacimiento", "empleado_fecha_ingreso", "empleado_piso", "empleado_depto", "empleado_calle", "empleado_numero",
            "empleado_provincia", "empleado_codigo_postal", "empresa_localidad", "empresa_provincia", "empresa_codigo_postal", "empresa_piso", 
            "empresa_depto", "empresa_calle", "empresa_numero"
            ]

    # widget = pymupdf.Widget()
    # widget.rect = pymupdf.Rect(105, 259, 397, 271)
    # widget.field_name = fields[0]
    # widget.field_type = 7
    # widget.text_fontsize = 10
    # widget.border_color = [1,0,0]
    # widget.border_width = 1
    # widget.field_value = fields[0]
    # page.add_widget(widget)

    x0 = x1 = y0 = y1 = None
    contador = 0
    for rect in lista_rects:
        if x1 is None:
            x1 = rect.x0
            y0 = rect.y0
            y1 = rect.y1
            continue
        if x0 is None:
            x0 = rect.x1
            if x0 > x1:
                x0, x1 = x1, x0
            print(f"Las coordenadas son x0: {x0}, x1: {x1}, y0: {y0}, y1: {y1}")

            widget = pymupdf.Widget()
            widget.rect = pymupdf.Rect(x0, y0, x1, y1)
            widget.field_name = fields[contador]
            widget.field_type = 7
            widget.text_fontsize = 10
            # widget.border_color = [1,0,0]
            # widget.border_width = 1
            # widget.field_value = fields[contador]
            page.add_widget(widget)
            contador += 1
            x0 = x1 = y0 = y1 = None
        if contador == len(fields):
            break

    # Legajo
    widget = pymupdf.Widget()
    widget.rect = pymupdf.Rect(200, 76, 397, 88)
    widget.field_name = "empleado_legajo"
    widget.field_type = 7
    widget.text_fontsize = 10
    # widget.field_value = "legajo"
    # widget.border_color = [1,0,0]
    # widget.border_width = 1
    page.add_widget(widget)

    # Lugar y fecha
    widget = pymupdf.Widget()
    widget.rect = pymupdf.Rect(115, 650, 222, 662)
    widget.field_name = "documento_lugar_y_fecha"
    widget.field_type = 7
    widget.text_fontsize = 10
    # widget.field_value = "Bariloche 22/12/2022"
    # widget.border_color = [1,0,0]
    # widget.border_width = 1
    page.add_widget(widget)

    doc.save(output_path)


generar_formulario_galeno()
