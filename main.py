import os
import importlib
from nicegui import ui
from fastapi.staticfiles import StaticFiles
from nicegui import app

PAGES_DIR = 'pages'


for filename in os.listdir(PAGES_DIR):
    if filename.endswith('.py') and filename != '__init__.py':
        module_name = f'{PAGES_DIR}.{filename[:-3]}'
        module = importlib.import_module(module_name)
        if hasattr(module, 'create_page'):
            # 自动注册路由，路由名为 /文件名
            ui.page(f'/{filename[:-3]}')(module.create_page)

# 提供 favicon.ico 文件
app.mount('/static', StaticFiles(directory='.'), name='static')

ui.run(
    host='0.0.0.0',
    port=9090
)