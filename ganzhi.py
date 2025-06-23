def datetime_to_ganzhi(year, month, day, hour):
    """
    将公历年月日时转换为天干地支表示法
    
    参数:
        year: 年份（公历）
        month: 月份（1-12）
        day: 日期（1-31）
        hour: 小时（0-23）
    
    返回:
        dict: 包含年月日时的天干地支表示
    """
    # 定义天干和地支
    tiangan = ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸']  # 10个天干
    dizhi = ['子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥']  # 12个地支

    # 1. 计算年干支
    # 修正：使用正确的干支起始年份（公元前2637年）
    year_tiangan_index = (year + 2637) % 10
    year_dizhi_index = (year + 2637) % 12
    year_ganzhi = tiangan[year_tiangan_index] + dizhi[year_dizhi_index]

    # 2. 计算月干支
    # 修正：使用正确的月干计算公式
    # 月干 = (年干序号 * 2 + 月份 - 1) % 10
    month_tiangan_index = (year_tiangan_index * 2 + month - 1) % 10
    # 月支：正月寅、二月卯、三月辰...
    month_dizhi_index = (month + 1) % 12
    month_ganzhi = tiangan[month_tiangan_index] + dizhi[month_dizhi_index]

    # 3. 计算日干支
    # 使用修正后的儒略日计算公式
    if month <= 2:
        month += 12
        year -= 1
    
    # 修正：使用更准确的儒略日计算公式
    a = (14 - month) // 12
    y = year + 4800 - a
    m = month + 12 * a - 3
    
    jd = day + (153 * m + 2) // 5 + 365 * y + y // 4 - y // 100 + y // 400 - 32045
    
    # 修正：使用正确的日干支起始点
    day_ganzhi_index = (jd - 1721426 + 11) % 60
    day_tiangan_index = day_ganzhi_index % 10
    day_dizhi_index = day_ganzhi_index % 12
    day_ganzhi = tiangan[day_tiangan_index] + dizhi[day_dizhi_index]

    # 4. 计算时干支
    # 修正：使用正确的时辰对应关系
    # 子时(23-1点)、丑时(1-3点)、寅时(3-5点)...
    hour_dizhi_index = ((hour + 1) % 24) // 2
    # 修正：使用正确的时干计算公式
    hour_tiangan_index = (day_tiangan_index * 2 + hour_dizhi_index) % 10
    hour_ganzhi = tiangan[hour_tiangan_index] + dizhi[hour_dizhi_index]

    return {
        '年': year_ganzhi,
        '月': month_ganzhi,
        '日': day_ganzhi,
        '时': hour_ganzhi,
        '完整': f"{year_ganzhi}年 {month_ganzhi}月 {day_ganzhi}日 {hour_ganzhi}时"
    }

def test_ganzhi_converter():
    """测试函数，展示几个例子"""
    test_cases = [
        (2024, 1, 1, 12),    # 2024年1月1日12点
        (2023, 6, 15, 18),   # 2023年6月15日18点
        (2025, 3, 8, 9),     # 2025年3月8日9点
        (2024, 2, 10, 23),   # 2024年2月10日23点（测试子时）
        (2024, 12, 31, 0),   # 2024年12月31日0点（测试跨年）
    ]
    
    for year, month, day, hour in test_cases:
        result = datetime_to_ganzhi(year, month, day, hour)
        print(f"公历 {year}年{month}月{day}日{hour}时")
        print(f"干支 {result['完整']}")
        print(f"详细：年{result['年']} 月{result['月']} 日{result['日']} 时{result['时']}")
        print("-" * 40)

if __name__ == "__main__":
    test_ganzhi_converter() 