# pages/home.py
from nicegui import ui
from components.navbar import create_navbar

@ui.page('/')  # 注册根路径
def main():
    # 添加视口设置和样式
    ui.add_head_html('''
        <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
        <style>
            body {
                margin: 0;
                padding: 0;
                background-color: #f5f5f5;
            }
            .home-container {
                max-width: 100%;
                margin: 0 auto;
                padding: 0 12px 16px;
            }
            .info-card {
                margin-bottom: 14px;
                padding: 14px;
                border-radius: 8px;
                box-shadow: 0 1px 3px rgba(0,0,0,0.08);
                background: #ffffff;
            }
            .card-title {
                font-size: 16px;
                font-weight: bold;
                display: flex;
                align-items: center;
                gap: 6px;
                margin-bottom: 8px;
            }
            .card-content {
                font-size: 14px;
                color: #444;
                line-height: 1.4;
            }
            .icon {
                font-size: 16px;
            }
            /* 移动端优化 */
            @media (max-width: 480px) {
                .home-container {
                    padding: 0 8px 12px;
                }
                .info-card {
                    margin-bottom: 12px;
                    padding: 12px;
                }
                .card-title {
                    font-size: 15px;
                }
                .card-content {
                    font-size: 13px;
                }
            }
        </style>
    ''')
    
    # 添加导航栏
    create_navbar()
    
    # 主要内容
    with ui.column().classes('home-container'):
        # 信息显示框1
        with ui.card().classes('info-card w-full'):
            with ui.element('div').classes('card-title'):
                ui.html('<i class="fas fa-bell text-blue-500 icon"></i>')
                ui.label('系统公告')
            with ui.element('div').classes('card-content'):
                ui.label('''欢迎使用奇门遁甲排盘系统！本系统提供精准的奇门遁甲排盘服务，支持真太阳时计算。点击上方"排盘系统"开始使用。''')
        
        # 信息显示框2
        with ui.card().classes('info-card w-full'):
            with ui.element('div').classes('card-title'):
                ui.html('<i class="fas fa-chart-line text-green-500 icon"></i>')
                ui.label('使用统计')
            with ui.element('div').classes('card-content'):
                ui.label('今日排盘次数：58次')
                ui.label('系统已服务用户：1,245人').classes('mt-1')