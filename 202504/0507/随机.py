from openpyxl import Workbook
import random
from datetime import datetime, timedelta

# 创建工作簿
wb = Workbook()
ws = wb.active
ws.title = "热管理日报"

# 写入表头
ws.append(["日期", "部位", "温度 (℃)", "备注"])

# 模拟数据
parts = ['电池包', '电机', '电控', '空调']
start_date = datetime.today() - timedelta(days=6)  # 过去7天

for i in range(7):  # 7天
    date = (start_date + timedelta(days=i)).strftime("%Y-%m-%d")
    for part in parts:
        temp = round(random.uniform(30, 48), 1)  # 30～48℃ 之间
        note = "正常" if temp < 40 else "偏高"
        ws.append([date, part, temp, note])

# 保存文件
wb.save("热管理日报.xlsx")
print("✅ 文件已生成：热管理日报.xlsx")
