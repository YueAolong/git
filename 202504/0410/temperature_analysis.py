#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
这个脚本创建一个包含温度数据的CSV文件，然后读取并分析这些数据。
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
from datetime import datetime, timedelta
from typing import List, Dict, Any


def generate_temperature_data(num_days: int = 30, output_file: str = 'temperature_data.csv') -> str:
    """
    生成温度数据并保存为CSV文件
    
    参数:
        num_days (int): 生成的天数
        output_file (str): 输出文件名
        
    返回:
        str: 生成的文件路径
    """
    # 生成日期
    end_date = datetime.now()
    start_date = end_date - timedelta(days=num_days-1)
    dates = [start_date + timedelta(days=i) for i in range(num_days)]
    
    # 生成温度数据（模拟真实温度变化）
    base_temp = 20  # 基准温度
    amplitude = 5   # 温度变化幅度
    
    # 使用正弦函数模拟温度变化
    temps = []
    for i in range(num_days):
        # 添加一些随机波动
        random_factor = np.random.normal(0, 1)
        temp = base_temp + amplitude * np.sin(2 * np.pi * i / 7) + random_factor
        temps.append(round(temp, 1))
    
    # 创建DataFrame
    df = pd.DataFrame({
        '日期': [d.strftime('%Y-%m-%d') for d in dates],
        '温度': temps
    })
    
    # 保存为CSV文件
    df.to_csv(output_file, index=False, encoding='utf-8-sig')
    print(f"已生成温度数据文件: {output_file}")
    
    return output_file


def analyze_temperature_data(file_path: str) -> None:
    """
    分析温度数据
    
    参数:
        file_path (str): CSV文件路径
    """
    # 读取CSV文件
    try:
        df = pd.read_csv(file_path, encoding='utf-8-sig')
    except UnicodeDecodeError:
        # 尝试其他编码
        df = pd.read_csv(file_path, encoding='gbk')
    
    # 显示基本信息
    print("\n===== 温度数据基本信息 =====")
    print(f"数据天数: {len(df)}")
    print("\n前5行数据:")
    print(df.head())
    
    # 使用describe()方法查看统计结果
    print("\n===== 使用describe()方法的统计结果 =====")
    print(df['温度'].describe())
    
    # 计算统计信息
    stats = {
        '平均温度': df['温度'].mean(),
        '最高温度': df['温度'].max(),
        '最低温度': df['温度'].min(),
        '温度中位数': df['温度'].median(),
        '温度标准差': df['温度'].std(),
        '温度范围': df['温度'].max() - df['温度'].min()
    }
    
    # 显示统计信息
    print("\n===== 温度统计信息 =====")
    for key, value in stats.items():
        print(f"{key}: {value:.2f}°C")
    
    # 找出最高温和最低温的日期
    max_temp_date = df.loc[df['温度'].idxmax(), '日期']
    min_temp_date = df.loc[df['温度'].idxmin(), '日期']
    print(f"\n最高温度日期: {max_temp_date}, 温度: {stats['最高温度']:.2f}°C")
    print(f"最低温度日期: {min_temp_date}, 温度: {stats['最低温度']:.2f}°C")
    
    # 计算温度变化趋势
    df['温度变化'] = df['温度'].diff()
    avg_change = df['温度变化'].mean()
    print(f"\n平均温度变化: {avg_change:.2f}°C/天")
    
    # 可视化数据
    visualize_temperature_data(df)


def visualize_temperature_data(df: pd.DataFrame) -> None:
    """
    可视化温度数据
    
    参数:
        df (pd.DataFrame): 温度数据DataFrame
    """
    # 设置中文字体
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
    plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
    
    # 创建图表
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))
    
    # 温度变化折线图
    ax1.plot(df['日期'], df['温度'], marker='o', linestyle='-', color='red')
    ax1.set_title('温度变化趋势')
    ax1.set_xlabel('日期')
    ax1.set_ylabel('温度 (°C)')
    ax1.grid(True, linestyle='--', alpha=0.7)
    plt.setp(ax1.xaxis.get_majorticklabels(), rotation=45, ha='right')
    
    # 添加平均温度线
    avg_temp = df['温度'].mean()
    ax1.axhline(y=avg_temp, color='blue', linestyle='--', label=f'平均温度: {avg_temp:.2f}°C')
    ax1.legend()
    
    # 温度分布直方图
    ax2.hist(df['温度'], bins=10, color='skyblue', edgecolor='black')
    ax2.set_title('温度分布')
    ax2.set_xlabel('温度 (°C)')
    ax2.set_ylabel('频次')
    ax2.grid(True, linestyle='--', alpha=0.7)
    
    plt.tight_layout()
    plt.savefig('temperature_visualization.png')
    print("\n温度数据可视化已保存为 'temperature_visualization.png'")


def main():
    """主函数"""
    print("===== 温度数据分析程序 =====")
    
    # 生成温度数据
    num_days = int(input("请输入要生成的天数 (默认30): ") or "30")
    output_file = 'temperature_data.csv'
    
    # 检查文件是否已存在
    if os.path.exists(output_file):
        use_existing = input(f"文件 '{output_file}' 已存在，是否使用现有文件? (y/n): ").lower()
        if use_existing != 'y':
            file_path = generate_temperature_data(num_days, output_file)
        else:
            file_path = output_file
    else:
        file_path = generate_temperature_data(num_days, output_file)
    
    # 分析温度数据
    analyze_temperature_data(file_path)


if __name__ == "__main__":
    main() 