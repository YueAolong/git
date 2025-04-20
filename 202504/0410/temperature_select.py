#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
温度数据分析脚本
功能：
1. 通过弹窗选择CSV文件
2. 读取数据并显示前5行
3. 找出最高温度和对应日期
4. 计算平均温度
5. 输出超过平均温度的日期
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import tkinter as tk
from tkinter import filedialog, messagebox
from typing import Optional


def select_file() -> Optional[str]:
    """
    通过文件对话框选择CSV文件
    
    返回:
        Optional[str]: 选择的文件路径，如果用户取消则返回None
    """
    # 创建Tkinter根窗口
    root = tk.Tk()
    root.withdraw()  # 隐藏主窗口
    
    # 打开文件选择对话框
    file_path = filedialog.askopenfilename(
        title="选择温度数据CSV文件",
        filetypes=[("CSV文件", "*.csv"), ("所有文件", "*.*")]
    )
    
    return file_path if file_path else None


def generate_sample_data(output_file: str = 'temperature_data.csv') -> str:
    """
    生成示例温度数据并保存为CSV文件
    
    参数:
        output_file (str): 输出文件名
        
    返回:
        str: 生成的文件路径
    """
    # 生成随机数据
    np.random.seed(42)  # 设置随机种子，确保结果可重现
    
    # 创建日期范围（30天）
    dates = pd.date_range(start='2023-01-01', periods=30, freq='D')
    
    # 生成温度数据（模拟夏季温度，有日变化）
    base_temp = 25  # 基础温度
    daily_variation = np.sin(np.linspace(0, 2*np.pi, 30)) * 5  # 日变化
    random_variation = np.random.normal(0, 2, 30)  # 随机变化
    
    temperatures = base_temp + daily_variation + random_variation
    
    # 创建DataFrame
    df = pd.DataFrame({
        '日期': dates,
        '温度': temperatures.round(1)
    })
    
    # 保存为CSV文件
    df.to_csv(output_file, index=False, encoding='utf-8-sig')
    print(f"已生成示例温度数据文件: {output_file}")
    
    return output_file


def analyze_temperature_data(file_path: str) -> None:
    """
    分析温度数据并显示结果
    
    参数:
        file_path (str): CSV文件路径
    """
    # 读取CSV文件
    try:
        df = pd.read_csv(file_path, encoding='utf-8-sig')
    except UnicodeDecodeError:
        # 尝试其他编码
        df = pd.read_csv(file_path, encoding='gbk')
    
    # 确保日期列是日期类型
    if '日期' in df.columns:
        df['日期'] = pd.to_datetime(df['日期'])
    
    # 1. 输出前5行数据
    print("\n===== 数据前5行 =====")
    print(df.head())
    
    # 2. 找出最高温度和对应日期
    max_temp = df['温度'].max()
    max_temp_date = df.loc[df['温度'] == max_temp, '日期'].iloc[0]
    
    print("\n===== 最高温度信息 =====")
    print(f"最高温度: {max_temp:.1f}°C")
    print(f"对应日期: {max_temp_date.strftime('%Y-%m-%d')}")
    
    # 3. 计算平均温度
    avg_temp = df['温度'].mean()
    
    print("\n===== 平均温度 =====")
    print(f"平均温度: {avg_temp:.1f}°C")
    
    # 4. 输出超过平均温度的日期
    above_avg = df[df['温度'] > avg_temp]
    
    print("\n===== 超过平均温度的日期 =====")
    print(f"共有 {len(above_avg)} 天温度超过平均值")
    
    for _, row in above_avg.iterrows():
        print(f"日期: {row['日期'].strftime('%Y-%m-%d')}, 温度: {row['温度']:.1f}°C")
    
    # 可视化温度数据
    visualize_temperature_data(df, avg_temp)


def visualize_temperature_data(df: pd.DataFrame, avg_temp: float) -> None:
    """
    可视化温度数据
    
    参数:
        df (pd.DataFrame): 温度数据DataFrame
        avg_temp (float): 平均温度
    """
    # 设置中文字体
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
    plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
    
    # 创建图表
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # 绘制温度曲线
    ax.plot(df['日期'], df['温度'], marker='o', linestyle='-', color='blue', linewidth=2, markersize=6)
    
    # 绘制平均温度线
    ax.axhline(y=avg_temp, color='red', linestyle='--', label=f'平均温度: {avg_temp:.1f}°C')
    
    # 标记最高温度点
    max_temp = df['温度'].max()
    max_temp_date = df.loc[df['温度'] == max_temp, '日期'].iloc[0]
    ax.plot(max_temp_date, max_temp, marker='*', color='red', markersize=12, label=f'最高温度: {max_temp:.1f}°C')
    
    # 设置图表属性
    ax.set_title('温度变化趋势', fontsize=16)
    ax.set_xlabel('日期', fontsize=12)
    ax.set_ylabel('温度 (°C)', fontsize=12)
    ax.grid(True, linestyle='--', alpha=0.7)
    ax.legend(loc='upper right')
    
    # 旋转x轴日期标签
    plt.xticks(rotation=45)
    
    # 调整布局
    plt.tight_layout()
    
    # 保存图表
    plt.savefig('temperature_visualization.png')
    print("\n温度数据可视化已保存为 'temperature_visualization.png'")


def main():
    """主函数"""
    print("===== 温度数据分析程序 =====")
    
    # 选择文件或生成示例数据
    choice = input("是否生成示例温度数据? (y/n): ").lower()
    
    if choice == 'y':
        file_path = generate_sample_data()
    else:
        # 通过文件对话框选择文件
        file_path = select_file()
        
        # 检查是否选择了文件
        if not file_path:
            print("未选择文件，程序退出")
            return
        
        # 检查文件是否存在
        if not os.path.exists(file_path):
            messagebox.showerror("错误", f"文件 '{file_path}' 不存在")
            print(f"错误: 文件 '{file_path}' 不存在")
            return
    
    # 分析温度数据
    analyze_temperature_data(file_path)


if __name__ == "__main__":
    main() 