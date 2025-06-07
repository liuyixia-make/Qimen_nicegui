import datetime
import pytz
from nicegui import ui
from Services.paipan_servise import 奇门遁甲
from urllib.parse import urlencode
from components.navbar import create_navbar

@ui.page('/paipan')
async def paipan_page():
    # 获取北京时间
    beijing_tz = pytz.timezone('Asia/Shanghai')
    current_beijing_time = datetime.datetime.now(beijing_tz)
    default_time = current_beijing_time.strftime("%Y-%m-%dT%H:%M")

    ui.add_head_html(f'''
        <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
        <style>
            body {{
                margin: 0;
                padding: 0;
                background-color: #f5f5f5;
            }}
            .datetime-input {{
                -webkit-appearance: none;
                font-size: 15px !important;
                touch-action: manipulation;
                height: 40px !important;
                width: 100%;
                border: 1px solid #ccc;
                border-radius: 6px;
                padding: 0 10px;
            }}
            
            .form-card {{
                padding: 16px !important;
                border-radius: 8px;
                box-shadow: 0 1px 3px rgba(0,0,0,0.08);
                background: #ffffff;
                margin: 0 12px;
            }}
            
            .form-grid {{
                display: grid;
                grid-template-columns: 1fr;
                gap: 14px;
                width: 100%;
            }}
            
            .form-title {{
                margin-bottom: 12px !important;
                font-size: 18px;
            }}
            
            .form-label {{
                font-size: 14px;
                font-weight: 500;
                margin-bottom: 4px;
                display: block;
            }}
            
            .form-group {{
                margin-bottom: 6px;
            }}
            
            .submit-btn {{
                height: 40px;
                font-size: 15px !important;
                width: 100%;
                margin-top: 8px;
            }}
            
            /* 移动端优化 */
            @media (max-width: 480px) {{
                .form-card {{
                    padding: 14px !important;
                    margin: 0 8px;
                }}
                
                .form-grid {{
                    gap: 12px;
                }}
                
                .form-title {{
                    margin-bottom: 10px !important;
                    font-size: 17px;
                }}
                
                .datetime-input {{
                    font-size: 14px !important;
                    height: 38px !important;
                }}
                
                .submit-btn {{
                    height: 38px;
                    font-size: 14px !important;
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

    # 添加导航栏
    create_navbar()

    with ui.card().classes('form-card w-full max-w-md mx-auto'):
        ui.label('奇门遁甲排盘').classes('text-center w-full form-title font-bold')
        
        with ui.element('div').classes('form-grid'):
            # 第一行：日期时间选择器
            with ui.element('div').classes('form-group'):
                ui.label('起卦时间 (北京时间)').classes('form-label')
                ui.html(f'''
                    <input type="datetime-local" 
                           id="datetime_input"
                           class="datetime-input">
                ''')
            
            # 第二行：起局法选择器
            with ui.element('div').classes('form-group'):
                ui.label('起局法').classes('form-label')
                method = ui.select(
                    options=['拆补法', '置润法'],
                    value='拆补法'
                ).classes('w-full')
            
            # 第三行：真太阳时开关
            with ui.element('div').classes('form-group items-center'):
                use_true_solar_time = ui.switch(text='使用真太阳时', value=True)
                ui.tooltip('开启后需要输入地区，以计算真太阳时；关闭则直接使用北京时间').classes('text-xs')
            
            # 第四行：地区输入框
            area_container = ui.element('div').classes('form-group')
            with area_container:
                ui.label('地区').classes('form-label')
                area = ui.input(
                    value='合浦县'
                ).classes('w-full')
            
            # 第五行：生成按钮
            with ui.element('div').classes('form-group'):
                ui.button(
                    '生成奇门遁甲排盘', 
                    on_click=lambda: on_submit()
                ).classes('submit-btn bg-blue-500 hover:bg-blue-600 text-white rounded-lg font-medium')
        
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