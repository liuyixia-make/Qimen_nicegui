from datetime import datetime, timedelta
from skyfield.api import load, Topos
from geopy.geocoders import Nominatim
from datetime import datetime
from nicegui import ui

class 奇门遁甲:
    # 类属性：初始化奇门遁甲数据结构
    奇门遁甲数据 = {
        "起局信息": {
            "起局时间": None,
            "农历": None,
            "局数": None,
            "四柱干支": [],
            "四柱纳音": [],
            "节气": [
                {"name": None, "date": None},
                {"name": None, "date": None}
            ],
            "全局旬空": [],
            "值符": None,
            "值使": None,
            "旬首": None
        },
        "一宫": {},  # 具体数据将在计算时填充
        "二宫": {},
        "三宫": {},
        "四宫": {   "四害": "巽",        "宫名": "巽", "方位": "东南", "宫数": "四", "宫支": ["辰", "巳"], "宫属性": "木", "宫符号": "☴", "本位星": "天辅星", "本位门": "杜", "隐干": "壬", "地八神": "禽", "地盘干": "戊", "地盘干长生": [ "养"], "天盘干": "甲", "天盘干长生": ["生", "养"], "天盘星": "天冲", "天盘星旺衰": ["相", "旺"], "天八神": "值符", "天八神旺衰": ["相", "旺"],"天盘门": "开门","天盘门旺衰": ["相", "旺"], "马星": "马", "空亡": [ "辰","巳"], "建除": "建", "寄宫干": "乙","寄宫干长生": ["生", "养"],"寄宫星": "心","寄宫星旺衰": ["相", "旺"],"格局": ["飞鸟跌穴", "三奇受制","太白入荧"]
},
        "五宫": {},
        "六宫": {},
        "七宫": {},
        "八宫": {},
        "九宫": {}
    }

    def __init__(self, container: ui.element, 起卦时间=None, 起局法='拆补法', 地区=None):
        """
        初始化奇门遁甲排盘类。

        :param container: NiceGUI容器元素
        :param 起卦时间: 起卦时间，默认为None，表示当前时间。
        :param 起局法: 起局方法，支持 '拆补法' 或 '置润法'，默认为 '拆补法'。
        :param 地区: 地区名称（如城市名称），如果提供则自动启用真太阳时。
        """
        self.container = container
        
        # 初始化数据结构（创建实例自己的副本）
        self.数据 = self.奇门遁甲数据.copy()
        
        # 初始化基本属性
        self.地区 = 地区
        self.标准时间 = 起卦时间 if 起卦时间 else datetime.now()
        self.真太阳时 = None

        # 根据地区设置起局时
        self.起局时 = self.标准时间 if self.地区 is None else self.真太阳时

        # 起局干支
        self.起局干支 = None

        # 校验起局法是否合法
        if 起局法 not in {"拆补法", "置润法"}:
            raise ValueError("起局法只能是 '拆补法' 或 '置润法'")
        self.起局法 = 起局法

        # 节气
        self.节气 = None

        # 起局数
        self.局数 = None

        # 符头
        self.符头 = None
        
        # 旬首
        self.旬首 = None

        # 值符
        self.值符 = None

        # 值使
        self.值使 = None
        

