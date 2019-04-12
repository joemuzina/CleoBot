# -*- mode: python ; coding: utf-8 -*-

block_cipher = None
added_data = [
	('cleo_data/*.txt', 'cleo_data')
	]

a = Analysis(['cleobot.py'],
             pathex=['/Users/joemuzina/Documents/coding/cleopatrick_bot'],
             binaries=[],
             datas= added_data,
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='cleobot',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=True )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='cleobot')
