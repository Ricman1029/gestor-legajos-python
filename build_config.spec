# -*- mode: python ; coding: utf-8 -*-


block_cipher = None

# 1. DEFINICIÓN DE LIBRERÍAS OCULTAS
# Aquí listamos TODAS las librerías que PyInstaller suele ignorar.
hidden_imports = [
    'sqlalchemy',
    'sqlalchemy.ext.asyncio',
    'aiosqlite',
    'babel',
    'babel.dates',
    'pydantic',
    'pymupdf',
    'typst',
    'flet',
]

a = Analysis(
    ['main.py'],
    pathex=['.'],
    binaries=[],
    datas=[
        ('assets', 'assets'),
    ],
    hiddenimports=hidden_imports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='GestorLegajos',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='GestorLegajos',
)
