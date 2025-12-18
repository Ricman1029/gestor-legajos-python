import sys
import os
import multiprocessing

if getattr(sys, "frozen", False):
    os.chdir(sys._MEIPASS)
    sys.path.append(sys._MEIPASS)
else:
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import flet as ft
from src.main_app import main

if __name__ == "__main__":
    multiprocessing.freeze_support()
    ft.app(target=main, assets_dir="assets")
