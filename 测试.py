from datetime import datetime
from typing import Dict, Tuple, List, Optional
from dataclasses import dataclass

@dataclass
class GanzhiResult:
    """天干地支计算结果的数据类"""
    year: str
    month: str
    day: str
    hour: str
    
    @property
    def full_string(self) -> str:
        """返回完整的干支表示"""
        return f"{self.year}年 {self.month}月 {self.day}日 {self.hour}时"

# 定义常量
TIANGAN: List[str] = ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸']
DIZHI: List[str] = ['子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥']
GANZHI_START_YEAR: int = -2697  # 干支纪年起始年份

# 月支对应表（寅月为正月）
MONTH_DIZHI: List[str] = ['寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥', '子', '丑']

def get_days_in_month(year: int, month: int) -> int:
    """
    获取指定年月的天数
    
    Args:
        year: 年份
        month: 月份
        
    Returns:
        int: 该月的天数
    """
    if month == 2:
        return 29 if year % 4 == 0 and (year % 100 != 0 or year % 400 == 0) else 28
    return 31 if month in (1, 3, 5, 7, 8, 10, 12) else 30

def validate_input(year: int, month: int, day: int, hour: int) -> None:
    """
    验证输入的年月日时是否有效
    
    Args:
        year: 年份
        month: 月份
        day: 日期
        hour: 小时
        
    Raises:
        ValueError: 当输入参数无效时抛出
    """
    if not isinstance(year, int) or year < GANZHI_START_YEAR:
        raise ValueError(f"年份必须为整数且不小于{GANZHI_START_YEAR}")
    if not isinstance(month, int) or not (1 <= month <= 12):
        raise ValueError("月份必须为1-12之间的整数")
    if not isinstance(day, int) or not (1 <= day <= 31):
        raise ValueError("日期必须为1-31之间的整数")
    if not isinstance(hour, int) or not (0 <= hour <= 23):
        raise ValueError("小时必须为0-23之间的整数")
    
    max_days = get_days_in_month(year, month)
    if day > max_days:
        raise ValueError(f"{year}年{month}月只有{max_days}天")

def calculate_julian_day(year: int, month: int, day: int) -> int:
    """
    计算儒略日
    
    Args:
        year: 年份
        month: 月份
        day: 日期
        
    Returns:
        int: 儒略日
    """
    if month <= 2:
        month += 12
        year -= 1
    
    a = (14 - month) // 12
    y = year + 4800 - a
    m = month + 12 * a - 3
    
    return day + (153 * m + 2) // 5 + 365 * y + y // 4 - y // 100 + y // 400 - 32045

def get_month_ganzhi(year_tiangan: int, month: int) -> Tuple[str, str]:
    """
    计算月干支
    
    Args:
        year_tiangan: 年干索引
        month: 月份（1-12）
        
    Returns:
        Tuple[str, str]: (月干, 月支)
    """
    # 月干 = (年干 × 2 + 月数) % 10
    month_tiangan_index = (year_tiangan * 2 + month) % 10
    # 月支 = (月数 + 2) % 12
    month_dizhi_index = (month + 2) % 12
    
    return TIANGAN[month_tiangan_index], MONTH_DIZHI[month - 1]

def get_day_ganzhi(jd: int) -> Tuple[str, str]:
    """
    计算日干支
    
    Args:
        jd: 儒略日
        
    Returns:
        Tuple[str, str]: (日干, 日支)
    """
    # 日干支索引 = (儒略日 - 1721426 + 11) % 60
    day_ganzhi_index = (jd - 1721426 + 11) % 60
    day_tiangan_index = day_ganzhi_index % 10
    day_dizhi_index = day_ganzhi_index % 12
    
    return TIANGAN[day_tiangan_index], DIZHI[day_dizhi_index]

def get_hour_ganzhi(day_tiangan: int, hour: int) -> Tuple[str, str]:
    """
    计算时干支
    
    Args:
        day_tiangan: 日干索引
        hour: 小时（0-23）
        
    Returns:
        Tuple[str, str]: (时干, 时支)
    """
    # 时支 = (小时 + 1) // 2 % 12
    hour_dizhi_index = (hour + 1) // 2 % 12
    # 时干 = (日干 × 2 + 时支) % 10
    hour_tiangan_index = (day_tiangan * 2 + hour_dizhi_index) % 10
    
    return TIANGAN[hour_tiangan_index], DIZHI[hour_dizhi_index]

def datetime_to_ganzhi(year: int, month: int, day: int, hour: int) -> GanzhiResult:
    """
    将公历年月日时转换为天干地支表示法
    
    Args:
        year: 年份（公历）
        month: 月份（1-12）
        day: 日期（1-31）
        hour: 小时（0-23）
    
    Returns:
        GanzhiResult: 包含年月日时的天干地支表示
        
    Raises:
        ValueError: 当输入参数无效时抛出
    """
    # 验证输入
    validate_input(year, month, day, hour)
    
    # 计算年干支
    year_tiangan_index = (year - 4) % 10
    year_dizhi_index = (year - 4) % 12
    year_ganzhi = TIANGAN[year_tiangan_index] + DIZHI[year_dizhi_index]

    # 计算月干支
    month_tiangan, month_dizhi = get_month_ganzhi(year_tiangan_index, month)
    month_ganzhi = month_tiangan + month_dizhi

    # 计算日干支
    jd = calculate_julian_day(year, month, day)
    day_tiangan, day_dizhi = get_day_ganzhi(jd)
    day_ganzhi = day_tiangan + day_dizhi

    # 计算时干支
    hour_tiangan, hour_dizhi = get_hour_ganzhi(TIANGAN.index(day_tiangan), hour)
    hour_ganzhi = hour_tiangan + hour_dizhi

    return GanzhiResult(
        year=year_ganzhi,
        month=month_ganzhi,
        day=day_ganzhi,
        hour=hour_ganzhi
    )

def test_ganzhi_converter() -> None:
    """测试函数，展示多个测试用例"""
    test_cases = [
        (2020, 6, 1, 22),    # 2020年6月1日22点
        (2024, 2, 29, 12),   # 闰年2月29日
        (2023, 12, 31, 23),  # 年末最后一天
        (datetime.now().year, datetime.now().month, datetime.now().day, datetime.now().hour),  # 当前时间
    ]
    
    for year, month, day, hour in test_cases:
        try:
            result = datetime_to_ganzhi(year, month, day, hour)
            print(f"公历 {year}年{month}月{day}日{hour}时")
            print(f"干支 {result.full_string}")
            print(f"详细：年{result.year} 月{result.month} 日{result.day} 时{result.hour}")
            print("-" * 40)
        except ValueError as e:
            print(f"测试用例 ({year}, {month}, {day}, {hour}) 失败：{str(e)}")
            print("-" * 40)

if __name__ == "__main__":
    test_ganzhi_converter() 