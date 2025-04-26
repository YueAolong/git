import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from io import BytesIO
from PIL import Image
import openpyxl

# 设置中文字体，避免显示乱码
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

# 生成一周的日期
start_date = datetime.now()
dates = [start_date + timedelta(days=x) for x in range(7)]

# 生成模拟数据
data = {
    '日期': dates,
    '前端模块温度(℃)': np.random.normal(35, 1, 7).round(1),
    '中部模块温度(℃)': np.random.normal(34, 1, 7).round(1),
    '后部模块温度(℃)': np.random.normal(35, 1, 7).round(1),
    '左侧模块温度(℃)': np.random.normal(36, 1, 7).round(1),
    '右侧模块温度(℃)': np.random.normal(35, 1, 7).round(1),
    '环境温度(℃)': np.random.normal(25, 2, 7).round(1)
}

# 创建DataFrame
df = pd.DataFrame(data)

# 格式化日期列
df['日期'] = df['日期'].dt.strftime('%Y-%m-%d')

# 筛选温度超过35℃的预警数据
warning_data = pd.DataFrame()
for column in df.columns[1:]:  # 跳过日期列
    mask = df[column] > 35
    if mask.any():
        warning_rows = df[mask][['日期', column]]
        warning_rows.columns = ['日期', '温度(℃)']
        warning_rows['模块'] = column.replace('温度(℃)', '')
        warning_data = pd.concat([warning_data, warning_rows])

# 计算温度波动（标准差）
fluctuation_stats = pd.DataFrame({
    '模块': [col.replace('温度(℃)', '') for col in df.columns[1:]],
    '温度波动(℃)': [df[col].std().round(2) for col in df.columns[1:]],
    '最大波动(℃)': [(df[col].max() - df[col].min()).round(2) for col in df.columns[1:]]
})

# 添加统计信息
stats = pd.DataFrame({
    '统计项': ['最高温度', '最低温度', '平均温度'],
    '前端模块温度(℃)': [df['前端模块温度(℃)'].max(), df['前端模块温度(℃)'].min(), df['前端模块温度(℃)'].mean().round(1)],
    '中部模块温度(℃)': [df['中部模块温度(℃)'].max(), df['中部模块温度(℃)'].min(), df['中部模块温度(℃)'].mean().round(1)],
    '后部模块温度(℃)': [df['后部模块温度(℃)'].max(), df['后部模块温度(℃)'].min(), df['后部模块温度(℃)'].mean().round(1)],
    '左侧模块温度(℃)': [df['左侧模块温度(℃)'].max(), df['左侧模块温度(℃)'].min(), df['左侧模块温度(℃)'].mean().round(1)],
    '右侧模块温度(℃)': [df['右侧模块温度(℃)'].max(), df['右侧模块温度(℃)'].min(), df['右侧模块温度(℃)'].mean().round(1)],
    '环境温度(℃)': [df['环境温度(℃)'].max(), df['环境温度(℃)'].min(), df['环境温度(℃)'].mean().round(1)]
})

# 创建温度折线图
plt.figure(figsize=(12, 6))
for column in df.columns[1:]:  # 跳过日期列
    plt.plot(df['日期'], df[column], marker='o', label=column)

plt.title('各模块温度变化趋势', fontsize=14, pad=15)
plt.xlabel('日期', fontsize=12)
plt.ylabel('温度（℃）', fontsize=12)
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plt.grid(True, linestyle='--', alpha=0.7)
plt.xticks(rotation=45)

# 添加35℃警戒线
plt.axhline(y=35, color='r', linestyle='--', alpha=0.5, label='警戒温度')

# 调整布局，确保图例完全显示
plt.tight_layout()

# 将图表保存到内存中
img_buffer = BytesIO()
plt.savefig(img_buffer, format='png', dpi=300, bbox_inches='tight')
img_buffer.seek(0)

# 创建Excel写入器
with pd.ExcelWriter('热管理日报_带图表.xlsx', engine='openpyxl') as writer:
    # 写入每日数据
    df.to_excel(writer, sheet_name='每日温度数据', index=False)
    
    # 写入统计信息
    stats.to_excel(writer, sheet_name='温度统计', index=False)
    
    # 写入温度波动统计
    fluctuation_stats.to_excel(writer, sheet_name='温度波动统计', index=False)
    
    # 写入预警数据
    if not warning_data.empty:
        warning_data.to_excel(writer, sheet_name='温度预警数据', index=False)
    
    # 获取工作簿对象
    workbook = writer.book
    
    # 获取工作表对象
    daily_sheet = workbook['每日温度数据']
    stats_sheet = workbook['温度统计']
    fluctuation_sheet = workbook['温度波动统计']
    
    # 调整列宽
    for sheet in [daily_sheet, stats_sheet, fluctuation_sheet]:
        for column in sheet.columns:
            max_length = 0
            column = [cell for cell in column]
            for cell in column:
                try:
                    if len(str(cell.value)) > max_length:
                        max_length = len(str(cell.value))
                except:
                    pass
            adjusted_width = (max_length + 2)
            sheet.column_dimensions[column[0].column_letter].width = adjusted_width
    
    # 在每日温度数据工作表下方插入图表
    img = Image.open(img_buffer)
    # 计算图片大小（像素转Excel单位）
    width = img.width * 0.75
    height = img.height * 0.75
    
    # 插入图片到Excel
    daily_sheet.add_image(
        openpyxl.drawing.image.Image(img_buffer),
        f'A{len(df) + 3}'  # 在数据下方留出空间插入图表
    )

print("热管理日报_带图表.xlsx 文件已生成完成！") 