# 初始化奇门遁甲数据
        self.奇门遁甲数据 = {
            "起局信息": {
                "起局时间": None,
                "是否真太阳时": False,
                "农历": "",
                "节气": [],  # 初始化为空列表，避免后续引用错误
                "局数": "",
                "四柱干支": [["甲", "子"], ["乙", "丑"], ["丙", "寅"], ["丁", "卯"]],  # 设置默认的四柱干支数据
                "四柱纳音": ["海中金", "海中金", "炉中火", "炉中火"],
                "四柱旬空": ["戌亥空", "戌亥空", "戌亥空", "戌亥空"],
                "符头": "",
                "值符": "天辅",
                "值使": "休门",
                "旬首": "甲寅癸"
            },
            "一宫": {
                "宫名": "坎", "方位": "正北", "宫数": "一", "宫支": ["子"],
                "宫属性": "水", "本位星": "天蓬星", "本位门": "休", "隐干": "",
                "地八神": "", "地盘干": "", "地盘干长生": [""], "天盘干": "",
                "天盘干长生": [""], "天盘星": "", "天盘星旺衰": ["", ""],
                "天八神": "", "天八神旺衰": ["", ""], "天盘门": "", "天盘门旺衰": ["", ""],
                "马星": "", "空亡": [], "建除": "", "寄宫干": "",
                "寄宫干长生": [""], "寄宫星": "", "寄宫星旺衰": ["", ""],
                "格局": [],"四害": ""
            },
            "二宫": {
                "宫名": "坤", "方位": "西南", "宫数": "二", "宫支": ["未","申"],
                "宫属性": "土", "本位星": "天芮星", "本位门": "死", "隐干": "",
                "地八神": "", "地盘干": "", "地盘干长生": [""], "天盘干": "",
                "天盘干长生": [""], "天盘星": "", "天盘星旺衰": ["", ""],
                "天八神": "", "天八神旺衰": ["", ""], "天盘门": "", "天盘门旺衰": ["", ""],
                "马星": "", "空亡": [], "建除": "", "寄宫干": "",
                "寄宫干长生": [""], "寄宫星": "", "寄宫星旺衰": ["", ""],
                "格局": [],"四害": ""
            },
            "三宫": {
                "宫名": "震", "方位": "正东", "宫数": "三", "宫支": ["卯"],
                "宫属性": "木", "本位星": "天冲星", "本位门": "伤", "隐干": "",
                "地八神": "", "地盘干": "", "地盘干长生": [""], "天盘干": "",
                "天盘干长生": [""], "天盘星": "", "天盘星旺衰": ["", ""],
                "天八神": "", "天八神旺衰": ["", ""], "天盘门": "", "天盘门旺衰": ["", ""],
                "马星": "", "空亡": [], "建除": "", "寄宫干": "",
                "寄宫干长生": [""], "寄宫星": "", "寄宫星旺衰": ["", ""],
                "格局": [],"四害": ""
            },
            "四宫": {
               "宫名": "巽", "方位": "东南", "宫数": "四", "宫支": ["巳","辰"],
                "宫属性": "木", "本位星": "天辅星", "本位门": "杜", "隐干": "",
                "地八神": "", "地盘干": "", "地盘干长生": [""], "天盘干": "",
                "天盘干长生": [""], "天盘星": "", "天盘星旺衰": ["", ""],
                "天八神": "", "天八神旺衰": ["", ""], "天盘门": "", "天盘门旺衰": ["", ""],
                "马星": "", "空亡": [], "建除": "", "寄宫干": "",
                "寄宫干长生": [""], "寄宫星": "", "寄宫星旺衰": ["", ""],
                "格局": [],"四害": ""
            },
            "五宫": {
                "宫名": "", "方位": "中", "宫数": "五", "宫支": [""],
                "宫属性": "土", "本位星": "天禽星", "隐干": "",
                "地八神": "", "地盘干": "", "地盘干长生": ["中"], "天盘干": ""
            },
            "六宫": {
                "宫名": "乾", "方位": "西北", "宫数": "六", "宫支": ["戌","亥"],
                "宫属性": "金", "本位星": "天心星", "本位门": "开", "隐干": "",
                "地八神": "", "地盘干": "", "地盘干长生": [""], "天盘干": "",
                "天盘干长生": [""], "天盘星": "", "天盘星旺衰": ["", ""],
                "天八神": "", "天八神旺衰": ["", ""], "天盘门": "", "天盘门旺衰": ["", ""],
                "马星": "", "空亡": [], "建除": "", "寄宫干": "",
                "寄宫干长生": [""], "寄宫星": "", "寄宫星旺衰": ["", ""],
                "格局": [],"四害": ""
            },
            "七宫": {
                "宫名": "兑", "方位": "正西", "宫数": "七", "宫支": ["酉"],
                "宫属性": "金", "本位星": "天柱星", "本位门": "惊", "隐干": "",
                "地八神": "", "地盘干": "", "地盘干长生": [""], "天盘干": "",
                "天盘干长生": [""], "天盘星": "", "天盘星旺衰": ["", ""],
                "天八神": "", "天八神旺衰": ["", ""], "天盘门": "", "天盘门旺衰": ["", ""],
                "马星": "", "空亡": [], "建除": "", "寄宫干": "",
                "寄宫干长生": [""], "寄宫星": "", "寄宫星旺衰": ["", ""],
                "格局": [],"四害": ""
            },
            "八宫": {
                "宫名": "艮", "方位": "东北", "宫数": "八", "宫支": ["丑","寅"],
                "宫属性": "土", "本位星": "天任星", "本位门": "生", "隐干": "",
                "地八神": "", "地盘干": "", "地盘干长生": [""], "天盘干": "",
                "天盘干长生": [""], "天盘星": "", "天盘星旺衰": ["", ""],
                "天八神": "", "天八神旺衰": ["", ""], "天盘门": "", "天盘门旺衰": ["", ""],
                "马星": "", "空亡": [], "建除": "", "寄宫干": "",
                "寄宫干长生": [""], "寄宫星": "", "寄宫星旺衰": ["", ""],
                "格局": [],"四害": ""
            },
            "九宫": {
                "宫名": "离", "方位": "正南", "宫数": "九", "宫支": ["午"],
                "宫属性": "火", "本位星": "天英星", "本位门": "景", "隐干": "",
                "地八神": "", "地盘干": "", "地盘干长生": [""], "天盘干": "",
                "天盘干长生": [""], "天盘星": "", "天盘星旺衰": ["", ""],
                "天八神": "", "天八神旺衰": ["", ""], "天盘门": "", "天盘门旺衰": ["", ""],
                "马星": "", "空亡": [], "建除": "", "寄宫干": "",
                "寄宫干长生": [""], "寄宫星": "", "寄宫星旺衰": ["", ""],
                "格局": [],"四害": ""
            }
        }


