import matplotlib.pyplot as plt
import numpy as np
import matplotlib
matplotlib.use('TkAgg')  # 放在最上面
# 设置中文字体，避免显示乱码
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

# 数据
modules = ['前端模块', '中部模块', '后部模块', '左侧模块', '右侧模块']
temperatures = [36.5, 34.8, 35.9, 37.2, 35.0]

# 创建图形对象，设置图形大小和DPI
plt.figure(figsize=(10, 6), dpi=300)

# 创建柱状图
bars = plt.bar(modules, temperatures, width=0.6)

# 设置最高温度模块为红色
max_temp_index = temperatures.index(max(temperatures))
bars[max_temp_index].set_color('red')

# 设置图表标题和轴标签
plt.title('电池模块温度分布', fontsize=14, pad=15)
plt.xlabel('模块位置', fontsize=12)
plt.ylabel('温度（℃）', fontsize=12)

# 在柱子上方添加温度值
for bar in bars:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2., height,
             f'{height}℃',
             ha='center', va='bottom')

# 设置y轴范围，留出一定空间显示温度值
plt.ylim(30, 40)

# 添加网格线
plt.grid(True, axis='y', linestyle='--', alpha=0.7)

# 保存图片
plt.savefig('battery_temperature.png', dpi=300, bbox_inches='tight')

# 显示图表
plt.show() 