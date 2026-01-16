# -*- mode: python ; coding: utf-8 -*-

import sys
from PyInstaller.utils.hooks import collect_data_files, collect_submodules

block_cipher = None

# Collect all data files
datas = [
    ('config.yaml', '.'),
    ('copilot_agent_client', 'copilot_agent_client'),
    ('copilot_agent_server', 'copilot_agent_server'),
    ('copilot_front_end', 'copilot_front_end'),
    ('copilot_tools', 'copilot_tools'),
    ('tools', 'tools'),
]

# Collect hidden imports
hiddenimports = [
    # GUI
    'tkinter',
    'tkinter.ttk',
    'tkinter.scrolledtext',
    'tkinter.filedialog',
    'tkinter.messagebox',
    
    # Image processing
    'PIL',
    'PIL.Image',
    'PIL.ImageDraw',
    'PIL.ImageFont',
    'cv2',
    
    # YAML
    'yaml',
    
    # HTTP clients
    'aiohttp',
    'aiohttp.client',
    'aiohttp.connector',
    'httpx',
    'httpx._client',
    'httpcore',
    'httpcore._sync',
    'httpcore._async',
    
    # Async
    'asyncio',
    'aiohttp',
    'aiohappyeyeballs',
    'aiosignal',
    
    # Data processing
    'numpy',
    'pandas',
    'openpyxl',
    
    # Networking
    'requests',
    'urllib3',
    'certifi',
    'charset_normalizer',
    
    # JSON/Data
    'json',
    'jsonlines',
    'jsonschema',
    
    # Crypto
    'cryptography',
    'bcrypt',
    'pynacl',
    
    # SSH/Network
    'paramiko',
    
    # Redis/Cache
    'redis',
    'fakeredis',
    'diskcache',
    
    # FastAPI/Starlette
    'fastapi',
    'starlette',
    'uvicorn',
    'pydantic',
    'pydantic_core',
    
    # MCP
    'mcp',
    'fastmcp',
    
    # OpenAI
    'openai',
    
    # Logging
    'python_json_logger',
    
    # Other utilities
    'click',
    'tqdm',
    'rich',
    'markdown_it_py',
    'pygments',
    'docstring_parser',
    'beartype',
    'cyclopts',
    'typer',
    'shellingham',
    
    # File handling
    'megfile',
    'pathvalidate',
    
    # Windows specific
    'pywin32',
    'win32api',
    'win32con',
    'win32gui',
    'pygetwindow',
    
    # Subprocess and system
    'subprocess',
    'threading',
    'queue',
    'datetime',
    'pathlib',
]

# Analysis
a = Analysis(
    ['gui_app.py'],
    pathex=[],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'matplotlib',
        'scipy',
        'jupyter',
        'notebook',
        'IPython',
        'pytest',
        'sphinx',
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='GelabZeroTaskRunner_v1.0.0',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # Set to False to hide console window
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='app_icon.ico',  # Icon file for the executable
    version='version_info.txt',  # Version information file
)
