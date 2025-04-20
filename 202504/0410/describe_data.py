#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
这个脚本演示如何使用pandas的.describe()方法查看数据统计结果。
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import tkinter as tk
from tkinter import filedialog, messagebox
from typing import Optional, Dict, Any


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
        title="选择CSV文件",
        filetypes=[("CSV文件", "*.csv"), ("所有文件", "*.*")]
    )
    
    return file_path if file_path else None


def generate_sample_data(output_file: str = 'sample_data.csv') -> str:
    """
    生成示例数据并保存为CSV文件
    
    参数:
        output_file (str): 输出文件名
        
    返回:
        str: 生成的文件路径
    """
    # 生成随机数据
    np.random.seed(42)  # 设置随机种子，确保结果可重现
    
    # 创建示例数据
    data = {
        '年龄': np.random.normal(35, 10, 100).round(1),  # 正态分布
        '身高': np.random.normal(170, 10, 100).round(1),  # 正态分布
        '体重': np.random.normal(65, 15, 100).round(1),   # 正态分布
        '收入': np.random.exponential(5000, 100).round(0),  # 指数分布
        '满意度': np.random.uniform(1, 10, 100).round(1),  # 均匀分布
        '教育年限': np.random.randint(8, 22, 100),  # 整数
        '性别': np.random.choice(['男', '女'], 100),  # 分类数据
        '婚姻状况': np.random.choice(['未婚', '已婚', '离异'], 100, p=[0.3, 0.6, 0.1])  # 带权重的分类数据
    }
    
    # 创建DataFrame
    df = pd.DataFrame(data)
    
    # 保存为CSV文件
    df.to_csv(output_file, index=False, encoding='utf-8-sig')
    print(f"已生成示例数据文件: {output_file}")
    
    return output_file


def analyze_data(file_path: str) -> None:
    """
    分析数据并显示统计结果
    
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
    print("\n===== 数据基本信息 =====")
    print(f"行数: {df.shape[0]}")
    print(f"列数: {df.shape[1]}")
    print("\n列名:")
    for i, col in enumerate(df.columns, 1):
        print(f"  {i}. {col}")
    
    print("\n前5行数据:")
    print(df.head())
    
    # 使用describe()方法查看数值列的统计结果
    print("\n===== 数值列描述性统计 (describe()) =====")
    print(df.describe())
    
    # 分别查看每个数值列的describe()结果
    print("\n===== 各数值列单独的描述性统计 =====")
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    
    if not numeric_cols:
        print("数据中没有数值列")
    else:
        for col in numeric_cols:
            print(f"\n{col} 的描述性统计:")
            print(df[col].describe())
    
    # 查看分类列的统计结果
    print("\n===== 分类列统计 =====")
    categorical_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
    
    if not categorical_cols:
        print("数据中没有分类列")
    else:
        for col in categorical_cols:
            print(f"\n{col} 的值计数:")
            print(df[col].value_counts())
            print(f"{col} 的唯一值数量: {df[col].nunique()}")
    
    # 可视化数值列的分布
    visualize_data(df)


def visualize_data(df: pd.DataFrame) -> None:
    """
    可视化数据
    
    参数:
        df (pd.DataFrame): 数据DataFrame
    """
    # 设置中文字体
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
    plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
    
    # 获取数值列
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    
    if not numeric_cols:
        print("数据中没有数值列，无法生成可视化图表")
        return
    
    # 创建图表
    num_cols = len(numeric_cols)
    num_rows = (num_cols + 1) // 2  # 向上取整
    
    fig, axes = plt.subplots(num_rows, 2, figsize=(15, 5 * num_rows))
    axes = axes.flatten()
    
    for i, col in enumerate(numeric_cols):
        # 直方图
        axes[i].hist(df[col], bins=20, color='skyblue', edgecolor='black', alpha=0.7)
        axes[i].set_title(f'{col} 分布')
        axes[i].set_xlabel(col)
        axes[i].set_ylabel('频次')
        axes[i].grid(True, linestyle='--', alpha=0.7)
        
        # 添加描述性统计信息
        stats = df[col].describe()
        stats_text = f"计数: {stats['count']:.0f}\n"
        stats_text += f"平均值: {stats['mean']:.2f}\n"
        stats_text += f"标准差: {stats['std']:.2f}\n"
        stats_text += f"最小值: {stats['min']:.2f}\n"
        stats_text += f"25%分位数: {stats['25%']:.2f}\n"
        stats_text += f"中位数: {stats['50%']:.2f}\n"
        stats_text += f"75%分位数: {stats['75%']:.2f}\n"
        stats_text += f"最大值: {stats['max']:.2f}"
        
        # 在图表上添加文本
        axes[i].text(0.95, 0.95, stats_text, transform=axes[i].transAxes, 
                    verticalalignment='top', horizontalalignment='right',
                    bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
    
    # 隐藏多余的子图
    for i in range(len(numeric_cols), len(axes)):
        axes[i].set_visible(False)
    
    plt.tight_layout()
    plt.savefig('data_visualization.png')
    print("\n数据可视化已保存为 'data_visualization.png'")


def main():
    """主函数"""
    print("===== 数据统计分析程序 =====")
    
    # 选择文件或生成示例数据
    choice = input("是否生成示例数据? (y/n): ").lower()
    
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
    
    # 分析数据
    analyze_data(file_path)


if __name__ == "__main__":
    main() 