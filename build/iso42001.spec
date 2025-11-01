# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller spec file for ISO 42001 AI Management System

This spec file creates a standalone executable for the ISO 42001 application
with all dependencies bundled.
"""

import os
import sys
from pathlib import Path

# Get the project root directory (parent of build directory)
spec_root = Path(os.getcwd())

# Add the src directory to Python path
sys.path.insert(0, str(spec_root / 'src'))

# Import version information
from iso42001 import __version__, __author__

block_cipher = None

# Data files to include
datas = [
    # Include the entire data directory
    (str(spec_root / 'data'), 'data'),
    # Include docs directory
    (str(spec_root / 'docs'), 'docs'),
    # Include requirements for reference
    (str(spec_root / 'requirements.txt'), '.'),
    # Include README
    (str(spec_root / 'README.md'), '.'),
    # Include LICENSE
    (str(spec_root / 'LICENSE'), '.'),
]

# Hidden imports for Dash and dependencies
hiddenimports = [
    'dash',
    'dash.dependencies',
    'dash_bootstrap_components',
    'plotly',
    'plotly.express',
    'plotly.graph_objects',
    'pandas',
    'sqlite3',
    'base64',
    'io',
    'datetime',
    'openpyxl',
    'werkzeug.security',
    'flask',
    'flask.helpers',
    'dash_table',
    'dash.dash_table',
    'dash.html',
    'dash.dcc',
    'iso42001.app',
    'iso42001.database',
    'iso42001.callbacks',
    'iso42001.cli',
]

# Binaries - empty for now
binaries = []

# Analysis
a = Analysis(
    ['main.py'],
    pathex=[str(spec_root)],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'tkinter',
        'matplotlib',
        'IPython',
        'jupyter',
        'notebook',
        'sphinx',
        'pytest',
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

# Remove duplicates
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

# Executable configuration
exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='ISO42001-AIManagementSystem',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,  # Set to False for windowed app
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    version='version_info.txt',  # We'll create this
    icon='assets/icon.ico' if os.path.exists('assets/icon.ico') else None,
)

# Optional: Create app bundle for distribution
# Uncomment if you want a directory distribution instead of single file
# coll = COLLECT(
#     exe,
#     a.binaries,
#     a.zipfiles,
#     a.datas,
#     strip=False,
#     upx=True,
#     upx_exclude=[],
#     name='ISO42001-AIManagementSystem'
# )