from nicegui import ui
from Services.paipan_servise import 奇门遁甲
from Services.db_service import QimenDBService
import datetime  # 修改这里
from urllib.parse import unquote
from components.navbar import create_navbar


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
        max-width: 800px;
        margin: 0 auto;
        display: flex;
        flex-direction: column;
        align-items: center;
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
        width: 330px;
        height: 330px;
        margin: 0 auto;
        border: 2px solid #3a5fae;
        background: #fff;
        box-sizing: border-box;
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        grid-template-rows: repeat(3, 1fr);
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
.qimen-info-row {
  display: grid;
  grid-template-columns: auto minmax(0.5em, 4.5em) auto minmax(0.5em, 4.5em);
  align-items: center;
  column-gap: 0em;
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
  font-size: 12px  !important;
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
.xunkong-cell {
  color: #848180;
  font-weight: bold;
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
  grid-template-columns: 0.65fr 0.65fr 0.65fr 2fr 0.2fr 1.35fr 0.85fr;
  grid-template-rows: repeat(5, 1fr);
  width: 100%;
  height: 100%;
  position: relative;
  box-sizing: border-box;
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
  justify-content: flex-start !important;
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
    border: none !important;
    outline: none !important;
    text-shadow: none !important;
    box-shadow: none !important;
    background-color: transparent !important;
    text-decoration: none !important;
}

/* 确保格局字符不显示为红色 */
.pattern-corner-multiline span {
    border: none !important;
    background: transparent !important; 
    box-shadow: none !important;
    outline: none !important;
    text-shadow: none !important;
    text-decoration: none !important;
}

/* 格局性质颜色 */
.pattern-ji {
    color: #8a2be2 !important; /* 吉格使用紫色 */
}
.pattern-xiong {
    color: #dc3545 !important; /* 凶格使用红色 */
}
.pattern-zhong {
    color: #007bff !important; /* 中格使用蓝色 */
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
    left: 0px;
    right: 0px;
    z-index: 100;
    font-size: 8px;
    line-height: 1;
    display: flex;
    justify-content: space-between;
    width: calc(100% - 2px);
    padding-left: 1px;
    padding-right: 1px;
    box-sizing: border-box;
}
.second-line-container .mx {
    text-align: left;
    color: white;
    background-color: red;
    border-radius: 2px;
    flex-grow: 0;
    margin-right: auto; /* 确保马星靠左 */
    margin-left: 2px; /* 添加这行，设置左边距等于四害的右边距 */
    padding: 1px;
    max-width: 45%;
    overflow: hidden;
    white-space: nowrap;
}
.second-line-container .sh-group {
    display: inline-block;
    text-align: right;
    margin-left: auto;
}
.second-line-container .sh {
    display: inline-block;
    margin-left: 2px;
    margin-right: 0;
    padding: 1px 1px;
    background: red;
    color: white;
    border-radius: 2px;
}
.second-line-container .sh:first-child {
    margin-left: 0;
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
    border-radius: 3px;
    padding: 0.5px 0.5px;
    font-size: 12px;
    font-weight: 700;
    display: inline-block;
    box-shadow: 0 1px 2px rgba(128, 0, 128, 0.3);
}

/* A列设置宽度并保持左对齐 */
.cell-block[style*="grid-column:4"] {
  justify-content: flex-start !important;
  padding-left: 2px !important;
  border: none !important;
  max-width: 100%;
  overflow: visible;
  display: flex !important;
  z-index: 5 !important;
}

/* 为A列的绝对定位准备一个容器 */
.cell-inner-grid-position-container {
  display: none;
}

/* 天盘星的固定位置 */
.a-column-tienpan {
  display: block;
}

/* 天八神的固定位置 */
.a-column-bashen {
  display: block;
}

/* 天盘门的固定位置 */
.a-column-door {
  display: block;
}

/* 寄宫元素所在列的样式 */
.cell-block[style*="grid-column:6"] {
  justify-content: flex-start !important; 
  padding-left: 2px !important;
  border: none !important;
  overflow: visible;
  margin-left: -2.5px !important;  /* 增加左移距离到8px */
}

/* 移除相邻列的边界线 */
.cell-inner-grid > .cell-block[style*="grid-column:4"], 
.cell-inner-grid > .cell-block[style*="grid-column:5"],
.cell-inner-grid > .cell-block[style*="grid-column:6"] {
  border-right: none !important;
  border-left: none !important;
}

/* 减小天盘星/天八神/天盘门的字号 */
.cell-block[style*="grid-column:4"] .main-content {
  font-size: 12px !important;
  display: inline-block !important;
  visibility: visible !important;
  white-space: nowrap !important;
  color: inherit !important;
}

/* 修改空隙填充 */
.cell-inner-grid > .cell-block[style*="grid-column:5"] {
  min-width: 0.3em;  /* 减小第5列宽度 */
  padding: 0;
  margin: 0;
}

/* 寄宫元素相对定位 */
.cell-block-guest {
  position: relative;
  text-align: left;
  padding: 0;
  white-space: nowrap;
}

/* 天盘星/天八神/天盘门的左移样式 */
.cell-left-shift {
  margin-left: 0 !important;
  width: 100% !important;
  z-index: 5 !important;
  visibility: visible !important;
  display: flex !important;
}

/* 寄宫列的左移样式 */
.guest-left-shift {
  margin-left: 0 !important; /* 移除左移 */
  margin-right: 5px !important; /* 添加右移 */
  z-index: 3;
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

def apply_geju_style(geju_name):
    """根据格局名称应用格局样式，需要查询格局数据获取性质"""
    try:
        # 尝试导入格局数据模块
        try:
            from Services.qimen_gejudata import GEJU_DATA
        except ImportError:
            # 尝试相对路径导入
            import sys
            import os
            sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            from Services.qimen_gejudata import GEJU_DATA
        
        # 遍历格局数据查找对应格局
        for (天盘干, 地盘干), 格局数据 in GEJU_DATA.items():
            if 格局数据["名称"] == geju_name:
                nature = 格局数据["性质"]
                if nature == "吉":
                    return f'<span class="pattern-ji">{geju_name}</span>'
                elif nature == "凶":
                    return f'<span class="pattern-xiong">{geju_name}</span>'
                elif nature == "中":
                    return f'<span class="pattern-zhong">{geju_name}</span>'
                return geju_name
    except Exception as e:
        print(f"应用格局样式时发生错误: {e}")
    
    # 如果找不到或出错，返回原样
    return geju_name

def generate_vertical_text(items):
    if not items:
        return ""
    mode = "single" if len(items) == 1 else "multi"
    spans = "".join([f'<span>{apply_vertical_color(item)}</span>' for item in items if item])  # 只处理非空项
    return f'<span class="vertical-mini-text {mode}">{spans}</span>' if spans else ""

def generate_cell_content(palace_data, palace_num):
    # 添加调试输出
    print(f"[DEBUG] 宫位 {palace_num}宫 数据: 天盘星={palace_data.get('天盘星')}, 天八神={palace_data.get('天八神')}, 天盘门={palace_data.get('天盘门')}")
    
    pattern_text = ""
    content_blocks = []
    
    # 修改格局文本的处理方式，根据格局性质显示不同颜色
    if "格局" in palace_data and palace_data["格局"]:
        # 对每个格局应用颜色样式
        styled_patterns = []
        for geju in palace_data["格局"]:
            styled_patterns.append(apply_geju_style(geju))
        pattern_text = f'<span class="pattern-corner-multiline">{" ".join(styled_patterns)}</span>'

    # 生成第二行元素（马星、四害）
    second_line_elements = []
    
    # 始终添加马星元素的容器，即使为空
    mx_element = ""
    if palace_data.get("马星"):
        # 判断马星是列表还是字符串，修改为正确处理列表格式
        if isinstance(palace_data["马星"], list):
            maxing_text = ", ".join(palace_data["马星"])
            mx_element = f'<span class="mx">{maxing_text}</span>'
        elif palace_data["马星"]:  # 如果是非空字符串
            mx_element = f'<span class="mx">{palace_data["马星"]}</span>'
    
    # 四害每个元素单独渲染，并用sh-group包裹
    sh_element = ""
    if palace_data.get("四害") and palace_data["四害"]:
        sh_element = '<span class="sh-group">' + "".join([f'<span class="sh">{item}</span>' for item in palace_data["四害"]]) + '</span>'
    
    # 按固定顺序添加元素：马星在左，四害在右
    second_line_elements.append(mx_element)  # 马星始终在第一位
    second_line_elements.append(sh_element)  # 四害始终在最后一位
    
    second_line_text = "".join(second_line_elements)
    if second_line_text:  # 如果有任何内容才添加容器
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
            changsheng = generate_vertical_text(palace_data["寄地盘干长生"])
        content_blocks.append(f'<div class="cell-block" style="grid-row:5;grid-column:6"><div class="cell-flex-align"><span class="main-content">{apply_color_to_text(palace_data["寄地盘干"])}</span>{changsheng}</div></div>')
    else:
        # 添加空占位符
        content_blocks.append(f'<div class="cell-block" style="grid-row:5;grid-column:6"><div class="cell-flex-align"><span class="main-content">&nbsp;&nbsp;</span></div></div>')
    
    # 寄天盘干及其长生
    if palace_data.get("寄天盘干"):
        changsheng = ""
        if palace_data.get("寄天盘干长生"):
            changsheng = generate_vertical_text(palace_data["寄天盘干长生"])
        content_blocks.append(f'<div class="cell-block" style="grid-row:4;grid-column:6"><div class="cell-flex-align"><span class="main-content">{apply_color_to_text(palace_data["寄天盘干"])}</span>{changsheng}</div></div>')
    else:
        # 添加空占位符
        content_blocks.append(f'<div class="cell-block" style="grid-row:4;grid-column:6"><div class="cell-flex-align"><span class="main-content">&nbsp;&nbsp;</span></div></div>')

    # 寄宫星及其旺衰
    if palace_data.get("寄宫星"):
        wangshuai = ""
        if palace_data.get("寄宫星旺衰"):
            wangshuai = generate_vertical_text(palace_data["寄宫星旺衰"])
        content_blocks.append(f'<div class="cell-block" style="grid-row:3;grid-column:6"><div class="cell-flex-align"><span class="main-content">{apply_color_to_text(palace_data["寄宫星"])}</span>{wangshuai}</div></div>')
    else:
        # 添加空占位符
        content_blocks.append(f'<div class="cell-block" style="grid-row:3;grid-column:6"><div class="cell-flex-align"><span class="main-content">&nbsp;&nbsp;</span></div></div>')

    # 地盘干及其长生
    if palace_data.get("地盘干"):
        changsheng = ""
        if palace_data.get("地盘干长生"):
            changsheng = generate_vertical_text(palace_data["地盘干长生"])
        content_blocks.append(f'<div class="cell-block" style="grid-row:5;grid-column:7"><div class="cell-flex-align"><span class="main-content">{apply_color_to_text(palace_data["地盘干"])}</span>{changsheng}</div></div>')
    else:
        # 添加空占位符
        content_blocks.append(f'<div class="cell-block" style="grid-row:5;grid-column:7"><div class="cell-flex-align"><span class="main-content">&nbsp;</span></div></div>')

    # 天盘干及其长生
    if palace_data.get("天盘干"):
        changsheng = ""
        if palace_data.get("天盘干长生"):
            changsheng = generate_vertical_text(palace_data["天盘干长生"])
        content_blocks.append(f'<div class="cell-block" style="grid-row:4;grid-column:7"><div class="cell-flex-align"><span class="main-content">{apply_color_to_text(palace_data["天盘干"])}</span>{changsheng}</div></div>')
    else:
        # 添加空占位符
        content_blocks.append(f'<div class="cell-block" style="grid-row:4;grid-column:7"><div class="cell-flex-align"><span class="main-content">&nbsp;</span></div></div>')

    # 天盘星及其旺衰，确保对齐
    if palace_data.get("天盘星"):
        wangshuai = ""
        if palace_data.get("天盘星旺衰") and any(palace_data["天盘星旺衰"]):  # 检查是否有任何非空旺衰状态
            wangshuai = generate_vertical_text(palace_data["天盘星旺衰"])
        content_blocks.append(f'<div class="cell-block cell-left-shift" style="grid-row:3;grid-column:4;border:none !important;"><div class="cell-flex-align" style="justify-content:flex-start !important;padding-left:5px;"><span class="main-content" style="text-align:left;">{apply_color_to_text(palace_data["天盘星"])}</span>{wangshuai}</div></div>')
    else:
        # 添加空占位符
        content_blocks.append(f'<div class="cell-block cell-left-shift" style="grid-row:3;grid-column:4;border:none !important;"><div class="cell-flex-align" style="justify-content:flex-start !important;padding-left:5px;"><span class="main-content" style="text-align:left;">&nbsp;&nbsp;</span></div></div>')

    # 天八神及其旺衰，确保对齐
    if palace_data.get("天八神"):
        wangshuai = ""
        if palace_data.get("天八神旺衰") and any(palace_data["天八神旺衰"]):  # 检查是否有任何非空旺衰状态
            wangshuai = generate_vertical_text(palace_data["天八神旺衰"])
        content_blocks.append(f'<div class="cell-block cell-left-shift" style="grid-row:4;grid-column:4;border:none !important;"><div class="cell-flex-align" style="justify-content:flex-start !important;padding-left:5px;"><span class="main-content" style="text-align:left;">{apply_bashen_style(palace_data["天八神"])}</span>{wangshuai}</div></div>')
    else:
        # 添加空占位符
        content_blocks.append(f'<div class="cell-block cell-left-shift" style="grid-row:4;grid-column:4;border:none !important;"><div class="cell-flex-align" style="justify-content:flex-start !important;padding-left:5px;"><span class="main-content" style="text-align:left;">&nbsp;&nbsp;</span></div></div>')

    # 天盘门及其旺衰，确保对齐
    if palace_data.get("天盘门"):
        wangshuai = ""
        if palace_data.get("天盘门旺衰") and any(palace_data["天盘门旺衰"]):  # 检查是否有任何非空旺衰状态
            wangshuai = generate_vertical_text(palace_data["天盘门旺衰"])
        content_blocks.append(f'<div class="cell-block cell-left-shift" style="grid-row:5;grid-column:4;border:none !important;"><div class="cell-flex-align" style="justify-content:flex-start !important;padding-left:5px;"><span class="main-content" style="text-align:left;">{apply_color_to_text(palace_data["天盘门"])}</span>{wangshuai}</div></div>')
    else:
        # 添加空占位符
        content_blocks.append(f'<div class="cell-block cell-left-shift" style="grid-row:5;grid-column:4;border:none !important;"><div class="cell-flex-align" style="justify-content:flex-start !important;padding-left:5px;"><span class="main-content" style="text-align:left;">&nbsp;&nbsp;</span></div></div>')
    
    return pattern_text + ''.join(content_blocks)

def generate_nine_palaces(qimen_data):
    """
    生成九宫格内容
    """
    palace_order = ["四宫", "九宫", "二宫", "三宫", "五宫", "七宫", "八宫", "一宫", "六宫"]
    palace_nums = ["四", "九", "二", "三", "五", "七", "八", "一", "六"]
    bg_classes = ["bg-southeast", "bg-south", "bg-southwest",
                  "bg-east", "bg-center", "bg-west",
                  "bg-northeast", "bg-north", "bg-northwest"]

    html_content = ""
    for i, (palace_key, palace_num, bg_class) in enumerate(zip(palace_order, palace_nums, bg_classes)):
        palace_data = qimen_data.get(palace_key, {})
        if palace_data:
            cell_content = generate_cell_content(palace_data, palace_num)
            html_content += f'''
            <div class="grid-cell {bg_class}">
                <div class="cell-inner-grid">
                    {cell_content}
                </div>
            </div>'''
        else:
            # 如果宫位数据为空，显示简单的宫位数字
            html_content += f'''
            <div class="grid-cell {bg_class}">
                <div class="cell-inner-grid">
                    <div class="cell-block" style="grid-row:3;grid-column:4">
                        <div class="cell-flex-align">
                            <span class="main-content">{palace_num}宫</span>
                        </div>
                    </div>
                </div>
            </div>'''
    
    return html_content

@ui.page('/qimen_info')
def qimen_info_page(datetime_str: str = None, method: str = None, area: str = None, question: str = None, notes: str = None, record_id: str = None):
    print(f"[DEBUG] 接收到的参数: datetime_str={datetime_str}, method={method}, area={area}, question={question}, notes={notes}, record_id={record_id}")
    
    try:
        # 添加样式
        ui.add_head_html(QIMEN_STYLES)
        ui.add_head_html('''
        <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
        ''')
        
        # 添加导航栏
        create_navbar()
        
        # 检查参数是否完整
        if not datetime_str:
            ui.label("未提供日期时间参数，无法排盘").classes('text-red')
            return
        if not method:
            ui.label("未提供起局法参数，无法排盘").classes('text-red')
            return
        
        # 解码URL参数
        if datetime_str:
            datetime_str = unquote(datetime_str)
        if method:
            method = unquote(method)
        if area:
            area = unquote(area)
        if question:
            question = unquote(question)
        if notes:
            notes = unquote(notes)
        if record_id:
            try:
                record_id = int(record_id)
            except ValueError:
                record_id = None
            
        # 实例化奇门遁甲类
        qimen = 奇门遁甲(起局时间=datetime_str, 起局法=method, 地区=area)
        qimen_data = qimen.奇门遁甲数据
        
        # 调试节气数据
        print(f"[DEBUG] 节气数据类型: {type(qimen_data['起局信息'].get('节气'))}")
        print(f"[DEBUG] 节气数据内容: {qimen_data['起局信息'].get('节气')}")
        if qimen_data['起局信息'].get('节气'):
            for i, item in enumerate(qimen_data['起局信息'].get('节气')):
                print(f"[DEBUG] 节气[{i}] 类型: {type(item)}, 值: {item}")
        
        # 仅增加外部容器宽度，不变更九宫格
        with ui.card().tight().classes('w-full max-w-6xl mx-auto shadow-lg rounded-xl overflow-hidden p-5'):
            # 将基础信息放在顶部的卡片内
            with ui.card().tight().classes('w-full mx-auto my-2 rounded-lg shadow-sm text-center'):
                ui.html(f'''
                <div class="qimen-info-box">
                    <div class="qimen-main-block">
                      <div class="qimen-main-row">
                          <div class="main-label">时间：</div>
                          <div class="main-value">{"<span style='color:red;'>●</span>" if qimen_data["起局信息"].get("是否真太阳时", False) else ""} {qimen_data["起局信息"].get("起局时间", "")}</div>
                          <div class="main-cells" style="margin-left:5em;">
                              <span class="main-label">农历：</span>
                              <span class="main-value">&nbsp;&nbsp;{qimen_data["起局信息"].get("农历", "")}</span>
                          </div>
                      </div>
                      <div class="qimen-main-row">
                          <div class="main-label">旬首：</div>
                          <div class="main-value">{qimen_data["起局信息"].get("旬首", "")}</div>
                          <div class="main-cells">
                              {"".join([f'<span class="nayin-cell">{apply_color_to_text(ny)}</span>' for ny in qimen_data["起局信息"].get("四柱纳音", [])])}
                          </div>
                      </div>
                      <div class="qimen-main-row">
                          <div class="main-label">局数：</div>
                          <div class="main-value">{qimen_data["起局信息"].get("局数", "")}</div>
                          <div class="main-cells">
                              {generate_ganzhi_cells(qimen_data["起局信息"].get("四柱干支", []), 0)}
                          </div>
                      </div>
                      <div class="qimen-main-row">
                          <div class="main-label">值符：</div>
                          <div class="main-value">{qimen_data["起局信息"].get("值符", "")}</div>
                          <div class="main-cells">
                              {generate_ganzhi_cells(qimen_data["起局信息"].get("四柱干支", []), 1)}
                          </div>
                      </div>
                      <div class="qimen-main-row">
                          <div class="main-label">值使：</div>
                          <div class="main-value">{qimen_data["起局信息"].get("值使", "")}</div>
                          <div class="main-cells">
                              {"".join([f'<span class="xunkong-cell">{xk}</span>' for xk in qimen_data["起局信息"].get("四柱旬空", [])])}
                          </div>
                         </div>
                     </div>
                     <div class="qimen-info-row">
                         <span class="main-label">{获取当前节气名称(qimen_data["起局信息"].get("节气", []))}：</span>
                         <span class="main-value">{获取当前节气日期(qimen_data["起局信息"].get("节气", []))}</span>
                         {节气显示(qimen_data["起局信息"].get("节气", []))}
                      </div>
                </div>
                ''')
            
            # 九宫格显示
            with ui.card().tight().classes('w-full mx-auto my-2 rounded-lg shadow-sm text-center'):
                ui.html(f'''
                <div class="nine-grid" style="margin: 0 auto;">
                    {generate_nine_palaces(qimen_data)}
                </div>
                ''')
            
            # 添加笔记和保存功能
            with ui.card().tight().classes('w-full mx-auto my-2 rounded-lg shadow-sm'):
                # 直接使用容器而不是表单
                with ui.column().classes('w-full px-6 py-3 gap-3'):
                    # 添加自动调整大小的文本域样式
                    ui.add_head_html('''
                    <style>
                    .auto-height-textarea textarea {
                        overflow-y: hidden;
                        resize: none;
                        min-height: 24px;
                        height: auto;
                    }
                    </style>
                    <script>
                    document.addEventListener('DOMContentLoaded', function() {
                        setTimeout(function() {
                            const textareas = document.querySelectorAll('.auto-height-textarea textarea');
                            
                            textareas.forEach(function(textarea) {
                                function adjustHeight() {
                                    textarea.style.height = 'auto';
                                    textarea.style.height = textarea.scrollHeight + 'px';
                                }
                                
                                // 初始调整高度
                                adjustHeight();
                                
                                // 监听输入事件
                                textarea.addEventListener('input', adjustHeight);
                            });
                        }, 300);
                    });
                    </script>
                    ''')
                    
                    # 第一排：所问事情（占满整行，使用单行输入框）
                    question_input = ui.input(label='所问事情', placeholder='请输入所问事情...', value=question or '').classes('w-full')
                    # 第二排：笔记（占满整行，使用自动调整高度的文本域）
                    notes_input = ui.textarea(label='笔记', placeholder='请输入笔记...', value=notes or '').classes('w-full auto-height-textarea')
                    
                    # 如果是从历史记录打开的，显示记录ID
                    if record_id:
                        ui.label(f"正在编辑记录 #{record_id}").classes('text-xs text-gray-500 mt-1')
            
            # 返回按钮
            with ui.card().tight().classes('w-full mx-auto my-2 rounded-lg shadow-sm text-center'):
                with ui.row().classes('justify-center items-center gap-2 py-2'):
                    ui.button('首页', on_click=lambda: ui.navigate.to('/')).classes('bg-gray-500 hover:bg-gray-600 text-white text-sm py-1 px-3')
                    ui.button('重新排盘', on_click=lambda: ui.navigate.to('/paipan')).classes('bg-blue-500 hover:bg-blue-600 text-white text-sm py-1 px-3')
                    ui.button('历史记录', on_click=lambda: ui.navigate.to('/qimen_records')).classes('bg-purple-500 hover:bg-purple-600 text-white text-sm py-1 px-3')
                    save_btn_text = '更新' if record_id else '保存'
                    ui.button(save_btn_text, on_click=lambda: save_record(qimen_data, datetime_str, method, area, question_input.value, notes_input.value, record_id)).classes('bg-green-500 hover:bg-green-600 text-white text-sm py-1 px-3')

    except Exception as e:
        ui.label(f"排盘发生错误: {str(e)}").classes('text-red')
        print(f"排盘错误: {str(e)}")
        import traceback
        traceback.print_exc()
        ui.button('返回重新排盘', on_click=lambda: ui.navigate.to('/paipan')).classes('bg-blue-500 hover:bg-blue-600 text-white')

def save_record(qimen_data, datetime_str, method, area, question, notes, record_id=None):
    """保存或更新排盘记录到数据库"""
    try:
        # 初始化数据库服务
        db_service = QimenDBService()
        
        if record_id:
            # 更新已有记录
            success = db_service.update_record(
                record_id=record_id,
                question=question,
                notes=notes
            )
            
            if success:
                ui.notify(f'记录已更新 (ID: {record_id})', type='positive')
            else:
                ui.notify('记录更新失败，可能该记录已不存在', type='negative')
        else:
            # 创建新记录
            # 准备排盘参数
            paipan_params = {
                'datetime_str': datetime_str,
                'method': method,
                'area': area
            }
            
            # 保存记录
            new_record_id = db_service.save_record(
                date=datetime_str,
                question=question,
                notes=notes,
                paipan_params=paipan_params,
                paipan_data=qimen_data
            )
            
            # 显示成功消息
            ui.notify(f'记录已保存 (ID: {new_record_id})', type='positive')
        
    except Exception as e:
        ui.notify(f'保存失败: {str(e)}', type='negative')
        print(f"保存记录错误: {str(e)}")
        import traceback
        traceback.print_exc()

def 格式化节气列表(节气列表):
    """
    格式化节气列表为显示文本
    """
    if not 节气列表:
        return "无节气数据"
    
    # 检查节气列表的格式
    if isinstance(节气列表[0], dict):
        # 旧格式：[{"name": "节气名", "date": "日期"}, {"name": "节气名", "date": "日期"}]
        if len(节气列表) >= 2:
            当前节气 = 节气列表[0].get("name", "")
            当前节气时间 = 节气列表[0].get("date", "")
            下一节气 = 节气列表[1].get("name", "")
            下一节气时间 = 节气列表[1].get("date", "")
        elif len(节气列表) == 1:
            当前节气 = 节气列表[0].get("name", "")
            当前节气时间 = 节气列表[0].get("date", "")
            下一节气 = ""
            下一节气时间 = ""
        else:
            return "无节气数据"
    else:
        # 新格式：["节气名", "日期", "节气名", "日期"]
        if len(节气列表) >= 4:
            当前节气, 当前节气时间, 下一节气, 下一节气时间 = 节气列表[:4]
        elif len(节气列表) == 3:
            当前节气, 当前节气时间, 下一节气 = 节气列表
            下一节气时间 = ""
        elif len(节气列表) == 2:
            当前节气, 当前节气时间 = 节气列表
            下一节气 = ""
            下一节气时间 = ""
        elif len(节气列表) == 1:
            当前节气 = 节气列表[0]
            当前节气时间 = ""
            下一节气 = ""
            下一节气时间 = ""
        else:
            return "无节气数据"
    
    formatted_当前节气时间 = 格式化节气日期(当前节气时间) if 当前节气时间 else ""
    formatted_下一节气时间 = 格式化节气日期(下一节气时间) if 下一节气时间 else ""
    
    if 下一节气:
        return f"{当前节气}{formatted_当前节气时间} {下一节气}{formatted_下一节气时间}"
    else:
        return f"{当前节气}{formatted_当前节气时间}"

def 格式化节气日期(date_str):
    """
    将完整的日期时间字符串格式化为简短格式
    例如: "2025-06-05 17:56:16" -> "06-05 17:56"
    """
    if not date_str:
        return ""
    
    try:
        dt = datetime.datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
        return f"{dt.strftime('%m-%d %H:%M')}"
    except:
        return f"{date_str}"

def 获取当前节气名称(节气列表):
    """
    从节气列表中获取当前节气名称，支持不同的数据格式
    """
    if not 节气列表:
        return "无节气"
    
    # 字典格式: [{"name": "节气名", "date": "日期"}, ...]
    if isinstance(节气列表[0], dict):
        return 节气列表[0].get("name", "无节气")
    
    # 列表格式: ["节气名", "日期", "节气名", "日期"]
    if isinstance(节气列表[0], str):
        return 节气列表[0]
    
    return "无节气"

def 获取当前节气日期(节气列表):
    """
    从节气列表中获取当前节气日期，支持不同的数据格式
    """
    if not 节气列表:
        return ""
    
    # 字典格式: [{"name": "节气名", "date": "日期"}, ...]
    if isinstance(节气列表[0], dict):
        return 格式化节气日期(节气列表[0].get("date", ""))
    
    # 列表格式: ["节气名", "日期", "节气名", "日期"]
    if len(节气列表) >= 2 and isinstance(节气列表[0], str) and isinstance(节气列表[1], str):
        return 格式化节气日期(节气列表[1])
    
    return ""

def 节气显示(节气列表):
    """
    安全处理节气数据，确保即使节气列表只有一个元素也不会报错
    可以处理不同格式的节气数据
    """
    if not 节气列表 or len(节气列表) <= 1:
        return ""
    
    # 第二个节气的信息
    if isinstance(节气列表[1], dict):
        节气名称 = 节气列表[1].get("name", "")
        节气日期 = 节气列表[1].get("date", "")
    else:
        # 处理可能的其他格式
        try:
            if len(节气列表) >= 4 and isinstance(节气列表[2], str) and isinstance(节气列表[3], str):
                节气名称 = 节气列表[2]
                节气日期 = 节气列表[3]
            else:
                return ""
        except:
            return ""
    
    return f'''
    <span class="main-label" style="margin-left:1.6em;">{节气名称}：</span>
    <span class="main-value">{格式化节气日期(节气日期)}</span>
    '''

def generate_four_pillars_display(info_data):
    """
    生成四柱显示的HTML代码
    """
    html = ""
    if "四柱干支" not in info_data or not info_data["四柱干支"]:
        return '<div class="ganzhi-cell">未知</div>' * 4
    
    for pillar in info_data["四柱干支"]:
        if len(pillar) == 2:
            html += f'<div class="ganzhi-cell">{pillar[0]}{pillar[1]}</div>'
        else:
            html += '<div class="ganzhi-cell">未知</div>'
    
    return html

def generate_ganzhi_cells(干支列表, index):
    """
    生成干支单元格的HTML代码
    """
    cells = []
    for 干支 in 干支列表:
        if isinstance(干支, (list, tuple)) and len(干支) > index:
            cells.append(f'<span class="ganzhi-cell">{apply_color_to_text(干支[index])}</span>')
        elif isinstance(干支, str) and " " in 干支:
            # 处理字符串格式的四柱干支，例如: "甲子 乙丑 丙寅 丁卯"
            干支数组 = 干支.split()
            if 0 <= index < len(干支数组[0]):
                cells.append(f'<span class="ganzhi-cell">{apply_color_to_text(干支数组[index])}</span>')
            else:
                cells.append('<span class="ganzhi-cell">未知</span>')
        else:
            cells.append('<span class="ganzhi-cell">未知</span>')
    return "".join(cells)