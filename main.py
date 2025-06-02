# main.py
import os
import importlib
from nicegui import ui

PAGES_DIR = 'pages'

for filename in os.listdir(PAGES_DIR):
    if filename.endswith('.py') and filename != '__init__.py':
        module_name = f'{PAGES_DIR}.{filename[:-3]}'
        module = importlib.import_module(module_name)
        if hasattr(module, 'create_page'):
            # 自动注册路由，路由名为 /文件名
            ui.page(f'/{filename[:-3]}')(module.create_page)

ui.run()