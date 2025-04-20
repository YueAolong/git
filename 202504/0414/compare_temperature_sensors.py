#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
温度传感器对比分析脚本
功能：
1. 通过弹窗选择温度记录CSV文件
2. 清洗数据中的空值
3. 绘制两个传感器的温度折线图进行对比
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import tkinter as tk
from tkinter import filedialog, messagebox
from typing import Optional
import matplotlib
matplotlib.use('TkAgg')  # 放在最上面

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
        title="选择温度记录CSV文件",
        filetypes=[("CSV文件", "*.csv"), ("所有文件", "*.*")]
    )
    
    return file_path if file_path else None


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    清洗数据，处理空值
    
    参数:
        df (pd.DataFrame): 原始数据DataFrame
        
    返回:
        pd.DataFrame: 清洗后的DataFrame
    """
    # 显示原始数据信息
    print("\n===== 原始数据信息 =====")
    print(f"行数: {df.shape[0]}")
    print(f"列数: {df.shape[1]}")
    
    # 检查空值
    missing_values = df.isnull().sum()
    print("\n空值统计:")
    print(missing_values)
    
    # 删除包含空值的行
    df_cleaned = df.dropna()
    
    print("\n===== 清洗后数据信息 =====")
    print(f"行数: {df_cleaned.shape[0]}")
    print(f"删除的行数: {df.shape[0] - df_cleaned.shape[0]}")
    
    return df_cleaned


def plot_temperature_comparison(df: pd.DataFrame, save_path: str = 'temperature_comparison.png') -> None:
    """
    绘制两个传感器的温度对比折线图
    
    参数:
        df (pd.DataFrame): 清洗后的数据DataFrame
        save_path (str): 图表保存路径
    """
    # 设置中文字体
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
    plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
    
    # 创建图表
    plt.figure(figsize=(12, 6))
    
    # 绘制两个传感器的温度曲线
    plt.plot(df['日期'], df['传感器1温度'], 
            marker='o',  # 数据点标记
            linestyle='-',  # 线型
            linewidth=2,  # 线宽
            color='#2E86C1',  # 线条颜色
            markersize=6,  # 标记大小
            label='传感器1')  # 图例标签
    
    plt.plot(df['日期'], df['传感器2温度'], 
            marker='s',  # 数据点标记
            linestyle='-',  # 线型
            linewidth=2,  # 线宽
            color='#E74C3C',  # 线条颜色
            markersize=6,  # 标记大小
            label='传感器2')  # 图例标签
    
    # 添加平均温度线
    avg_temp1 = df['传感器1温度'].mean()
    avg_temp2 = df['传感器2温度'].mean()
    
    plt.axhline(y=avg_temp1, 
                color='#2E86C1',  # 蓝色
                linestyle='--',  # 虚线
                alpha=0.5,
                label=f'传感器1平均: {avg_temp1:.1f}°C')
    
    plt.axhline(y=avg_temp2, 
                color='#E74C3C',  # 红色
                linestyle='--',  # 虚线
                alpha=0.5,
                label=f'传感器2平均: {avg_temp2:.1f}°C')
    
    # 标记最高和最低温度点
    max_temp1_idx = df['传感器1温度'].idxmax()
    min_temp1_idx = df['传感器1温度'].idxmin()
    max_temp2_idx = df['传感器2温度'].idxmax()
    min_temp2_idx = df['传感器2温度'].idxmin()
    
    plt.plot(df['日期'][max_temp1_idx], df['传感器1温度'][max_temp1_idx], 
            'b*',  # 蓝色星形
            markersize=12,
            label=f'传感器1最高: {df["传感器1温度"][max_temp1_idx]:.1f}°C')
    
    plt.plot(df['日期'][min_temp1_idx], df['传感器1温度'][min_temp1_idx], 
            'b^',  # 蓝色三角形
            markersize=12,
            label=f'传感器1最低: {df["传感器1温度"][min_temp1_idx]:.1f}°C')
    
    plt.plot(df['日期'][max_temp2_idx], df['传感器2温度'][max_temp2_idx], 
            'r*',  # 红色星形
            markersize=12,
            label=f'传感器2最高: {df["传感器2温度"][max_temp2_idx]:.1f}°C')
    
    plt.plot(df['日期'][min_temp2_idx], df['传感器2温度'][min_temp2_idx], 
            'r^',  # 红色三角形
            markersize=12,
            label=f'传感器2最低: {df["传感器2温度"][min_temp2_idx]:.1f}°C')
    
    # 计算温度差异
    temp_diff = df['传感器1温度'] - df['传感器2温度']
    avg_diff = temp_diff.mean()
    max_diff = temp_diff.max()
    min_diff = temp_diff.min()
    
    # 设置图表标题和轴标签
    plt.title('温度传感器对比', fontsize=16, pad=15)
    plt.xlabel('日期', fontsize=12)
    plt.ylabel('温度 (°C)', fontsize=12)
    
    # 设置网格
    plt.grid(True, linestyle='--', alpha=0.7)
    
    # 自动调整x轴日期标签
    plt.gcf().autofmt_xdate()
    
    # 添加图例
    plt.legend(loc='upper left', bbox_to_anchor=(1, 1))
    
    # 添加温度差异信息
    plt.figtext(0.02, 0.02, 
                f"平均温度差异: {avg_diff:.1f}°C\n最大温度差异: {max_diff:.1f}°C\n最小温度差异: {min_diff:.1f}°C", 
                fontsize=10, 
                bbox=dict(facecolor='white', alpha=0.8, edgecolor='gray'))
    
    # 调整布局，确保所有元素都能显示
    plt.tight_layout()
    
    # 保存图表
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    print(f"\n温度对比图表已保存为: {save_path}")
    
    # 显示图表
    plt.show()


def main():
    """主函数"""
    print("===== 温度传感器对比分析程序 =====")
    
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
    
    # 读取CSV文件
    try:
        df = pd.read_csv(file_path, encoding='utf-8-sig')
    except UnicodeDecodeError:
        # 尝试其他编码
        df = pd.read_csv(file_path, encoding='gbk')
    
    # 确保日期列是日期类型
    if '日期' in df.columns:
        df['日期'] = pd.to_datetime(df['日期'])
    
    # 清洗数据
    df_cleaned = clean_data(df)
    
    # 显示数据概要
    print("\n===== 数据概要 =====")
    print(f"数据范围: {df_cleaned['日期'].min().strftime('%Y-%m-%d')} 到 {df_cleaned['日期'].max().strftime('%Y-%m-%d')}")
    print(f"传感器1温度范围: {df_cleaned['传感器1温度'].min():.1f}°C 到 {df_cleaned['传感器1温度'].max():.1f}°C")
    print(f"传感器2温度范围: {df_cleaned['传感器2温度'].min():.1f}°C 到 {df_cleaned['传感器2温度'].max():.1f}°C")
    print(f"传感器1平均温度: {df_cleaned['传感器1温度'].mean():.1f}°C")
    print(f"传感器2平均温度: {df_cleaned['传感器2温度'].mean():.1f}°C")
    
    # 计算温度差异
    temp_diff = df_cleaned['传感器1温度'] - df_cleaned['传感器2温度']
    print(f"平均温度差异: {temp_diff.mean():.1f}°C")
    print(f"最大温度差异: {temp_diff.max():.1f}°C")
    print(f"最小温度差异: {temp_diff.min():.1f}°C")
    
    # 绘制温度对比图
    print("\n正在生成温度对比图表...")
    plot_temperature_comparison(df_cleaned)


if __name__ == "__main__":
    main() 