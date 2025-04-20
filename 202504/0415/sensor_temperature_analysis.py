#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
温度传感器分析脚本
功能：
1. 通过弹窗选择CSV文件
2. 读取两个传感器的温度数据
3. 清洗空值
4. 计算统计值（平均值、最大值及对应日期）
5. 绘制对比折线图
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import tkinter as tk
from tkinter import filedialog, messagebox
from typing import Optional, Dict, Any, Tuple
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
        title="选择温度传感器数据CSV文件",
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


def calculate_statistics(df: pd.DataFrame) -> Dict[str, Dict[str, Any]]:
    """
    计算每个传感器的统计值
    
    参数:
        df (pd.DataFrame): 清洗后的数据DataFrame
        
    返回:
        Dict[str, Dict[str, Any]]: 包含每个传感器统计值的字典
    """
    stats = {}
    
    # 计算传感器1的统计值
    sensor1_stats = {
        '平均值': df['传感器1温度'].mean(),
        '最大值': df['传感器1温度'].max(),
        '最小值': df['传感器1温度'].min(),
        '最大值日期': df.loc[df['传感器1温度'].idxmax(), '日期'],
        '最小值日期': df.loc[df['传感器1温度'].idxmin(), '日期']
    }
    stats['传感器1'] = sensor1_stats
    
    # 计算传感器2的统计值
    sensor2_stats = {
        '平均值': df['传感器2温度'].mean(),
        '最大值': df['传感器2温度'].max(),
        '最小值': df['传感器2温度'].min(),
        '最大值日期': df.loc[df['传感器2温度'].idxmax(), '日期'],
        '最小值日期': df.loc[df['传感器2温度'].idxmin(), '日期']
    }
    stats['传感器2'] = sensor2_stats
    
    # 计算温度差异
    temp_diff = df['传感器1温度'] - df['传感器2温度']
    diff_stats = {
        '平均差异': temp_diff.mean(),
        '最大差异': temp_diff.max(),
        '最小差异': temp_diff.min(),
        '最大差异日期': df.loc[temp_diff.idxmax(), '日期'],
        '最小差异日期': df.loc[temp_diff.idxmin(), '日期']
    }
    stats['温度差异'] = diff_stats
    
    return stats


def display_statistics(stats: Dict[str, Dict[str, Any]]) -> None:
    """
    显示统计结果
    
    参数:
        stats (Dict[str, Dict[str, Any]]): 统计结果字典
    """
    print("\n===== 统计结果 =====")
    
    # 显示传感器1的统计值
    print("\n传感器1:")
    print(f"  平均值: {stats['传感器1']['平均值']:.1f}°C")
    print(f"  最大值: {stats['传感器1']['最大值']:.1f}°C (日期: {stats['传感器1']['最大值日期'].strftime('%Y-%m-%d')})")
    print(f"  最小值: {stats['传感器1']['最小值']:.1f}°C (日期: {stats['传感器1']['最小值日期'].strftime('%Y-%m-%d')})")
    
    # 显示传感器2的统计值
    print("\n传感器2:")
    print(f"  平均值: {stats['传感器2']['平均值']:.1f}°C")
    print(f"  最大值: {stats['传感器2']['最大值']:.1f}°C (日期: {stats['传感器2']['最大值日期'].strftime('%Y-%m-%d')})")
    print(f"  最小值: {stats['传感器2']['最小值']:.1f}°C (日期: {stats['传感器2']['最小值日期'].strftime('%Y-%m-%d')})")
    
    # 显示温度差异
    print("\n温度差异 (传感器1 - 传感器2):")
    print(f"  平均差异: {stats['温度差异']['平均差异']:.1f}°C")
    print(f"  最大差异: {stats['温度差异']['最大差异']:.1f}°C (日期: {stats['温度差异']['最大差异日期'].strftime('%Y-%m-%d')})")
    print(f"  最小差异: {stats['温度差异']['最小差异']:.1f}°C (日期: {stats['温度差异']['最小差异日期'].strftime('%Y-%m-%d')})")


def plot_temperature_comparison(df: pd.DataFrame, stats: Dict[str, Dict[str, Any]], save_path: str = 'temperature_comparison.png') -> None:
    """
    绘制温度对比折线图
    
    参数:
        df (pd.DataFrame): 清洗后的数据DataFrame
        stats (Dict[str, Dict[str, Any]]): 统计结果字典
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
    plt.axhline(y=stats['传感器1']['平均值'], 
                color='#2E86C1',  # 蓝色
                linestyle='--',  # 虚线
                alpha=0.5,
                label=f"传感器1平均: {stats['传感器1']['平均值']:.1f}°C")
    
    plt.axhline(y=stats['传感器2']['平均值'], 
                color='#E74C3C',  # 红色
                linestyle='--',  # 虚线
                alpha=0.5,
                label=f"传感器2平均: {stats['传感器2']['平均值']:.1f}°C")
    
    # 标记最高和最低温度点
    plt.plot(stats['传感器1']['最大值日期'], stats['传感器1']['最大值'], 
            'b*',  # 蓝色星形
            markersize=12,
            label=f"传感器1最高: {stats['传感器1']['最大值']:.1f}°C")
    
    plt.plot(stats['传感器1']['最小值日期'], stats['传感器1']['最小值'], 
            'b^',  # 蓝色三角形
            markersize=12,
            label=f"传感器1最低: {stats['传感器1']['最小值']:.1f}°C")
    
    plt.plot(stats['传感器2']['最大值日期'], stats['传感器2']['最大值'], 
            'r*',  # 红色星形
            markersize=12,
            label=f"传感器2最高: {stats['传感器2']['最大值']:.1f}°C")
    
    plt.plot(stats['传感器2']['最小值日期'], stats['传感器2']['最小值'], 
            'r^',  # 红色三角形
            markersize=12,
            label=f"传感器2最低: {stats['传感器2']['最小值']:.1f}°C")
    
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
                f"平均温度差异: {stats['温度差异']['平均差异']:.1f}°C\n最大温度差异: {stats['温度差异']['最大差异']:.1f}°C\n最小温度差异: {stats['温度差异']['最小差异']:.1f}°C", 
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
    print("===== 温度传感器分析程序 =====")
    
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
    
    # 计算统计值
    stats = calculate_statistics(df_cleaned)
    
    # 显示统计结果
    display_statistics(stats)
    
    # 绘制温度对比图
    print("\n正在生成温度对比图表...")
    plot_temperature_comparison(df_cleaned, stats)


if __name__ == "__main__":
    main() 