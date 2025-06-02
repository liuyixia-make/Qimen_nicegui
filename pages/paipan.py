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
                font-size: 16px !important;
                touch-action: manipulation;
            }}
            
            @media (max-width: 640px) {{
                .mobile-container {{
                    padding: 0.5rem !important;
                }}
                .mobile-card {{
                    padding: 1rem !important;
                    margin: 0.5rem !important;
                }}
                .mobile-input {{
                    height: 42px !important;
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

    with ui.column().classes('w-full max-w-md mx-auto p-4 mobile-container'):
        with ui.card().classes('w-full p-4 shadow mobile-card'):
            ui.label('奇门遁甲排盘').classes('text-xl md:text-2xl font-bold text-center w-full mb-4')
            
            ui.html(f'''
                <div class="w-full mb-4">
                    <label class="block text-sm font-medium text-gray-700 mb-1">起卦时间 (北京时间)</label>
                    <input type="datetime-local" 
                           id="datetime_input"
                           class="datetime-input mobile-input w-full px-3 py-2 bg-white border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
                           style="height: 42px;">
                </div>
            ''')
            
            with ui.element('div').classes('mb-4'):
                method = ui.select(
                    label='起局法',
                    options=['拆补法', '时家法', '日家法'],
                    value='拆补法'
                ).classes('w-full mobile-input')
            
            with ui.element('div').classes('mb-4'):
                area = ui.input(
                    label='地区',
                    value='none'
                ).classes('w-full mobile-input')

            async def on_submit():
                try:
                    datetime_str = await ui.run_javascript(
                        'document.getElementById("datetime_input").value.replace("T", " ")'
                    )
                    
                    if not datetime_str:
                        ui.notify('请选择时间', color='warning', position='center')
                        return
                    
                    params = {
                        'datetime_str': datetime_str,
                        'method': method.value,
                        'area': area.value
                    }
                    
                    print(f"[DEBUG] 发送参数: {params}")
                    ui.navigate.to(f'/qimen_info?{urlencode(params)}')
                    
                except Exception as e:
                    print(f"Error in submit: {str(e)}")
                    ui.notify(f'错误: {str(e)}', color='negative', position='center')

            ui.button(
                '生成奇门遁甲排盘', 
                on_click=on_submit
            ).classes('w-full bg-blue-500 hover:bg-blue-600 text-white py-3 rounded-lg text-lg font-medium mt-2')