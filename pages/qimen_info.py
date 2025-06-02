from nicegui import ui
from Services.paipan_servise import 奇门遁甲
import datetime  # 修改这里
from urllib.parse import unquote


QIMEN_STYLES = '''

<style>
/* ...你的所有CSS原样保留... */
 /* 整体容器居中 */
    body {
        display: flex;
        justify-content: center;
        margin: 0;
        padding: 20px;
    }

    /* 内容容器 */
    .qimen-info-box {
        width: 100%;
        max-width: 1200px;
        margin: 0 auto;
    }

    /* 原有的其他样式 */
    .qimen-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 10px;
        margin: 20px;
    }
    .qimen-cell {
        border: 1px solid #ccc;
        padding: 10px;
        text-align: center;
    }
    /* 确保九宫格居中 */
    .nine-grid {
        width: 100%;
        max-width: 900px;
        margin: 0 auto;
    }
.qimen-info-box {
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 100%;
}
.qimen-main-block {
  font-size: 16px;
}
.qimen-main-row {
  display: grid;
  grid-template-columns: auto minmax(0.5em, 4.5em) 1fr;
  align-items: center;
  column-gap: 0em;
  font-size: 16px;
}
.main-label {
  font-weight: bold;
  color: #222;
  text-align: right;
  white-space: nowrap;
  font-size: 13px  !important;
}
.main-value {
  font-weight: normal;
  color: #333;
  text-align: center;
  min-width: 3.5em;
  white-space: nowrap;
  display: inline-block;
  font-size: 13px  !important;
}
.main-cells {
  display: flex;
}
.nayin-cell {
  font-weight: bold;
  color: #3e8ed0;
  min-width: 3.5em;
  text-align: center;
  margin-right: 0.7em;
  white-space: nowrap;
  font-size: 13px  !important;
}
.ganzhi-cell {
  font-weight: bold;
  color: #fa7d00;
  min-width: 3.5em;
  text-align: center;
  margin-right: 0.7em;
  white-space: nowrap;
  font-size: 12px  !important;
}
.nayin-cell:last-child, .ganzhi-cell:last-child {
  margin-right: 0;
}
.nine-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  grid-template-rows: repeat(3, 1fr);
  width: 330px;
  height: 330px;
  margin: 3px auto;
  border: 2px solid #3a5fae;
  background: #fff;
  box-sizing: border-box;
}
.grid-cell {
  border: 1px solid #3a5fae;
  box-sizing: border-box;
  height: 100%;
  overflow: visible;
  position: relative;
  min-width: 0; min-height: 0;
  background: #fff;
  padding: 0;
  cursor: pointer;
}
.cell-inner-grid {
  line-height: 0.8;
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  grid-template-rows: repeat(5, 1fr);
  width: 100%;
  height: 100%;
  position: relative;
}
.cell-block {
  white-space: nowrap;
  letter-spacing: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 100%;
  height: 100%;
  padding: 0;
  box-sizing: border-box;
  font-size: 12px;
  overflow: visible;
  z-index: 1;
}
.cell-block:last-child {
  z-index: 2;
}
.cell-flex-align {
  display: flex;
  align-items: center;
  height: 100%;
  justify-content: flex-start;
  padding-left: 2px;
}
.pattern-corner-multiline {
    position: absolute;
    left: 0;
    top: 0;
    right: 0;
    font-size: 8px;
    color: #283f59;
    background: transparent;
    max-width: 100%;
    line-height: 1.3;
    pointer-events: none;
    z-index: 10;
    word-break: break-word;
    padding: 2px;
    border-radius: 0;
    box-sizing: border-box;
    white-space: normal;
    width: 100%;
    word-break: break-all;
}
.vertical-mini-text {
  display: inline-flex;
  flex-direction: column;
  font-size: 7px;
  margin-left: 0.5px;
  letter-spacing: 3px;
  vertical-align: middle;
}
.vertical-mini-text.single  {
  justify-content: center;
  line-height: 1;
}
.vertical-mini-text.multi  {
  line-height: 1;
  transform: translateY(1px);
}
.vertical-mini-text.multi  span {
  display: block;
  margin-bottom: 1px;
}
.vertical-mini-text.size-1 {
  font-size: 7px;
  line-height: 0.5;
}
.vertical-mini-text.size-2 {
  font-size: 7px;
  line-height: 1;
}
.vertical-mini-text span {
  display: block;
}
.cell-block[style*="grid-column:7"] {
  overflow: visible !important;
  z-index: 3;
}
.second-line-container {
        position: absolute;
        top: 28px;
        left: 1.5px;
        right: 1.5px;
        z-index: 100;
        font-size: 10px;
        line-height: 1;
        display: flex;
        justify-content: space-between;
        
    }
.second-line-container .kw {
        text-align: left;
        color: white;
        background-color: red;
        border-radius: 2px;
    }
.second-line-container .mx {
        margin: 0 auto;
        color: white;
        background-color: red;
        border-radius: 2px;
    }
.second-line-container .sh {
        text-align: right;
        color: white;
        background-color: red;
        border-radius: 2px;
    }
.second-line-container .kw,
.second-line-container .mx,
.second-line-container .sh {
    padding: 2px 2px;
    line-height: 1;
}
.jin {
    color: #FFB800;
    font-weight: bold;
}
.mu {
    color: #00A86B;
    font-weight: bold;
}
.shui {
    color: #1E90FF;
    font-weight: bold;
}
.huo {
    color: #FF4500;
    font-weight: bold;
}
.tu {
    color: #8B4513;
    font-weight: bold;
}
.xunkong-cell {
    color: #848180;
    font-weight: bold;
}
.grid-cell {
    border: 1px solid #3a5fae;
    box-sizing: border-box;
    height: 100%;
    overflow: visible;
    position: relative;
    min-width: 0;
    min-height: 0;
    padding: 0;
    cursor: pointer;
}

/* 在 旺相休囚死 中添加以下样式 */
.wang-status { color: #FF0000; } /* 旺 - 红色 */
.xiang-status { color: #FFA500; } /* 相 - 橙色 */
.xiu-status { color: #008000; } /* 休 - 绿色 */
.qiu-status { color: #4169E1; } /* 囚 - 蓝色 */
.si-status { color: #808080; } /* 死 - 灰色 */


/* 新的半透明样式 */
.bg-north { background-color: rgba(30, 144, 255, 0.1);} /* 一宫 */
.bg-south { background-color: rgba(255, 69, 0, 0.1);} /* 九宫 */
.bg-east { background-color: rgba(0, 168, 107, 0.1);} /* 三宫 */
.bg-west { background-color: rgba(255, 184, 0, 0.1);} /* 七宫 */
.bg-center { background-color: rgba(139, 69, 19, 0.1);} /* 五宫 */
.bg-southeast { background-color: rgba(0, 168, 107, 0.1);} /* 四宫 */
.bg-northwest { background-color: rgba(255, 184, 0, 0.1);} /* 六宫 */
.bg-northeast { background-color: rgba(139, 69, 19, 0.1);} /* 八宫 */
.bg-southwest { background-color: rgba(139, 69, 19, 0.1);} /* 二宫 */


/* 八神通用样式 - 加粗 */
.bashen {
    font-weight: 700;
    font-size: 12px;
}

/* 合并后的印章效果样式 */
.seal {
    color: white;
    background-color: purple;
    border: 1px solid purple;
    border-radius: 4px;
    padding: 1.5px 1px;
    font-size: 10px;
    font-weight: 700;
    display: inline-block;
    box-shadow: 0 1px 2px rgba(128, 0, 128, 0.3);
}
</style>
'''


def apply_color_to_text(text): 
    # 原始字典生成逻辑（无需手动维护）
    
    color_groups = { 
        
        'jin': ['金', '乾', '兑', '覆灯火', '庚', '辛', '申', '酉', '开门', '开', '天心', '心', '惊门', '惊', '天柱', '柱'], 
        'mu': ['木', '震', '巽', '甲', '乙', '寅', '卯', '伤门', '伤', '天冲', '冲', '杜门', '杜', '天辅', '辅'],
        'shui': ['水', '坎', '壬', '癸', '子', '亥', '休门', '休', '天蓬', '蓬'], 
        'huo': ['火', '离', '丙', '丁', '巳', '午', '天英', '英', '景门', '景'], 
        'tu': ['土', '艮', '坤', '戊', '己', '辰', '戌', '丑', '未', '天芮', '芮', '死门', '死', '天任', '任', '生门', '生','天禽', '禽', ],
    } 
    
    # 自动合并为原始字典格式 
    color_mapping = {}
    for color, group in color_groups.items():  
        for char in group:
            color_mapping[char] = color 
    
    # 原函数逻辑完全保留 
    return f'<span class="{color_mapping[text]}">{text}</span>' if text in color_mapping else text

def apply_vertical_color(text):
    """对竖排文字应用颜色"""
    # 状态映射
    status_mapping = {
        "wang": ["生", "帝", "临", "旺"],
        "xiang": ["沐", "冠", "相", "养"],
        "xiu": ["墓", "绝", "休"],
        "qiu": ["衰", "病", "囚"],
        "si": ["死"]
    }
    
    # 生成反向映射
    text_to_status = {}
    for status, items in status_mapping.items():
        for item in items:
            text_to_status[item] = status
    
    # 应用颜色类
    if text in text_to_status:
        status = text_to_status[text]
        return f'<span class="{status}-status">{text}</span>'
    return text

def apply_bashen_style(text):
    """应用八神样式"""
    if text in ["值符", "符"]:
        return f'<span class="seal">{text}</span>'
    return f'<span class="bashen">{text}</span>'

def generate_vertical_text(items):
    if not items:
        return ""
    mode = "single" if len(items) == 1 else "multi"
    spans = "".join([f'<span>{apply_vertical_color(item)}</span>' for item in items])
    return f'<span class="vertical-mini-text {mode}">{spans}</span>'

def generate_cell_content(palace_data, palace_num):
    pattern_text = ""
    content_blocks = []
    if "格局" in palace_data and palace_data["格局"]:
        pattern_text = f'<span class="pattern-corner-multiline">{" ".join(palace_data["格局"])}</span>'
    second_line_elements = []
    if palace_data.get("空亡") and palace_data["空亡"]:
        kongwang_text = ", ".join(palace_data["空亡"])
        second_line_elements.append(f'<span class="kw">{kongwang_text}</span>')
    if palace_data.get("马星"):
        second_line_elements.append(f'<span class="mx">{palace_data["马星"]}</span>')
    if palace_data.get("四害") and palace_data["四害"]:
        sihai_text = ", ".join(palace_data["四害"])
        second_line_elements.append(f'<span class="sh">{sihai_text}</span>')
    second_line_text = "".join(second_line_elements)
    if second_line_text:
        content_blocks.append(f'<div class="second-line-container">{second_line_text}</div>')
    # if palace_data.get("地八神"):
    #     content_blocks.append(f'<div class="cell-block" style="grid-row:5;grid-column:1"><div class="cell-flex-align"><span class="main-content">{apply_color_to_text(palace_data["地八神"])}</span></div></div>')
    if palace_data.get("隐干"):
        content_blocks.append(f'<div class="cell-block" style="grid-row:3;grid-column:1"><div class="cell-flex-align"><span class="main-content">{apply_color_to_text(palace_data["隐干"])}</span></div></div>')
    
    
    
    if palace_data.get("地盘干"):
        changsheng = ""
        if palace_data.get("地盘干长生"):
            changsheng = generate_vertical_text(palace_data["地盘干长生"])  # 使用原始文本，让 generate_vertical_text 内部处理颜色
        content_blocks.append(f'<div class="cell-block" style="grid-row:5;grid-column:7"><div class="cell-flex-align"><span class="main-content">{apply_color_to_text(palace_data["地盘干"])}</span>{changsheng}</div></div>')

    if palace_data.get("天盘干"):
        changsheng = ""
        if palace_data.get("天盘干长生"):
            changsheng = generate_vertical_text(palace_data["天盘干长生"])  # 使用原始文本，让 generate_vertical_text 内部处理颜色
        content_blocks.append(f'<div class="cell-block" style="grid-row:4;grid-column:7"><div class="cell-flex-align"><span class="main-content">{apply_color_to_text(palace_data["天盘干"])}</span>{changsheng}</div></div>')

    if palace_data.get("寄宫干"):
        changsheng = ""
        if palace_data.get("寄宫干长生"):
            changsheng = generate_vertical_text(palace_data["寄宫干长生"])  # 使用原始文本
        content_blocks.append(f'<div class="cell-block" style="grid-row:4;grid-column:6"><div class="cell-flex-align"><span class="main-content">{apply_color_to_text(palace_data["寄宫干"])}</span>{changsheng}</div></div>')

    if palace_data.get("寄宫星"):
        wangshuai = ""
        if palace_data.get("寄宫星旺衰"):
            wangshuai = generate_vertical_text(palace_data["寄宫星旺衰"])  # 使用原始文本
        content_blocks.append(f'<div class="cell-block" style="grid-row:3;grid-column:6"><div class="cell-flex-align"><span class="main-content">{apply_color_to_text(palace_data["寄宫星"])}</span>{wangshuai}</div></div>')

    if palace_data.get("天盘门"):
        wangshuai = ""
        if palace_data.get("天盘门旺衰"):
            wangshuai = generate_vertical_text(palace_data["天盘门旺衰"])  # 使用原始文本
        content_blocks.append(f'''
            <div class="cell-block" style="grid-row:5;grid-column:4">
                <div class="cell-flex-align">
                    <span class="main-content">{apply_color_to_text(palace_data["天盘门"])}</span>
                    {wangshuai}
                </div>
            </div>
        ''')

    if palace_data.get("天八神"):
        wangshuai = ""
        if palace_data.get("天八神旺衰"):
            wangshuai = generate_vertical_text(palace_data["天八神旺衰"])  # 使用原始文本
        content_blocks.append(f'''
            <div class="cell-block" style="grid-row:4;grid-column:4">
                <div class="cell-flex-align">
                    <span class="main-content">{apply_bashen_style(palace_data["天八神"])}</span>
                    {wangshuai}
                </div>
            </div>
        ''')

    if palace_data.get("天盘星"):
        wangshuai = ""
        if palace_data.get("天盘星旺衰"):
            wangshuai = generate_vertical_text(palace_data["天盘星旺衰"])  # 使用原始文本
        content_blocks.append(f'''
            <div class="cell-block" style="grid-row:3;grid-column:4">
                <div class="cell-flex-align">
                    <span class="main-content">{apply_color_to_text(palace_data["天盘星"])}</span>
                    {wangshuai}
                </div>
            </div>
        ''')
    if not content_blocks and not pattern_text:
        palace_name = f'{palace_data.get("宫数", palace_num)}宫'
        content_blocks.append(f'<div class="cell-block" style="grid-row:3;grid-column:4"><div class="cell-flex-align"><span class="main-content">{apply_color_to_text(palace_name)}</span></div></div>')
    return pattern_text + ''.join(content_blocks)




@ui.page('/qimen_info')
def qimen_info_page(datetime_str: str = None, method: str = None, area: str = None):
    print(f"[DEBUG] 接收到的参数: datetime_str={datetime_str}, method={method}, area={area}")
    
    try:
        # 添加样式
        ui.html(QIMEN_STYLES)
        
        # 创建居中容器
        with ui.column().classes('w-full max-w-md mx-auto p-4 mobile-container'):
            with ui.card().classes('w-full p-4 shadow mobile-card'):
                # 检查参数是否完整
                if not all([datetime_str, method, area]):
                    ui.label("没有排盘数据，请先生成排盘。")
                    ui.button('返回', on_click=lambda: ui.navigate.to('/paipan'))
                    return
                
                # 实例化奇门遁甲类
                qimen = 奇门遁甲(
                    container=ui.element('div'),
                    起卦时间=datetime_str,
                    起局法=method,
                    地区=area
                )
                
                qimenData = qimen.奇门遁甲数据

                if "起局信息" not in qimenData:
                    ui.label("没有排盘数据，请先生成排盘。")
                    ui.button('返回', on_click=lambda: ui.navigate.to('/paipan'))
                    return

                info = qimenData["起局信息"]

                html_content = f'''
                <div class="qimen-info-box">
                    <div class="qimen-info-row">
                        <span class="main-label">时间：</span>
                        <span class="main-value">{info.get("起局时间", "")}</span>
                        <span class="main-label" style="margin-left:1em;">农历：</span>
                        <span class="main-value">{info.get("农历", "")}</span>
                    </div>
                    <div class="qimen-main-block">
                        <div class="qimen-main-row">
                            <div class="main-label">旬首：</div>
                            <div class="main-value">{info.get("旬首", "")}</div>
                            <div class="main-cells">
                                {"".join([f'<span class="ganzhi-cell">{apply_color_to_text(ny)}</span>' for ny in info.get("四柱纳音", [])])}
                            </div>
                        </div>
                        <div class="qimen-main-row">
                            <div class="main-label">局数：</div>
                            <div class="main-value">{info.get("局数", "")}</div>
                            <div class="main-cells">
                                {"".join([f'<span class="ganzhi-cell">{apply_color_to_text(gz[0])}</span>' for gz in info.get("四柱干支", [])])}
                            </div>
                        </div>
                        <div class="qimen-main-row">
                            <div class="main-label">值符：</div>
                            <div class="main-value">{info.get("值符", "")}</div>
                            <div class="main-cells">
                                {"".join([f'<span class="ganzhi-cell">{apply_color_to_text(gz[1])}</span>' for gz in info.get("四柱干支", [])])}
                            </div>
                        </div>
                        <div class="qimen-main-row">
                            <div class="main-label">值使：</div>
                            <div class="main-value">{info.get("值使", "")}</div>
                            <div class="main-cells">
                                {"".join([f'<span class="ganzhi-cell xunkong-cell">{xk}</span>' for xk in info.get("全局旬空", [])])}
                            </div>
                        </div>
                    </div>
                    <div class="qimen-info-row">
                        <span class="main-label">{info.get("节气", [{}])[0].get("name", "")}：</span>
                        <span class="main-value">{info.get("节气", [{}])[0].get("date", "")}</span>
                        <span class="main-label" style="margin-left:1.6em;">{info.get("节气", [{}, {}])[1].get("name", "")}：</span>
                        <span class="main-value">{info.get("节气", [{}, {}])[1].get("date", "")}</span>
                    </div>
                    <div class="nine-grid">
                '''

                palace_order = ["四宫", "九宫", "二宫", "三宫", "五宫", "七宫", "八宫", "一宫", "六宫"]
                palace_nums = ["四", "九", "二", "三", "五", "七", "八", "一", "六"]
                bg_classes = ["bg-southeast", "bg-south", "bg-southwest",
                            "bg-east", "bg-center", "bg-west",
                            "bg-northeast", "bg-north", "bg-northwest"]

                for i, (palace_key, palace_num, bg_class) in enumerate(zip(palace_order, palace_nums, bg_classes)):
                    palace_data = qimenData.get(palace_key, {})
                    cell_content = generate_cell_content(palace_data, palace_num)
                    html_content += f'''
                    <div class="grid-cell {bg_class}">
                        <div class="cell-inner-grid">
                            {cell_content}
                        </div>
                    </div>'''

                html_content += '''
                    </div>
                </div>
                '''

                ui.html(html_content)
                ui.button('返回', on_click=lambda: ui.navigate.to('/paipan')).classes('w-full bg-blue-500 hover:bg-blue-600 text-white py-3 rounded-lg text-lg font-medium mt-2')

    except Exception as e:
        print(f"Error: {str(e)}")
        ui.notify(f"发生错误: {str(e)}", color='negative')
        ui.button('返回', on_click=lambda: ui.navigate.to('/paipan'))