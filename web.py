import os
import sys

os.environ["APP_TYPE"] = "WEB"

import flet as ft
from src.main_app import main

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    print(f"Iniciando en modo WEB en el puerto {port}...")

    ft.app(
            target=main,
            view=ft.WEB_BROWSER,
            port=port,
            host="0.0.0.0",
            assets_dir="assets",
            )
