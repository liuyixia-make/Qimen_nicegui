# components/qimen_info.py
from nicegui import ui
from Services.paipan_servise import 奇门遁甲

qimenData ={}

# 添加CSS样式
ui.add_head_html('''
<style>
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
  overflow: visible;  /* 改为visible，允许内容溢出 */
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
  position: relative;  /* 添加相对定位 */
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
  overflow: visible;  /* 允许内容溢出 */
  z-index: 1;  /* 确保内容在上层 */
}
.cell-block:last-child {
  z-index: 2;  /* 最右边的内容优先级更高 */
}
.cell-flex-align {
  display: flex;
  align-items: center;
  height: 100%;
  justify-content: flex-start;  /* 改为左对齐 */
  padding-left: 2px;  /* 添加左边距 */
}
 /* 格局 */                
.pattern-corner-multiline {
    position: absolute;
    left: 0;
    top: 0;  /* 改为0 */
    right: 0;
    font-size: 7px;
    color: #283f59;
    background: transparent;  /* 改为透明背景 */
    max-width: 100%;
    line-height: 1.3;
    pointer-events: none;
    z-index: 10;
    word-break: break-word;
    padding: 2px;  /* 调整padding */
    border-radius: 0;  /* 移除圆角 */
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
  letter-spacing: 3px; /* 竖排字间微调 */             
  vertical-align: middle;
}
 
/* 单字模式 */
.vertical-mini-text.single  {
  justify-content: center;
  line-height: 1;
}
 
/* 多字模式 */
.vertical-mini-text.multi  {
  line-height: 1;
  transform: translateY(1px);  /* 调整为更小的偏移量 */
}
 
.vertical-mini-text.multi  span {
  display: block;
  margin-bottom: 1px;  /* 恢复字间距 */
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
/* 特殊处理第7列的内容，确保不被裁剪 */
.cell-block[style*="grid-column:7"] {
  overflow: visible !important;
  z-index: 3;
# }
# .cell-block[style*="grid-column:7"] .cell-flex-align {
#   position: relative;
#   padding-right: 15px;  /* 给右边留出空间 */
}

/* 第二行容器 */
.second-line-container {
        position: absolute;
        top: 28px;          /* 调整垂直位置 */
        left: 0;            /* 左对齐 */
        right: 0;           /* 右对齐，占据整个宽度 */
        z-index: 100;
        font-size: 10px;
        line-height: 1;
        display: flex;      /* 使用 Flex 布局 */
        justify-content: space-between; /* 左右元素顶置，中间居中 */
    }

    /* 空亡（左对齐）印章样式 */
.second-line-container .kw {
        text-align: left;
        color: white;       /* 白色文字 */
        background-color: red; /* 红色背景 */
        border-radius: 2px; /* 方形无圆角 */
    }

    /* 马星（居中）印章样式 */
.second-line-container .mx {
        margin: 0 auto;     /* 水平居中 */
        color: white;       /* 白色文字 */
        background-color: red; /* 红色背景 */
        border-radius: 2px; /* 方形无圆角 */
    }

    /* 四害（右对齐）印章样式 */
.second-line-container .sh {
        text-align: right;
        color: white;       /* 白色文字 */
        background-color: red; /* 红色背景 */
        border-radius: 2px; /* 方形无圆角 */
    }
.second-line-container .kw,
.second-line-container .mx,
.second-line-container .sh {
    padding: 2px 2px; /* 减少上下内边距，仅保留左右 */
    line-height: 1; /* 确保行高紧凑 */
}
/* 在原有的CSS基础上添加以下样式 */
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
/* 添加到原有CSS中 */
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

/* 各宫位的背景色 */
.bg-north {     /* 一宫坎 */
    background-color: rgba(30, 144, 255, 0.1); /* 淡蓝色 */
}
.bg-southwest { /* 二宫坤 */
    background-color: rgba(139, 69, 19, 0.1);  /* 淡褐色 */
}
.bg-east {      /* 三宫震 */
    background-color: rgba(0, 168, 107, 0.1);  /* 淡绿色 */
}
.bg-southeast { /* 四宫巽 */
    background-color: rgba(0, 168, 107, 0.1);  /* 淡绿色 */
}
.bg-center {    /* 五宫中 */
    background-color: rgba(139, 69, 19, 0.1);  /* 淡褐色 */
}
.bg-northwest { /* 六宫乾 */
    background-color: rgba(255, 184, 0, 0.1);  /* 淡金色 */
}
.bg-west {      /* 七宫兑 */
    background-color: rgba(255, 184, 0, 0.1);  /* 淡金色 */
}
.bg-northeast { /* 八宫艮 */
    background-color: rgba(139, 69, 19, 0.1);  /* 淡褐色 */
}
.bg-south {     /* 九宫离 */
    background-color: rgba(255, 69, 0, 0.1);   /* 淡红色 */
}
</style>
''')


def apply_color_to_text(text):
    """
    对特定文字应用颜色样式
    可以根据需要添加更多的对应关系
    """
    # 定义文字和颜色的对应关系
    color_mapping = {
        # 五行
        '金': 'jin',
        '木': 'mu',
        '水': 'shui',
        '火': 'huo',
        '土': 'tu',
        # 八卦
        '乾': 'jin',
        '兑': 'jin',
        '离': 'huo',
        '震': 'mu',
        '巽': 'mu',
        '坎': 'shui',
        '艮': 'tu',
        '坤': 'tu',
        # 天干
        '庚': 'jin',
        '辛': 'jin',
        '甲': 'mu',
        '乙': 'mu',
        '壬': 'shui',
        '癸': 'shui',
        '丙': 'huo',
        '丁': 'huo',
        '戊': 'tu',
        '己': 'tu',
        # 地支
        '申': 'jin',
        '酉': 'jin',
        '寅': 'mu',
        '卯': 'mu',
        '子': 'shui',
        '亥': 'shui',
        '巳': 'huo',
        '午': 'huo',
        '辰': 'tu',
        '戌': 'tu',
        '丑': 'tu',
        '未': 'tu',
    }
    
    # 检查文字是否在映射表中，如果在则添加对应的样式
    if text in color_mapping:
        return f'<span class="{color_mapping[text]}">{text}</span>'
    return text



def generate_vertical_text(items):
    if not items:
        return ""
    
    # 根据元素数量选择模式 
    mode = "single" if len(items) == 1 else "multi"
    spans = "".join([f'<span>{item}</span>' for item in items])
    return f'<span class="vertical-mini-text {mode}">{spans}</span>'



def apply_color_to_text(text):
    """对特定文字应用颜色样式"""
    color_mapping = {
        # 五行
        '金': 'jin', '木': 'mu', '水': 'shui', '火': 'huo', '土': 'tu','覆灯火': 'jin',
        # 八卦
        '乾': 'jin', '兑': 'jin', '离': 'huo', '震': 'mu', '巽': 'mu',
        '坎': 'shui', '艮': 'tu', '坤': 'tu',
        # 天干
        '庚': 'jin', '辛': 'jin', '甲': 'mu', '乙': 'mu', '壬': 'shui',
        '癸': 'shui', '丙': 'huo', '丁': 'huo', '戊': 'tu', '己': 'tu',
        # 地支
        '申': 'jin', '酉': 'jin', '寅': 'mu', '卯': 'mu', '子': 'shui',
        '亥': 'shui', '巳': 'huo', '午': 'huo', '辰': 'tu', '戌': 'tu',
        '丑': 'tu', '未': 'tu',
    }
    return f'<span class="{color_mapping[text]}">{text}</span>' if text in color_mapping else text

def generate_cell_content(palace_data, palace_num):
    """生成每个宫位的内容"""
    pattern_text = ""
    content_blocks = []

    # 生成格局文本（第一行）
    if "格局" in palace_data and palace_data["格局"]:
        pattern_text = f'<span class="pattern-corner-multiline">{" ".join(palace_data["格局"])}</span>'

    # 空亡、马星、四害（第二行）
    second_line_elements = []

    # 空亡（左对齐）
    if palace_data.get("空亡") and palace_data["空亡"]:
        kongwang_text = ", ".join(palace_data["空亡"])
        second_line_elements.append(f'<span class="kw">{kongwang_text}</span>')

    # 马星（居中）
    if palace_data.get("马星"):
        second_line_elements.append(f'<span class="mx">{palace_data["马星"]}</span>')

    # 四害（右对齐）
    if palace_data.get("四害") and palace_data["四害"]:
        sihai_text = ", ".join(palace_data["四害"])
        second_line_elements.append(f'<span class="sh">{sihai_text}</span>')

    # 合并为第二行文本
    second_line_text = "".join(second_line_elements)
    if second_line_text:
        content_blocks.append(f'<div class="second-line-container">{second_line_text}</div>')
        
    # 地八神
    if palace_data.get("地八神"):
        content_blocks.append(f'<div class="cell-block" style="grid-row:5;grid-column:1"><div class="cell-flex-align"><span class="main-content">{apply_color_to_text(palace_data["地八神"])}</span></div></div>')
    
    # 隐干
    if palace_data.get("隐干"):
        content_blocks.append(f'<div class="cell-block" style="grid-row:3;grid-column:1"><div class="cell-flex-align"><span class="main-content">{apply_color_to_text(palace_data["隐干"])}</span></div></div>')
    
    # 寄地盘干及其长生
    if palace_data.get("寄地盘干"):
        changsheng = ""
        if palace_data.get("寄地盘干长生"):
            changsheng = generate_vertical_text([apply_color_to_text(cs) for cs in palace_data["寄地盘干长生"]])
        content_blocks.append(f'<div class="cell-block" style="grid-row:5;grid-column:6"><div class="cell-flex-align"><span class="main-content">{apply_color_to_text(palace_data["寄地盘干"])}</span>{changsheng}</div></div>')
    
    # 地盘干及其长生
    if palace_data.get("地盘干"):
        changsheng = ""
        if palace_data.get("地盘干长生"):
            changsheng = generate_vertical_text([apply_color_to_text(cs) for cs in palace_data["地盘干长生"]])
        content_blocks.append(f'<div class="cell-block" style="grid-row:5;grid-column:7"><div class="cell-flex-align"><span class="main-content">{apply_color_to_text(palace_data["地盘干"])}</span>{changsheng}</div></div>')
    
    # 天盘干及其长生
    if palace_data.get("天盘干"):
        changsheng = ""
        if palace_data.get("天盘干长生"):
            changsheng = generate_vertical_text([apply_color_to_text(cs) for cs in palace_data["天盘干长生"]])
        content_blocks.append(f'<div class="cell-block" style="grid-row:4;grid-column:7"><div class="cell-flex-align"><span class="main-content">{apply_color_to_text(palace_data["天盘干"])}</span>{changsheng}</div></div>')
    
    # 寄天盘干及其长生
    if palace_data.get("寄天盘干"):
        changsheng = ""
        if palace_data.get("寄天盘干长生"):
            changsheng = generate_vertical_text([apply_color_to_text(cs) for cs in palace_data["寄天盘干长生"]])
        content_blocks.append(f'<div class="cell-block" style="grid-row:4;grid-column:6"><div class="cell-flex-align"><span class="main-content">{apply_color_to_text(palace_data["寄天盘干"])}</span>{changsheng}</div></div>')
    
    # 寄宫星及其旺衰
    if palace_data.get("寄宫星"):
        wangshuai = ""
        if palace_data.get("寄宫星旺衰"):
            wangshuai = generate_vertical_text([apply_color_to_text(ws) for ws in palace_data["寄宫星旺衰"]])
        content_blocks.append(f'<div class="cell-block" style="grid-row:3;grid-column:6"><div class="cell-flex-align"><span class="main-content">{apply_color_to_text(palace_data["寄宫星"])}</span>{wangshuai}</div></div>')
    
    # 天盘门及其旺衰
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
    
    # 天八神及其旺衰
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
    
    # 天盘星及其旺衰
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
    
    # 默认宫位名称
    if not content_blocks and not pattern_text:
        palace_name = f'{palace_data.get("宫数", palace_num)}宫'
        content_blocks.append(f'<div class="cell-block" style="grid-row:3;grid-column:4"><div class="cell-flex-align"><span class="main-content">{apply_color_to_text(palace_name)}</span></div></div>')
    
    return pattern_text + ''.join(content_blocks)
















# 生成动态HTML
info = qimenData["起局信息"]

# 构建HTML
html_content = f'''
<div class="qimen-info-box">
  <!-- 时间信息区 -->
  <div class="qimen-info-row">
    <span class="main-label">时间：</span>
    <span class="main-value">{info["起局时间"]}</span>
    <span class="main-label" style="margin-left:1em;">农历：</span>
    <span class="main-value">{info["农历"]}</span>
  </div>
  <!-- 主信息块 -->
  <div class="qimen-main-block">
    <div class="qimen-main-row">
      <div class="main-label">旬首：</div>
      <div class="main-value">{info["旬首"]}</div>
      <div class="main-cells">
        {"".join([f'<span class="ganzhi-cell">{apply_color_to_text(ny)}</span>' for ny in info["四柱纳音"]])}
      </div>
    </div>
    <div class="qimen-main-row">
      <div class="main-label">局数：</div>
      <div class="main-value">{info["局数"]}</div>
      <div class="main-cells">
        {"".join([f'<span class="ganzhi-cell">{apply_color_to_text(gz[0])}</span>' for gz in info["四柱干支"]])}
      </div>
    </div>
    <div class="qimen-main-row">
      <div class="main-label">值符：</div>
      <div class="main-value">{info["值符"]}</div>
      <div class="main-cells">
        {"".join([f'<span class="ganzhi-cell">{apply_color_to_text(gz[1])}</span>' for gz in info["四柱干支"]])}
      </div>
    </div>
    <div class="qimen-main-row">
      <div class="main-label">值使：</div>
      <div class="main-value">{info["值使"]}</div>
      <div class="main-cells">
        {"".join([f'<span class="ganzhi-cell xunkong-cell">{xk}</span>' for xk in info["全局旬空"]])}
      </div>
    </div>
  </div>
  <!-- 节气区 -->
  <div class="qimen-info-row">
    <span class="main-label">{info["节气"][0]["name"]}：</span>
    <span class="main-value">{info["节气"][0]["date"]}</span>
    <span class="main-label" style="margin-left:1.6em;">{info["节气"][1]["name"]}：</span>
    <span class="main-value">{info["节气"][1]["date"]}</span>
  </div>
  <!-- 九宫格 -->
  <div class="nine-grid">'''

# 生成九宫格内容 - 按正确的顺序排列
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

if __name__ in {"__main__", "__mp_main__"}:
    ui.run()