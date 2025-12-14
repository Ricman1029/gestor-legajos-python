import pymupdf
from src.core.config import FORMS_TEMPLATES_DIR, OUTPUT_DIR

def inspeccionar_widgets(nombre_archivo: str):
    """
    Imprime en consola los nombres de los campos del formulario
    para saber qué claves usar en el diccionario de datos.
    """
    ruta_formulario = FORMS_TEMPLATES_DIR / nombre_archivo
    
    doc = pymupdf.Document(ruta_formulario)
    
    print(f"--- Inspeccionando: {nombre_archivo} ---")
    if not doc.is_form_pdf:
        print("❌ Este PDF no parece ser un formulario interactivo (AcroForm).")
        return

    contador = 0
    for pagina_num, pagina in enumerate(doc.pages()):
        for widget in pagina.widgets():
            contador += 1
            # print(f"Campo: '{widget.field_name}'")
            print(f"Pág {pagina_num+1} | Campo: '{widget.field_name}' | Valor actual: '{widget.field_value}'")
    

    print(f"--- Total de campos encontrados: {contador} ---")

def inspccionar_dibujos(nombre_archivo: str):
    """
    Imprime en consola los nombres de los dibujos del formulario
    para saber qué claves usar en el diccionario de datos.
    """
    ruta_formulario = OUTPUT_DIR / nombre_archivo
    
    doc = pymupdf.Document(ruta_formulario)
    
    print(f"--- Inspeccionando: {nombre_archivo} ---")
    contador = 0
    for pagina in doc:
        for dibujo in pagina.get_drawings():
            if dibujo["color"] == (0.0, 0.33521997928619385, 0.589614987373352) and dibujo["rect"].x0 == dibujo["rect"].x1:
                contador += 1
                print(dibujo)
                print(f"Tipo: {dibujo["type"]}")
                print(f"Color: {dibujo["color"]}")
                print(f"Grosor: {dibujo["width"]}")
                print("*" * 20)

    print(f"--- Total de dibujos encontrados: {contador} ---")

def llenar_campo(
        pagina: pymupdf.Page,
        campo_buscado: str,
        nombre_widget: str,
        coincidencia: int = 0,
        x: int = 10, y: int = 0,
        ):
    print(f"Buscando campo '{campo_buscado}'...")
    areas = pagina.search_for(campo_buscado)

    if areas:
        print("Encontrado! Creando Widget...\n")

        rectangulo = areas[coincidencia]
        x0 = rectangulo.x1 + x
        x1 = x0 + 10
        y1 = rectangulo.y1 - y
        y0 = y1 - 5

        widget = pymupdf.Widget()
        widget.rect = pymupdf.Rect(x0, y0, x1, y1)
        widget.field_name = nombre_widget
        widget.field_type = 7
        widget.text_fontsize = 10
        widget.border_color = [1,0,0]
        widget.border_width = 1
        widget.field_value = campo_buscado.upper()
        pagina.add_widget(widget)
    else:
        print(f"No se encontró el campo {campo_buscado}\n")
