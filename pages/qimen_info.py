from nicegui import ui
from Services.paipan_servise import 奇门遁甲
import datetime  # 修改这里
from urllib.parse import unquote


QIMEN_STYLES = '''

<style>
/* ...你的所有CSS原样保留... */
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
  font-size: 11px  !important;
}
.main-value {
  font-weight: normal;
  color: #333;
  text-align: center;
  min-width: 3.5em;
  white-space: nowrap;
  display: inline-block;
  font-size: 11px  !important;
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
  font-size: 11px  !important;
}
.ganzhi-cell {
  font-weight: bold;
  color: #fa7d00;
  min-width: 3.5em;
  text-align: center;
  margin-right: 0.7em;
  white-space: nowrap;
  font-size: 11px  !important;
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
    font-size: 7px;
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
        left: 0;
        right: 0;
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
.bg-north { background-color: rgba(30, 144, 255, 0.1);}
.bg-southwest { background-color: rgba(139, 69, 19, 0.1);}
.bg-east { background-color: rgba(0, 168, 107, 0.1);}
.bg-southeast { background-color: rgba(0, 168, 107, 0.1);}
.bg-center { background-color: rgba(139, 69, 19, 0.1);}
.bg-northwest { background-color: rgba(255, 184, 0, 0.1);}
.bg-west { background-color: rgba(255, 184, 0, 0.1);}
.bg-northeast { background-color: rgba(139, 69, 19, 0.1);}
.bg-south { background-color: rgba(255, 69, 0, 0.1);}
</style>
'''

def apply_color_to_text(text):
    color_mapping = {
        '金': 'jin', '木': 'mu', '水': 'shui', '火': 'huo', '土': 'tu', '覆灯火': 'jin',
        '乾': 'jin', '兑': 'jin', '离': 'huo', '震': 'mu', '巽': 'mu',
        '坎': 'shui', '艮': 'tu', '坤': 'tu',
        '庚': 'jin', '辛': 'jin', '甲': 'mu', '乙': 'mu', '壬': 'shui',
        '癸': 'shui', '丙': 'huo', '丁': 'huo', '戊': 'tu', '己': 'tu',
        '申': 'jin', '酉': 'jin', '寅': 'mu', '卯': 'mu', '子': 'shui',
        '亥': 'shui', '巳': 'huo', '午': 'huo', '辰': 'tu', '戌': 'tu',
        '丑': 'tu', '未': 'tu',
    }
    return f'<span class="{color_mapping[text]}">{text}</span>' if text in color_mapping else text

def generate_vertical_text(items):
    if not items:
        return ""
    mode = "single" if len(items) == 1 else "multi"
    spans = "".join([f'<span>{item}</span>' for item in items])
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
    if palace_data.get("地八神"):
        content_blocks.append(f'<div class="cell-block" style="grid-row:5;grid-column:1"><div class="cell-flex-align"><span class="main-content">{apply_color_to_text(palace_data["地八神"])}</span></div></div>')
    if palace_data.get("隐干"):
        content_blocks.append(f'<div class="cell-block" style="grid-row:3;grid-column:1"><div class="cell-flex-align"><span class="main-content">{apply_color_to_text(palace_data["隐干"])}</span></div></div>')
    if palace_data.get("地盘干"):
        changsheng = ""
        if palace_data.get("地盘干长生"):
            changsheng = generate_vertical_text([apply_color_to_text(cs) for cs in palace_data["地盘干长生"]])
        content_blocks.append(f'<div class="cell-block" style="grid-row:5;grid-column:7"><div class="cell-flex-align"><span class="main-content">{apply_color_to_text(palace_data["地盘干"])}</span>{changsheng}</div></div>')
    if palace_data.get("天盘干"):
        changsheng = ""
        if palace_data.get("天盘干长生"):
            changsheng = generate_vertical_text([apply_color_to_text(cs) for cs in palace_data["天盘干长生"]])
        content_blocks.append(f'<div class="cell-block" style="grid-row:4;grid-column:7"><div class="cell-flex-align"><span class="main-content">{apply_color_to_text(palace_data["天盘干"])}</span>{changsheng}</div></div>')
    if palace_data.get("寄宫干"):
        changsheng = ""
        if palace_data.get("寄宫干长生"):
            changsheng = generate_vertical_text([apply_color_to_text(cs) for cs in palace_data["寄宫干长生"]])
        content_blocks.append(f'<div class="cell-block" style="grid-row:4;grid-column:6"><div class="cell-flex-align"><span class="main-content">{apply_color_to_text(palace_data["寄宫干"])}</span>{changsheng}</div></div>')
    if palace_data.get("寄宫星"):
        wangshuai = ""
        if palace_data.get("寄宫星旺衰"):
            wangshuai = generate_vertical_text([apply_color_to_text(ws) for ws in palace_data["寄宫星旺衰"]])
        content_blocks.append(f'<div class="cell-block" style="grid-row:3;grid-column:6"><div class="cell-flex-align"><span class="main-content">{apply_color_to_text(palace_data["寄宫星"])}</span>{wangshuai}</div></div>')
    if palace_data.get("天盘门"):
        wangshuai = ""
        if palace_data.get("天盘门旺衰"):
            wangshuai = generate_vertical_text([apply_color_to_text(ws) for ws in palace_data["天盘门旺衰"]])
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
            wangshuai = generate_vertical_text([apply_color_to_text(ws) for ws in palace_data["天八神旺衰"]])
        content_blocks.append(f'''
            <div class="cell-block" style="grid-row:4;grid-column:4">
                <div class="cell-flex-align">
                    <span class="main-content">{apply_color_to_text(palace_data["天八神"])}</span>
                    {wangshuai}
                </div>
            </div>
        ''')
    if palace_data.get("天盘星"):
        wangshuai = ""
        if palace_data.get("天盘星旺衰"):
            wangshuai = generate_vertical_text([apply_color_to_text(ws) for ws in palace_data["天盘星旺衰"]])
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
        # 创建container元素
        container = ui.element('div')
        
        # 检查参数是否完整
        if not all([datetime_str, method, area]):
            ui.label("没有排盘数据，请先生成排盘。")
            ui.button('返回', on_click=lambda: ui.navigate.to('/paipan'))
            return
        
        # 实例化奇门遁甲类
        qimen = 奇门遁甲(
            container=container,
            起卦时间=datetime_str,
            起局法=method,
            地区=area
        )
        
        qimenData = qimen.奇门遁甲数据  # 直接使用实例的奇门遁甲数据属性

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
        ui.button('返回', on_click=lambda: ui.navigate.to('/paipan'))

    except Exception as e:
        print(f"Error: {str(e)}")
        ui.notify(f"发生错误: {str(e)}", color='negative')
        ui.button('返回', on_click=lambda: ui.navigate.to('/paipan'))