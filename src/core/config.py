import sys
import os
from pathlib import Path

def get_base_path():
    if getattr(sys, "frozen", False):
        return Path(sys._MEIPASS)
    else:
        return Path(__file__).resolve().parents[2]

BASE_DIR = get_base_path()

if getattr(sys, "frozen", False):
    USER_DOCS = Path(os.path.expanduser("~")) / "Documents" / "GestorLegajos"
else:
    USER_DOCS = BASE_DIR

OUTPUT_DIR = USER_DOCS / "Contratos Generados"
TEMP_DIR = BASE_DIR / "temp"
TEMP_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

ASSETS_DIR = BASE_DIR / "assets"
TEMPLATES_DIR = ASSETS_DIR / "templates"
TYPST_TEMPLATES_DIR = TEMPLATES_DIR / "typst"
FORMS_TEMPLATES_DIR = TEMPLATES_DIR / "forms"


