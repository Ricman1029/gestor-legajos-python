import typst
import json
import logging
from pathlib import Path
from uuid import uuid4

# Definimos rutas
BASE_DIR = Path(__file__).resolve().parents[3]
TEMPLATE_PATH = BASE_DIR / "assets" / "templates" / "contrato_base.typ"
OUTPUT_DIR = BASE_DIR / "output_pdfs"

# Creamos carpeta de salida si no existe
OUTPUT_DIR.mkdir(exist_ok=True)

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

            # 2. Generamos nombres de archivo únicos para que no se pisen los templates temporales
            unique_id = uuid4().hex[:8]
            json_filename = f"temp_{nombre_base}_{unique_id}.json"
            typ_filenmae = f"temp_{nombre_base}_{unique_id}.typ"
            pdf_filename = f"{nombre_base}.pdf"

            json_path = OUTPUT_DIR / json_filename
            typ_path = OUTPUT_DIR / typ_filenmae
            pdf_path = OUTPUT_DIR / pdf_filename
            
            # 3. Guardamos los datos en JSON
            # ensure_ascii=False permite guardar tildes y ñ correctametne
            with open(json_path, "w", encoding="utf-8") as archivo:
                json.dump(datos, archivo, indent=2, ensure_ascii=False)

            # 4. Leemos el template y apuntamos al json creado
            with open(TEMPLATE_PATH, "r", encoding="utf-8") as archivo:
                content = archivo.read()

            # Reemplazamos solo la ruta del JSON
            content = content.replace("DATA_JSON_PATH", json_filename)

            # 5. Guardar el archivo .typ temporal listo para compilar
            with open(typ_path, "w", encoding="utf-8") as archivo:
                archivo.write(content)

            # 6. Compilar
            logging.info(f"Compilando Typst: {typ_path} -> {pdf_path}")
            typst.compile(str(typ_path), output=str(pdf_path))

            # 7. Limpiamos los archivos temporales
            json_path.unlink()
            typ_path.unlink()

            return str(pdf_path)
        except Exception as e:
            logging.error(f"Error generando PDF: {e}")
            return None
            
