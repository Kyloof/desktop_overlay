# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['src/desktop_overlay/main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('src/desktop_overlay/mods', 'desktop_overlay/mods'),
        ('src/desktop_overlay/ui/assets', 'desktop_overlay/ui/assets'),
        ('src/desktop_overlay/definitions.py', 'desktop_overlay')
    ],
    hiddenimports=[
        'desktop_overlay.mods.note_mod.note_mod',
        'desktop_overlay.mods.spotify_mod.spotify_mod',
        'desktop_overlay.mods.web_mod.web_mod',
    ],
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
    [],
    exclude_binaries=True,
    name='main',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='main',
)
