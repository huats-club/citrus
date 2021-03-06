# -*- mode: python ; coding: utf-8 -*-


block_cipher = None

# Info: if ttkbootstrap causes error:
# https://stackoverflow.com/questions/67850998/ttkbootstrap-not-working-with-pyinstaller

a = Analysis(["main.py"],
             pathex=["C:\\Users\\65844\\Desktop\\citrus"],
             binaries=[],
             datas=[('assets\\themes.json', 'ttkbootstrap'), ('assets\\Symbola.ttf', 'ttkbootstrap')],
             hiddenimports=["ttkbootstrap"],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)

a.datas += [("assets/seedling.ico", "C:\\Users\\65844\\Desktop\\citrus\\assets\\seedling.ico", "DATA")]

pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name="citrus",
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=True,
          icon="assets\\seedling.ico"
          )