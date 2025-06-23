import os
import importlib
from nicegui import ui
from fastapi.staticfiles import StaticFiles
from nicegui import app
from cnlunar import Lunar
from fastapi.responses import HTMLResponse
from fastapi import Request

PAGES_DIR = 'pages'

# 添加PWA支持的HTML头部
pwa_head = '''
    <link rel="manifest" href="/static/manifest.json">
    <meta name="theme-color" content="#4CAF50">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <link rel="icon" href="/static/favicon.ico">
    <script>
        // 简化的Service Worker注册
        if ('serviceWorker' in navigator) {
            navigator.serviceWorker.register('/static/service-worker.js')
                .catch(err => console.log('ServiceWorker 注册失败: ', err));
        }
    </script>
'''

# 添加全局头部
ui.add_head_html(pwa_head)

# 创建简化版离线页面
@app.get("/offline", response_class=HTMLResponse)
async def offline():
    return '''
    <!DOCTYPE html>
    <html lang="zh-CN">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>奇门遁甲 - 离线</title>
        <style>
            body { 
                font-family: sans-serif; 
                text-align: center; 
                padding: 20px; 
            }
            h1 { color: #4CAF50; }
            button { 
                background: #4CAF50; 
                color: white; 
                border: none; 
                padding: 10px 20px; 
                border-radius: 4px; 
                cursor: pointer; 
            }
        </style>
    </head>
    <body>
        <h1>奇门遁甲</h1>
        <p>您当前处于离线状态</p>
        <button onclick="location.reload()">重试</button>
    </body>
    </html>
    '''

for filename in os.listdir(PAGES_DIR):
    if filename.endswith('.py') and filename != '__init__.py':
        module_name = f'{PAGES_DIR}.{filename[:-3]}'
        module = importlib.import_module(module_name)
        if hasattr(module, 'create_page'):
            # 自动注册路由，路由名为 /文件名
            ui.page(f'/{filename[:-3]}')(module.create_page)

# 提供静态文件
app.mount('/static', StaticFiles(directory='static'), name='static')

ui.run(
    host='0.0.0.0',
    port=9080
)