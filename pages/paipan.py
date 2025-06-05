import datetime
import pytz
from nicegui import ui
from Services.paipan_servise import 奇门遁甲
from urllib.parse import urlencode

@ui.page('/paipan')
async def paipan_page():
    # 获取北京时间
    beijing_tz = pytz.timezone('Asia/Shanghai')
    current_beijing_time = datetime.datetime.now(beijing_tz)
    default_time = current_beijing_time.strftime("%Y-%m-%dT%H:%M")

    ui.add_head_html(f'''
        <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
        <style>
            .datetime-input {{
                -webkit-appearance: none;
                font-size: 14px !important;
                touch-action: manipulation;
                height: 36px !important;
            }}
            
            .compact-card {{
                padding: 0.75rem !important;
            }}
            
            .compact-grid {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
                gap: 8px;
                width: 100%;
            }}
            
            .compact-title {{
                margin-bottom: 0.5rem !important;
            }}
            
            .full-width {{
                grid-column: 1 / -1;
            }}
            
            @media (max-width: 480px) {{
                .compact-grid {{
                    grid-template-columns: 1fr;
                }}
            }}
        </style>
        <script>
            document.addEventListener('DOMContentLoaded', function() {{
                setTimeout(function() {{
                    var input = document.getElementById("datetime_input");
                    if(input) {{
                        input.value = "{default_time}";
                    }}
                }}, 100);
            }});
        </script>
    ''')

    with ui.card().classes('w-full max-w-3xl mx-auto compact-card'):
        ui.label('奇门遁甲排盘').classes('text-lg font-bold text-center w-full compact-title')
        
        with ui.element('div').classes('compact-grid'):
            # 第一行：日期时间选择器（占据整行）
            with ui.element('div').classes('full-width'):
                ui.html(f'''
                    <div class="w-full">
                        <label class="block text-sm font-medium text-gray-700 mb-1">起卦时间 (北京时间)</label>
                        <input type="datetime-local" 
                               id="datetime_input"
                               class="datetime-input w-full px-2 py-1 bg-white border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm">
                    </div>
                ''')
            
            # 第二行：左侧 - 起局法选择器
            with ui.element('div'):
                method = ui.select(
                    label='起局法',
                    options=['拆补法', '置润法'],
                    value='拆补法'
                ).classes('w-full')
            
            # 第二行：右侧 - 真太阳时开关
            with ui.element('div').classes('flex items-center'):
                use_true_solar_time = ui.switch(text='使用真太阳时', value=True)
                ui.tooltip('开启后需要输入地区，以计算真太阳时；关闭则直接使用北京时间').classes('text-xs')
            
            # 第三行：地区输入框（受真太阳时开关控制）
            area_container = ui.element('div').classes('full-width')
            with area_container:
                area = ui.input(
                    label='地区',
                    value='合浦县'
                ).classes('w-full')
            
            # 第四行：生成按钮（占据整行）
            with ui.element('div').classes('full-width'):
                ui.button(
                    '生成奇门遁甲排盘', 
                    on_click=lambda: on_submit()
                ).classes('w-full bg-blue-500 hover:bg-blue-600 text-white py-2 rounded-lg text-base font-medium')
        
        # 当真太阳时开关状态变化时，控制地区输入框的显示与隐藏
        def update_area_visibility():
            if use_true_solar_time.value:
                area_container.set_visibility(True)
            else:
                area_container.set_visibility(False)
        
        use_true_solar_time.on_value_change(update_area_visibility)
        
        # 初始化时调用一次
        update_area_visibility()

        async def on_submit():
            try:
                datetime_str = await ui.run_javascript(
                    'document.getElementById("datetime_input").value.replace("T", " ")'
                )
                
                if not datetime_str:
                    ui.notify('请选择时间', color='warning', position='center')
                    return
                
                # 验证日期格式
                try:
                    import datetime
                    datetime.datetime.strptime(datetime_str, '%Y-%m-%d %H:%M')
                except ValueError:
                    ui.notify('日期格式错误，请使用正确的日期时间格式', color='negative', position='center')
                    return
                
                # 验证方法和地区
                if not method.value:
                    ui.notify('请选择起局法', color='warning', position='center')
                    return
                
                # 如果使用真太阳时，则验证地区
                area_value = None
                if use_true_solar_time.value:
                    if not area.value:
                        ui.notify('请输入地区', color='warning', position='center')
                        return
                    area_value = area.value
                
                params = {
                    'datetime_str': datetime_str,
                    'method': method.value,
                    'area': area_value if use_true_solar_time.value else ''
                }
                
                print(f"[DEBUG] 发送参数: {params}")
                ui.navigate.to(f'/qimen_info?{urlencode(params)}')
                
            except Exception as e:
                print(f"Error in submit: {str(e)}")
                ui.notify(f'错误: {str(e)}', color='negative', position='center')