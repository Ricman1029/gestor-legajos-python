from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]

STORAGE_DIR = BASE_DIR / "storage"
TEMP_DIR = STORAGE_DIR / "temp"

ASSETS_DIR = BASE_DIR / "assets"
TEMPLATES_DIR = ASSETS_DIR / "templates"

TYPST_TEMPLATES_DIR = TEMPLATES_DIR / "typst"
FORMS_TEMPLATES_DIR = TEMPLATES_DIR / "forms"

OUTPUT_DIR = BASE_DIR / "output_pdfs"

OUTPUT_DIR.mkdir(exist_ok=True)
