from nicegui import ui
from Services.db_service import QimenDBService
from components.navbar import create_navbar
from urllib.parse import urlencode
import datetime

# 添加样式
RECORDS_STYLES = '''
<style>
    body {
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
        background-color: #f5f5f5;
    }
    .record-card {
        transition: all 0.2s ease;
        cursor: pointer;
    }
    .record-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }
    .result-badge {
        padding: 2px 8px;
        border-radius: 12px;
        font-size: 12px;
        font-weight: bold;
    }
    .result-correct {
        background-color: #4CAF50;
        color: white;
    }
    .result-incorrect {
        background-color: #F44336;
        color: white;
    }
    .result-unknown {
        background-color: #9E9E9E;
        color: white;
    }
    .stats-card {
        background-color: #fff;
        border-radius: 8px;
        padding: 10px 16px;
        margin-bottom: 16px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    }
    .stats-container {
        display: flex;
        flex-wrap: wrap;
        justify-content: space-between;
        align-items: center;
        gap: 10px;
    }
    .stats-item {
        display: flex;
        flex-direction: column;
        align-items: center;
        min-width: 60px;
    }
    .stats-label {
        font-size: 12px;
        font-weight: 500;
        color: #666;
        margin-bottom: 2px;
    }
    .stats-value {
        font-weight: 600;
        font-size: 14px;
    }
    .stats-value-correct {
        color: #4CAF50;
    }
    .stats-value-incorrect {
        color: #F44336;
    }
    .stats-value-total {
        color: #2196F3;
    }
    .stats-progress {
        height: 8px;
        width: 100%;
        background-color: #e0e0e0;
        border-radius: 4px;
        margin-top: 8px;
        overflow: hidden;
    }
    .stats-progress-bar {
        height: 100%;
        background-color: #4CAF50;
        border-radius: 4px;
    }
</style>
'''

@ui.page('/qimen_records')
def qimen_records_page():
    """显示历史排盘记录"""
    # 添加样式
    ui.add_head_html(RECORDS_STYLES)
    ui.add_head_html('''
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    ''')
    
    # 添加导航栏
    create_navbar()
    
    # 初始化数据库服务
    db_service = QimenDBService()
    
    # 获取所有记录
    records = db_service.get_all_records()
    
    with ui.column().classes('w-full max-w-3xl mx-auto p-4 gap-4'):
        with ui.row().classes('w-full justify-between items-center'):
            ui.label('历史排盘记录').classes('text-2xl font-bold')
            ui.button('返回排盘', on_click=lambda: ui.navigate.to('/paipan')).classes('bg-blue-500 hover:bg-blue-600 text-white')
        
        # 添加统计信息卡片
        if records:
            # 计算统计数据
            total_records = len(records)
            correct_records = sum(1 for r in records if r['result'] == '对')
            incorrect_records = sum(1 for r in records if r['result'] == '错')
            unknown_records = sum(1 for r in records if r['result'] == '未知')
            
            # 计算正确率
            accuracy_rate = 0
            if correct_records + incorrect_records > 0:
                accuracy_rate = (correct_records / (correct_records + incorrect_records)) * 100
            
            # 显示统计卡片
            with ui.card().classes('w-full stats-card'):
                ui.label('预测统计').classes('font-bold text-lg mb-2')
                
                with ui.row().classes('stats-container'):
                    with ui.element('div').classes('stats-item'):
                        ui.label('总记录数:').classes('stats-label')
                        ui.label(f"{total_records}").classes('stats-value stats-value-total')
                    with ui.element('div').classes('stats-item'):
                        ui.label('已验证:').classes('stats-label')
                        ui.label(f"{correct_records + incorrect_records}").classes('stats-value')
                    with ui.element('div').classes('stats-item'):
                        ui.label('正确:').classes('stats-label')
                        ui.label(f"{correct_records}").classes('stats-value stats-value-correct')
                    with ui.element('div').classes('stats-item'):
                        ui.label('错误:').classes('stats-label')
                        ui.label(f"{incorrect_records}").classes('stats-value stats-value-incorrect')
                    with ui.element('div').classes('stats-item'):
                        ui.label('未知:').classes('stats-label')
                        ui.label(f"{unknown_records}").classes('stats-value')
                    with ui.element('div').classes('stats-item'):
                        ui.label('正确率:').classes('stats-label')
                        ui.label(f"{accuracy_rate:.1f}%").classes('stats-value stats-value-correct font-bold')
                
                # 添加进度条
                with ui.element('div').classes('stats-progress'):
                    ui.element('div').classes('stats-progress-bar').style(f'width: {accuracy_rate}%')
        
        if not records:
            ui.label('暂无记录').classes('text-gray-500 text-center w-full my-8')
        else:
            # 显示记录列表
            for record in records:
                with ui.card().classes('w-full record-card'):
                    with ui.row().classes('w-full justify-between items-center'):
                        ui.label(f"日期: {record['date']}").classes('font-bold')
                        
                        # 结果标签
                        result_class = {
                            '对': 'result-correct',
                            '错': 'result-incorrect',
                            '未知': 'result-unknown'
                        }.get(record['result'], 'result-unknown')
                        
                        ui.label(record['result']).classes(f'result-badge {result_class}')
                    
                    if record['question']:
                        ui.label(f"所问事情: {record['question']}").classes('text-sm text-gray-700')
                    
                    if record['notes']:
                        ui.label(f"笔记: {record['notes']}").classes('text-sm text-gray-600')
                    
                    with ui.row().classes('w-full justify-end gap-2 mt-2'):
                        ui.button('查看', on_click=lambda r=record: view_record(r['id'])).classes('bg-blue-500 hover:bg-blue-600 text-white text-sm px-3 py-1')
                        
                        # 结果按钮
                        if record['result'] == '未知':
                            ui.button('标记为对', on_click=lambda r=record: update_result(r['id'], '对')).classes('bg-green-500 hover:bg-green-600 text-white text-sm px-3 py-1')
                            ui.button('标记为错', on_click=lambda r=record: update_result(r['id'], '错')).classes('bg-red-500 hover:bg-red-600 text-white text-sm px-3 py-1')
                        else:
                            ui.button('重置结果', on_click=lambda r=record: update_result(r['id'], '未知')).classes('bg-gray-500 hover:bg-gray-600 text-white text-sm px-3 py-1')
                        
                        ui.button('删除', on_click=lambda r=record: delete_record(r['id'])).classes('bg-red-500 hover:bg-red-600 text-white text-sm px-3 py-1')

def view_record(record_id):
    """查看排盘记录详情"""
    # 初始化数据库服务
    db_service = QimenDBService()
    
    # 获取记录详情
    record = db_service.get_record_by_id(record_id)
    
    if record:
        # 构建排盘参数
        params = {
            'datetime_str': record['paipan_params']['datetime_str'],
            'method': record['paipan_params']['method'],
            'question': record['question'] if record['question'] else '',
            'notes': record['notes'] if record['notes'] else '',
            'record_id': str(record_id)  # 添加记录ID
        }
        
        if record['paipan_params'].get('area'):
            params['area'] = record['paipan_params']['area']
        
        # 跳转到排盘页面
        query_string = urlencode(params)
        ui.navigate.to(f'/qimen_info?{query_string}')
    else:
        ui.notify('记录不存在或已被删除', type='negative')

def update_result(record_id, result):
    """更新排盘记录结果"""
    # 初始化数据库服务
    db_service = QimenDBService()
    
    # 更新结果
    success = db_service.update_record_result(record_id, result)
    
    if success:
        ui.notify('结果已更新', type='positive')
        # 刷新页面
        ui.navigate.to('/qimen_records')
    else:
        ui.notify('更新失败', type='negative')

def delete_record(record_id):
    """删除排盘记录"""
    # 初始化数据库服务
    db_service = QimenDBService()
    
    # 删除记录
    success = db_service.delete_record(record_id)
    
    if success:
        ui.notify('记录已删除', type='positive')
        # 刷新页面
        ui.navigate.to('/qimen_records')
    else:
        ui.notify('删除失败', type='negative') 