from datetime import datetime, timedelta, timezone
# from skyfield.api import load, wgs84
from geopy.geocoders import Nominatim
from lunar_python import Lunar  # 用于农历和节气计算
from nicegui import ui
import ephem

class 奇门遁甲:
    def __init__(self, container=None, 起局时间=None, 起局法='拆补法', 地区=None):
        """
        初始化奇门遁甲排盘类。

        :param container: NiceGUI容器元素（可选，默认为 None），用于 UI 渲染
        :param 起局时间: 起局时间，必须为字符串格式 'YYYY-MM-DD HH:MM'，不能为空
        :param 起局法: 起局方法，支持 '拆补法' 或 '置润法'，默认为 '拆补法'
        :param 地区: 地区名称（如城市名称），用于真太阳时计算，若为 None 则直接使用起局时间
        """
        # 处理起局时间：必须为字符串格式，解析为 datetime 对象
        if not isinstance(起局时间, str):
            raise TypeError("起局时间必须为字符串格式，例如 '2025-06-02 14:00'")
        try:
            self.起局时 = datetime.strptime(起局时间, '%Y-%m-%d %H:%M')
        except ValueError as e:
            raise ValueError(f"起局时间格式错误，应为 'YYYY-MM-DD HH:MM'，例如 '2025-06-02 14:00'，错误：{e}")

        # 确保起局时不带时区信息，以避免与不支持时区的库冲突
        if self.起局时.tzinfo is not None:
            self.起局时 = self.起局时.replace(tzinfo=None)

        self.container = container  # 存储 container，供 NiceGUI 使用，测试时可为 None
        self.地区 = 地区
        self.起局法 = 起局法
        self.经纬度 = None

        # 初始化奇门遁甲数据
        self.奇门遁甲数据 = {
            "起局信息": {
                "起局时间": None,
                "是否真太阳时": False,
                "农历": None,
                "节气": [],  # 初始化为空列表，避免后续引用错误
                "局数": "阳九局",
                "四柱干支": [["甲", "子"], ["乙", "丑"], ["丙", "寅"], ["丁", "卯"]],  # 设置默认的四柱干支数据
                "四柱纳音": ["覆灯火", "覆灯火", "覆灯火", "覆灯火"],
                "四柱旬空": ["戊子空", "丁巳空", "戊子空", "丁巳空"],
                "符头": None,
                "值符": "天辅",
                "值使": "休门",
                "旬首": "甲寅癸"
            },
            "一宫": {
                "宫名": "坎", "方位": "正北", "宫数": "一", "宫支": ["子"],
                "宫属性": "水",  "本位星": "天蓬星", "本位门": "休", "隐干": "None",
                "地八神": "None", "地盘干": "None", "地盘干长生": ["None"], "天盘干": "None",
                "天盘干长生": ["None"], "天盘星": "None", "天盘星旺衰": ["None", "None"],
                "天八神": "None", "天八神旺衰": ["None", "None"], "天盘门": "None", "天盘门旺衰": ["None", "None"],
                "马星": "None", "空亡": [], "建除": "None", "寄宫干": "None",
                "寄宫干长生": ["None"], "寄宫星": "None", "寄宫星旺衰": ["None", "None"],
                "格局": ["None"],"四害": ""
            },
            "二宫": {
                "宫名": "坤", "方位": "西南", "宫数": "二", "宫支": ["未","申"],
                "宫属性": "土",  "本位星": "天芮星", "本位门": "死", "隐干": "None",
                "地八神": "None", "地盘干": "None", "地盘干长生": ["None"], "天盘干": "None",
                "天盘干长生": ["None"], "天盘星": "None", "天盘星旺衰": ["None", "None"],
                "天八神": "None", "天八神旺衰": ["None", "None"], "天盘门": "None", "天盘门旺衰": ["None", "None"],
                "马星": "None", "空亡": [], "建除": "None", "寄宫干": "None",
                "寄宫干长生": ["None"], "寄宫星": "None", "寄宫星旺衰": ["None", "None"],
                "格局": ["None"],"四害": ""
            },
            "三宫": {
                "宫名": "震", "方位": "正东", "宫数": "三", "宫支": ["卯"],
                "宫属性": "木",  "本位星": "天冲星", "本位门": "伤", "隐干": "None",
                "地八神": "None", "地盘干": "None", "地盘干长生": ["None"], "天盘干": "None",
                "天盘干长生": ["None"], "天盘星": "None", "天盘星旺衰": ["None", "None"],
                "天八神": "None", "天八神旺衰": ["None", "None"], "天盘门": "None", "天盘门旺衰": ["None", "None"],
                "马星": "None", "空亡": [], "建除": "None", "寄宫干": "None",
                "寄宫干长生": ["None"], "寄宫星": "None", "寄宫星旺衰": ["None", "None"],
                "格局": ["None"],"四害": ""
            },
            "四宫": {
               "宫名": "巽", "方位": "东南", "宫数": "四", "宫支": ["巳","辰"],
                "宫属性": "木",  "本位星": "天辅星", "本位门": "杜", "隐干": "None",
                "地八神": "None", "地盘干": "None", "地盘干长生": ["None"], "天盘干": "None",
                "天盘干长生": ["None"], "天盘星": "None", "天盘星旺衰": ["None", "None"],
                "天八神": "None", "天八神旺衰": ["None", "None"], "天盘门": "None", "天盘门旺衰": ["None", "None"],
                "马星": "None", "空亡": [], "建除": "None", "寄宫干": "None",
                "寄宫干长生": ["None"], "寄宫星": "None", "寄宫星旺衰": ["None", "None"],
                "格局": ["None"],"四害": ""
            },
            "五宫": {
                "宫名": "", "方位": "中", "宫数": "五", "宫支": [""],
                "宫属性": "土",  "本位星": "天禽星",  "隐干": "None",
                "地八神": "None", "地盘干": "None", "地盘干长生": ["None"], "天盘干": "None"
            },
            "六宫": {
                "宫名": "乾", "方位": "西北", "宫数": "六", "宫支": ["戌","亥"],
                "宫属性": "金",  "本位星": "天心星", "本位门": "开", "隐干": "None",
                "地八神": "None", "地盘干": "None", "地盘干长生": ["None"], "天盘干": "None",
                "天盘干长生": ["None"], "天盘星": "None", "天盘星旺衰": ["None", "None"],
                "天八神": "None", "天八神旺衰": ["None", "None"], "天盘门": "None", "天盘门旺衰": ["None", "None"],
                "马星": "None", "空亡": [], "建除": "None", "寄宫干": "None",
                "寄宫干长生": ["None"], "寄宫星": "None", "寄宫星旺衰": ["None", "None"],
                "格局": ["None"],"四害": ""
            },
            "七宫": {
                "宫名": "兑", "方位": "正西", "宫数": "七", "宫支": ["酉"],
                "宫属性": "金",  "本位星": "天柱星", "本位门": "惊", "隐干": "None",
                "地八神": "None", "地盘干": "None", "地盘干长生": ["None","None"], "天盘干": "None",
                "天盘干长生": ["None","None"], "天盘星": "None", "天盘星旺衰": ["None", "None"],
                "天八神": "None", "天八神旺衰": ["None", "None"], "天盘门": "None", "天盘门旺衰": ["None", "None"],
                "马星": "None", "空亡": [], "建除": "None", "寄宫干": "None",
                "寄宫干长生": ["None"], "寄宫星": "None", "寄宫星旺衰": ["None", "None"],
                "格局": ["None"],"四害": ""
            },
            "八宫": {
                "宫名": "艮坎", "方位": "东北", "宫数": "八", "宫支": ["丑","寅"],
                "宫属性": "土",  "本位星": "天任星", "本位门": "生", "隐干": "None",
                "地八神": "None", "地盘干": "None", "地盘干长生": ["None"], "天盘干": "None",
                "天盘干长生": ["None"], "天盘星": "None", "天盘星旺衰": ["None", "None"],
                "天八神": "None", "天八神旺衰": ["None", "None"], "天盘门": "None", "天盘门旺衰": ["None", "None"],
                "马星": "None", "空亡": [], "建除": "None", "寄宫干": "None",
                "寄宫干长生": ["None"], "寄宫星": "None", "寄宫星旺衰": ["None", "None"],
                "格局": ["None"],"四害": ""
            },
            "九宫": {
                "宫名": "离", "方位": "正南", "宫数": "九", "宫支": ["午"],
                "宫属性": "火",  "本位星": "天英星", "本位门": "景门", "隐干": "None",
                "地八神": "None", "地盘干": "None", "地盘干长生": ["None"], "天盘干": "None",
                "天盘干长生": ["None"], "天盘星": "None", "天盘星旺衰": ["None", "None"],
                "天八神": "None", "天八神旺衰": ["None", "None"], "天盘门": "None", "天盘门旺衰": ["None", "None"],
                "马星": "None", "空亡": [], "建除": "None", "寄宫干": "None",
                "寄宫干长生": ["None"], "寄宫星": "None", "寄宫星旺衰": ["None", "None"],
                "格局": ["None"],"四害": ""
            },
           
        }

        # 根据是否提供地区来决定使用真太阳时或直接使用起局时间
        if self.地区:
            # 如果提供了地区，计算真太阳时
            latitude, longitude, true_solar_time = self.真太阳时计算()
            self.奇门遁甲数据["起局信息"]["起局时间"] = true_solar_time.strftime('%Y-%m-%d %H:%M:%S')
            self.奇门遁甲数据["起局信息"]["是否真太阳时"] = True
            self.奇门遁甲数据["起局信息"]["农历"] = self.计算农历(true_solar_time)
            self.奇门遁甲数据["起局信息"]["节气"] = self.计算节气(true_solar_time)
            
            # 计算四柱干支
            self.计算四柱干支(true_solar_time)
        else:
            # 如果没有提供地区，直接使用起局时间
            self.奇门遁甲数据["起局信息"]["起局时间"] = self.起局时.strftime('%Y-%m-%d %H:%M:%S')
            self.奇门遁甲数据["起局信息"]["是否真太阳时"] = False
            self.奇门遁甲数据["起局信息"]["农历"] = self.计算农历(self.起局时)
            self.奇门遁甲数据["起局信息"]["节气"] = self.计算节气(self.起局时)
            
            # 计算四柱干支
            self.计算四柱干支(self.起局时)

    def 计算节气(self, 时间):
        """
        计算当前节气和下一个节气，返回节气列表
        :param 时间: datetime对象
        :return: 节气列表，格式为 [{"name": "节气名", "date": "日期"}, {"name": "节气名", "date": "日期"}]
        """
        from datetime import datetime, timedelta
        from lunar_python import Solar, JieQi, Lunar
        
        # 将输入时间转换为Lunar对象
        lunar = Lunar.fromDate(时间)
        
        # 获取上一个节气
        上一节气 = lunar.getPrevJieQi()
        上一节气名称 = 上一节气.getName()
        
        # 通过JieQi获取节气对应的阳历日期
        上一节气阳历 = 上一节气.getSolar()
        上一节气年 = 上一节气阳历.getYear()
        上一节气月 = 上一节气阳历.getMonth()
        上一节气日 = 上一节气阳历.getDay()
        上一节气时 = 上一节气阳历.getHour()
        上一节气分 = 上一节气阳历.getMinute()
        上一节气日期 = datetime(上一节气年, 上一节气月, 上一节气日, 上一节气时, 上一节气分)
        
        # 获取下一个节气
        下一节气 = lunar.getNextJieQi()
        下一节气名称 = 下一节气.getName()
        
        # 通过JieQi获取节气对应的阳历日期
        下一节气阳历 = 下一节气.getSolar()
        下一节气年 = 下一节气阳历.getYear()
        下一节气月 = 下一节气阳历.getMonth()
        下一节气日 = 下一节气阳历.getDay()
        下一节气时 = 下一节气阳历.getHour()
        下一节气分 = 下一节气阳历.getMinute()
        下一节气日期 = datetime(下一节气年, 下一节气月, 下一节气日, 下一节气时, 下一节气分)
        
        # 创建节气列表，修改日期格式为"MM-DD HH:MM"
        节气列表 = [
            {
                "name": 上一节气名称,
                "date": 上一节气日期.strftime('%m-%d %H:%M')
            },
            {
                "name": 下一节气名称,
                "date": 下一节气日期.strftime('%m-%d %H:%M')
            }
        ]
        
        print(f"[DEBUG] 计算节气: 当前={节气列表[0]['name']}({节气列表[0]['date']}), 下一个={节气列表[1]['name']}({节气列表[1]['date']})")
        return 节气列表

    def 真太阳时计算(self):
        """
        计算真太阳时，返回纬度、经度和真太阳时间，并更新奇门遁甲数据的起局时间。
        如果地区为 None，直接使用起局时间。
        """
        起局时 = self.起局时
        地区 = self.地区

        # 确保起局时是 datetime 类型
        if isinstance(起局时, str):
            try:
                起局时 = datetime.strptime(起局时, '%Y-%m-%d %H:%M')
            except ValueError as e:
                raise ValueError(f"起局时间格式错误，应为 'YYYY-MM-DD HH:MM'，例如 '2025-06-02 14:00'，错误：{e}")

        # 移除时区信息，避免与不支持时区的库冲突
        if 起局时.tzinfo is not None:
            起局时 = 起局时.replace(tzinfo=None)

        # 如果没有提供地区，返回 None 作为纬度和经度
        if not 地区:
            self.奇门遁甲数据["起局信息"]["起局时间"] = 起局时.strftime('%Y-%m-%d %H:%M:%S')
            self.经纬度 = None
            
            # 计算节气信息
            self.奇门遁甲数据["起局信息"]["节气"] = self.计算节气(起局时)
            return None, None, 起局时

        try:
            # 使用 geopy 获取经纬度，增加超时设置
            地理定位器 = Nominatim(user_agent="solar_time_calc", timeout=10)
            位置 = 地理定位器.geocode(地区)
            if not 位置:
                raise ValueError(f"无法找到地区: {地区}")

            纬度, 经度 = 位置.latitude, 位置.longitude
            self.经纬度 = (纬度, 经度)  # 更新类的经纬度属性

            # 计算真太阳时
            # 1. 计算与北京标准时区(东经120度)的经度差
            经度差 = 经度 - 120.0
            
            # 2. 计算地方时差（每1度经度差4分钟）
            地方时差分钟 = 经度差 * 4
            
            # 3. 计算日期对应的均时差(误差方程)
            # 使用简化的均时差计算公式
            年份 = 起局时.year
            月份 = 起局时.month
            日期 = 起局时.day
            
            # 计算当年的第几天
            一月一日 = datetime(年份, 1, 1)
            当前日期 = datetime(年份, 月份, 日期)
            年内天数 = (当前日期 - 一月一日).days + 1
            
            # 计算均时差（单位：分钟）
            # 使用简化的均时差计算公式：E = 9.87 * sin(2B) - 7.53 * cos(B) - 1.5 * sin(B)
            # 其中 B = 2π * (日期 - 81) / 364
            import math
            角度B = 2 * math.pi * (年内天数 - 81) / 364
            均时差分钟 = 9.87 * math.sin(2 * 角度B) - 7.53 * math.cos(角度B) - 1.5 * math.sin(角度B)
            
            # 4. 计算真太阳时 = 区时 + 地方时差 + 均时差
            总时差分钟 = 地方时差分钟 + 均时差分钟
            真太阳时间 = 起局时 + timedelta(minutes=总时差分钟)

            # 更新奇门遁甲数据
            self.奇门遁甲数据["起局信息"]["起局时间"] = 真太阳时间.strftime('%Y-%m-%d %H:%M:%S')
            self.奇门遁甲数据["起局信息"]["是否真太阳时"] = True
            self.奇门遁甲数据["起局信息"]["农历"] = self.计算农历(真太阳时间)
            self.奇门遁甲数据["起局信息"]["节气"] = self.计算节气(真太阳时间)

            return 纬度, 经度, 真太阳时间

        except Exception as e:
            print(f"计算真太阳时时发生错误: {str(e)}")
            # 发生错误时使用原始时间
            self.奇门遁甲数据["起局信息"]["起局时间"] = 起局时.strftime('%Y-%m-%d %H:%M:%S')
            self.经纬度 = None
            return None, None, 起局时

    def 计算农历(self, 时间):
        """
        计算农历日期
        :param 时间: datetime对象
        :return: 农历日期字符串，格式为 "五月初十 戌时"
        """
        try:
            import cnlunar
            农历 = cnlunar.Lunar(时间, godType='8char')
            
            # 获取农历月日（去掉"小"字）
            农历月 = 农历.lunarMonthCn
            if "小" in 农历月:
                农历月 = 农历月.replace("小", "")
            农历日 = 农历.lunarDayCn
            
            # 获取时辰
            时辰 = 农历.twohour8Char[1]  # 取地支作为时辰
            
            # 返回格式化的农历日期字符串（不含年份，添加时辰）
            return f"{农历月}{农历日} {时辰}时"
        except Exception as e:
            print(f"计算农历时发生错误: {str(e)}")
            # 返回简单格式的农历日期
            try:
                from lunar_python import Lunar
                农历 = Lunar.fromDate(时间)
                时辰地支 = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]
                时辰索引 = (时间.hour + 1) // 2 % 12  # 计算时辰索引
                时辰 = 时辰地支[时辰索引]
                月名 = 农历.getMonthInChinese()
                if "小" in 月名:
                    月名 = 月名.replace("小", "")
                return f"{月名}月{农历.getDayInChinese()} {时辰}时"
            except Exception as e:
                print(f"使用lunar_python计算农历时发生错误: {str(e)}")
                # 如果两种方法都失败，返回原始日期
                时辰地支 = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]
                时辰索引 = (时间.hour + 1) // 2 % 12  # 计算时辰索引
                时辰 = 时辰地支[时辰索引]
                return f"{时间.month}月{时间.day}日 {时辰}时"

    def 计算四柱干支(self, 时间):
        """
        计算四柱干支并更新奇门遁甲数据
        :param 时间: datetime对象
        """
        try:
            import cnlunar
            农历 = cnlunar.Lunar(时间, godType='8char')
            
            # 设置四柱干支为数组格式
            年柱 = [农历.year8Char[0], 农历.year8Char[1]]
            月柱 = [农历.month8Char[0], 农历.month8Char[1]]
            日柱 = [农历.day8Char[0], 农历.day8Char[1]]
            时柱 = [农历.twohour8Char[0], 农历.twohour8Char[1]]
            self.奇门遁甲数据["起局信息"]["四柱干支"] = [年柱, 月柱, 日柱, 时柱]
            
            print(f"[DEBUG] 四柱干支: {self.奇门遁甲数据['起局信息']['四柱干支']}")
            return True
        except Exception as e:
            print(f"计算四柱干支时发生错误: {str(e)}")
            # 设置默认四柱干支
            self.奇门遁甲数据["起局信息"]["四柱干支"] = [
                ["甲", "子"], ["乙", "丑"], ["丙", "寅"], ["丁", "卯"]
            ]
            return False

# 测试代码
if __name__ == "__main__":
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M')
    print(f"当前时间: {current_time}")
    
    # 创建奇门遁甲对象，使用当前时间和地区
    try:
        qm = 奇门遁甲(起局时间=current_time, 起局法='拆补法', 地区='合浦县')
        
        # 四柱干支在初始化时已计算，无需重复计算
        
        # 打印结果
        latitude, longitude, true_solar_time = qm.真太阳时计算()
        print(f"经纬度: {longitude},{latitude}")
        print(f"真太阳时间: {true_solar_time}")
        print(f"奇门遁甲数据起局时间: {qm.奇门遁甲数据['起局信息']['起局时间']}")
        
        # 打印农历信息
        print(f"农历: {qm.奇门遁甲数据['起局信息']['农历']}")
        
        # 打印节气内容
        节气列表 = qm.奇门遁甲数据['起局信息']['节气']
        if len(节气列表) >= 2:
            print(f"当前节气: {节气列表[0]['name']}, 交节时间: {节气列表[0]['date']}")
            print(f"下一节气: {节气列表[1]['name']}, 交节时间: {节气列表[1]['date']}")
        else:
            print(f"节气信息不完整: {节气列表}")
        
        print(f"是否真太阳时: {qm.奇门遁甲数据['起局信息']['是否真太阳时']}")
        print(f"四柱干支: {qm.奇门遁甲数据['起局信息']['四柱干支']}")
        
        # 只打印必要的奇门遁甲数据，避免过多输出
        简化数据 = {
            "起局信息": qm.奇门遁甲数据["起局信息"]
        }
        print(f"奇门遁甲起局信息: {简化数据}")
    
    except Exception as e:
        print(f"测试时发生错误: {str(e)}")
        import traceback
        traceback.print_exc()
        