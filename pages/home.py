# pages/home.py
from nicegui import ui
from components.navbar import create_navbar
from Services.lunar_build_service import LunarBuildService
from datetime import datetime, timedelta
from cnlunar import Lunar
import sys

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
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
                display: flex;
                justify-content: center;
            }
            .home-container {
                width: 100%;
                max-width: 600px;
                margin: 0 auto;
                padding: 0 10px 16px;
            }
            .info-card {
                margin-bottom: 14px;
                padding: 16px;
                border-radius: 12px;
                box-shadow: 0 2px 8px rgba(0,0,0,0.06);
                background: #ffffff;
                text-align: center;
            }
            .card-title {
                font-size: 17px;
                font-weight: 600;
                display: flex;
                align-items: center;
                justify-content: center;
                gap: 8px;
                margin-bottom: 12px;
                color: #333;
            }
            .card-content {
                font-size: 14px;
                color: #444;
                line-height: 1.5;
                text-align: center;
            }
            .icon {
                font-size: 18px;
            }
            /* 建除日网格布局 */
            .days-grid-container {
                display: flex;
                justify-content: center;
                width: 100%;
            }
            .days-grid {
                display: grid;
                grid-template-columns: repeat(3, 1fr);
                gap: 6px;
                margin-top: 12px;
                width: 100%;
                max-width: 500px;
            }
            .day-card {
                padding: 6px;
                border-radius: 6px;
                background: #f9f9f9;
                border: 1px solid #eaeaea;
                text-align: center;
                cursor: pointer;
                transition: all 0.2s;
                display: grid;
                grid-template-columns: 45px 1fr;
                grid-template-rows: 1fr auto;
                grid-template-areas: 
                    "date build"
                    "date badhours";
                gap: 2px;
                align-items: center;
                height: auto;
                min-height: 70px;
            }
            .day-card:hover {
                box-shadow: 0 3px 10px rgba(0,0,0,0.08);
                transform: translateY(-1px);
            }
            .day-left {
                grid-area: date;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                padding-right: 6px;
                border-right: 1px dashed #eaeaea;
                min-width: 40px;
            }
            .day-date {
                font-size: 18px;
                color: #333;
                font-weight: 600;
                margin: 0;
                line-height: 1;
            }
            .day-day-branch {
                font-size: 12px;
                color: #8e44ad;
                font-weight: 500;
                margin: 2px 0 0 0;
                line-height: 1;
                white-space: nowrap;
                width: 100%;
                text-align: center;
                display: inline-block;
                word-break: keep-all;
                overflow: visible;
            }
            .day-weekday {
                font-size: 10px;
                color: #888;
                margin: 2px 0 0 0;
                line-height: 1;
            }
            .day-build-container {
                grid-area: build;
                text-align: center;
                display: flex;
                flex-direction: column;
                justify-content: center;
            }
            .day-build {
                font-size: 16px;
                font-weight: bold;
                color: #1a73e8;
                margin: 0;
                line-height: 1.2;
                display: flex;
                align-items: center;
                justify-content: center;
            }
            .yellow-path-day {
                color: #f39c12 !important;
                font-weight: bold;
            }
            .black-path-day {
                color: #000000 !important;
                font-weight: bold;
            }
            .day-shensha {
                font-size: 9px;
                color: #9c27b0;
                margin-left: 2px;
                line-height: 1;
                display: inline-block;
            }
            .day-bottom {
                grid-area: badhours;
                text-align: center;
                border-top: 1px dashed #eaeaea;
                padding-top: 2px;
                min-height: 32px; /* 确保有足够的高度容纳两行五不遇时 */
                display: flex;
                flex-direction: column;
                justify-content: center;
            }
            .day-hint {
                font-size: 11px;
                color: #4caf50;
                margin: 0;
                line-height: 1;
                min-height: 24px; /* 与五不遇时区域保持一致的高度 */
                display: flex;
                align-items: center;
                justify-content: center;
            }
            .today-card {
                background: #e8f5e9;
                border-color: #81c784;
            }
            .bad-hours {
                font-size: 11px;
                color: #e53935;
                margin: 0;
                line-height: 1.2;
                display: flex;
                flex-direction: column;
                padding: 2px 0;
                min-height: 24px; /* 确保有足够的高度容纳两行 */
            }
            .bad-hours-items {
                display: flex;
                flex-direction: column;
                align-items: center;
                gap: 2px;
                min-height: 24px; /* 确保有足够的高度容纳两行 */
            }
            .bad-hour-item {
                font-size: 10px;
                color: #e53935;
                margin: 0;
                line-height: 1.2;
                white-space: nowrap;
                overflow: hidden;
                text-overflow: ellipsis;
                max-width: 100%;
            }
            /* 功能卡片样式 */
            .feature-container {
                display: flex;
                flex-direction: column;
                align-items: center;
                width: 100%;
            }
            .feature-card {
                display: flex;
                align-items: center;
                padding: 12px;
                border-radius: 8px;
                background: #f9f9f9;
                margin-bottom: 10px;
                border: 1px solid #f0f0f0;
                width: 100%;
                max-width: 500px;
            }
            .feature-icon {
                width: 44px;
                height: 44px;
                display: flex;
                align-items: center;
                justify-content: center;
                border-radius: 50%;
                margin-right: 14px;
                color: white;
                font-size: 20px;
            }
            .feature-text {
                flex: 1;
            }
            .feature-title {
                font-weight: 600;
                margin-bottom: 3px;
                color: #333;
                font-size: 15px;
            }
            .feature-desc {
                font-size: 12px;
                color: #666;
                line-height: 1.4;
            }
            /* 移动端优化 */
            @media (max-width: 480px) {
                .home-container {
                    padding: 0 8px 12px;
                }
                .info-card {
                    margin-bottom: 12px;
                    padding: 14px;
                    border-radius: 10px;
                }
                .card-title {
                    font-size: 16px;
                    margin-bottom: 10px;
                }
                .card-content {
                    font-size: 13px;
                }
                .days-grid {
                    grid-template-columns: repeat(2, 1fr);
                    gap: 6px;
                }
                .day-card {
                    padding: 6px 3px;
                }
                .day-date {
                    font-size: 15px;
                }
                .day-build {
                    font-size: 16px;
                }
                .day-shensha {
                    font-size: 9px;
                }
            }
            /* 添加CSS样式，用于处理高亮状态 */
            .selected-card {
                background-color: #e8f5e9 !important;
                border-color: #81c784 !important;
                box-shadow: 0 0 8px rgba(0, 128, 0, 0.3) !important;
            }
            .selected-day-card {
                background-color: #e8f5e9 !important;
                border-color: #81c784 !important;
                box-shadow: 0 0 8px rgba(0,128,0,0.3) !important;
            }
            .highlight-card {
                background-color: #e8f5e9 !important;
                border-color: #81c784 !important;
                box-shadow: 0 0 8px rgba(0,128,0,0.3) !important;
            }
        </style>
    ''')
    
    # 添加导航栏
    create_navbar()
    
    # 初始化建除服务
    build_service = LunarBuildService()
    days_info = build_service.get_next_12_days_build_info()
    
    # 主要内容
    with ui.column().classes('home-container'):
        # 信息显示框1 - 不需要标题
        with ui.card().classes('info-card w-full'):
            # 显示北京时间和八字
            with ui.element('div').classes('card-content w-full'):
                # 创建一个美观的容器，使其填满宽度
                with ui.element('div').classes('p-3 rounded-lg bg-gray-50 w-full'):
                    # 时间显示，使其填满宽度
                    with ui.element('div').classes('text-center mb-3 pb-2 border-b border-gray-200 w-full'):
                        ui.label('').classes('text-lg font-bold beijing-time-pure w-full')
                    
                    # 八字内容，直接显示，不需要标题
                    current_bazi_html = ui.html("加载中...").classes('text-center text-purple-600 font-bold w-full')
            
            # 添加JavaScript更新北京时间
            ui.add_body_html("""
            <script>
            function updateBeijingTime() {
                // 获取北京时间
                let now = new Date();
                let beijingOffset = 8 * 60 * 60 * 1000; // 北京时间偏移量（+8小时）
                let beijingTime = new Date(now.getTime() + (beijingOffset + now.getTimezoneOffset() * 60 * 1000));
                
                // 格式化时间
                let year = beijingTime.getFullYear();
                let month = (beijingTime.getMonth() + 1).toString().padStart(2, '0');
                let day = beijingTime.getDate().toString().padStart(2, '0');
                let hours = beijingTime.getHours().toString().padStart(2, '0');
                let minutes = beijingTime.getMinutes().toString().padStart(2, '0');
                let seconds = beijingTime.getSeconds().toString().padStart(2, '0');
                
                let timeString = `${year}年${month}月${day}日 ${hours}:${minutes}:${seconds}`;
                
                // 更新显示
                let elements = document.getElementsByClassName('beijing-time-pure');
                if (elements.length > 0) {
                    elements[0].textContent = timeString;
                }
                
                // 每秒更新一次
                setTimeout(updateBeijingTime, 1000);
            }
            
            // 立即执行一次
            updateBeijingTime();
            </script>
            """)
            
            # 服务器端获取当前八字并显示
            def update_bazi():
                now = datetime.now()
                lunar = Lunar(now, godType='8char')
                
                # 获取各柱的天干和地支
                year_gan = lunar.year8Char[0]  # 年柱天干
                year_zhi = lunar.year8Char[1]  # 年柱地支
                month_gan = lunar.month8Char[0]  # 月柱天干
                month_zhi = lunar.month8Char[1]  # 月柱地支
                day_gan = lunar.day8Char[0]  # 日柱天干
                day_zhi = lunar.day8Char[1]  # 日柱地支
                hour_gan = lunar.twohour8Char[0]  # 时柱天干
                hour_zhi = lunar.twohour8Char[1]  # 时柱地支
                
                # 获取五行颜色
                service = LunarBuildService()
                year_gan_color = service.wuxing_colors.get(service.tiangan_wuxing.get(year_gan, ""), "#000000")
                year_zhi_color = service.wuxing_colors.get(service.dizhi_wuxing.get(year_zhi, ""), "#000000")
                month_gan_color = service.wuxing_colors.get(service.tiangan_wuxing.get(month_gan, ""), "#000000")
                month_zhi_color = service.wuxing_colors.get(service.dizhi_wuxing.get(month_zhi, ""), "#000000")
                day_gan_color = service.wuxing_colors.get(service.tiangan_wuxing.get(day_gan, ""), "#000000")
                day_zhi_color = service.wuxing_colors.get(service.dizhi_wuxing.get(day_zhi, ""), "#000000")
                hour_gan_color = service.wuxing_colors.get(service.tiangan_wuxing.get(hour_gan, ""), "#000000")
                hour_zhi_color = service.wuxing_colors.get(service.dizhi_wuxing.get(hour_zhi, ""), "#000000")
                
                # 格式化为柱型显示，添加样式，使其填满宽度
                formatted_bazi = f"""
                <div style="display: flex; justify-content: space-around; width: 100%; text-align: center;">
                    <div class="pillar" style="flex: 1;">
                        <div style="font-size: 22px;"><span style="color: {year_gan_color};">{year_gan}</span></div>
                        <div style="font-size: 22px; margin-top: 4px;"><span style="color: {year_zhi_color};">{year_zhi}</span></div>
                        <div style="font-size: 10px; color: #888; margin-top: 2px;">年柱</div>
                    </div>
                    <div class="pillar" style="flex: 1;">
                        <div style="font-size: 22px;"><span style="color: {month_gan_color};">{month_gan}</span></div>
                        <div style="font-size: 22px; margin-top: 4px;"><span style="color: {month_zhi_color};">{month_zhi}</span></div>
                        <div style="font-size: 10px; color: #888; margin-top: 2px;">月柱</div>
                    </div>
                    <div class="pillar" style="flex: 1;">
                        <div style="font-size: 22px;"><span style="color: {day_gan_color};">{day_gan}</span></div>
                        <div style="font-size: 22px; margin-top: 4px;"><span style="color: {day_zhi_color};">{day_zhi}</span></div>
                        <div style="font-size: 10px; color: #888; margin-top: 2px;">日柱</div>
                    </div>
                    <div class="pillar" style="flex: 1;">
                        <div style="font-size: 22px;"><span style="color: {hour_gan_color};">{hour_gan}</span></div>
                        <div style="font-size: 22px; margin-top: 4px;"><span style="color: {hour_zhi_color};">{hour_zhi}</span></div>
                        <div style="font-size: 10px; color: #888; margin-top: 2px;">时柱</div>
                    </div>
                </div>
                """
                current_bazi_html.set_content(formatted_bazi)
            
            # 初始更新一次八字
            update_bazi()
            
            # 每分钟更新一次八字
            ui.timer(60, update_bazi)
        
        # 信息显示框2 - 十二建除日（网格布局）
        with ui.card().classes('info-card w-full'):
            with ui.element('div').classes('card-title'):
                ui.html('<i class="fas fa-calendar-alt text-green-500 icon"></i>')
                ui.label('未来十二天建除日')
            
            with ui.element('div').classes('card-content days-grid-container'):
                with ui.element('div').classes('days-grid'):
                    for i, day in enumerate(days_info):
                        # 判断是否为今天
                        is_today = i == 0
                        day_class = 'day-card today-card' if is_today else 'day-card'
                        
                        # 获取日期和日柱
                        day_number = day['date'].split('-')[2]
                        day_pillar = day['bazi'].split(' ')[2]  # 八字的第三个元素是日柱
                        
                        # 创建格子元素
                        day_card = ui.element('div').classes(day_class)
                        
                        # 左侧日期和日柱
                        with day_card:
                            with ui.element('div').classes('day-left'):
                                ui.label(day_number).classes('day-date')  # 日期数字
                                # 使用天干地支的五行颜色
                                ui.html(f"<div class='day-day-branch'><span style='color:{day['bazi_colors']['day_gan']};'>{day['day_gan']}</span><span style='color:{day['bazi_colors']['day_zhi']};'>{day['day_zhi']}</span></div>")
                                ui.label(f"周{day['weekday']}").classes('day-weekday')
                            
                            # 右上建除日和神煞
                            with ui.element('div').classes('day-build-container'):
                                # 将建除日和神煞放在同一行
                                if day['is_yellow_path']:
                                    ui.html(f"<span class='yellow-path-day'>{day['jianchu']}</span> <span class='day-shensha'>({day['shensha']})</span>").classes('day-build')
                                elif day['is_black_path']:
                                    ui.html(f"<span class='black-path-day'>{day['jianchu']}</span> <span class='day-shensha'>({day['shensha']})</span>").classes('day-build')
                                else:
                                    ui.html(f"{day['jianchu']} <span class='day-shensha'>({day['shensha']})</span>").classes('day-build')
                            
                            # 右下五不遇时
                            with ui.element('div').classes('day-bottom'):
                                # 显示五不遇时摘要
                                if day['five_bad_hours']:
                                    with ui.element('div').classes('bad-hours'):
                                        with ui.element('div').classes('bad-hours-items'):
                                            # 始终显示两个位置的五不遇时
                                            for j in range(min(2, len(day['five_bad_hours']))):
                                                ui.label(day['five_bad_hours'][j]).classes('bad-hour-item')
                                            
                                            # 如果只有一个五不遇时，添加一个空的占位符保持高度一致
                                            if len(day['five_bad_hours']) == 1:
                                                ui.label('').classes('bad-hour-item')
                                            
                                            # 如果有超过两个，在第二个后显示...
                                            elif len(day['five_bad_hours']) > 2:
                                                ui.label('...').classes('bad-hour-item')
                                else:
                                    ui.label('点击查看详情').classes('day-hint')
                        
                        # 定义点击事件处理函数
                        def create_click_handler(day_data):
                            def on_click():
                                # 显示详情对话框
                                with ui.dialog() as dialog, ui.card().classes('p-4'):
                                    ui.label(f"{day_data['date']}（周{day_data['weekday']}）").classes('text-lg font-bold mb-2 text-center')
                                    
                                    # 八字和建除十二神放在同一排
                                    with ui.element('div').classes('flex justify-center items-center gap-4 mb-1'):
                                        # 使用五行颜色显示八字
                                        bazi_html = f"八字：<span style='color:{day_data['bazi_colors']['year_gan']};'>{day_data['bazi'].split(' ')[0][0]}</span><span style='color:{day_data['bazi_colors']['year_zhi']};'>{day_data['bazi'].split(' ')[0][1]}</span> <span style='color:{day_data['bazi_colors']['month_gan']};'>{day_data['bazi'].split(' ')[1][0]}</span><span style='color:{day_data['bazi_colors']['month_zhi']};'>{day_data['bazi'].split(' ')[1][1]}</span> <span style='color:{day_data['bazi_colors']['day_gan']};'>{day_data['bazi'].split(' ')[2][0]}</span><span style='color:{day_data['bazi_colors']['day_zhi']};'>{day_data['bazi'].split(' ')[2][1]}</span> <span style='color:{day_data['bazi_colors']['hour_gan']};'>{day_data['bazi'].split(' ')[3][0]}</span><span style='color:{day_data['bazi_colors']['hour_zhi']};'>{day_data['bazi'].split(' ')[3][1]}</span>"
                                        ui.html(bazi_html).classes('text-center')
                                        ui.label("|").classes('text-gray-400')
                                        
                                        # 根据是否为黄道日或黑道日使用不同的样式
                                        if day_data['is_yellow_path']:
                                            build_class = 'text-yellow-500 font-bold'
                                            day_type_text = f"（{day_data['day_type']}）"
                                        elif day_data['is_black_path']:
                                            build_class = 'text-black font-bold'
                                            day_type_text = f"（{day_data['day_type']}）"
                                        else:
                                            build_class = 'text-blue-600'
                                            day_type_text = ""
                                        ui.html(f"建除十二神：<span class='{build_class}'>{day_data['jianchu']} <span style='color: #9c27b0;'>({day_data['shensha']})</span>{day_type_text}</span>").classes('text-center')
                                    
                                    ui.label('宜：' + (day_data['yi'] or '无')).classes('mb-1 text-green-600 text-center')
                                    ui.label('忌：' + (day_data['ji'] or '无')).classes('mb-1 text-red-600 text-center')
                                    
                                    # 显示全部时辰，五不遇时标红
                                    ui.label("当日时辰：").classes('mt-2 font-bold text-center')
                                    
                                    # 创建时辰列表 - 分两排显示
                                    with ui.element('div').classes('mt-1 text-center'):
                                        # 去掉最后一个时辰
                                        display_hours = day_data['twohour_list'][:-1]
                                        
                                        # 分为两排，每排6个
                                        first_row = []
                                        second_row = []
                                        
                                        for j, hour in enumerate(display_hours):
                                            # 判断是否为五不遇时
                                            is_bad_hour = False
                                            for bad_hour in day_data['five_bad_hours']:
                                                if bad_hour.startswith(hour):
                                                    is_bad_hour = True
                                                    break
                                            
                                            # 获取时辰天干地支的五行颜色
                                            service = LunarBuildService()
                                            hour_gan_color = service.wuxing_colors.get(service.tiangan_wuxing.get(hour[0], ""), "#000000")
                                            hour_zhi_color = service.wuxing_colors.get(service.dizhi_wuxing.get(hour[1], ""), "#000000")
                                            
                                            # 添加到对应行，五不遇时用红色标记，其他时辰用五行颜色
                                            if is_bad_hour:
                                                hour_text = f'<span class="text-red-600 font-bold">{hour}</span>'
                                            else:
                                                hour_text = f'<span style="color:{hour_gan_color};">{hour[0]}</span><span style="color:{hour_zhi_color};">{hour[1]}</span>'
                                            
                                            if j < 6:  # 前6个放第一行
                                                first_row.append(hour_text)
                                            else:  # 后5个放第二行
                                                second_row.append(hour_text)
                                        
                                        # 显示第一行
                                        ui.html('、'.join(first_row)).classes('text-sm mb-1')
                                        # 显示第二行
                                        ui.html('、'.join(second_row)).classes('text-sm')
                                    
                                    with ui.element('div').classes('flex justify-center mt-3'):
                                        ui.button('关闭', on_click=dialog.close).classes('bg-blue-500 text-white')
                                
                                dialog.open()
                            return on_click
                        
                        # 绑定点击事件
                        day_card.on('click', create_click_handler(day))