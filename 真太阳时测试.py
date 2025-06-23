import math
from datetime import datetime, timedelta
import pytz
from geopy.geocoders import Nominatim

def get_solar_time_and_solar_terms(current_time, location_name):
“””
计算真太阳时和节气信息

```
参数:
current_time: datetime对象，当前时间
location_name: str，地区名称（中文或英文）

返回:
dict: 包含真太阳时、上一个节气、下一个节气等信息
"""

# 二十四节气名称和对应的太阳黄经度数
SOLAR_TERMS = [
    ("小寒", 285), ("大寒", 300), ("立春", 315), ("雨水", 330),
    ("惊蛰", 345), ("春分", 0), ("清明", 15), ("谷雨", 30),
    ("立夏", 45), ("小满", 60), ("芒种", 75), ("夏至", 90),
    ("小暑", 105), ("大暑", 120), ("立秋", 135), ("处暑", 150),
    ("白露", 165), ("秋分", 180), ("寒露", 195), ("霜降", 210),
    ("立冬", 225), ("小雪", 240), ("大雪", 255), ("冬至", 270)
]

try:
    # 获取地理坐标
    geolocator = Nominatim(user_agent="solar_calculator")
    location = geolocator.geocode(location_name)
    if not location:
        raise ValueError(f"无法找到地区: {location_name}")
    
    latitude = location.latitude
    longitude = location.longitude
    
    # 计算真太阳时
    solar_time = calculate_true_solar_time(current_time, longitude)
    
    # 计算当前年份的所有节气时间
    year = current_time.year
    solar_term_times = []
    
    for term_name, longitude_deg in SOLAR_TERMS:
        term_time = calculate_solar_term_time(year, longitude_deg)
        solar_term_times.append((term_name, term_time))
    
    # 添加下一年的前几个节气，以防当前时间接近年底
    for i in range(4):
        term_name, longitude_deg = SOLAR_TERMS[i]
        term_time = calculate_solar_term_time(year + 1, longitude_deg)
        solar_term_times.append((term_name, term_time))
    
    # 找到上一个和下一个节气
    prev_term = None
    next_term = None
    
    for i, (term_name, term_time) in enumerate(solar_term_times):
        if term_time <= current_time:
            prev_term = (term_name, term_time)
        elif term_time > current_time and next_term is None:
            next_term = (term_name, term_time)
            break
    
    return {
        "当前时间": current_time.strftime("%Y-%m-%d %H:%M:%S"),
        "地区": location_name,
        "经纬度": f"({latitude:.4f}, {longitude:.4f})",
        "真太阳时": solar_time.strftime("%H:%M:%S"),
        "上一个节气": prev_term[0] if prev_term else "未找到",
        "上一个节气时间": prev_term[1].strftime("%Y-%m-%d %H:%M:%S") if prev_term else "未找到",
        "下一个节气": next_term[0] if next_term else "未找到",
        "下一个节气时间": next_term[1].strftime("%Y-%m-%d %H:%M:%S") if next_term else "未找到"
    }
    
except Exception as e:
    return {"错误": str(e)}
```

def calculate_true_solar_time(local_time, longitude):
“”“计算真太阳时”””
# 儒略日数计算
jd = datetime_to_julian_day(local_time)

```
# 计算时差方程 (Equation of Time)
n = jd - 2451545.0  # 自J2000.0以来的日数
L = (280.460 + 0.9856474 * n) % 360  # 平太阳黄经
g = math.radians((357.528 + 0.9856003 * n) % 360)  # 平近点角

# 时差方程（分钟）
equation_of_time = 4 * (L - 0.0057183 - math.degrees(math.atan2(math.tan(math.radians(23.44 - 0.00013 * n)), math.cos(math.radians(L)))))
equation_of_time += 4 * 1.915 * math.sin(g) + 4 * 0.020 * math.sin(2 * g)

# 经度时差（分钟）
longitude_correction = 4 * longitude  # 每度经度4分钟时差

# 计算真太阳时
total_correction = equation_of_time - longitude_correction
solar_time = local_time + timedelta(minutes=total_correction)

return solar_time
```

def datetime_to_julian_day(dt):
“”“将datetime转换为儒略日”””
a = (14 - dt.month) // 12
y = dt.year + 4800 - a
m = dt.month + 12 * a - 3

```
jd = dt.day + (153 * m + 2) // 5 + 365 * y + y // 4 - y // 100 + y // 400 - 32045
jd += (dt.hour - 12) / 24.0 + dt.minute / 1440.0 + dt.second / 86400.0

return jd
```

def calculate_solar_term_time(year, target_longitude):
“”“计算指定年份和太阳黄经的节气时间”””
# 粗略估计：从春分开始计算
base_date = datetime(year, 3, 20, 12, 0, 0)  # 大致的春分时间

```
# 根据目标黄经调整日期
if target_longitude >= 315 or target_longitude < 90:
    # 春季节气或跨年节气
    days_offset = (target_longitude if target_longitude >= 315 else target_longitude + 360) / 360 * 365.25
    if target_longitude >= 315:
        days_offset -= 360 / 360 * 365.25  # 调整为从春分开始
else:
    days_offset = target_longitude / 360 * 365.25

estimated_date = base_date + timedelta(days=days_offset)

# 使用牛顿法精确计算
for _ in range(10):  # 最多迭代10次
    current_longitude = calculate_sun_longitude(estimated_date)
    
    # 计算角度差（考虑360度周期）
    diff = target_longitude - current_longitude
    if diff > 180:
        diff -= 360
    elif diff < -180:
        diff += 360
        
    if abs(diff) < 0.001:  # 精度达到0.001度
        break
        
    # 太阳每天移动约1度
    estimated_date += timedelta(days=diff)

return estimated_date
```

def calculate_sun_longitude(dt):
“”“计算太阳黄经”””
jd = datetime_to_julian_day(dt)
n = jd - 2451545.0  # 自J2000.0以来的日数

```
# 平黄经
L = (280.460 + 0.9856474 * n) % 360

# 平近点角
g = math.radians((357.528 + 0.9856003 * n) % 360)

# 真黄经
true_longitude = L + 1.915 * math.sin(g) + 0.020 * math.sin(2 * g)

return true_longitude % 360
```

# 使用示例

if **name** == “**main**”:
# 示例1：北京时间
beijing_time = datetime(2024, 6, 21, 14, 30, 0)
result1 = get_solar_time_and_solar_terms(beijing_time, “北京”)
print(”=== 北京示例 ===”)
for key, value in result1.items():
print(f”{key}: {value}”)

```
print("\n=== 上海示例 ===")
shanghai_time = datetime(2024, 12, 22, 10, 0, 0)
result2 = get_solar_time_and_solar_terms(shanghai_time, "上海")
for key, value in result2.items():
    print(f"{key}: {value}")
    
print("\n=== 广州示例 ===")
guangzhou_time = datetime(2024, 3, 20, 16, 0, 0)
result3 = get_solar_time_and_solar_terms(guangzhou_time, "广州")
for key, value in result3.items():
    print(f"{key}: {value}")
```