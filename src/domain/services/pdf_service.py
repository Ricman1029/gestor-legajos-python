import typst
import json
import logging
import pymupdf
from src.core.config import BASE_DIR, TYPST_TEMPLATES_DIR, TEMP_DIR, FORMS_TEMPLATES_DIR, OUTPUT_DIR

TEMPLATE_PATH = TYPST_TEMPLATES_DIR / "generador_legajo.typ"

class PdfService:
    @staticmethod
    def generar_contrato(datos: dict, nombre_base: str) -> str | None:
        """
        Toma un diccionario de datos, reemplaza en el template y compila a PDF.
        Retorna la ruta del archivo generado.
        """
        try: 
            # 1. Leer el template
            if not TEMPLATE_PATH.exists():
                raise FileNotFoundError(f"No se encontró el template en {TEMPLATE_PATH}")

            json_filename = f"temp_datos_typst.json"
            pdf_filename = f"temp_{nombre_base}.pdf"

            json_path = TEMP_DIR / json_filename
            pdf_path = TEMP_DIR / pdf_filename
            
            # 3. Guardamos los datos en JSON
            # ensure_ascii=False permite guardar tildes y ñ correctametne
            with open(json_path, "w", encoding="utf-8") as archivo:
                json.dump(datos, archivo, indent=2, ensure_ascii=False)

            # 6. Compilar
            logging.info(f"Compilando Typst: {TEMPLATE_PATH} -> {pdf_path}")
            typst.compile(str(TEMPLATE_PATH), output=str(pdf_path), root=str(BASE_DIR))

            # 7. Limpiamos los archivos temporales
            json_path.unlink()

            return str(pdf_path)
        except Exception as e:
            logging.error(f"Error generando PDF: {e}")
            return None

    def rellenar_formulario(
            self, 
            datos: dict,
            nombre_formulario: str,
            ) -> str | None:

        ruta_formulario = FORMS_TEMPLATES_DIR / nombre_formulario
        ruta_salida = TEMP_DIR / f"temp_{nombre_formulario}"

        if not ruta_formulario.exists():
            raise FileNotFoundError(f"No existe el archivo {ruta_formulario}")

        try:
            doc = pymupdf.Document(ruta_formulario)

            for page in doc.pages():
                for widget in page.widgets():
                    if widget.field_name in datos:
                        valor = datos[widget.field_name] 

                        rectangulo = widget.rect
                        page.delete_widget(widget)
                        page.insert_text(
                                pymupdf.Point(rectangulo.x0, rectangulo.y1), 
                                str(valor),
                                )
                    
            doc.save(ruta_salida)
            doc.close()
            return str(ruta_salida)
        except Exception as ex:
            print(f"Error rellenando el PDF {ruta_formulario}: {ex}")
            return None

    def _unir_pdfs(self, rutas_pdfs: list[str], nombre_empleado) -> str | None:
        try:
            nombre_archivo = f"Legajo_{nombre_empleado}.pdf"
            ruta_destino = OUTPUT_DIR / nombre_archivo
            
            doc_final = pymupdf.Document()
            for archivo in rutas_pdfs:
                doc = pymupdf.Document(archivo)
                paginas_seguro = 0
                if "anses" in archivo:
                    doc.select([0, 0, 1, 2, 3, 4])
                elif "galeno" in archivo:
                    doc.select([0, 0, 0, 1])
                    paginas_seguro = 4
                elif "mapfre" in archivo:
                    doc.select([0, 2, 4, 5])
                    paginas_seguro = 4
                elif "andina" in archivo:
                    doc.select([0, 0])
                    paginas_seguro = 2
                doc_final.insert_pdf(doc, annots=True, widgets=True)

            doc_final.select([
                # Contrato
                0, 1, 2, 3,
                # Anses
                8, 9, 10, 11, 12, 13,
                # Seguro
                *[i + 14 for i in range(paginas_seguro)],
                # Notificación ART y Obra Social
                4, 5, 6, 7,
                ])
            doc_final.save(ruta_destino)
            return str(ruta_destino)

        except Exception as ex:
            print(f"Error uniendo PDFs: {ex}")
            return None
