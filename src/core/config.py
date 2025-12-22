import sys
import os
from pathlib import Path

IS_FROZEN = getattr(sys, "frozen", False)
IS_WEB = os.environ.get("APP_TYPE") == "WEB"

def get_base_path():
    if IS_FROZEN:
        if hasattr(sys, "_MEIPASS"):
            return Path(sys._MEIPASS)
        return Path(sys.executable).parent / "_internal"
    else:
        return Path(__file__).resolve().parents[2]

BASE_DIR = get_base_path()
ASSETS_DIR = BASE_DIR / "assets"
TEMP_DIR = BASE_DIR / "temp"

if IS_FROZEN:
    USER_DOCS = Path(os.path.expanduser("~")) / "Documents" / "GestorLegajos"
    OUTPUT_DIR = USER_DOCS / "Contratos Generados"
elif IS_WEB:
    USER_DOCS = BASE_DIR
    OUTPUT_DIR = ASSETS_DIR / "generated"
else:
    USER_DOCS = BASE_DIR
    OUTPUT_DIR = USER_DOCS / "Contratos Generados"

USER_DOCS.mkdir(parents=True, exist_ok=True)
TEMP_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

TEMPLATES_DIR = ASSETS_DIR / "templates"
TYPST_TEMPLATES_DIR = TEMPLATES_DIR / "typst"
FORMS_TEMPLATES_DIR = TEMPLATES_DIR / "forms"


