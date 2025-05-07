import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import filedialog
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import os
import matplotlib
matplotlib.use('TkAgg')  # 放在最上面
# 设置中文字体，避免显示乱码
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

def select_file():
    """打开文件选择对话框"""
    root = tk.Tk()
    root.withdraw()  # 隐藏主窗口
    file_path = filedialog.askopenfilename(
        title="选择温度数据文件",
        filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")]
    )
    return file_path

def read_data(file_path):
    """读取Excel文件中的数据"""
    try:
        # 尝试读取"每日温度数据"工作表
        df = pd.read_excel(file_path, sheet_name='每日温度数据')
        return df
    except:
        try:
            # 如果没有"每日温度数据"工作表，尝试读取第一个工作表
            df = pd.read_excel(file_path, sheet_name=0)
            return df
        except Exception as e:
            print(f"读取文件时出错: {e}")
            return None

def plot_max_temperatures(df):
    """绘制各部件的最高温度柱状图"""
    # 获取所有温度列（假设列名中包含"温度"）
    temp_columns = [col for col in df.columns if '温度' in col and '℃' in col]
    
    if not temp_columns:
        print("未找到温度数据列")
        return
    
    # 计算每个部件的最高温度
    max_temps = {col: df[col].max() for col in temp_columns}
    
    # 创建柱状图
    plt.figure(figsize=(12, 8))
    components = [col.replace('温度(℃)', '') for col in temp_columns]
    temperatures = [max_temps[col] for col in temp_columns]
    
    # 绘制柱状图
    bars = plt.bar(components, temperatures, width=0.6)
    
    # 设置图表标题和轴标签
    plt.title('各部件最高温度', fontsize=14, pad=15)
    plt.xlabel('部件', fontsize=12)
    plt.ylabel('温度（℃）', fontsize=12)
    
    # 在柱子上方添加温度值
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.1f}℃',
                ha='center', va='bottom')
    
    # 设置y轴范围，留出一定空间显示温度值
    plt.ylim(0, max(temperatures) * 1.2)
    
    # 添加网格线
    plt.grid(True, axis='y', linestyle='--', alpha=0.7)
    
    # 旋转x轴标签，避免重叠
    plt.xticks(rotation=45, ha='right')
    
    # 调整布局
    plt.tight_layout()
    
    # 保存图片
    output_dir = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.join(output_dir, '各部件最高温度.png')
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    
    # 显示图表
    plt.show()
    
    print(f"图表已保存至: {output_path}")

def main():
    # 选择文件
    file_path = select_file()
    
    if not file_path:
        print("未选择文件")
        return
    
    print(f"已选择文件: {file_path}")
    
    # 读取数据
    df = read_data(file_path)
    
    if df is None:
        print("无法读取数据")
        return
    
    # 绘制图表
    plot_max_temperatures(df)

if __name__ == "__main__":
    main() 