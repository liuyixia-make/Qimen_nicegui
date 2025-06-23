from datetime import datetime, timedelta
from cnlunar import Lunar

class LunarBuildService:
    """
    提供未来十二天的建除日及宜忌信息服务
    """
    def __init__(self):
        # 建除十二神对应的宜忌
        self.jianchu_yiji = {
            "建": {
                "yi": "祭祀、祈福、求嗣、开光、出行、开市、立券、交易、纳财、入宅、安葬",
                "ji": "动土、破土、安门、开池"
            },
            "除": {
                "yi": "除服、疗病、破屋、坏垣、求医、治病、破土、余事勿取",
                "ji": "嫁娶、安葬、开市、入宅、安床、开张、搬家"
            },
            "满": {
                "yi": "祭祀、祈福、嫁娶、开市、纳采、修造、入宅、动土、安葬、破土",
                "ji": "开仓、出货、启攒、安门、安床"
            },
            "平": {
                "yi": "祭祀、祈福、嫁娶、出行、立券、纳财、纳畜、牧养、开市",
                "ji": "安葬、行船、破土、修造"
            },
            "定": {
                "yi": "祭祀、祈福、嫁娶、纳采、修造、安葬、入殓、破土、安香、谢土",
                "ji": "移徙、出行、开市、纳畜、安床"
            },
            "执": {
                "yi": "祭祀、祈福、纳采、嫁娶、纳财、开市、立券、交易",
                "ji": "动土、破土、安葬、入宅、开池"
            },
            "破": {
                "yi": "破屋、坏垣、求医、治病、余事勿取",
                "ji": "嫁娶、开市、安葬、入宅、开张、搬家、出行"
            },
            "危": {
                "yi": "祭祀、祈福、斋醮、纳畜、牧养",
                "ji": "嫁娶、出行、移徙、开市、入宅、安葬、修造"
            },
            "成": {
                "yi": "祭祀、祈福、嫁娶、纳采、出行、开市、立券、纳财、入宅、修造、安床",
                "ji": "安葬、破土、行船"
            },
            "收": {
                "yi": "祭祀、祈福、纳财、安葬、修造、动土、纳畜",
                "ji": "嫁娶、开市、立券、出行、移徙"
            },
            "开": {
                "yi": "祭祀、祈福、嫁娶、纳采、出行、开市、立券、纳财、入宅、开池、开井",
                "ji": "安葬、破土、行船"
            },
            "闭": {
                "yi": "祭祀、祈福、纳财、埋穴、安葬、修坟",
                "ji": "嫁娶、开市、立券、出行、移徙、开池、开井、入宅"
            }
        }
        
        # 五不遇时对应关系
        self.five_bad_times = {
            "甲": "庚", "乙": "辛", "丙": "壬", "丁": "癸", "戊": "甲",
            "己": "乙", "庚": "丙", "辛": "丁", "壬": "戊", "癸": "己"
        }
        
        # 时辰对应的时间段
        self.hour_time_ranges = {
            "子": "23点-1点",
            "丑": "1点-3点",
            "寅": "3点-5点",
            "卯": "5点-7点",
            "辰": "7点-9点",
            "巳": "9点-11点",
            "午": "11点-13点",
            "未": "13点-15点",
            "申": "15点-17点",
            "酉": "17点-19点",
            "戌": "19点-21点",
            "亥": "21点-23点"
        }
        
        # 天干五行属性
        self.tiangan_wuxing = {
            "甲": "木", "乙": "木",
            "丙": "火", "丁": "火",
            "戊": "土", "己": "土",
            "庚": "金", "辛": "金",
            "壬": "水", "癸": "水"
        }
        
        # 地支五行属性
        self.dizhi_wuxing = {
            "子": "水", "丑": "土", "寅": "木", "卯": "木",
            "辰": "土", "巳": "火", "午": "火", "未": "土",
            "申": "金", "酉": "金", "戌": "土", "亥": "水"
        }
        
        # 五行对应的颜色
        self.wuxing_colors = {
            "木": "#4CAF50",  # 绿色
            "火": "#F44336",  # 红色
            "土": "#FF9800",  # 橙色/黄色
            "金": "#FFD700",  # 金色
            "水": "#2196F3"   # 蓝色
        }
        
        # 建除十二神对应的神煞
        self.jianchu_shenshas = {
            "建": "天恩",
            "除": "玉堂",
            "满": "司命",
            "平": "民日",
            "定": "天马",
            "执": "天赦",
            "破": "天罡",
            "危": "天巫",
            "成": "明堂",
            "收": "天德",
            "开": "金堂",
            "闭": "普护"
        }
        
        # 黄道吉日（六黄道日）
        self.yellow_path_days = ["除", "满", "定", "执", "成", "开"]
        
        # 黑道凶日（六黑道日）
        self.black_path_days = ["建", "平", "破", "危", "收", "闭"]
    
    def get_next_12_days_build_info(self):
        today = datetime.today()
        days_info = []
        for i in range(12):
            day = today + timedelta(days=i)
            lunar = Lunar(day, godType='8char')
            jianshen_tuple = lunar.get_today12DayOfficer()
            
            # 从元组中获取建除日、神煞和黄道/黑道日信息
            print(f"Debug - 原始十二神数据: {jianshen_tuple}")
            if isinstance(jianshen_tuple, (list, tuple)) and len(jianshen_tuple) >= 3:
                jianshen = jianshen_tuple[0]  # 建除日，如"成"
                shensha = jianshen_tuple[1]   # 神煞，如"明堂"
                day_type = jianshen_tuple[2]  # 黄道/黑道日，如"黄道日"
            else:
                jianshen = jianshen_tuple[0] if isinstance(jianshen_tuple, (list, tuple)) and len(jianshen_tuple) > 0 else ''
                shensha = ""
                day_type = ""
            
            # 判断是否为黄道日或黑道日
            is_yellow_path = "黄道" in day_type
            is_black_path = "黑道" in day_type
            
            # 根据建除神获取宜忌
            yi = self.jianchu_yiji.get(jianshen, {}).get("yi", "无")
            ji = self.jianchu_yiji.get(jianshen, {}).get("ji", "无")
            
            # 获取八字
            year_gan = lunar.year8Char[0]
            year_zhi = lunar.year8Char[1]
            month_gan = lunar.month8Char[0]
            month_zhi = lunar.month8Char[1]
            day_gan = lunar.day8Char[0]
            day_zhi = lunar.day8Char[1]
            hour_gan = lunar.twohour8Char[0]
            hour_zhi = lunar.twohour8Char[1]
            
            # 获取天干地支的五行和颜色
            bazi_colors = {
                "year_gan": self.wuxing_colors.get(self.tiangan_wuxing.get(year_gan, ""), "#000000"),
                "year_zhi": self.wuxing_colors.get(self.dizhi_wuxing.get(year_zhi, ""), "#000000"),
                "month_gan": self.wuxing_colors.get(self.tiangan_wuxing.get(month_gan, ""), "#000000"),
                "month_zhi": self.wuxing_colors.get(self.dizhi_wuxing.get(month_zhi, ""), "#000000"),
                "day_gan": self.wuxing_colors.get(self.tiangan_wuxing.get(day_gan, ""), "#000000"),
                "day_zhi": self.wuxing_colors.get(self.dizhi_wuxing.get(day_zhi, ""), "#000000"),
                "hour_gan": self.wuxing_colors.get(self.tiangan_wuxing.get(hour_gan, ""), "#000000"),
                "hour_zhi": self.wuxing_colors.get(self.dizhi_wuxing.get(hour_zhi, ""), "#000000")
            }
            
            bazi = ' '.join([lunar.year8Char, lunar.month8Char, lunar.day8Char, lunar.twohour8Char])
            
            # 获取当日时辰列表
            twohour_list = lunar.twohour8CharList
            
            # 计算五不遇时
            five_bad_hours = self.calculate_five_bad_times(lunar.day8Char[0], twohour_list)
            
            # 正确计算星期几
            # Python的weekday()返回0-6代表周一到周日，需要转换为"日一二三四五六"
            weekday_index = day.weekday()
            weekday_char = '一二三四五六日'[weekday_index]
            
            days_info.append({
                'date': day.strftime('%Y-%m-%d'),
                'weekday': weekday_char,
                'jianchu': jianshen,
                'shensha': shensha,
                'day_type': day_type,
                'is_yellow_path': is_yellow_path,
                'is_black_path': is_black_path,
                'yi': yi,
                'ji': ji,
                'bazi': bazi,
                'day_gan': day_gan,
                'day_zhi': day_zhi,
                'bazi_colors': bazi_colors,
                'twohour_list': twohour_list,
                'five_bad_hours': five_bad_hours
            })
        return days_info
    
    def calculate_five_bad_times(self, day_gan, twohour_list):
        """
        计算五不遇时
        
        参数:
            day_gan: 日干，如"甲"
            twohour_list: 当日时辰列表，格式如["甲子", "乙丑", ...]
        
        返回:
            五不遇时列表，包含完整时柱和时间段
        """
        bad_gan = self.five_bad_times.get(day_gan)
        if not bad_gan:
            return []
        
        bad_hours = []
        for hour in twohour_list:
            if hour[0] == bad_gan:  # 时干与五不遇时对应干相同
                time_range = self.hour_time_ranges.get(hour[1], "")
                bad_hours.append(f"{hour} ({time_range})")
        
        return bad_hours 