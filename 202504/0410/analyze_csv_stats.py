#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
这个脚本使用pandas读取CSV文件并显示基本统计信息。
包括数据概览、数值列的描述性统计、缺失值统计等。
"""

import pandas as pd
import numpy as np
import os
import sys
import tkinter as tk
from tkinter import filedialog, messagebox
from typing import Optional, List, Dict, Any


def read_csv_file(file_path: str) -> Optional[pd.DataFrame]:
    """
    读取CSV文件
    
    参数:
        file_path (str): CSV文件路径
        
    返回:
        Optional[pd.DataFrame]: 读取的DataFrame，如果出错则返回None
    """
    try:
        # 尝试不同的编码方式读取文件
        encodings = ['utf-8', 'utf-8-sig', 'gbk', 'gb2312', 'latin1']
        
        for encoding in encodings:
            try:
                df = pd.read_csv(file_path, encoding=encoding)
                print(f"成功使用 {encoding} 编码读取文件")
                return df
            except UnicodeDecodeError:
                continue
        
        print("无法使用常见编码读取文件，尝试使用默认编码")
        return pd.read_csv(file_path)
    
    except Exception as e:
        print(f"读取文件时发生错误: {e}")
        return None


def display_basic_info(df: pd.DataFrame) -> None:
    """
    显示DataFrame的基本信息
    
    参数:
        df (pd.DataFrame): 要分析的DataFrame
    """
    print("\n===== 数据基本信息 =====")
    print(f"行数: {df.shape[0]}")
    print(f"列数: {df.shape[1]}")
    print("\n列名:")
    for i, col in enumerate(df.columns, 1):
        print(f"  {i}. {col}")
    
    print("\n数据类型:")
    print(df.dtypes)
    
    print("\n前5行数据:")
    print(df.head())
    
    print("\n后5行数据:")
    print(df.tail())


def display_missing_values(df: pd.DataFrame) -> None:
    """
    显示缺失值统计
    
    参数:
        df (pd.DataFrame): 要分析的DataFrame
    """
    print("\n===== 缺失值统计 =====")
    missing_values = df.isnull().sum()
    missing_percentages = (missing_values / len(df)) * 100
    
    missing_stats = pd.DataFrame({
        '缺失值数量': missing_values,
        '缺失百分比': missing_percentages
    })
    
    # 只显示有缺失值的列
    missing_stats = missing_stats[missing_stats['缺失值数量'] > 0]
    
    if len(missing_stats) > 0:
        print(missing_stats)
    else:
        print("数据中没有缺失值")


def display_numeric_statistics(df: pd.DataFrame) -> None:
    """
    显示数值列的描述性统计
    
    参数:
        df (pd.DataFrame): 要分析的DataFrame
    """
    print("\n===== 数值列描述性统计 =====")
    
    # 获取数值列
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    
    if not numeric_cols:
        print("数据中没有数值列")
        return
    
    # 计算描述性统计
    stats = df[numeric_cols].describe()
    print(stats)
    
    # 计算偏度和峰度
    print("\n偏度和峰度:")
    skew_kurt = pd.DataFrame({
        '偏度': df[numeric_cols].skew(),
        '峰度': df[numeric_cols].kurtosis()
    })
    print(skew_kurt)


def display_categorical_statistics(df: pd.DataFrame) -> None:
    """
    显示分类列的描述性统计
    
    参数:
        df (pd.DataFrame): 要分析的DataFrame
    """
    print("\n===== 分类列描述性统计 =====")
    
    # 获取分类列
    categorical_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
    
    if not categorical_cols:
        print("数据中没有分类列")
        return
    
    for col in categorical_cols:
        print(f"\n{col} 的唯一值数量: {df[col].nunique()}")
        
        # 显示前10个最常见的值
        value_counts = df[col].value_counts().head(10)
        print(f"{col} 的前10个最常见值:")
        print(value_counts)


def analyze_csv(file_path: str) -> None:
    """
    分析CSV文件并显示统计信息
    
    参数:
        file_path (str): CSV文件路径
    """
    # 读取CSV文件
    df = read_csv_file(file_path)
    if df is None:
        return
    
    # 显示基本信息
    display_basic_info(df)
    
    # 显示缺失值统计
    display_missing_values(df)
    
    # 显示数值列统计
    display_numeric_statistics(df)
    
    # 显示分类列统计
    display_categorical_statistics(df)


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


def main():
    """主函数"""
    print("===== CSV文件统计分析工具 =====")
    
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
    
    print(f"正在分析文件: {file_path}")
    analyze_csv(file_path)


if __name__ == "__main__":
    main() 